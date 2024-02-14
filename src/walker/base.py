import numpy as np


class DirectoryWalker:
    def __init__(self, root: str, cache: bool=True):
        self.root = root
        self.cache = cache
        self.elements = None

        self.paths = self._extract_paths()
        if self.cache:
            self.elements = self._load_images()
    
    def _extract_paths(self) -> list[str]:
        raise NotImplementedError('This function needs to be implemented in the derived class!')

    def _load_image(self, path: str) -> np.ndarray:
        raise NotImplementedError('This function needs to be implemented in the derived class!')

    def _load_images(self) -> list[np.ndarray]:
        result = []
        for path in self.paths:
            image = self._load_image(path=path)
            result.append(image)
        return result

    def __getitem__(self, index: int):
        if self.cache:
            return self.paths[index], self.elements[index]
        return self.paths[index], self._load_image(path=self.paths[index])

    def __len__(self) -> int:
        return len(self.paths)