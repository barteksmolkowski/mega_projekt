from abc import ABC, abstractmethod

from common import (
    TypeIMG,
    MatrixChannels
)
class __ImageToMatrixConverter__(ABC):
    @abstractmethod
    def convert_image_to_matrix(self, path: str) -> MatrixChannels:
        pass

    @abstractmethod
    def separate_channels(self, matrix: TypeIMG) -> MatrixChannels:
        pass

class ImageToMatrixConverter(__ImageToMatrixConverter__):
    def convert_image_to_matrix(self, path):
        img, width, height = self.open_image(path)
        matrix = []

        for y in range(height):
            row = []
            for x in range(width):
                row.append(img.getpixel((x, y)))
            matrix.append(row)

        return matrix

    def separate_channels(self, matrix):
        return [
            [[matrix[y][x][i] for x in range(len(matrix[0]))]
             for y in range(len(matrix))]
            for i in range(3)
        ]