from abc import ABC, abstractmethod
from itertools import product
from typing import List, Literal, overload

from .common import TypeMatrix
from .geometry import ImageGeometry


class __ConvolutionActions__(ABC):
    @abstractmethod
    def convolution_2d(
        self,
        M: TypeMatrix,
        filtrs: List[TypeMatrix] = None,
        dilated: int = 1
        ) -> List[TypeMatrix]:
        pass

    @overload
    @abstractmethod
    def apply_filters(
        self, 
        channels_or_path: List[TypeMatrix], 
        filtr: List[TypeMatrix], 
        padding: Literal[True] = True
    ) -> List[TypeMatrix]: ...

    @overload
    @abstractmethod
    def apply_filters(
        self, 
        channels_or_path: List[TypeMatrix], 
        filtr: List[TypeMatrix], 
        padding: Literal[False]
    ) -> List[TypeMatrix]: ...

    @abstractmethod
    def apply_filters(
        self, 
        channels_or_path: List[TypeMatrix], 
        filtr: List[TypeMatrix], 
        padding: bool = True
    ) -> List[TypeMatrix]:
        pass

class ConvolutionActions(__ConvolutionActions__):
    def convolution_2d(
            M: TypeMatrix,
            filtrs: List[TypeMatrix] = None,
            dilated: int = 1
            ) -> List[TypeMatrix]:
        
        if filtrs is None or len(filtrs) == 0:
            return [M]

        results = []
        h, w = len(M), len(M[0])

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
                        s += M[y + fy * dil][x + fx * dil] * filtr[fy][fx]
                    row.append(s)
                result.append(row)
            results.append(result)

        return results

    def apply_filters(
            M_three_channels: List[TypeMatrix],
            filtrs: List[TypeMatrix]
            ) -> List[TypeMatrix]:
        
        results = []
        for filtr, M in product(filtrs, M_three_channels):
            print(f"aktualny filtr: {filtr}")
            M = ImageGeometry.pad(M, -1, 1)
            results = ConvolutionActions.convolution_2d(M, filtr)

        return results