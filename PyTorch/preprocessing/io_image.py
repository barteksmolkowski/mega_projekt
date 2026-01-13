from abc import ABC, abstractmethod
from typing import Literal, overload

import numpy as np
from PIL import Image


class __ImageHandler__(ABC):
    @abstractmethod
    def open_image(self, path: str) -> tuple[np.ndarray, int, int]:
        pass

    @overload
    @abstractmethod
    def save(self, data: np.ndarray, path: str) -> None: ...

    @overload
    @abstractmethod
    def save(self, data: list[np.ndarray], path: str) -> None: ...

    @abstractmethod
    def save(self, data, path):
        pass

    @overload
    @abstractmethod
    def handle_file(self, path: str, data: None = None, is_save_mode: Literal[False] = False) -> np.ndarray: ...

    @overload
    @abstractmethod
    def handle_file(self, path: str, data: np.ndarray, is_save_mode: Literal[True]) -> None: ...

    @abstractmethod
    def handle_file(self, path, data=None, is_save_mode=False):
        pass

class ImageHandler(__ImageHandler__):
    def open_image(self, path):
        img = Image.open(path).convert("RGB")
        width, height = img.size
        array = np.array(img)
        img_list = [[tuple(pixel) for pixel in row] for row in array.tolist()]

        return img_list, width, height
    
    def save(self, data, path):
        array = np.array(data, dtype=np.uint8)
        imgpil = Image.fromarray(array)
        imgpil.save(path)

    def handle_file(self, path, data=None, is_save_mode=False):
        if is_save_mode:
            if data is None:
                raise ValueError("Musisz podać 'data', aby zapisać plik!")
            self.save(data, path)
            return None
        else:
            matrix, _, _ = self.open_image(path)
            return matrix