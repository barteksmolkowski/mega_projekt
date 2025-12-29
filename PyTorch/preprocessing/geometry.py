from common import (
    ABC,
    abstractmethod,
    random,
    math,
    TypeColor,
    TypeMatrix,
    TypeIMG,
    MatrixChannels,
    List,
    Tuple
)

class __MatrixCreator__(ABC):
    @abstractmethod
    def create(self, height: int, width: int, value: int = -1) -> TypeMatrix:
        pass

    @abstractmethod
    def pad(self, matrix: TypeMatrix, pad_value: int = -1, pad_size: int = 1) -> TypeMatrix:
        pass

class __MatrixProcessor__(ABC):
    @abstractmethod
    def normalization(self, matrix_channels: MatrixChannels) -> MatrixChannels:
        pass

    @abstractmethod
    def resize(self, matrix_channels: MatrixChannels) -> MatrixChannels:
        pass

class MatrixCreator(__MatrixCreator__):
    def create(self, height, width, value):
        return [[value for _ in range(width)] for _ in range(height)]

    def pad(self, matrix, pad_value, pad_size):
        h, w = len(matrix), len(matrix[0])
        new_h, new_w = h + 2 * pad_size, w + 2 * pad_size
        new_matrix = self.create(new_h, new_w, pad_value)

        for y in range(h):
            for x in range(w):
                new_matrix[y + pad_size][x + pad_size] = matrix[y][x]

        return new_matrix
    
class MatrixProcessor(__MatrixProcessor__):
    def normalization(self, matrix_channels):
        0

    def resize(self, matrix_channels):
        0

