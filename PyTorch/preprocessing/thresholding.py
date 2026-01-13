from abc import ABC, abstractmethod
from typing import Literal, overload

import numpy as np

from .common import TypeMatrix
from .decorators import parameter_complement


class __Thresholding__(ABC):
    @overload
    @abstractmethod
    def adaptive_threshold(
        self, 
        matrix: TypeMatrix, 
        block_size: int = 0, 
        c: int = 0, 
        auto_params: Literal[True] = True
    ) -> TypeMatrix: ...

    @overload
    @abstractmethod
    def adaptive_threshold(
        self, 
        matrix: TypeMatrix, 
        block_size: int, 
        c: int, 
        auto_params: Literal[False]
    ) -> TypeMatrix: ...

    @abstractmethod
    def adaptive_threshold(
        self, 
        matrix: TypeMatrix, 
        block_size: int = 5, 
        c: int = 2, 
        auto_params: bool = True
    ) -> TypeMatrix:
        pass

class Thresholding(__Thresholding__):
    def _generate_gaussian_kernel(self, size: int) -> np.ndarray:
        v_abs = np.abs(np.arange(-size + 1, size))
        v = size - v_abs
        return np.outer(v, v)

    def _get_gaussian_mean(self, window: np.ndarray, kernel: np.ndarray) -> float:
        kernel_sum = np.sum(kernel)
        weighted_sum = np.sum(window * kernel)
        return weighted_sum // kernel_sum

    @parameter_complement
    def adaptive_threshold(
        self, 
        matrix: np.ndarray, 
        block_size: int = 5, 
        c: int = 2, 
        auto_params: bool = True
    ) -> np.ndarray:
        kernel = self._generate_gaussian_kernel((block_size // 2) + 1)
        
        padded_matrix = np.pad(matrix, pad_width=block_size // 2, mode='reflect')

        windows = np.lib.stride_tricks.sliding_window_view(padded_matrix, (block_size, block_size))

        weighted_windows = windows * kernel
        local_thresholds = np.sum(weighted_windows, axis=(2, 3)) / np.sum(kernel)
                
        return np.where(matrix > (local_thresholds - c), 255, 0).astype(np.uint8)