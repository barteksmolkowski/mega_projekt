import math
import random
from abc import ABC, abstractmethod
from itertools import product
from typing import List, Optional, Tuple

import numpy as np

from common import (
    TypeMatrix,
)

from decorators import (
    auto_fill_color,
    get_number_repeats,
    kernel_data_processing,
    prepare_angle,
    prepare_values,
    with_dimensions
)

class DataAugmentationABC(ABC):
    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def augment(self, matrix: TypeMatrix, repeats: int) -> List[TypeMatrix]:
        pass

class GeometryAugmentationABC(ABC):
    @abstractmethod
    def horizontal_flip(self, matrix: TypeMatrix) -> TypeMatrix:
        pass

    @abstractmethod
    def vertical_flip(self, matrix: TypeMatrix) -> TypeMatrix:
        pass

    @abstractmethod
    def rotate_90(self, matrix: TypeMatrix, is_right: bool = True) -> TypeMatrix:
        pass

    @abstractmethod
    def rotate_small_angle(self, matrix: TypeMatrix, angle: Optional[float] = None, fill: Optional[int] = None) -> TypeMatrix:
        pass

    @abstractmethod
    def random_shift(self, matrix: TypeMatrix, max_dx_dy: Optional[Tuple[int, int]] = None, fill: Optional[int] = None, is_right: bool = None) -> TypeMatrix:
        pass

class NoiseAugmentationABC(ABC):
    @abstractmethod
    def gaussian_noise(self, matrix: TypeMatrix, std: float) -> TypeMatrix:
        pass

    @abstractmethod
    def salt_and_pepper(self, matrix: TypeMatrix, prob: float) -> TypeMatrix:
        pass

class MorphologyAugmentationABC(ABC):
    @abstractmethod
    def __max_neighbor__(matrix: TypeMatrix, pos_x: int, pos_y: int, r):
        pass

    @abstractmethod
    def dilate(self, matrix: TypeMatrix, kernel_size: int) -> TypeMatrix:
        pass

    @abstractmethod
    def erode(self, matrix: TypeMatrix, kernel_size: int, fill: int = None, r: range = None) -> TypeMatrix:
        pass
        
    @abstractmethod
    def get_boundaries(self, matrix: TypeMatrix, kernel_size: int, fill: int = None, r: range = None) -> TypeMatrix:
        pass

    @abstractmethod
    def opening(self, matrix: TypeMatrix, kernel_size: int, fill: int = None):
        pass

    @abstractmethod
    def closing(self, matrix: TypeMatrix, kernel_size: int, fill: int = None):
        pass

class DataAugmentation(DataAugmentationABC):
    def __init__(self):
        self.geometry_augmentation = GeometryAugmentation()
        self.horizontal_flip = self.geometry_augmentation.horizontal_flip
        self.vertical_flip = self.geometry_augmentation.vertical_flip
        self.rotate_90 = self.geometry_augmentation.rotate_90
        self.rotate_small_angle = self.geometry_augmentation.rotate_small_angle
        self.random_shift = self.geometry_augmentation.random_shift

        self.noise_augmentation = NoiseAugmentation()
        self.gaussian_noise = self.noise_augmentation.gaussian_noise
        self.salt_and_pepper = self.noise_augmentation.salt_and_pepper

        self.morphology_augmentation = MorphologyAugmentation()
        self.dilate = self.morphology_augmentation.dilate
        self.erode = self.morphology_augmentation.erode
        self.get_boundaries = self.morphology_augmentation.get_boundaries
        self.opening = self.morphology_augmentation.opening
        self.closing = self.morphology_augmentation.closing

    @get_number_repeats
    def augment(self, matrix, repeats=None):
        augmentations = [
            lambda m: self.horizontal_flip(m),
            lambda m: self.vertical_flip(m),
            lambda m: self.rotate_90(m, is_right=True),
            lambda m: self.rotate_90(m, is_right=False),
            lambda m: self.rotate_small_angle(m, is_right=True),
            lambda m: self.rotate_small_angle(m, is_right=False),
            lambda m: self.random_shift(m, is_right=True),
            lambda m: self.random_shift(m, is_right=False),
            lambda m: self.gaussian_noise(m),
            lambda m: self.salt_and_pepper(m),
            lambda m: self.dilate(m, kernel_size=3),
            lambda m: self.erode(m, kernel_size=3),
            lambda m: self.get_boundaries(m, kernel_size=3),
            lambda m: self.opening(m, kernel_size=3),
            lambda m: self.closing(m, kernel_size=3),
        ]

        result = []

        for _ in range(repeats):
            new_m = [row[:] for row in matrix]

            chosen = random.sample(augmentations, 3)

            for aug in chosen:
                new_m = aug(new_m)

            new_m_int = [[int(el) for el in row] for row in new_m]
            result.append(new_m_int)

        return result

