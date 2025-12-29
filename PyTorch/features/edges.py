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

class __EdgeDetector__(ABC):
    @abstractmethod
    def apply(self, matrix: TypeMatrix) -> TypeMatrix:
        pass

class Sobel(__EdgeDetector__):
    def apply(self, matrix: TypeMatrix) -> TypeMatrix:
        pass

class Prewitt(__EdgeDetector__):
    def apply(self, matrix: TypeMatrix) -> TypeMatrix:
        pass
