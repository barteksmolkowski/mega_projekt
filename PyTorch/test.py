import numpy as np

from preprocessing import ImageDataPreprocessing
from preprocessing.utils import get_test_digit_28x28


def test_system():
    matrix = get_test_digit_28x28()
    
    prepro = ImageDataPreprocessing()
    
    result = prepro.pipeline.apply(matrix)
    print("Testowa macierz wygenerowana, system gotowy!")

if __name__ == "__main__":
    test_system()
