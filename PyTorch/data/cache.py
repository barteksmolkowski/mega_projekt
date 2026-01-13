from .common import ABC, abstractmethod


class __CacheManager__(ABC):
    @abstractmethod
    def cache(self, data):
        pass

    @abstractmethod
    def load(self):
        pass


class CacheManager(__CacheManager__):
    def cache(self, data):
        0

    def load(self):
        0