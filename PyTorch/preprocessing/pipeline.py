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

class __TransformPipeline__(ABC):
    @abstractmethod
    def apply(self, matrix_channels: MatrixChannels) -> MatrixChannels:
        pass

class TransformPipeline(__TransformPipeline__):
    def apply(self, matrix_channels):
        0

class __ImageDataPreprocessing__(ABC):
    @abstractmethod
    def preprocess(self, path: str) -> MatrixChannels:
        pass

class ImageDataPreprocessing(__ImageDataPreprocessing__):
    def preprocess(self, path):
        0