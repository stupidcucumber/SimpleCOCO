import json, os
import cv2


class Saver:
    def __init__(self, output: str):

        if os.path.exists(output):
            raise ValueError('Folder with the name %s already exists!' % output)
        
        os.mkdir(output)
        self.output = output

    def _process_image(self, image_path: str) -> cv2.Mat:
        image = cv2.imread(image_path)
        return cv2.resize(image, dsize=(512, 512))
    
    def _build_image_dict(self, id, image: cv2.Mat, filename):
        return  {
                    'id': id,
                    'width': image.shape[1],
                    'height': image.shape[0],
                    'file_name': filename,
                    'license': None,
                    'date_captured': None 
        }
    
    def _build_annotation_dict(self, image_id, annotation_id, bbox):
        return {
                    'id': annotation_id,
                    'image_id': image_id,
                    'category_id': 1,
                    'segmentation': bbox,
                    'area': bbox[2] * bbox[3],
                    'bbox': bbox,
                    'iscrowd': 0
        }
    
    def build_saving_lists(self, labeled: dict, images: list, annotations: list):
        raise NotImplementedError('This method must be implemented in the derived class!')

    def save(self, result: dict) -> str:
        images = []
        annotations = []
        categories = [
            {
                'id': 1,
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
        with open(os.path.join(self.output, 'dataset.json'), 'w') as f:
            f.write(final_json)

        print('Saved to the path: ', self.output)

