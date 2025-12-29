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

class __ConvolutionActions__(ABC):
    @staticmethod
    @abstractmethod
    def convolution_2d(self, matrix: TypeMatrix, filtrs: List[TypeMatrix] = None, dilated: int = 1) -> List[TypeMatrix]:
        pass

    @staticmethod
    @abstractmethod
    def apply_filter_to_channels_or_path(self, channels_or_path: List[TypeMatrix], filtr: List[TypeMatrix], padding: bool = True) -> List[TypeMatrix]:
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
                    for fy in range(fh):
                        for fx in range(fw):
                            s += matrix[y + fy * dil][x + fx * dil] * filtr[fy][fx]
                    row.append(s)
                result.append(row)
            results.append(result)

        return results

    @staticmethod
    def apply_filter_to_channels_or_path(channels_or_path: List[TypeMatrix], filtr: List[TypeMatrix], padding: bool = True) -> List[TypeMatrix]:
        results = []
        for channel in channels_or_path:
            if padding:
                channel = MatrixProcessor.pad(channel, -1, 1)
            results.append(
                ConvolutionActions.convolution_2d(channel, filtr)
            )

        return results