from abc import ABC, abstractmethod

import numpy as np
from PIL import Image

from .common import MatrixChannels


class __ImageToMatrixConverter__(ABC):
    @abstractmethod
    def get_channels_from_file(self, path: str) -> MatrixChannels:
        pass

class ImageToMatrixConverter(__ImageToMatrixConverter__):
    def _separate_channels(self, M):
        return [M[:, :, i] for i in range(3)]

    def _convert_image_to_matrix(self, path):
        img = Image.open(path).convert("RGB")
        return np.array(img)

    def get_channels_from_file(self, path):
        M = self._convert_image_to_matrix(path)
        return self._separate_channels(M)
    