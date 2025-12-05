import os
from abc import ABC, abstractmethod

class PamiecBase(ABC):
    """Abstrakcyjna klasa odpowiedzialna za operacje na plikach."""

    def __init__(self):
        self.dane_pliku = {
            "nazwa": "pamiec_file_explorer",
            "rodzaj": "txt",
            "zawartosc": None
        }

    @abstractmethod
    def reset_pamiec(self) -> None:
        pass

    @abstractmethod
    def odczytaj(self) -> list[str]:
        pass

    @abstractmethod
    def wpisz(self, zawartosc: list[str]) -> None:
        pass


class Pamiec(PamiecBase):
    def __init__(self):
        super().__init__()
        self.dane_pliku = { # potem usunąć bo nie potrzebne
            "nazwa": "pamiec_file_explorer",
            "rodzaj": "txt",
            "zawartosc": None
        }

    def reset_pamiec(self):
        with open("plik.txt", "w") as plik:
            pass

    def odczytaj(self):
        with open("pamiec_file_explorer.txt", "a+") as plik:
            zawartosc = plik.readlines()
            return zawartosc

    def wpisz(self, zawartosc):
        with open("pamiec_file_explorer.txt", "a+") as plik:
            for linia in zawartosc:
                plik.write(linia)


class UstawieniaBase(ABC):
    """Abstrakcyjna klasa odpowiedzialna za ustawienia eksploratora."""

    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def updateDaneLista(self, nazwa : str, wartosc: list[str | int], lista: list[str | int]) -> list:
        pass

    @abstractmethod
    def edycja_danych(self, zmiany: list[tuple[str, str | list[str]]]) -> None:
        pass

    @abstractmethod
    def otworzSciezke(self, sciezka: str) -> list[str]:
        pass

    @abstractmethod
    def edycja_sciezki(self, stara: str, nowa: str) -> None:
        pass

    @abstractmethod
    def scroll(self, kierunek: str) -> None:
        pass

    @abstractmethod
    def pokaz_aktualne(self, lista: str, od_ktorej: int) -> list[str]:
        pass

    @abstractmethod
    def wskaz_aktualny(self, numer: int):
        pass

    @abstractmethod
    def zmien_nazwe(self, staraSciezka, nowaSciezka):
        pass

    @abstractmethod
    def usun_plik(self, nazwa):
        pass

class failedAttemptToDeleteNonExistentPathException(Exception):
    def __init__(self, sciezka):
        super().__init__(f"Próba usunięcia nieistniejącej ścieżki {sciezka}")
class failedAttemptToEditPathNameExcetion(Exception):
    def __init__(self, wybrany, nowy):
        super().__init__(f"Nie udana próba edycji ścieżki {wybrany}, na ścieżkę {nowy}")
class unsupportedTypeInSelfDataException(Exception):
    def __init__(self, dane):
        super().__init__(f"Nie obsługiwany typ {dane}: {type(dane)}")
class unrecognizedScrollDirectionException(Exception):
    def __init__(self, kierunek):
        super().__init__(f"Nie rozpoznany kierunek {kierunek} w metodzie scroll")

class Ustawienia(UstawieniaBase):
    def __init__(self):
        self.dane = {
            "liczba_pokazywanych_plikow": 10,
            "aktualny_numer": 0,
            "moc_strzalek": 1,
            "filtry": ["litery", "dlugosc", "slowa"],
            "zablokowane_pliki": [],
            "priorytetowe_pliki": []
        }
        aktualnaSciezka = "C:/"
        openAktualSciezka = []

    def updateDaneLista(self, nazwa : str, wartosc: list[str | int], lista: list[str | int]) -> list:
        print(f"Update listy: {lista}")
        return list

    def edycja_danych(self, zmiany):
        zmiany = dict(zmiany)

        for klucz, wartosc in self.dane.items():
            if klucz in zmiany:
                nowe = zmiany[klucz]

                if isinstance(wartosc, (int, str)):
                    self.dane[klucz] = nowe

                elif isinstance(wartosc, list):
                    self.dane[klucz] = self.updateDaneLista(klucz, wartosc, nowe)

                else:
                    raise unsupportedTypeInSelfDataException(wartosc)

    def otworzSciezke(self, sciezka: str) -> list[str]:
        listaSciezek = []
        if os.path.isdir(sciezka):
            for el in os.listdir(sciezka):
                try:
                    pelna_sciezka = os.path.join(sciezka, el)
                    listaSciezek.append(pelna_sciezka)
                except PermissionError:
                    continue
                except Exception:
                    continue
        elif os.path.is
        return listaSciezek

    def edycja_sciezki(self, stara, nowa):
        if not os.path.exists(stara):
            raise failedAttemptToEditPathNameExcetion(stara, nowa)

        os.rename(stara, nowa)

    def scroll(self, kierunek):
        wartosc, ilosc = self.dane["aktualny_numer"], self.dane["moc_strzalek"]
        match kierunek:
            case "gora":
                wartosc -= ilosc
            case "dol":
                wartosc += ilosc
            case _:
                assert unrecognizedScrollDirectionException(kierunek)

    def pokaz_aktualne(self, lista, od_ktorej): # te 3 z dołu jeszcze nie zrobione
        0

    def wskaz_aktualny(self, numer):
        0 # nie oblicza od zera z listy tylko z pokazywanej listy jaki numer

    def zmien_nazwe(self, do_zmiany, nowa_nazwa):
        pass

    def usun_plik(self, nazwa):
        if os.path.exists(nazwa):
            os.remove(nazwa)
        else:
            assert failedAttemptToDeleteNonExistentPathException(nazwa)