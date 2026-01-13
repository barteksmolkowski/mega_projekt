# from augmentation import DataAugmentation
#     # def augment(self, matrix: TypeMatrix, repeats: int) -> List[TypeMatrix]:
#     #     pass

# from conversion import ImageToMatrixConverter
#     # def get_channels_from_file(self, path: str) -> MatrixChannels:
#     #     pass

# from convolution import ConvolutionActions
#     # def convolution_2d(self, matrix: TypeMatrix, filtrs: List[TypeMatrix] = None, dilated: int = 1) -> List[TypeMatrix]:
#     #     pass
# from .geometry import ImageGeometry
#     # def prepare_standard_geometry(
#     #     self,
#     #     matrix: TypeMatrix,
#     #     target_size: tuple[int, int] = (28, 28),
#     #     padding: int = 2,
#     #     pad_value: int = 0
#     #     ) -> np.ndarray:
#     #     pass
# from grayscale import GrayScaleProcessing # 2
#     # def convert_color_space(self, matrix: TypeMatrix, to_gray: bool = True) -> TypeMatrix:
#     #     pass
# from io_image import ImageHandler # 1
#     # def handle_file(self, path, data=None, is_save_mode=False):
#     #     pass
# from normalization import Normalization
#     # def process(self, M, use_z_score=True, old_r=(0, 255), new_r=(0, 1)):
#     #     pass

import numpy as np
from normalization import Normalization
from pooling import Pooling
from thresholding import Thresholding


def verify(name, result, expected=None, shape=None, binary=False):
    try:
        if expected is not None: assert np.array_equal(result, expected)
        if shape is not None: assert result.shape == shape
        if binary: assert np.all(np.isin(result, [0, 255]))
        print(f"✅ {name}")
        return True
    except Exception as e:
        print(f"❌ {name} | Błąd: {e}")
        return False

def test_thresholding():
    th = Thresholding()
    print("Test Thresholding")

    m_grad = np.zeros((10, 10), dtype=np.uint8); m_grad[:, 5:] = 200
    verify("Th: Gradient 10x10", th.adaptive_threshold(m_grad, 3), shape=(10, 10), binary=True)
    
    m_noise = np.random.randint(0, 255, (20, 20), dtype=np.uint8)
    verify("Th: Noise 20x20", th.adaptive_threshold(m_noise, 5, c=10), shape=(20, 20), binary=True)

    verify("Edge: Big Block 5x5 on 3x3", th.adaptive_threshold(np.ones((3,3))*100, 5), shape=(3,3))
    verify("Edge: Even Block 4", th.adaptive_threshold(np.ones((10,10)), 4), shape=(10,10))
    verify("Edge: Flat Matrix", th.adaptive_threshold(np.ones((5,5))*100, 3, c=2), expected=np.ones((5,5))*255)    

def test_pooling():
    p = Pooling()
    print("Test Pooling")

    m_p = [[1, 2, 3, 4], [5, 6, 7, 8], [9, 1, 2, 3], [4, 5, 6, 7]]
    verify("Pool: Standard 2x2", p.max_pool(m_p), expected=[[6, 8], [9, 7]])

    verify("Pool: Padding 1x1", p.max_pool([[10]], 2, stride=2, pad_width=1), expected=[[10, 0], [0, 0]])

def test_normalization():
    norm = Normalization()
    print("Test Normalization")

    m_range = np.array([0, 127.5, 255])
    expected_minmax = np.array([0.0, 0.5, 1.0])
    res_minmax = norm.process(m_range, use_z_score=False, old_r=(0, 255), new_r=(0, 1))
    verify("Norm: Min-Max (0-1)", res_minmax, expected=expected_minmax)

    m_z = np.array([1, 2, 3])
    res_z = norm.process(m_z, use_z_score=True)
    is_mean_zero = np.isclose(np.mean(res_z), 0)
    verify("Norm: Z-Score Mean Zero", is_mean_zero, expected=True)

    m_flat = np.array([100, 100, 100])
    res_flat = norm.process(m_flat, use_z_score=True)
    verify("Norm: Zero Variance", res_flat, expected=np.array([0.0, 0.0, 0.0]))

    res_custom = norm.process([0, 255], use_z_score=False, old_r=(0, 255), new_r=(-1, 1))
    verify("Norm: Custom Range (-1, 1)", res_custom, expected=np.array([-1.0, 1.0]))

def run_all_tests():
    test_thresholding()
    test_pooling()
    test_normalization()

if __name__ == "__main__":
    run_all_tests()