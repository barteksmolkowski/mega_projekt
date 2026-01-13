from .common import ABC, List, TypeMatrix, abstractmethod


class __HOG__(ABC):
    @abstractmethod
    def extract(self, matrix: TypeMatrix) -> List[float]:
        pass

class HOG(__HOG__):
    def extract(self, matrix: TypeMatrix) -> List[float]:
        pass
