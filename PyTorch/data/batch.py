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
    ) -> List[MatrixChannels]:
        pass

class BatchProcessing(__BatchProcessing__):
    def create_batches(self, data, batch_size, shuffle):
        0
    
    def process_batch(self, paths):
        0