class GeometryAugmentation(GeometryAugmentationABC):
    def horizontal_flip(self, matrix):
        print(f"horizontal_flip")
        return matrix[:, ::-1]
        
    def vertical_flip(self, matrix):
        print(f"vertical_flip")
        matrix = np.array(matrix)
        return np.flip(matrix, axis=0)

    def rotate_90(self, matrix, is_right=None):
        print(f"rotate_90")
        if is_right:
            return [row[::-1] for row in zip(*matrix)]

        else:
            return [row for row in zip(*matrix)][::-1]

    @auto_fill_color
    @with_dimensions
    @prepare_angle
    @prepare_values
    def rotate_small_angle(self, matrix, h, w, params, is_right=None, angle=None, fill=None):
        print(f"rotate_small_angle")
        c, s, cx, cy = params['cos_a'], params['sin_a'], params['cx'], params['cy']
        new_m = params['new_matrix']

        for y_new, x_new in product(range(h), range(w)):
            tx, ty = x_new - cx, y_new - cy
            xf = tx * c + ty * s + cx
            yf = -tx * s + ty * c + cy

            x1, y1 = math.floor(xf), math.floor(yf)
            
            if 0 <= y1 < h - 1 and 0 <= x1 < w - 1:
                dx, dy = xf - x1, yf - y1
                
                v = [matrix[y1][x1], matrix[y1][x1+1], matrix[y1+1][x1], matrix[y1+1][x1+1]]
                top = v[0] * (1 - dx) + v[1] * dx
                bottom = v[2] * (1 - dx) + v[3] * dx
                new_m[y_new][x_new] = int(round(top * (1 - dy) + bottom * dy))

            elif 0 <= x1 < w and 0 <= y1 < h:
                new_m[y_new][x_new] = matrix[y1][x1]
        
        return new_m

    def __create_supplement_all_sides__(self, matrix, x_y_axis, shade_gray_color):
        x_axis, y_axis = x_y_axis
        copy_len_row = len(matrix[0]) + y_axis * 2
        new_matrix = []

        for _ in range(x_axis):
            new_matrix.append([shade_gray_color] * copy_len_row)

        for row in matrix:
            new_matrix.append(
                [shade_gray_color] * y_axis + row + [shade_gray_color] * y_axis
            )

        for _ in range(x_axis):
            new_matrix.append([shade_gray_color] * copy_len_row)

        return new_matrix

    @auto_fill_color
    @with_dimensions
    def random_shift(self, matrix, h, w, max_dx_dy=None, fill=None, is_right=None):
        match is_right:
            case True:
                dx, dy = random.randint(1, 4), random.randint(-4, 4)
            case False:
                dx, dy = random.randint(-4, -1), random.randint(-4, 4)
            case _:
                dx, dy = max_dx_dy if max_dx_dy else (
                    random.randint(-4, 4),
                    random.randint(-4, 4)
                )

        padded = self.__create_supplement_all_sides__(matrix, (dx, dy), fill)

        sx = random.randint(0, abs(dx) * 2)
        sy = random.randint(0, abs(dy) * 2)

        return [row[sx : sx + w] for row in padded[sy : sy + h]]

class NoiseAugmentation(NoiseAugmentationABC):
    def gaussian_noise(self, matrix, std=random.uniform(0.1, 5)):
        np_matrix = np.array(matrix)

        std_matrix = np.random.normal(0, std, np_matrix.shape).round().astype(int)

        return np_matrix + std_matrix

    def salt_and_pepper(self, matrix, prob=random.uniform(0.01, 0.05)) -> TypeMatrix:
        result = np.array(matrix, copy=True)

        random_matrix = np.random.random(result.shape)

        result[random_matrix < (prob / 2)] = 0
        result[random_matrix > (1 - prob / 2)] = 255

        return result

class MorphologyAugmentation(MorphologyAugmentationABC):
    def __max_neighbor__(self, matrix, y, x, r):
        h, w = len(matrix), len(matrix[0])
        max_el = 0
        for dy, dx in product(r, repeat=2):
            ny, nx = y + dy, x + dx
            if 0 <= ny < h and 0 <= nx < w:
                max_el = max(matrix[ny][nx], max_el)
        return max_el

    @kernel_data_processing
    def dilate(self, matrix, kernel_size, fill=None, r=None):
        print(f"dilate")
        h, w = len(matrix), len(matrix[0])
        new_matrix = [[0 for _ in range(w)] for _ in range(h)]
        
        for y, x in product(range(h), range(w)):
            new_matrix[y][x] = self.__max_neighbor__(matrix, y, x, r)
            
        return new_matrix

    @auto_fill_color
    @kernel_data_processing
    def erode(self, matrix, kernel_size, fill=None, r=None):
        print(f"erode")
        h, w = len(matrix), len(matrix[0])
        new_matrix = [[fill for _ in range(w)] for _ in range(h)]

        for y, x in product(range(h), range(w)):
            is_obj = True
            for dy, dx in product(r, repeat=2):
                ny, nx = y + dy, x + dx
                if 0 <= ny < h and 0 <= nx < w:
                    if matrix[ny][nx] == fill:
                        is_obj = False
                        break
                else:
                    is_obj = False
                    break
            
            if is_obj:
                new_matrix[y][x] = matrix[y][x]

        return new_matrix

    @auto_fill_color
    @kernel_data_processing
    def get_boundaries(self, matrix, kernel_size, fill=None, r=None):
        print(f"get_boundaries")
        eroded_matrix = self.erode(matrix, kernel_size, fill=fill)
        
        h, w = len(matrix), len(matrix[0])
        
        new_matrix = [[fill for _ in range(w)] for _ in range(h)]

        for y, x in product(range(h), range(w)):
            orig_pixel = matrix[y][x]
            eroded_pixel = eroded_matrix[y][x]

            if orig_pixel != eroded_pixel:
                new_matrix[y][x] = orig_pixel
        
        return new_matrix
    
    @auto_fill_color
    def closing(self, matrix, kernel_size, fill=None):
        print(f"closing")
        temp = self.dilate(matrix, kernel_size=kernel_size, fill=fill)
        return self.erode(temp, kernel_size=kernel_size, fill=fill)

    @auto_fill_color
    def opening(self, matrix, kernel_size, fill=None):
        print(f"opening")
        temp = self.erode(matrix, kernel_size=kernel_size, fill=fill)
        return self.dilate(temp, kernel_size=kernel_size, fill=fill)