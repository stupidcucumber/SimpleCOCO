import cv2
from ..walker import DirectoryWalker
from ..saver import DefaultSaver


class ImageLabeler:
    def __init__(self, saver: DefaultSaver, directory_walker: DirectoryWalker, 
                 width: int=512, height: int=512):
        self.width = width
        self.height = height
        self.processed = dict()
        self.walker = directory_walker
        self.saver = saver

    def _preprocess(self, raw_image: cv2.Mat, bboxes: list, meta: bool=True) -> cv2.Mat:
        image = cv2.resize(raw_image, dsize=(self.width, self.height))
        for bbox in bboxes:
            x, y, w, h = [int(value) for value in bbox]
            image = cv2.rectangle(image, pt1=[x, y], pt2=[x + w, y + h], color=[0, 255, 0], thickness=2)
        if meta:
            image = cv2.putText(image, 'BBoxes: %d' % len(bboxes), 
                                org=(5, 30), fontFace=0, fontScale=1, color=(0, 0, 0), thickness=2)
        return image

    def choose_roi(self, image: cv2.Mat, entry: list):
        choose_roi = True
        window_name = 'Selecting ROI'
        while choose_roi:
            x, y, w, h = cv2.selectROI(window_name, image)
            if [x, y, w, h] == [0, 0, 0, 0]:
                choose_roi = False
                cv2.destroyWindow(winname=window_name)
            else:
                image = cv2.rectangle(image, pt1=[x, y], pt2=[x + w, y + h], color=[0, 255, 0], thickness=2)
                entry.append([x, y, w, h])

    def start(self):
        label = True
        window_name = 'Current image'
        current_index = 0
        while label:
            image_path, raw_image = self.walker[current_index]
            if self.processed.get(image_path, None) is None:
                self.processed[image_path] = []
            image = self._preprocess(raw_image=raw_image, bboxes=self.processed[image_path])
            cv2.imshow(window_name, image)
            pressed_key = cv2.waitKey(0)
            if pressed_key == ord('q'):
                label = False
            elif pressed_key == ord('s'):
                self.saver.save(result=self.processed)
            elif pressed_key == ord('n'):
                if current_index < len(self.walker) - 1:
                    current_index += 1
            elif pressed_key == ord('p'):
                if current_index > 0:
                    current_index -= 1
            elif pressed_key == ord('l'):
                image = self._preprocess(raw_image=raw_image, bboxes=self.processed[image_path], meta=False)
                self.choose_roi(image=image, entry=self.processed[image_path])



