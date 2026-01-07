from abc import ABC, abstractmethod
from typing import Tuple, Literal, overload

import numpy as np


class __Normalization__(ABC):
    @abstractmethod
    def normalize(self, M: np.ndarray, old_range: Tuple[int, int], new_range: Tuple[int, int]) -> np.ndarray:
        pass

    @abstractmethod
    def z_score_normalization(self, M: np.ndarray) -> np.ndarray:
        pass

    @overload
    @abstractmethod
    def process(self, M: np.ndarray, use_z_score: Literal[True]) -> np.ndarray: ...

    @overload
    @abstractmethod
    def process(
        self, 
        M: np.ndarray, 
        use_z_score: Literal[False], 
        old_r: Tuple[int, int], 
        new_r: Tuple[int, int]
    ) -> np.ndarray: ...

    @abstractmethod
    def process(
        self, 
        M: np.ndarray, 
        use_z_score: bool = True, 
        old_r: Tuple[int, int] = (0, 255), 
        new_r: Tuple[int, int] = (0, 1)
    ) -> np.ndarray:
        pass

class Normalization(__Normalization__):
    def normalize(self, M, old_r=(0, 255), new_r=(0, 1)):
        return (M - old_r[0]) * (new_r[1] - new_r[0]) / (old_r[1] - old_r[0]) + new_r[0]

    def z_score_normalization(self, M):
        mu, sigma = M.mean(), M.std()
        return (M - mu) / sigma if sigma != 0 else M - mu

    def process(self, M, use_z_score=True, old_r=(0, 255), new_r=(0, 1)):
        M_np = np.array(M, dtype=float)
        if use_z_score:
            return self.z_score_normalization(M_np)
        return self.normalize(M_np, old_r, new_r)