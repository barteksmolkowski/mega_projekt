import time
from functools import wraps

import numpy as np
from PIL import Image, ImageDraw

__all__ = ["get_test_digit_28x28", "with_dimensions", "timer"]

def with_dimensions(func):
    @wraps(func)
    def wrapper(self, matrix, *args, **kwargs):
        h = len(matrix)
        w = len(matrix[0]) if h > 0 else 0
        return func(self, matrix, h, w, *args, **kwargs)
    return wrapper

def timer(func):
    def wrapper(self, *args, **kwargs):
        start = time.perf_counter()
        result = func(self, *args, **kwargs)
        print(f"Metoda {func.__name__} zajęła {time.perf_counter() - start:.4f}s")
        return result
    return wrapper

def get_test_digit_28x28() -> np.ndarray:
    img = Image.new('L', (28, 28), 0)
    draw = ImageDraw.Draw(img)
    
    draw.ellipse([7, 3, 20, 14], outline=255, width=2)   # Górne kółko
    draw.ellipse([6, 13, 22, 25], outline=255, width=2)  # Dolne kółko
    
    return np.array(img, dtype=np.uint8)