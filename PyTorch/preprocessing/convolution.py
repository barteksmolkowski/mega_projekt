from abc import ABC, abstractmethod
from itertools import product

from common import (
    TypeMatrix,
    List
)

from geometry import MatrixCreator

class __ConvolutionActions__(ABC):
    @staticmethod
    @abstractmethod
    def convolution_2d(self, matrix: TypeMatrix, filtrs: List[TypeMatrix] = None, dilated: int = 1) -> List[TypeMatrix]:
        pass

    @staticmethod
    @abstractmethod
    def apply_filters(self, channels_or_path: List[TypeMatrix], filtr: List[TypeMatrix], padding: bool = True) -> List[TypeMatrix]:
        pass

class ConvolutionActions(__ConvolutionActions__):
    @staticmethod
    def convolution_2d(matrix: TypeMatrix, filtrs: List[TypeMatrix] = None, dilated: int = 1) -> List[TypeMatrix]:
        if filtrs is None or len(filtrs) == 0:
            return [matrix]

        results = []
        h, w = len(matrix), len(matrix[0])

        for filtr in filtrs:
            fh, fw = len(filtr), len(filtr[0])
            result = []

            dil = dilated

            out_h = h - (fh - 1) * dil
            out_w = w - (fw - 1) * dil

            for y in range(out_h):
                row = []
                for x in range(out_w):
                    s = 0
                    for fy, fx in product(range(fh), range(fw)):
                        s += matrix[y + fy * dil][x + fx * dil] * filtr[fy][fx]
                    row.append(s)
                result.append(row)
            results.append(result)

        return results

    @staticmethod
    def apply_filters(matrix_three_channels: List[TypeMatrix], filtrs: List[TypeMatrix]) -> List[TypeMatrix]:
        results = []
        for filtr, matrix in product(filtrs, matrix_three_channels):
            print(f"aktualny filtr: {filtr}")
            matrix = MatrixCreator.pad(matrix, -1, 1)
            results = ConvolutionActions.convolution_2d(matrix, filtr)

        return results
    
convAct = ConvolutionActions()
threematrix = [
    [[1,2,3],[1,2,3],[1,2,3]],
    [[1,2,3],[1,2,3],[1,2,3]],
    [[1,2,3],[1,2,3],[1,2,3]]
]

convAct.apply_filters(threematrix, filtrs)

filtr_h = [[-1, -2, -1], [0, 0, 0], [1, 2, 1]]
filtr_v = [[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]]

filtrs = [filtr_h, filtr_v]

threematrix = [
    [[1,2,3],[1,2,3],[1,2,3]],
    [[1,2,3],[1,2,3],[1,2,3]],
    [[1,2,3],[1,2,3],[1,2,3]]
]
