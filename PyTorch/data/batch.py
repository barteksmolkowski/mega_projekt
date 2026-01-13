import random
from abc import ABC, abstractmethod
from typing import List, Literal, Optional, Tuple, overload

import numpy as np
from PIL import Image

from .common import MatrixChannels, TypeIMG, TypeMatrix


# ZMIENIC NA SZARE
class __BatchProcessing__(ABC):
    @abstractmethod
    def create_batches(
        self,
        data: list[TypeMatrix],
        batch_size: int,
        shuffle: bool = True
    ) -> list[list[TypeMatrix]]:

        pass
    
    @abstractmethod
    def process_batch(
        self,
        paths: List[str]
    ) -> List[TypeMatrix]:
        pass

class BatchProcessing(__BatchProcessing__):
    def create_batches(self, data, batch_size, shuffle):
        """
        data - Lista zdjec
        batch_size ile zdj w 1 partii
        shuffle - czy mieszac czy nie

        return generator
        """

    
    def process_batch(self, paths):
        0