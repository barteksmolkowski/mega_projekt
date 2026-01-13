import random
from abc import ABC, abstractmethod
from typing import Any, List, Literal, Optional, Tuple, overload

import matplotlib.pyplot as plt
import numpy as np
from numpy.lib.stride_tricks import sliding_window_view

from .common import TypeMatrix
from .decorators import (
    auto_fill_color,
    get_number_repeats,
    kernel_data_processing,
    prepare_angle,
    prepare_values,
    with_dimensions,
)


class DataAugmentationABC(ABC):
    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def augment(
        self, 
        M: TypeMatrix, 
        repeats: int
    ) -> List[TypeMatrix]:
        pass

class GeometryAugmentationABC(ABC):
    @abstractmethod
    def horizontal_flip(
        self, 
        M: np.ndarray
    ) -> np.ndarray:
        pass

    @abstractmethod
    def vertical_flip(
        self, 
        M: np.ndarray
    ) -> np.ndarray:
        pass

    @overload
    @abstractmethod
    def rotate_90(
        self, 
        M: np.ndarray, 
        is_right: Literal[True] = True
    ) -> np.ndarray: ...

    @overload
    @abstractmethod
    def rotate_90(
        self, 
        M: np.ndarray, 
        is_right: Literal[False]
    ) -> np.ndarray: ...

    @abstractmethod
    def rotate_90(
        self, 
        M: np.ndarray, 
        is_right: bool = True
    ) -> np.ndarray:
        pass

    @abstractmethod
    def rotate_small_angle(
        self, 
        M: np.ndarray, 
        h: int, 
        w: int, 
        params: dict, 
        is_right: Optional[bool] = None, 
        angle: Optional[float] = None, 
        fill: Optional[int] = None,
        **kwargs
    ) -> np.ndarray:
        pass

    @abstractmethod
    def random_shift(
        self, 
        M: np.ndarray, 
        h: int, 
        w: int, 
        max_dx_dy: Optional[Tuple[int, int]] = None, 
        fill: Optional[int] = None, 
        is_right: Optional[bool] = None,
        **kwargs
    ) -> np.ndarray:
        pass

class NoiseAugmentationABC(ABC):
    @abstractmethod
    def gaussian_noise(
        self, 
        M: np.ndarray, 
        std: Optional[float] = None
    ) -> np.ndarray:
        pass

    @abstractmethod
    def salt_and_pepper(
        self,
        M: np.ndarray, 
        prob: Optional[float] = None
    ) -> np.ndarray:
        pass

class MorphologyAugmentationABC(ABC):
    @abstractmethod
    def dilate(
        self, 
        M: np.ndarray, 
        kernel_size: int, 
        **kwargs: Any
    ) -> np.ndarray:
        pass

    @abstractmethod
    def erode(
        self, 
        M: np.ndarray, 
        kernel_size: int, 
        fill: int = 0, 
        **kwargs: Any
    ) -> np.ndarray:
        pass
        
    @abstractmethod
    def get_boundaries(
        self, 
        M: np.ndarray, 
        kernel_size: int, 
        fill: int = 0, 
        **kwargs: Any
    ) -> np.ndarray:
        pass

    @abstractmethod
    def morphology_filter(
        self,
        M: np.ndarray, 
        kernel_size: int, 
        fill: int = 0,
        mode: Literal["open", "close"] = "open",
        **kwargs: Any
    ) -> np.ndarray:
        pass

