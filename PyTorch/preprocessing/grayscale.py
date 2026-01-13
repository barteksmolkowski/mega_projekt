from abc import ABC, abstractmethod
from typing import Literal, overload

import numpy as np

from .common import TypeMatrix


class __GrayScaleProcessing__(ABC):
    @overload
    @abstractmethod
    def convert_color_space(self, M: TypeMatrix, to_gray: Literal[True] = True) -> TypeMatrix: ...
    @overload
    @abstractmethod
    def convert_color_space(self, M: TypeMatrix, to_gray: Literal[False]) -> TypeMatrix: ...
    @abstractmethod
    def convert_color_space(self, M: TypeMatrix, to_gray: bool = True) -> TypeMatrix: pass

class GrayScaleProcessing(__GrayScaleProcessing__):
    def convert_color_space(self, M, to_gray = True):
        if to_gray:
            weights = np.array([0.299, 0.587, 0.114])
            return np.dot(M[..., :3], weights).astype(np.uint8)
        else:
            return np.stack([M] * 3, axis=-1).astype(np.uint8)