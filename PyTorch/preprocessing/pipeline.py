from abc import ABC, abstractmethod
import random
import math
# 
from common import MatrixChannels
# po hasztagu metody jakie sa
from augmentation import DataAugmentation
    # def augment(self, matrix: TypeMatrix, repeats: int) -> List[TypeMatrix]:
    #     pass

from conversion import ImageToMatrixConverter
    # def get_channels_from_file(self, path: str) -> MatrixChannels:
    #     pass

from convolution import ConvolutionActions
    # def convolution_2d(self, matrix: TypeMatrix, filtrs: List[TypeMatrix] = None, dilated: int = 1) -> List[TypeMatrix]:
    #     pass
from geometry import ImageGeometry
    # def prepare_standard_geometry(
    #     self,
    #     matrix: TypeMatrix,
    #     target_size: tuple[int, int] = (28, 28),
    #     padding: int = 2,
    #     pad_value: int = 0
    #     ) -> np.ndarray:
    #     pass
from grayscale import GrayScaleProcessing # 2
    # def convert_color_space(self, matrix: TypeMatrix, to_gray: bool = True) -> TypeMatrix:
    #     pass
from io_image import ImageHandler # 1
    # def handle_file(self, path, data=None, is_save_mode=False):
    #     pass
from normalization import Normalization
    # def process(self, M, use_z_score=True, old_r=(0, 255), new_r=(0, 1)):
    #     pass
from pooling import Pooling
    # def max_pool(self, matrix, kernel_size: tuple[int, int], stride: int, pad_width: int, pad_values: int):
    #     pass
from thresholding import Thresholding
    # def adaptive_threshold(self, matrix: TypeMatrix, block_size: int, c: int) -> TypeMatrix:
    #     pass

class __TransformPipeline__(ABC):
    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def apply(self, matrix_channels: MatrixChannels) -> MatrixChannels:
        pass

class __ImageDataPreprocessing__(ABC):
    @abstractmethod
    def preprocess(self, path: str) -> MatrixChannels:
        pass

class TransformPipeline(__TransformPipeline__):
# from augmentation import DataAugmentation. augment
# from conversion import ImageToMatrixConverter. get_channels_from_file
# from convolution import ConvolutionActions. convolution_2d
# from geometry import ImageGeometry. prepare_standard_geometry
# from grayscale import GrayScaleProcessing. convert_color_space # 2
# from io_image import ImageHandler. handle_file  # 1
# from normalization import Normalization. process
# from pooling import Pooling. max_pool
# from thresholding import Thresholding. adaptive_threshold  
  
    def __init__(self):
        self.image_handler = ImageHandler()
        self.gray_scale_processing = GrayScaleProcessing()

    def apply(self, matrix_channels):
        0

class ImageDataPreprocessing(__ImageDataPreprocessing__):
    def preprocess(self, path):
        0