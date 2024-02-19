from .base import Saver
import os, pathlib
import numpy as np
import cv2


class TFIconSaver(Saver):
    def build_saving_lists(self, labeled: dict[pathlib.Path, list], images: list, annotations: list):
        annotation_id = 0
        for index, (image_path, bboxes) in enumerate(labeled.items()):
            entry_folder = self.output.joinpath(str(index))
            entry_folder.mkdir()
            output_image_path = entry_folder.joinpath(image_path.name)
            bg_image_path = entry_folder.joinpath('bg01.png')
            image = self._process_image(image_path=image_path)
            images.append(self._build_image_dict(id=index, image=image, filename=str(bg_image_path)))

            cv2.imwrite(str(output_image_path), image)
            cv2.imwrite(str(bg_image_path), image)

            for bbox_index, bbox in enumerate(bboxes):
                x, y, w, h = bbox
                mask = np.zeros(shape=(512, 512))
                mask[y:y+h, x:x+w] = 255

                mask_path = entry_folder.joinpath('mask_bg_fg_%d.png' % bbox_index)
                cv2.imwrite(str(mask_path), mask)
                annotations.append(self._build_annotation_dict(image_id=index, annotation_id=annotation_id, bbox=bbox))
                annotation_id += 1