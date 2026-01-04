from abc import ABC, abstractmethod
from common import TypeMatrix
import numpy as np

class __ImageGeometry__(ABC):
    @abstractmethod
    def pad(self, matrix: TypeMatrix, pad_value: int, pad: int) -> TypeMatrix:
        pass

    @abstractmethod
    def resize(self, matrix: TypeMatrix, new_size: tuple[int, int]) -> TypeMatrix:
        pass

    @abstractmethod
    def prepare_standard_geometry(
        self,
        matrix: TypeMatrix,
        target_size: tuple[int, int] = (28, 28),
        padding: int = 2,
        pad_value: int = 0
        ) -> np.ndarray:
        pass

class ImageGeometry(__ImageGeometry__):
    def pad(self, matrix, pad_value=-1, pad=1):
        h, w = len(matrix), len(matrix[0])
        new_h, new_w = h + 2 * pad, w + 2 * pad
        new_matrix = np.full((new_h, new_w), pad_value)
        new_matrix[pad:pad + h, pad:pad + w] = matrix
        return new_matrix

    def _upscale_vertical(self, matrix, new_size):
        return np.repeat(matrix, new_size[0] // len(matrix), axis=0)

    def _upscale_horizontal(self, matrix, new_size): 
        return np.repeat(matrix, new_size[1] // len(matrix[0]), axis=1) 

    def _prepare_supersampling(self, matrix, new_size):
        if len(matrix) < new_size[0]:
            matrix = self._upscale_vertical(matrix, new_size)
        if len(matrix[0]) < new_size[1]:
            matrix = self._upscale_horizontal(matrix, new_size)
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

    def _apply_averaging(self, matrix, range_list):
        return np.array([
            [np.mean(matrix[y_s : y_e+1, x_s : x_e+1]) for x_s, x_e in range_list[1]]
            for y_s, y_e in range_list[0]
        ]).astype(int)

    def _downscale_to_target(self, matrix, new_size):
        curr_h, curr_w = len(matrix), len(matrix[0])
        if (curr_h, curr_w) == new_size:
            return matrix
            
        range_list = self._calculate_range_list((curr_h, curr_w), new_size)
        return self._apply_averaging(matrix, range_list)

    def resize(self, matrix, new_size=(28, 28)):
        matrix_np = np.array(matrix)
        expanded = self._prepare_supersampling(matrix_np, new_size)
        final = self._downscale_to_target(expanded, new_size)
        return final

    def prepare_standard_geometry(self, matrix, target_size, padding, pad_value):
        return self.pad(
            self.resize(matrix, 
                (target_size[0] - 2 * padding, target_size[1] - 2 * padding)
                ),
            pad_value=pad_value,
            pad=padding
            )