class DataAugmentation(DataAugmentationABC):
    def __init__(self):
        self.geometry = GeometryAugmentation()
        self.noise = NoiseAugmentation()
        self.morphology = MorphologyAugmentation()

    def _get_augmentation_groups(self):
        return {
            "Flip": [
                (lambda m: self.geometry.horizontal_flip(m), "H-Flip"),
                (lambda m: self.geometry.vertical_flip(m), "V-Flip")
            ],
            "Rotation": [
                (lambda m: self.geometry.rotate_90(m, is_right=True), "Rot90-R"),
                (lambda m: self.geometry.rotate_90(m, is_right=False), "Rot90-L"),
                (lambda m: self.geometry.rotate_small_angle(m, is_right=True), "RotSmall-R"),
                (lambda m: self.geometry.rotate_small_angle(m, is_right=False), "RotSmall-L")
            ],
            "Morphology": [
                (lambda m: self.morphology.dilate(m, kernel_size=3), "Dilate"),
                (lambda m: self.morphology.erode(m, kernel_size=3), "Erode"),
                (lambda m: self.morphology.get_boundaries(m, kernel_size=3), "Boundaries"),
                (lambda m: self.morphology.morphology_filter(m, 3, mode="open"), "Opening"),
                (lambda m: self.morphology.morphology_filter(m, 3, mode="close"), "Closing")
            ],
            "Noise_Shift": [
                (lambda m: self.noise.gaussian_noise(m), "Gauss-Noise"),
                (lambda m: self.noise.salt_and_pepper(m), "S&P-Noise"),
                (lambda m: self.geometry.random_shift(m, is_right=True), "Shift-R"),
                (lambda m: self.geometry.random_shift(m, is_right=False), "Shift-L")
            ]
        }

    @get_number_repeats
    def augment(
        self, 
        M: np.ndarray, 
        repeats: Optional[int] = None,
        debug: bool = False
    ) -> List[np.ndarray]:
        groups = {
            "Flip": [
                (lambda m: self.geometry.horizontal_flip(m), "H-Flip"),
                (lambda m: self.geometry.vertical_flip(m), "V-Flip")
            ],
            "Rotation": [
                (lambda m: self.geometry.rotate_90(m, is_right=True), "Rot90-R"),
                (lambda m: self.geometry.rotate_90(m, is_right=False), "Rot90-L"),
                (lambda m: self.geometry.rotate_small_angle(m, is_right=True), "RotSmall-R"),
                (lambda m: self.geometry.rotate_small_angle(m, is_right=False), "RotSmall-L")
            ],
            "Shift": [
                (lambda m: self.geometry.random_shift(m, is_right=True), "Shift-R"),
                (lambda m: self.geometry.random_shift(m, is_right=False), "Shift-L")
            ],
            "Noise": [
                (lambda m: self.noise.gaussian_noise(m), "Gauss-Noise"),
                (lambda m: self.noise.salt_and_pepper(m), "S&P-Noise")
            ],
            "Morphology": [
                (lambda m: self.morphology.dilate(m, kernel_size=3), "Dilate"),
                (lambda m: self.morphology.erode(m, kernel_size=3), "Erode"),
                (lambda m: self.morphology.get_boundaries(m, kernel_size=3), "Boundaries"),
                (lambda m: self.morphology.morphology_filter(m, 3, mode="open"), "Opening"),
                (lambda m: self.morphology.morphology_filter(m, 3, mode="close"), "Closing")
            ]
        }
        
        result = []
        histories = []
        M_arr = np.asanyarray(M).astype(np.uint8)
        orig_px = np.sum(M_arr > 0)

        while len(result) < repeats:
            new_m = M_arr.copy()
            chosen_ops = []

            available_groups = list(groups.keys())
            selected_groups = random.sample(available_groups, 3)

            for g_name in selected_groups:
                op = random.choice(groups[g_name])
                chosen_ops.append(op)

            names = [name for _, name in chosen_ops]
            
            if "Boundaries" in names and "Erode" in names:
                continue 

            for func, _ in chosen_ops:
                new_m = func(new_m)

            temp_test = self.morphology.erode(new_m, kernel_size=3)
            final_px = np.sum(temp_test > 0)
            retention = final_px / orig_px if orig_px > 0 else 0

            if 0.4 < retention < 2.5:
                img_final = new_m.astype(np.uint8)
                result.append(img_final)
                if debug:
                    histories.append(names)
        
        if debug:
            cols = 10
            rows = (len(result) + cols - 1) // cols
            
            fig, axes = plt.subplots(rows, cols, figsize=(15, 1.6 * rows), 
                                    gridspec_kw={'wspace': 0.1, 'hspace': 0.4},
                                    squeeze=False)
            
            axes_flat = axes.flatten()
            
            for i in range(len(result)):
                axes_flat[i].imshow(result[i], cmap='gray')
                axes_flat[i].set_title(f"NR: {i+1}", fontsize=9, fontweight='bold')
                axes_flat[i].axis('off')
            
            for j in range(len(result), len(axes_flat)):
                axes_flat[j].axis('off')
                
            plt.show()

            print("\n" + "="*50 + "TRYB INTERAKTYWNEGO DEBUGOWANIA (2026)" + "="*50)
            
            while True:
                user_input = input("\nPodaj numery rysunków, które wyglądają źle (np. 1, 5, 12) lub 'q' aby wyjść: ")
                
                if user_input.lower() == 'q':
                    break
                
                try:
                    selected_indices = [int(x.strip()) - 1 for x in user_input.split(",") if x.strip()]
                    
                    for idx in selected_indices:
                        if 0 <= idx < len(histories):
                            print(f"\n[RYSUNEK {idx+1}] Ścieżka operacji:")
                            steps = histories[idx]
                            formatted_history = " -> ".join([f"[{i+1}] {name}" for i, name in enumerate(steps)])
                            print(f"  {formatted_history}")
                        else:
                            print(f"[!] Numer {idx+1} jest poza zakresem.")
                except ValueError:
                    print("[!] Błąd! Wpisz liczby oddzielone przecinkami lub 'q'.")

        return result

