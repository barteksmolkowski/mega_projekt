from abc import ABC, abstractmethod
from typing import List, Tuple
import random
import math

TypeColor = Tuple[int, int, int]
TypeMatrix = List[List[int]]
TypeRandom = int
TypeIMG = List[List[Tuple[int, int, int]]]
MatrixChannels = Tuple[List[List[int]]]

__all__ = ["ABC",
           "abstractmethod",
           "random",
           "math",
           "TypeColor",
           "TypeMatrix",
           "TypeIMG",
           "MatrixChannels",
           "List",
           "Tuple"
           ]