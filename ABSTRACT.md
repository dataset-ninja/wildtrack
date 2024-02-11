The **Wildtrack: Multi-Camera Person Dataset** brings multi-camera detection and tracking methods into the wild. It meets the need of the deep learning methods for a large-scale multi-camera dataset of walking pedestrians, where the cameras’ fields of view in large part overlap. Being acquired by current high tech hardware it provides HD resolution data. Further, its high precision joint calibration and synchronization shall allow for development of new algorithms that go beyond what is possible with currently available datasets.

## Motivation

Pedestrian detection is a crucial problem within computer vision research, representing a specialized subset of object detection. However, the task's complexity arises from the diverse appearances of individuals and the critical need for high accuracy, particularly in applications like autonomous vehicle navigation. Consequently, pedestrian detection has evolved into a distinct field, garnering extensive research attention and spawning various algorithms with broad applications beyond their original scope.

Despite significant advancements, particularly with the integration of deep learning methods, current monocular detectors still face limitations, particularly in heavily occluded scenarios. This constraint is understandable given the inherent ambiguity in identifying individuals under such conditions, solely relying on single-camera observations. Genuinely, multi-camera detectors come at hand. Important research body in the past decade has also been devoted on this topic. In general, simple averaging of the per-view predictions, can only improve upon a single view detector. Further, more sophisticated methods jointly make use of the information to yield a prediction.

## Dataset description

