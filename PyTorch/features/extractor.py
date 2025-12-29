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

from edges import Sobel, Prewitt
from hog import HOG

class __FeatureExtraction__(ABC):
    @abstractmethod
    def extract_edges(self, matrix: TypeMatrix) -> TypeMatrix:
        pass

    @abstractmethod
    def extract_features(self, matrix: TypeMatrix) -> List[float]:
        pass

class FeatureExtraction(__FeatureExtraction__):
    def __init__(self):
        0

    def extract_edges(self, matrix: TypeMatrix) -> TypeMatrix:
        0

    def extract_features(self, matrix: TypeMatrix) -> List[float]:
        0
