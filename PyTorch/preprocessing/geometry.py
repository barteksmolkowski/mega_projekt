from abc import ABC, abstractmethod

import numpy as np

from .common import TypeMatrix


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
        M: TypeMatrix,
        target_size: tuple[int, int] = (28, 28),
        padding: int = 2,
        pad_value: int = 0
        ) -> np.ndarray:
        pass

class ImageGeometry(__ImageGeometry__):
    def pad(self, M, pad_val=-1, pad=1):
        h, w = len(M), len(M[0])
        new_h, new_w = h + 2 * pad, w + 2 * pad
        new_M = np.full((new_h, new_w), pad_val)
        new_M[pad:pad + h, pad:pad + w] = M
        return new_M

    def _upscale_vertical(self, M, new_size):
        return np.repeat(M, new_size[0] // len(M), axis=0)

    def _upscale_horizontal(self, M, new_size): 
        return np.repeat(M, new_size[1] // len(M[0]), axis=1) 

    def _prepare_supersampling(self, M, new_size):
        if len(M) < new_size[0]:
            M = self._upscale_vertical(M, new_size)
        if len(M[0]) < new_size[1]:
            M = self._upscale_horizontal(M, new_size)
        return M

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

    def _apply_averaging(self, M, range_list):
        return np.array([
            [np.mean(M[y_s : y_e+1, x_s : x_e+1]) for x_s, x_e in range_list[1]]
            for y_s, y_e in range_list[0]
        ]).astype(int)

    def _downscale_to_target(self, M, new_size):
        curr_h, curr_w = len(M), len(M[0])
        if (curr_h, curr_w) == new_size:
            return M
            
        range_list = self._calculate_range_list((curr_h, curr_w), new_size)
        return self._apply_averaging(M, range_list)

    def resize(self, M, new_size=(28, 28)):
        return self._downscale_to_target(
            self._prepare_supersampling(np.array(M), new_size),
            new_size
        )

    def prepare_standard_geometry(self, M, target_size, padding, pad_value):
        return self.pad(
            self.resize(M, 
                (target_size[0] - 2 * padding, target_size[1] - 2 * padding)
                ),
            pad_val=pad_value,
            pad=padding
            )
