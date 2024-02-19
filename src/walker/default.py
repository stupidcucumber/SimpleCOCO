import numpy as np
import cv2
import os
import pathlib
from .base import DirectoryWalker


class DefaultDirectoryWalker(DirectoryWalker):
    def _load_image(self, path: pathlib.Path) -> np.ndarray:
        image = cv2.imread(str(path))
        return np.asarray(image)
    
    def _extract_paths(self) -> list[pathlib.Path]:
        return [self.root.joinpath(image_path.name) for image_path in self.root.glob('*.*')]
