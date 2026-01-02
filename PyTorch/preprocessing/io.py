from abc import ABC, abstractmethod
from PIL import Image
import numpy as np
from typing import Union

from common import (
    TypeMatrix,
    TypeIMG
)

class __ImageHandler__(ABC):
    @abstractmethod
    def open_image(self, path: str) -> tuple[Image.Image, int, int]:
        pass

    @abstractmethod
    def save(self, data: Union[TypeIMG, list[TypeMatrix]], path: str) -> None:
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
        