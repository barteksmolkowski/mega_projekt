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

class __GrayScaleProcessing__(ABC):
    @staticmethod
    @abstractmethod
    def rgb_to_grayscale(matrix_channels: MatrixChannels) -> TypeMatrix:
        pass

    @staticmethod
    @abstractmethod
    def grayscale_to_rgb(matrix: TypeMatrix) -> TypeIMG:
        pass

class GrayScaleProcessing(__GrayScaleProcessing__):
    @staticmethod
    def rgb_to_grayscale(matrix_channels):
        gray = []

        for row in matrix_channels:
            gray_row = []
            for (r, g, b) in row:
                value = int(0.299 * r + 0.587 * g + 0.114 * b)
                gray_row.append(value)
            gray.append(gray_row)

        return gray

    @staticmethod
    def grayscale_to_rgb(matrix):
        return [
            [(v, v, v) for v in row]
            for row in matrix
        ]
