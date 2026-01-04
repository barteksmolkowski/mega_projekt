from abc import ABC, abstractmethod
from itertools import product
import numpy as np

from common import TypeMatrix

class __Thresholding__(ABC):
    @abstractmethod
    def adaptive_threshold(self, matrix: TypeMatrix, block_size: int, c: int) -> TypeMatrix:
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

    def adaptive_threshold(self, matrix: np.ndarray, block_size: int = 5, c: int = 2) -> np.ndarray:
        h, w = len(matrix), len(matrix[0])
        kernel = self._generate_gaussian_kernel((block_size // 2) + 1)
        
        padded_matrix = np.pad(matrix, pad_width=block_size // 2, mode='reflect')

        result = np.zeros((h, w), dtype=np.uint8)

        for i, j in product(range(h), range(w)):
            window = padded_matrix[i : i + block_size, j : j + block_size]
            
            local_threshold = self._get_gaussian_mean(window, kernel)
            
            result[i][j] = 255 if matrix[i][j] > (local_threshold - c) else 0
                
        return result