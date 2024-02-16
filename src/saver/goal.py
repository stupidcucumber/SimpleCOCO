from .base import Saver
import os, cv2


class GOALSaver(Saver):
    def _build_folder_tree(self, root: str) -> list:
        train_folder = os.path.join(root, 'train')
        train_images_folder = os.path.join(train_folder, 'images')
        train_labels_folder = os.path.join(train_folder, 'labels')
        valid_folder = os.path.join(root, 'val')
        valid_images_folder = os.path.join(valid_folder, 'images')
        valid_labels_folder = os.path.join(valid_folder, 'labels')
        _l = [train_images_folder, train_labels_folder, 
              valid_images_folder, valid_labels_folder]
        for folder in _l:
            os.makedirs(folder)
        return _l
    
    def _convert_bbox(self, bbox: list, img_size: int) -> list:
        x, y, w, h = bbox
        new_x = (x + (x + w)) / 2
        new_y = (y + (y + h)) / 2

        return [value / img_size for value in [new_x, new_y, w, h]]

    def build_saving_lists(self, labeled: dict, images: list, annotations: list):
        train_images_folder, train_labels_folder, \
            valid_images_folder, valid_labels_folder = self._build_folder_tree(root=self.output)

        train_index = int(len(labeled.keys()) * self.train_test_split)
        annotation_id = 0
        for id, (image_path, bboxes) in enumerate(labeled.items()):
            image = self._process_image(image_path=image_path)

            if id < train_index: 
                images_folder = train_images_folder
                labels_folder = train_labels_folder
            else:
                images_folder = valid_images_folder
                labels_folder = valid_labels_folder

            output_path = os.path.join(images_folder, image_path.split('/')[-1])
            cv2.imwrite(output_path, image)

            lines = []
            for bbox in bboxes:
                new_bbox = self._convert_bbox(bbox, 512)
                line = '%d %0.3f %0.3f %0.3f %0.3f\n' % (*[0, *new_bbox],)
                lines.append(line)
                annotations.append(self._build_annotation_dict(image_id=id, annotation_id=annotation_id, bbox=bbox))
                annotation_id += 1

            label_name = os.path.join(labels_folder, image_path.split('/')[-1].split('.')[0])
            with open(label_name + '.txt', 'w') as label_file:
                label_file.writelines(lines)

            images.append(self._build_image_dict(id=id, image=image, filename=output_path))