class GeometryAugmentation(GeometryAugmentationABC):
    def horizontal_flip(self, M: np.ndarray) -> np.ndarray:
        return np.asanyarray(M)[:, ::-1]
        
    def vertical_flip(self, M: np.ndarray) -> np.ndarray:
        return np.asanyarray(M)[::-1, :]

    def rotate_90(
        self, 
        M: np.ndarray, 
        is_right: bool = True
    ) -> np.ndarray:
        M = np.asanyarray(M)
        h, w = M.shape
        
        y, x = np.indices((h, w))

        if is_right:
            new_y = x
            new_x = h - (1 + y)
        else:
            new_y = w - (1 + x)
            new_x = y
        
        res = np.zeros((w, h), dtype=M.dtype)
        
        res[new_y, new_x] = M
        return res

    @auto_fill_color
    @with_dimensions
    @prepare_angle
    @prepare_values
    def rotate_small_angle(
        self, 
        M: np.ndarray, 
        h: int, 
        w: int, 
        params: dict, 
        is_right: Optional[bool] = None, 
        angle: Optional[float] = None, 
        fill: Optional[int] = None,
        **kwargs
    ) -> np.ndarray:
        c, s = params['cos_a'], params['sin_a']
        cx, cy = params['cx'], params['cy']
        new_m = params['new_matrix'] 

        y_new, x_new = np.indices((h, w))
        
        tx, ty = x_new - cx, y_new - cy
        xf = tx * c + ty * s + cx
        yf = -tx * s + ty * c + cy

        mask = (xf >= 0) & (xf < w - 1) & (yf >= 0) & (yf < h - 1)
        
        xi = xf[mask].astype(int)
        yi = yf[mask].astype(int)
        
        new_m[y_new[mask], x_new[mask]] = M[yi, xi]
        
        return new_m.astype(np.uint8)

    def __create_supplement_all_sides__(
        self, 
        M: np.ndarray, 
        x_y_axis: Tuple[int, int], 
        shade_gray_color: int
    ) -> np.ndarray:
        dx, dy = x_y_axis
        return np.pad(
            M, 
            pad_width=((abs(dy), abs(dy)), (abs(dx), abs(dx))), 
            mode='constant', 
            constant_values=shade_gray_color
        ).astype(np.uint8)

    @auto_fill_color
    @with_dimensions
    def random_shift(
        self, 
        M: np.ndarray, 
        h: int, 
        w: int, 
        max_dx_dy: Optional[Tuple[int, int]] = None, 
        fill: Optional[int] = None, 
        is_right: Optional[bool] = None,
        **kwargs
    ) -> np.ndarray:
        if is_right is True:
            dx, dy = random.randint(1, 4), random.randint(-4, 4)
        elif is_right is False:
            dx, dy = random.randint(-4, -1), random.randint(-4, 4)
        else:
            dx, dy = max_dx_dy if max_dx_dy else (random.randint(-4, 4), random.randint(-4, 4))

        padded = self.__create_supplement_all_sides__(M, (dx, dy), fill)

        sx = random.randint(0, abs(dx) * 2)
        sy = random.randint(0, abs(dy) * 2)

        return padded[sy : sy + h, sx : sx + w].copy()

