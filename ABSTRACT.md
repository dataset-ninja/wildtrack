The **Wildtrack: Multi-Camera Person Dataset** brings multi-camera detection and tracking methods into the wild. It meets the need of the deep learning methods for a large-scale multi-camera dataset of walking pedestrians, where the cameras’ fields of view in large part overlap. Being acquired by current high tech hardware it provides HD resolution data. Further, its high precision joint calibration and synchronization shall allow for development of new algorithms that go beyond what is possible with currently available datasets.

## Motivation

Pedestrian detection is a crucial problem within computer vision research, representing a specialized subset of object detection. However, the task's complexity arises from the diverse appearances of individuals and the critical need for high accuracy, particularly in applications like autonomous vehicle navigation. Consequently, pedestrian detection has evolved into a distinct field, garnering extensive research attention and spawning various algorithms with broad applications beyond their original scope.

Despite significant advancements, particularly with the integration of deep learning methods, current monocular detectors still face limitations, particularly in heavily occluded scenarios. This constraint is understandable given the inherent ambiguity in identifying individuals under such conditions, solely relying on single-camera observations. Genuinely, multi-camera detectors come at hand. Important research body in the past decade has also been devoted on this topic. In general, simple averaging of the per-view predictions, can only improve upon a single view detector. Further, more sophisticated methods jointly make use of the information to yield a prediction.

## Dataset description

The dataset was acquired using seven high-tech statically positioned cameras with overlapping fields of view. Precisely, three GoPro Hero 4 and four GoPro Hero 3 cameras were used.

<img src="https://github.com/dataset-ninja/wildtrack/assets/120389559/5c6ff509-9a82-4aef-9c2b-8fbcdf8a6771" alt="image" width="1200">

<span style="font-size: smaller; font-style: italic;">Synchronized corresponding frames from the seven views.</span>

The data acquisition took place in front of the main building of ETH Zurich, Switzerland, during nice weather conditions. The sequences are of resolution 1920×1080 pixels, shot at 60 frames per second.  The camera layout is such that their fields of view overlap in large part. As can be noticed, the height of the positions of the cameras is above humans’ average height. To obtain the illustration the authors pre-define an area of interest, and discretize it into a regular grid of points each defining a position. For each position they sum the cameras for which it is visible. The normalized values are then displayed, where the darker the filling color of a cell is the higher the number of such cameras is. The authors see that in large part the fields of view between the cameras overlap. Precisely, in the illustration they considered 1440×480 grid. Out of the total of 10800 positions, 77, 2489, 2466, 1662, 1711, 2066, 329, are simultaneously visible to 1, 2, . . . , 7 views, respectively. On average, each position is seen from 3.92 cameras.

<img src="https://github.com/dataset-ninja/wildtrack/assets/120389559/6f69feca-4171-41c8-bd82-4635b95731df" alt="image" width="800">

<span style="font-size: smaller; font-style: italic;">Top view visualisation of the amount of overlap between the cameras’ fields of view. Each cell represents a position, and the darker it is coloured the more visible it is from different cameras.</span>

The sequences were initially synchronised with a 50 ms accuracy, what was further refined by detailed manual inspection.

<img src="https://github.com/dataset-ninja/wildtrack/assets/120389559/87c5cc81-1d2a-4cd0-8f74-8874028937aa" alt="image" width="800">

<span style="font-size: smaller; font-style: italic;">Illustration of the camera calibration precision. Best seen in color: blue - clicked points; red - projection of the intersection of the two clicked points. Note that the authors omit one of the views, since the considered point is occluded in it.</span>

Currently, the initial 2000 frames, extracted from videos with a frame rate of 10fps, are undergoing annotation. This annotation process operates at a frame rate of 2fps, meaning that out of the aforementioned extracted frames, every fifth frame has been annotated. Consequently, a total of 400 frames have been annotated. There are 8725 multi-view annotations in total.

<img src="https://github.com/dataset-ninja/wildtrack/assets/120389559/6b404495-3cd7-4f92-a0b2-4729ec87f129" alt="image" width="800">

<span style="font-size: smaller; font-style: italic;">Multiview examples of our dataset. Each row represents a single positive multi-view annotation.</span>

## Calibration of the cameras

Camera calibration involves determining both the extrinsic and intrinsic parameters of a camera. The extrinsic parameters establish a rigid mapping from 3D world coordinates to the camera's 3D coordinates, while the intrinsic parameters, also known as projective transformation, entail identifying the optimal parameters to construct a projection model that relates 2D image points to 3D scene points. In the authors setup, all seven cameras remain static. Unlike existing multi-camera datasets, their focus lies in achieving joint camera calibration with utmost accuracy. This entails calibrating the cameras in such a way that a specific point in 3D space, visible within certain camera fields of view, appears at the expected 2D location—similar to how a human observer would perceive it. This goal doesn't necessarily align with obtaining individually accurate per-camera calibration. Since a 2D point from a single camera may ambiguously map to 3D space, the obtained parameters may not address this ambiguity.
