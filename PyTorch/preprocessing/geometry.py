from abc import ABC, abstractmethod
from itertools import product
from common import (
    TypeMatrix,
    Tuple
)

class __MatrixCreator__(ABC):
    @abstractmethod
    def create(self, height: int, width: int, value: int = -1) -> TypeMatrix:
        pass

    @abstractmethod
    def pad(self, matrix: TypeMatrix, pad_value: int = -1, pad_size: int = 1) -> TypeMatrix:
        pass

class __MatrixProcessor__(ABC):
    @abstractmethod
    def resize(self, matrix: TypeMatrix, new_size: list[int, int]) -> TypeMatrix:
        pass

class MatrixCreator(__MatrixCreator__):
    def create(self, height, width, value):
        return [[value for _ in range(width)] for _ in range(height)]

    def pad(self, matrix, pad_value, pad_size):
        h, w = len(matrix), len(matrix[0])
        new_h, new_w = h + 2 * pad_size, w + 2 * pad_size
        new_matrix = self.create(new_h, new_w, pad_value)

        for y, x in product(range(h), range(w)):
            new_matrix[y + pad_size][x + pad_size] = matrix[y][x]

        return new_matrix
    
class MatrixProcessor(__MatrixProcessor__):
    def _upscale_vertical(self, matrix: TypeMatrix, target_h: int):
        old_h = len(matrix)
        if old_h < target_h:
            height_multiplier = 1
            while old_h * height_multiplier <= target_h:
                height_multiplier += 1
            return [row for row in matrix for _ in range(height_multiplier)]
        return matrix

    def _upscale_horizontal(self, matrix, target_w):
        old_w = len(matrix[0])
        if old_w < target_w:
            weight_multiplier = 1
            while old_w * weight_multiplier <= target_w:
                weight_multiplier += 1
            return [[pixel for pixel in row for _ in range(weight_multiplier)] for row in matrix]
        return matrix

    def _prepare_supersampling(self, matrix, new_size):
        matrix = self._upscale_vertical(matrix, new_size[0])
        matrix = self._upscale_horizontal(matrix, new_size[1])
        return matrix

    def _calculate_range_list(self, curr_size, new_size):
        rangeList = [[], []]
        for axis in range(2):
            step = curr_size[axis] / new_size[axis]
            for i in range(new_size[axis]):
                start = int(round(i * step))
                end = int(round((i + 1) * step))
                if i == new_size[axis] - 1:
                    end = curr_size[axis]
                if start == end and end < curr_size[axis]:
                    end += 1
                rangeList[axis].append((start, end - 1))
        return rangeList

    def _apply_averaging(self, matrix, rangeList, new_matrix):
        for (idx_h, pair_h), (idx_w, pair_w) in product(enumerate(rangeList[0]), enumerate(rangeList[1])):
            sum_numbers = 0
            divider = 0
            for i, j in product(range(pair_h[0], pair_h[1] + 1), range(pair_w[0], pair_w[1] + 1)):
                sum_numbers += matrix[i][j]
                divider += 1
            if divider > 0:
                new_matrix[idx_h][idx_w] = sum_numbers // divider
        return new_matrix

    def _downscale_to_target(self, matrix, new_size):
        curr_size = (len(matrix), len(matrix[0]))
        if curr_size == new_size:
            return matrix
            
        new_matrix = [[0 for _ in range(new_size[1])] for _ in range(new_size[0])]
        rangeList = self._calculate_range_list(curr_size, new_size)
        return self._apply_averaging(matrix, rangeList, new_matrix)

    def resize(self, matrix, new_size=(28, 28)):
        expanded_matrix = self._prepare_supersampling(matrix, new_size)
        final_matrix = self._downscale_to_target(expanded_matrix, new_size)
        return final_matrix