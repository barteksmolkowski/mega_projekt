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
class __HOG__(ABC):
    @abstractmethod
    def extract(self, matrix: TypeMatrix) -> List[float]:
        pass

class HOG(__HOG__):
    def extract(self, matrix: TypeMatrix) -> List[float]:
        pass
