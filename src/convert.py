import glob
import os
import shutil
from urllib.parse import unquote, urlparse

import supervisely as sly
from dataset_tools.convert import unpack_if_archive
from supervisely.io.fs import file_exists, get_file_name, get_file_name_with_ext
from supervisely.io.json import load_json_file
from tqdm import tqdm

import src.settings as s


def download_dataset(teamfiles_dir: str) -> str:
    """Use it for large datasets to convert them on the instance"""
    api = sly.Api.from_env()
    team_id = sly.env.team_id()
    storage_dir = sly.app.get_data_dir()

    if isinstance(s.DOWNLOAD_ORIGINAL_URL, str):
        parsed_url = urlparse(s.DOWNLOAD_ORIGINAL_URL)
        file_name_with_ext = os.path.basename(parsed_url.path)
        file_name_with_ext = unquote(file_name_with_ext)

        sly.logger.info(f"Start unpacking archive '{file_name_with_ext}'...")
        local_path = os.path.join(storage_dir, file_name_with_ext)
        teamfiles_path = os.path.join(teamfiles_dir, file_name_with_ext)

        fsize = api.file.get_directory_size(team_id, teamfiles_dir)
        with tqdm(
            desc=f"Downloading '{file_name_with_ext}' to buffer...",
            total=fsize,
            unit="B",
            unit_scale=True,
        ) as pbar:
            api.file.download(team_id, teamfiles_path, local_path, progress_cb=pbar)
        dataset_path = unpack_if_archive(local_path)

    if isinstance(s.DOWNLOAD_ORIGINAL_URL, dict):
        for file_name_with_ext, url in s.DOWNLOAD_ORIGINAL_URL.items():
            local_path = os.path.join(storage_dir, file_name_with_ext)
            teamfiles_path = os.path.join(teamfiles_dir, file_name_with_ext)

            if not os.path.exists(get_file_name(local_path)):
                fsize = api.file.get_directory_size(team_id, teamfiles_dir)
                with tqdm(
                    desc=f"Downloading '{file_name_with_ext}' to buffer...",
                    total=fsize,
                    unit="B",
                    unit_scale=True,
                ) as pbar:
                    api.file.download(team_id, teamfiles_path, local_path, progress_cb=pbar)

                sly.logger.info(f"Start unpacking archive '{file_name_with_ext}'...")
                unpack_if_archive(local_path)
            else:
                sly.logger.info(
                    f"Archive '{file_name_with_ext}' was already unpacked to '{os.path.join(storage_dir, get_file_name(file_name_with_ext))}'. Skipping..."
                )

        dataset_path = storage_dir
    return dataset_path


def count_files(path, extension):
    count = 0
    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith(extension):
                count += 1
    return count


def convert_and_upload_supervisely_project(
    api: sly.Api, workspace_id: int, project_name: str
) -> sly.ProjectInfo:
    ### Function should read local dataset and upload it to Supervisely project, then return project info.###
    images_path = "/home/alex/DATASETS/TODO/archive/Wildtrack/Image_subsets"
    bboxes_path = "/home/alex/DATASETS/TODO/archive/Wildtrack/annotations_positions"
    batch_size = 30
    bboxes_ext = ".json"
    ds_name = "ds"

    def create_ann(image_path):
        labels = []

        subfolder_value = image_path.split("/")[-2]
        camera_meta = folder_to_camera[subfolder_value]
        camera = sly.Tag(camera_meta)

        view_num = int(subfolder_value[1]) - 1

        image_np = sly.imaging.image.read(image_path)[:, :, 0]
        img_height = image_np.shape[0]
        img_wight = image_np.shape[1]

        ann_path = os.path.join(bboxes_path, get_file_name(image_path) + bboxes_ext)
        if file_exists(ann_path):
            ann_data = load_json_file(ann_path)
            for curr_ann_data in ann_data:
                person_value = curr_ann_data["personID"]
                person = sly.Tag(tag_person_id, value=person_value)
                position_value = curr_ann_data["positionID"]
                position = sly.Tag(tag_position_id, value=position_value)

                for view in curr_ann_data["views"]:
                    if view["viewNum"] == view_num:
                        left = int(view["xmin"])
                        top = int(view["ymin"])
                        right = int(view["xmax"])
                        bottom = int(view["ymax"])
                        rect = sly.Rectangle(left=left, top=top, right=right, bottom=bottom)
                        label = sly.Label(rect, obj_class, tags=[person, position])
                        labels.append(label)

        return sly.Annotation(img_size=(img_height, img_wight), labels=labels, img_tags=[camera])

    obj_class = sly.ObjClass("pedestrian", sly.Rectangle)
    tag_c1 = sly.TagMeta("camera 1", sly.TagValueType.NONE)
    tag_c2 = sly.TagMeta("camera 2", sly.TagValueType.NONE)
    tag_c3 = sly.TagMeta("camera 3", sly.TagValueType.NONE)
    tag_c4 = sly.TagMeta("camera 4", sly.TagValueType.NONE)
    tag_c5 = sly.TagMeta("camera 5", sly.TagValueType.NONE)
    tag_c6 = sly.TagMeta("camera 6", sly.TagValueType.NONE)
    tag_c7 = sly.TagMeta("camera 7", sly.TagValueType.NONE)
    tag_person_id = sly.TagMeta("person id", sly.TagValueType.ANY_NUMBER)
    tag_position_id = sly.TagMeta("position id", sly.TagValueType.ANY_NUMBER)

    folder_to_camera = {
        "C1": tag_c1,
        "C2": tag_c2,
        "C3": tag_c3,
        "C4": tag_c4,
        "C5": tag_c5,
        "C6": tag_c6,
        "C7": tag_c7,
    }

    project = api.project.create(workspace_id, project_name, change_name_if_conflict=True)
    meta = sly.ProjectMeta(
        obj_classes=[obj_class],
        tag_metas=[
            tag_c1,
            tag_person_id,
            tag_position_id,
            tag_c2,
            tag_c3,
            tag_c4,
            tag_c5,
            tag_c6,
            tag_c7,
        ],
    )
    api.project.update_meta(project.id, meta.to_json())

    dataset = api.dataset.create(project.id, ds_name, change_name_if_conflict=True)

    images_pathes = glob.glob(images_path + "/*/*.png")

    progress = sly.Progress("Create dataset {}".format(ds_name), len(images_pathes))

    for img_pathes_batch in sly.batched(images_pathes, batch_size=batch_size):
        img_names_batch = [
            im_path.split("/")[-2] + "_" + get_file_name_with_ext(im_path)
            for im_path in img_pathes_batch
        ]

        img_infos = api.image.upload_paths(dataset.id, img_names_batch, img_pathes_batch)
        img_ids = [im_info.id for im_info in img_infos]

        anns = [create_ann(image_path) for image_path in img_pathes_batch]
        api.annotation.upload_anns(img_ids, anns)

        progress.iters_done_report(len(img_names_batch))

    return project
