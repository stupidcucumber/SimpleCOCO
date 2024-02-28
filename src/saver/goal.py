from .base import Saver
import pathlib
import cv2


class GOALSaver(Saver):
    def _build_folder_tree(self, root: pathlib.Path) -> list[pathlib.Path]:
        train_folder = root.joinpath('train')
        images_path = pathlib.Path('images')
        labels_path = pathlib.Path('labels')
        train_images_folder = train_folder.joinpath(images_path)
        train_labels_folder = train_folder.joinpath(labels_path)
        valid_folder = root.joinpath('val')
        valid_images_folder = valid_folder.joinpath(images_path)
        valid_labels_folder = valid_folder.joinpath(labels_path)
        _l = [train_images_folder, train_labels_folder, 
              valid_images_folder, valid_labels_folder]
        for folder in _l:
            folder.mkdir(parents=True)
        return _l
    
    def _convert_bbox(self, bbox: list, view_width: int, view_height: int, 
                      image_width: int, image_height: int) -> list:
        x, y, w, h = bbox
        x, y, w, h = [x * image_width / view_width, y * image_height / view_height, w * image_width / view_width, h * image_height / view_height]
        new_x = (x + (x + w)) / 2
        new_y = (y + (y + h)) / 2
        return [new_x / image_width, new_y / image_height, w / image_width, h / image_height]

    def build_saving_lists(self, labeled: dict[pathlib.Path, list], images: list, annotations: list, 
                           view_width: int, view_height: int):
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

            output_path = images_folder.joinpath(image_path.name)
            cv2.imwrite(str(output_path), image)

            lines = []
            height, width, _ = image.shape
            for bbox in bboxes:
                if self.width and self.height:
                    new_bbox = self._convert_bbox(bbox, view_width=view_width, view_height=view_height, image_width=self.width, image_height=self.height)
                else:
                    new_bbox = self._convert_bbox(bbox, view_width=view_width, view_height=view_height, image_width=width, image_height=height)
                line = '%d %0.3f %0.3f %0.3f %0.3f\n' % (*[0, *new_bbox],)
                lines.append(line)
                annotations.append(self._build_annotation_dict(image_id=id, annotation_id=annotation_id, bbox=bbox))
                annotation_id += 1

            label_name = labels_folder.joinpath(image_path.name.split('.')[0])
            with open(str(label_name) + '.txt', 'w') as label_file:
                label_file.writelines(lines)

            images.append(self._build_image_dict(id=id, image=image, filename=output_path))