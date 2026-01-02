from functools import wraps
import time

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