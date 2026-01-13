from abc import ABC, abstractmethod
from typing import overload, Literal, List, Union, Dict

import requests
import json
import os

class __DataDownloader__(ABC):
    @abstractmethod
    def fetch_data(self, source: str, force_reload: bool = False) -> Union[List, Dict]:
        """Pobiera JSON lub listę linków"""
        pass

    @abstractmethod
    def save_to_disk(self, data: Union[List, Dict]) -> bool:
        """Zapisuje pobrane pliki binarnie (Requests .content)"""
        pass

class __DataProcessor__(ABC):
    @abstractmethod
    def process_batch(self, items: List, grayscale: bool = True) -> bool:
        """Przetwarza pobrane zdjęcia na macierze"""
        pass

class __ProjectManager__(ABC):
    @overload
    @abstractmethod
    def run_pipeline(
        self, 
        source_url: str, 
        fast_mode: Literal[True]
    ) -> bool: 
        """Gdy wybieramy tryb szybki, zwracamy tylko status powodzenia."""
        ...

    @overload
    @abstractmethod
    def run_pipeline(
        self, 
        source_url: str, 
        fast_mode: Literal[False] = False
    ) -> str: 
        """Gdy wybieramy tryb pełny, zwracamy szczegółowy raport tekstowy."""# niech ai wytlumaczy dlaczego 
        ...

    @abstractmethod
    def run_pipeline(
        self, 
        source_url: str, 
        fast_mode: bool = False
    ) -> Union[str, bool]:
        """
        Główna metoda implementująca logikę.
        """
        pass

class DataDownloader(__DataDownloader__):
    def fetch_data(self, source, force_reload=False):
        0

    def save_to_disk(self, data):
        0

class DataProcessor(__DataProcessor__):
    def process_batch(self, items, grayscale=True):
        0

class ProjectManager:
    def __init__(self):
        data_downloader = DataDownloader()
        self.fetch_data = data_downloader.fetch_data
        self.save_to_disk = data_downloader.save_to_disk

        data_processor = DataProcessor()
        self.process_batch = data_processor.process_batch

    def run_pipeline(self, source_url: str, fast_mode: bool = False) -> str:
        """
        Główna metoda uruchamiająca cały proces.
        fast_mode: jeśli True, pomija niektóre kroki dla szybkości.
        """

