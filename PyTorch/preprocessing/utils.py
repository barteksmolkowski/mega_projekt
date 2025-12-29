from functools import wraps

def with_dimensions(func):
    """Techniczne wyciąganie h i w - przydatne w każdym module."""
    @wraps(func)
    def wrapper(self, matrix, *args, **kwargs):
        h = len(matrix)
        w = len(matrix[0]) if h > 0 else 0
        return func(self, matrix, h, w, *args, **kwargs)
    return wrapper

# Tutaj w przyszłości dodasz np. @timer lub @check_matrix_type
# takie ogolne