# strona to macierz gdzie każda literka może mieć swój rodzaj i to zamiast czcionka
# żeby było łatwiej

# stronawww_sciezki:
# dopisać rodzaje błędów
# napisać klasy except
# dokończyć kod
# import do strona www (żeby tam można było używać)

# bazadanych
# dodać tu import baza_danych.py
# żeby można było tam zapisywać ładnie
# failedFileReplacementException
from abc import ABC, abstractmethod


class lenNumeryNoweNotEqualException(Exception):
    def __init__(self, numery, nowe):
        super().__init__(f"Długość numery: {len(numery)} i długość nowe: {len(nowe)} są nie równe")
class tooShortLenPytaniaException(Exception):
    def __init__(self, numer, pytania):
        super().__init__(f"Error: {numer} not in range (len={len(pytania)})")
class numeryNotEqualIntException(Exception):
    def __init__(self):
        super().__init__("Error: numery zawiera nie-int")
class NumeryInvalidTypeException(Exception):
    def __init__(self):
        super().__init__("numery musi być int lub list[int]")

class __chat__(ABC):
    def __init__(self):
        self.pytania = {"wynUsNaw": [],
                        "sprawdzane": set(),
                        "aktualne": ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12"]}
        self.wynikUsunNawiasy = []
        print("Stworzono klasę chat...\nSprawdź jej wyjaśnienie pod klasa.wyjasnienie()")
        print("wpisz klasa = chat()")

    @abstractmethod
    def wyjasnienie(self) -> None:
        pass

    @abstractmethod
    def usunNawiasy(self, wynik: list, numer1: int | list, numer2: int | list) -> list:
        pass

    @abstractmethod
    def zmienPyt(self, numery: int | list[int], nowe: str | list[str]) -> str:
        pass

    @abstractmethod
    def wymienPyt(self, pierwsza: int | list = 0, ostatnia: int | list = None) -> list:
        pass

class Chat(__chat__):
    def __init__(self):
        super().__init__()

    def wyjasnienie(self):
        print(
            f"Wyjaśnienie klasy chat()\n"
            f"aktualne pytania: {self.pytania['aktualne']}\n"
            f"chat.zmienPyt(1, 'jeden') <= Zmienia dane pytanie (może być kilka zmian naraz)\n\n"
            f"{self.zmienPyt(1, 'jeden')}\n"
            f"wynik = chat.wymienPyt(1, [7, 9]) <= wypisuje pytania 1:7, 1:9\n"
            f"print(wynik) <= wypisuje te fragmenty...\n"
            f"{self.wymienPyt(1, [7, 9])}"
        )

    def usunNawiasy(self, wynik, numer1, numer2):

        wynUsNaw = self.pytania["wynUsNaw"]
        wynUsNaw.clear()

        powt = 1 if isinstance(numer1, int) else 2
        if isinstance(numer1, int) and isinstance(numer2, int):
            return wynik

        while powt > 1:
            nowy_wynik = []
            for element in wynik:
                if isinstance(element, list):
                    nowy_wynik.extend(element)
                else:
                    nowy_wynik.append(element)

            wynik = nowy_wynik
            powt -= 1

        self.wynikUsunNawiasy = wynik
        return wynik

    def zmienPyt(self, numery, nowe):
        pytania = self.pytania["aktualne"]
        n = len(pytania)

        if isinstance(nowe, str):
            nowe = [nowe]

        if isinstance(numery, list):
            if not all(isinstance(x, int) for x in numery):
                raise numeryNotEqualIntException()

            if not isinstance(nowe, list) or len(numery) != len(nowe):
                raise lenNumeryNoweNotEqualException(numery, nowe)

            for i, numer in enumerate(numery):
                if 0 <= numer < n:
                    pytania[numer] = nowe[i]
                else:
                    raise tooShortLenPytaniaException(numer, pytania)

            return "Zmieniono pytania"

        elif isinstance(numery, int):
            if not isinstance(nowe, list) or len(nowe) != 1:
                raise lenNumeryNoweNotEqualException([numery], nowe)

            if 0 <= numery < n:
                pytania[numery] = nowe[0]
                return "Zmieniono pytanie"
            else:
                raise tooShortLenPytaniaException(numery, pytania)

        else:
            raise NumeryInvalidTypeException()

    def wymienPyt(self, pierwsza: int | list = 0, ostatnia: int | list = None):
        pytania = self.pytania["aktualne"]
        ostatnia = len(pytania) - 1 if ostatnia is None else ostatnia
        returnwynik = []

        if isinstance(ostatnia, list):
            wyniki = []
            for wartoscKoncowa in ostatnia:
                odpowiedz = self.wymienPyt(pierwsza, wartoscKoncowa)
                if odpowiedz:
                    wyniki.append(odpowiedz)
            if wyniki:
                returnwynik.append(wyniki)

        else:
            for i, pytanie in enumerate(pytania):
                try:
                    if pierwsza <= i <= ostatnia:
                        returnwynik.append((i, pytanie))
                except TypeError:
                    wyniki = []
                    sprawdzane = self.pytania["sprawdzane"]

                    for wartoscPierwsza in pierwsza:
                        paraLiczb = (wartoscPierwsza, ostatnia)

                        if paraLiczb not in sprawdzane:
                            sprawdzane.add(paraLiczb)
                            odpowiedz = self.wymienPyt(wartoscPierwsza, ostatnia)
                            
                            if odpowiedz:
                                wyniki.append(odpowiedz)

                            break

                    if wyniki:
                        returnwynik.append(wyniki)

        wreturnwynik = [el for el in returnwynik if el]

        wynik = self.usunNawiasy(wreturnwynik, pierwsza, ostatnia)
        sumaInt = sum(isinstance(x, int) for x in (pierwsza, ostatnia))
        nWynik = []

        if sumaInt == 1:
            nWynik = wynik.copy()
        else:
            for el in wynik:
                nWynik.extend(el) if isinstance(el, list) else nWynik.append(el)                    

        wynik = nWynik

        if isinstance(pierwsza,int) and isinstance(ostatnia, list):
            return(wynik[0])

        return wynik

class __strona__(ABC):
    def __init__(self, zawartosc, aktualnyWiersz):
        self.zawartosc = zawartosc
        self.aktualnyWiersz = aktualnyWiersz

    @abstractmethod
    def dodajWiersz(self, naDole: bool, konkretny: int, ):
        pass

    @abstractmethod
    def usunWiersz(self):
        pass # usuwa ten aktualny wiersz

    @abstractmethod
    def edytujWiersz(self):
        pass # edytuje aktualny, odwołuje się do klasy Wiersz a tam implementacja

    @abstractmethod
    def zmienAktualnyWiersz(self, naNowy: bool, konkretny: int):
        pass

class Strona(__strona__): # nie zrobione
    def __init__(self):
        0

class __program__(ABC):
    def __init__(self, nazwa):
        self.nazwa = nazwa

    @abstractmethod
    def start(self):
        pass

class Program(__program__): # nie zrobione
    def __init__(self):
        pass

    def start(self):
        self.nazwa