import math
import random
from functools import wraps
from typing import Any, Callable, Dict, Optional, Tuple, TypeVar, cast

import numpy as np

__all__ = [
    "auto_fill_color",
    "with_dimensions",
    "prepare_angle",
    "prepare_values",
    "get_number_repeats",
    "kernel_data_processing",
    "parameter_complement"
]

F = TypeVar('F', bound=Callable[..., Any])

def auto_fill_color(func: F) -> F:
    @wraps(func)
    def wrapper(self, M: Any, *args, **kwargs):
        M = np.asanyarray(M)
        if kwargs.get("fill") is None:
            values, counts = np.unique(M, return_counts=True)
            kwargs["fill"] = values[np.argmax(counts)]
        return func(self, M, *args, **kwargs)
    return cast(F, wrapper)

def with_dimensions(func: F) -> F:
    @wraps(func)
    def wrapper(self, M: Any, *args, **kwargs):
        M = np.asanyarray(M)
        h, w = M.shape
        return func(self, M, h, w, *args, **kwargs)
    return cast(F, wrapper)

def prepare_angle(func: F) -> F:
    @wraps(func)
    def wrapper(self, M: Any, *args, **kwargs):
        is_right = kwargs.get("is_right")
        limits: Dict[Optional[bool], Tuple[int, int]] = {
            True: (0, 30),
            False: (-30, 0),
            None: (-30, 30)
        }
        low, high = limits.get(is_right, (-50, 50))
        
        if kwargs.get("angle") is None:
            kwargs["angle"] = random.randint(low, high)
        return func(self, M, *args, **kwargs)
    return cast(F, wrapper)

def prepare_values(func: F) -> F:
    @wraps(func)
    def wrapper(self, M: Any, h: int, w: int, angle: float = 0, fill: int = 0, **kwargs):
        rad = math.radians(angle)
        M = np.asanyarray(M)
        
        params = {
            'cos_a': math.cos(rad),
            'sin_a': math.sin(rad),
            'cx': w / 2.0,
            'cy': h / 2.0,
            'new_matrix': np.full((h, w), fill, dtype=M.dtype)
        }
        return func(self, M, h, w, params=params, angle=angle, fill=fill, **kwargs)
    return cast(F, wrapper)

def get_number_repeats(func: F) -> F:
    @wraps(func)
    def wrapper(*args, **kwargs):
        if "repeats" not in kwargs and len(args) <= 2:
            kwargs["repeats"] = random.randrange(2, 5)
        return func(*args, **kwargs)
    return cast(F, wrapper)

def kernel_data_processing(func: F) -> F:
    @wraps(func)
    def wrapper(self, M: Any, *args, **kwargs):
        k_size = kwargs.get("kernel_size")
        if k_size is None and args:
            k_size = args[0]
            
        if k_size is not None:
            r_val = (k_size - 1) // 2
            kwargs["r"] = range(-r_val, r_val + 1)
            
        return func(self, M, *args, **kwargs)
    return cast(F, wrapper)

def parameter_complement(func: F) -> F:
    @wraps(func)
    def wrapper(self, matrix: Any, *args, **kwargs):
        matrix = np.asanyarray(matrix)
        h, w = matrix.shape[:2]
        
        if kwargs.get("auto_params"):
            b_size = int(min(h, w) * 0.25)
            if b_size % 2 == 0:
                b_size += 1
            b_size = max(3, b_size)

            kwargs["block_size"] = b_size
            kwargs["c"] = 7
            
        return func(self, matrix, *args, **kwargs)
    return cast(F, wrapper)