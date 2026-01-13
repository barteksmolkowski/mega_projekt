from abc import ABC, abstractmethod
from typing import Optional

from .augmentation import DataAugmentation
from .common import MatrixChannels, TypeMatrix
from .conversion import ImageToMatrixConverter
from .convolution import ConvolutionActions
from .geometry import ImageGeometry
from .grayscale import GrayScaleProcessing
from .io_image import ImageHandler
from .normalization import Normalization
from .pooling import Pooling
from .thresholding import Thresholding


class __TransformPipeline__(ABC):
    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def apply(self, matrix: TypeMatrix) -> TypeMatrix:
        pass

class __ImageDataPreprocessing__(ABC):
    @abstractmethod
    def preprocess(self, path: str) -> Optional[MatrixChannels]:
        pass

class TransformPipeline(__TransformPipeline__):
    def __init__(self):
        self.image_handler = ImageHandler()
        self.gray_scale_processing = GrayScaleProcessing()
        self.geometry = ImageGeometry()
        self.normalization = Normalization()
        self.augmentation = DataAugmentation()
        self.pooling = Pooling()
        self.thresholding = Thresholding()
        self.convolution = ConvolutionActions()

    def apply(self, matrix: TypeMatrix) -> TypeMatrix:
        """def kolejności obróbki zdjęcia."""
        x = matrix
        return x

class ImageDataPreprocessing(__ImageDataPreprocessing__):
    def __init__(self):
        self.handler = ImageHandler()
        self.converter = ImageToMatrixConverter()
        self.pipeline = TransformPipeline()

    def preprocess(self, path: str) -> Optional[MatrixChannels]:
        """
        Główny punkt wejścia do przetwarzania konkretnego pliku.
        """
        return None