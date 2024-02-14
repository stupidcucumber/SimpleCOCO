import os
import cv2
from .base import Saver


class DefaultSaver(Saver):
    def build_saving_lists(self, labeled: dict, images: list, annotations: list):
        annotation_id = 0
        for id, (image_path, bboxes) in enumerate(labeled.items()):
            output_image_path = os.path.join(self.output, image_path.split('/')[-1])
            image = self._process_image(image_path=image_path)
            cv2.imwrite(output_image_path, image)
            
            images.append(self._build_image_dict(id=id, image=image, filename=output_image_path))

            for bbox in bboxes:
                annotations.append(self._build_annotation_dict(image_id=id, annotation_id=annotation_id, bbox=bbox))
                annotation_id += 1
