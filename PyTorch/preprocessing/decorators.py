import random
import math
from functools import wraps

__all__ = [
    "auto_fill_color",
    "with_dimensions",
    "prepare_angle",
    "prepare_values",
    "get_number_repeats",
    "kernel_data_processing"
]

def auto_fill_color(func):
    """Logiczne szukanie tła - specyficzne dla augmentacji i AI."""
    @wraps(func)
    def wrapper(self, matrix, *args, **kwargs):
        if kwargs.get("fill") is None:
            dict_colors = {}
            for row in matrix:
                for el in row:
                    dict_colors[el] = dict_colors.get(el, 0) + 1
            max_element = max(dict_colors, key=dict_colors.get)
            kwargs["fill"] = max_element
        return func(self, matrix, *args, **kwargs)
    return wrapper

def with_dimensions(func):
    def wrapper(self, matrix, *args, **kwargs):
        h = len(matrix)
        w = len(matrix[0]) if h > 0 else 0
        return func(self, matrix, h, w, *args, **kwargs)
    
    return wrapper

def prepare_angle(func):
    def wrapper(self, matrix, *args, **kwargs):
        is_right = kwargs.get("is_right")
        dict_rotation_limits = {
            True: (0, 15),
            False: (-15, 0),
            None: (-15, 15)
        }

        rotation_limit = dict_rotation_limits[is_right]

        if kwargs.get("angle") is None:
            kwargs["angle"] = random.randint(rotation_limit[0], rotation_limit[1])

        return func(self, matrix, *args, **kwargs)
    
    return wrapper

def prepare_values(func):
    """Logiczne przygotowanie macierzy rotacji i parametrów sin/cos."""
    @wraps(func)
    def wrapper(self, matrix, h, w, angle=None, fill=0, **kwargs):
        rad = math.radians(angle)
        
        params = {
            'cos_a': math.cos(rad),
            'sin_a': math.sin(rad),
            'cx': w / 2,
            'cy': h / 2,
            'new_matrix': [[fill for _ in range(w)] for _ in range(h)]
        }
        return func(self, matrix, h, w, params=params, angle=angle, fill=fill, **kwargs)

    return wrapper

def get_number_repeats(func):
    def wrapper(*args, **kwargs):
        repeats_positional = len(args) > 2
        repeats_kw = "repeats" in kwargs

        if not repeats_positional and not repeats_kw:
            kwargs["repeats"] = random.randrange(2, 5)

        return func(*args, **kwargs)

    return wrapper

def kernel_data_processing(func):
    @wraps(func)
    def wrapper(self, matrix, *args, **kwargs):
        k_size = kwargs.get("kernel_size")
        
        if k_size is None and len(args) > 0:
            k_size = args[0]
            
        if k_size is not None:
            new_size = (k_size - 1) // 2
            kwargs["r"] = range(-new_size, new_size + 1)
            
        return func(self, matrix, *args, **kwargs)
    return wrapper

# przeniesc wszystkie dekoratory pomocnicze
# i importowac tematycznie te z augmentation do augmentation np