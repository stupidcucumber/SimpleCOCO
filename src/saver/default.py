import json, os
import cv2


class DefaultSaver:
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
        
        for id, (image_path, bboxes) in enumerate(result.items()):
            output_image_path = os.path.join(self.output, image_path.split('/')[-1])
            image = self._process_image(image_path=image_path)
            cv2.imwrite(output_image_path, image)
            
            images.append(self._build_image_dict(id=id, image=image, filename=output_image_path))

            for annotation_id, bbox in enumerate(bboxes):
                annotations.append(self._build_annotation_dict(image_id=id, annotation_id=annotation_id, bbox=bbox))

        final = {
            'images': images,
            'annotations': annotations,
            'categories': categories
        }

        final_json = json.dumps(final, indent=4)
        with open(os.path.join(self.output, 'dataset.json'), 'w') as f:
            f.write(final_json)

        print('Saved to the path: ', self.output)

