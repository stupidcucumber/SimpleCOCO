from .base import Saver
import os
import numpy as np
import cv2


class TFIconSaver(Saver):
    def build_saving_lists(self, labeled: dict, images: list, annotations: list):
        annotation_id = 0
        for index, (image_path, bboxes) in enumerate(labeled.items()):
            entry_folder = os.path.join(self.output, str(index))
            os.mkdir(entry_folder)
            output_image_path = os.path.join(entry_folder, image_path.split('/')[-1])
            bg_image_path = os.path.join(entry_folder, 'bg01.png')
            image = self._process_image(image_path=image_path)
            images.append(self._build_image_dict(id=index, image=image, filename=bg_image_path))

            cv2.imwrite(output_image_path, image)
            cv2.imwrite(bg_image_path, image)

            for bbox_index, bbox in enumerate(bboxes):
                x, y, w, h = bbox
                mask = np.zeros(shape=(512, 512))
                mask[y:y+h, x:x+w] = 255

                mask_path = os.path.join(entry_folder, 'mask_bg_fg_%d.png' % bbox_index)
                cv2.imwrite(mask_path, mask)
                annotations.append(self._build_annotation_dict(image_id=index, annotation_id=annotation_id, bbox=bbox))
                annotation_id += 1