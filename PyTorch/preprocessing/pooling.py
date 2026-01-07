from abc import ABC, abstractmethod
from itertools import product

class __Pooling__(ABC):
    @abstractmethod
    def max_pool(self, matrix, kernel_size: tuple[int, int], stride: int, pad_width: int, pad_values: int):
        pass

class Pooling(__Pooling__):
    def _apply_padding(self, matrix, pad_width, pad_values):
        multipad = [
            [pad_values for _ in range(len(matrix[0]) + pad_width * 2)] 
            for _ in range(pad_width)
        ]
        
        middle_matrix = []
        side_padding = [pad_values] * pad_width
        
        for row in matrix:
            new_row = side_padding + list(row) + side_padding
            middle_matrix.append(new_row)

        final_matrix = multipad + middle_matrix + multipad
        
        return final_matrix

    def _max_window(self, matrix, axis_x, axis_y, kernel_size):
        return max(
            matrix[axis_y + fy][axis_x + fx]
            for fy, fx in product(range(kernel_size[0]), range(kernel_size[1]))
        )
    
    def max_pool(self, matrix, kernel_size=(2, 2), stride=None, pad_width=0, pad_values=0):
        if stride is None:
            stride = kernel_size[0]
            
        if pad_width > 0:
            matrix = self._apply_padding(matrix, pad_width, pad_values)

        return [
            [
                self._max_window(matrix, x, y, kernel_size)
                for x in range(0, len(matrix[0]) - kernel_size[1] + 1, stride)
            ]
            for y in range(0, len(matrix) - kernel_size[0] + 1, stride)
        ]
    
pooling = Pooling()
matrix = [
    [1, 2, 3, 4],
    [4, 5, 6, 7],
    [7, 8, 9, 10],
    [11, 12, 13, 14]
]

matrix = pooling.max_pool(matrix)
for row in matrix:
    print(row)