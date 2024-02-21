import json
import pathlib
import cv2


class Saver:
    def __init__(self, output: pathlib.Path, train_test_split: float | None=None):

        if output.exists():
            raise ValueError('Folder with the name %s already exists!' % str(output))
        
        output.mkdir()
        self.output = output
        self.train_test_split = train_test_split

    def _process_image(self, image_path: pathlib.Path) -> cv2.Mat:
        image = cv2.imread(str(image_path))
        return cv2.resize(image, dsize=(512, 512))
    
    def _build_image_dict(self, id, image: cv2.Mat, filename: str):
        return  {
                    'id': id,
                    'width': image.shape[1],
                    'height': image.shape[0],
                    'file_name': str(filename),
                    'license': None,
                    'date_captured': None 
        }
    
    def _build_annotation_dict(self, image_id: int, annotation_id: int, bbox: list):
        return {
                    'id': annotation_id,
                    'image_id': image_id,
                    'category_id': 0,
                    'segmentation': bbox,
                    'area': bbox[2] * bbox[3],
                    'bbox': bbox,
                    'iscrowd': 0
        }
    
    def build_saving_lists(self, labeled: dict[pathlib.Path, list], images: list, annotations: list):
        raise NotImplementedError('This method must be implemented in the derived class!')

    def save(self, result: dict) -> str:
        images = []
        annotations = []
        categories = [
            {
                'id': 0,
                'name': 'tomato',
                'supercategory': 'vegetable'
            }
        ]
        
        self.build_saving_lists(labeled=result, images=images, annotations=annotations)

        final = {
            'images': images,
            'annotations': annotations,
            'categories': categories
        }

        final_json = json.dumps(final, indent=4)
        with open(self.output.joinpath('dataset.json'), 'w') as f:
            f.write(final_json)

        print('Saved to the path: ', self.output)

