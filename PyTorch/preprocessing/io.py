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

class __ImageLoader__(ABC):
    @abstractmethod
    def open_image(self, path: str) -> tuple[TypeIMG, int, int]:
        pass

class __DataExporter__(ABC):
    @abstractmethod
    def save_as_image(
        self,
        matrix: TypeIMG,
        path: str
    ) -> None:
        pass

    @abstractmethod
    def save_as_matrix(
        self,
        matrix_channels: MatrixChannels,
        path: str
    ) -> None:
        pass


class ImageLoader(__ImageLoader__):
    def open_image(self, path):
        img = PILImage.open(path).convert("RGB")
        width, height = img.size
        return img, width, height
class DataExporter(__DataExporter__):
    def save_as_image(self, matrix, path):
        0

    def save_as_matrix(self, matrix_channels, path):
        0