class NoiseAugmentation(NoiseAugmentationABC):
    def gaussian_noise(
        self, 
        M: np.ndarray, 
        std: Optional[float] = None,
        **kwargs
    ) -> np.ndarray:
        if std is None:
            std = random.uniform(0.1, 5)

        np_M = np.asanyarray(M).astype(np.float32)

        noise = np.random.normal(0, std, np_M.shape)
        result = np.clip(np_M + noise, 0, 255)

        return result.astype(np.uint8)

    def salt_and_pepper(
        self, 
        M: np.ndarray, 
        prob: Optional[float] = None,
        **kwargs
    ) -> np.ndarray:
        if prob is None:
            prob = random.uniform(0.01, 0.05)
            
        result = np.array(M, copy=True).astype(np.uint8)

        random_M = np.random.random(result.shape)

        result[random_M < (prob / 2)] = 0
        result[random_M > (1 - prob / 2)] = 255

        return result
    
class MorphologyAugmentation(MorphologyAugmentationABC):
    def _apply_morphology(
        self, 
        M: np.ndarray, 
        kernel_size: int, 
        op: Literal["min", "max"], 
        pad_value: int
    ) -> np.ndarray:
        M = np.asanyarray(M).astype(np.uint8)
        pad_size = (kernel_size - 1) // 2
        
        padded = np.pad(M, pad_width=pad_size, mode='constant', constant_values=pad_value)
        
        windows = sliding_window_view(padded, (kernel_size, kernel_size))
        
        if op == "max":
            return np.max(windows, axis=(2, 3)).astype(np.uint8)
        return np.min(windows, axis=(2, 3)).astype(np.uint8)

    @kernel_data_processing
    def dilate(
        self, 
        M: np.ndarray, 
        kernel_size: int, 
        **kwargs
    ) -> np.ndarray:
        return self._apply_morphology(M, kernel_size, op="max", pad_value=0)

    @auto_fill_color
    @kernel_data_processing
    def erode(
        self, 
        M: np.ndarray, 
        kernel_size: int, 
        fill: int = 0, 
        **kwargs
    ) -> np.ndarray:
        return self._apply_morphology(M, kernel_size, op="min", pad_value=fill)

    @auto_fill_color
    @kernel_data_processing
    def get_boundaries(
        self, 
        M: np.ndarray, 
        kernel_size: int, 
        fill: int = 0, 
        **kwargs
    ) -> np.ndarray:
        eroded_M = self.erode(M, kernel_size, fill=fill)

        res = np.full(M.shape, fill, dtype=np.uint8)
        
        mask = M != eroded_M
        res[mask] = M[mask]

        return res
    
    @auto_fill_color
    def morphology_filter(
        self,
        M: np.ndarray, 
        kernel_size: int, 
        fill: int = 0,
        mode: Literal["open", "close"] = "open",
        **kwargs
    ) -> np.ndarray:
        if mode == "open":
            temp = self.erode(M, kernel_size=kernel_size, fill=fill)
            return self.dilate(temp, kernel_size=kernel_size)
        else:
            temp = self.dilate(M, kernel_size=kernel_size)
            return self.erode(temp, kernel_size=kernel_size, fill=fill)