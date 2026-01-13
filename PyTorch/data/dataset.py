from .common import ABC, abstractmethod


class __Dataset__(ABC):
    @abstractmethod
    def __len__(self) -> int:
        pass

    @abstractmethod
    def __getitem__(self, index: int):
        pass

class Dataset(__Dataset__):
    def __len__(self):
        0

    def __getitem__(self, index):
        0