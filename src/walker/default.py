import numpy as np
import cv2
import os
from .base import DirectoryWalker


class DefaultDirectoryWalker(DirectoryWalker):
    def _load_image(self, path) -> np.ndarray:
        image = cv2.imread(path)
        return np.asarray(image)
    
    def _extract_paths(self) -> list[str]:
        return [os.path.join(self.root, image_path) for image_path in os.listdir(self.root)]
