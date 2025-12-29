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

class __Normalization__(ABC):
    @abstractmethod
    def min_max_normalization(
        self,
        matrix_channels: MatrixChannels,
        new_min: float,
        new_max: float
    ) -> MatrixChannels:
        pass

    @abstractmethod
    def z_score_normalization(
        self,
        matrix_channels: MatrixChannels
    ) -> MatrixChannels:
        pass
