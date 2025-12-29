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

class __Thresholding__(ABC):
    @abstractmethod
    def apply_threshold(
        self,
        matrix: TypeMatrix,
        threshold: int
    ) -> TypeMatrix:
        pass

    @abstractmethod
    def adaptive_threshold(
        self,
        matrix: TypeMatrix,
        block_size: int,
        c: int
    ) -> TypeMatrix:
        pass

class Thresholding(__Thresholding__):
    def apply_threshold(self, matrix, threshold):
        0

    def adaptive_threshold(self, matrix, block_size, c):
        0