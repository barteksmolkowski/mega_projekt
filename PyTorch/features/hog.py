from common import (
    ABC,
    abstractmethod,
    TypeMatrix,
    List
)
class __HOG__(ABC):
    @abstractmethod
    def extract(self, matrix: TypeMatrix) -> List[float]:
        pass

class HOG(__HOG__):
    def extract(self, matrix: TypeMatrix) -> List[float]:
        pass
