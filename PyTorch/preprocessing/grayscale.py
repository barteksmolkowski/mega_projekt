from abc import ABC, abstractmethod
from typing import overload

from common import TypeMatrix

import numpy as np

class __GrayScaleProcessing__(ABC):
    @overload
    def convert_color_space(self, matrix: TypeMatrix, to_gray: bool = True) -> TypeMatrix: ...

    @overload
    def convert_color_space(self, matrix: TypeMatrix, to_gray: bool = False) -> TypeMatrix: ...

    @abstractmethod
    def convert_color_space(self, matrix: TypeMatrix, to_gray: bool = True) -> TypeMatrix:
        pass

class GrayScaleProcessing(__GrayScaleProcessing__):
    def convert_color_space(self, matrix, to_gray = True):
        if to_gray:
            weights = np.array([0.299, 0.587, 0.114])
            return np.dot(matrix[..., :3], weights).astype(np.uint8)
        else:
            return np.stack([matrix] * 3, axis=-1).astype(np.uint8)