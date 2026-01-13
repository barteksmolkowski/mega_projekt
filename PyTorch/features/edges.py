from .common import ABC, TypeMatrix, abstractmethod


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
