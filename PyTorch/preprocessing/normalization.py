from abc import ABC, abstractmethod
from itertools import product

import math
import numpy as np
from typing import Tuple

from common import TypeMatrix

class __Normalization__(ABC):
    @abstractmethod
    def normalize(self, matrix: TypeMatrix, old_range: Tuple[int, int], new_range: Tuple[int, int]) -> TypeMatrix:
        pass

    @abstractmethod
    def z_score_normalization(self, matrix: TypeMatrix) -> TypeMatrix:
        pass

class Normalization(__Normalization__):
    def _scale_range(self, value, old_range, new_range):
        return old_range[0] + ((value - new_range[0]) * (old_range[1] - old_range[0]) / (new_range[1] - new_range[0]))

    def normalize(self, matrix, old_range = (0, 1), new_range = (0, 255)):
        for x, y in product(range(len(matrix[0])), range(len(matrix))):
            matrix[x][y] = self._scale_range(matrix[x][y], old_range, new_range)
        return matrix

    def z_score_normalization(self, matrix):
        matrix = np.array(matrix, dtype=float)
        mean_all_px = matrix.mean()
        number_pixels = len(matrix[0]) * len(matrix)
    
        square_differences = 0
        for x, y in product(range(len(matrix[0])), range(len(matrix))):
            square_differences += (matrix[x][y] - mean_all_px) ** 2
        
        sigma = math.sqrt(square_differences / number_pixels)

        for x, y in product(range(len(matrix[0])), range(len(matrix))):
            matrix[x][y] = (matrix[x][y] - mean_all_px) / sigma
        
        return matrix