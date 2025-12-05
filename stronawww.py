from abc import ABC, abstractmethod
from typing import Literal, Any
import os
import time

def czasFunkcji(func):
    def wrapper(*args, **kwargs):
        
        if args:
            instacja = args[0]
            nazwa_klasy = instacja.__class__.__name__
        else:
            nazwa_klasy = "Brak klasy"

        start = time.time()
        wynik = func(*args, **kwargs)
        koniec = time.time()

        print(f"Czas metody {nazwa_klasy}.{func.__name__}: {koniec - start:.4f} sek.")

        return wynik
    return wrapper

class __SciezkaPliku__(ABC):

    def __init__(self):
        self.folder: str = ""
        self.rSciezek: dict[str, list[str]] = {
            "tekst": ["txt", "log", "csv", "json", "xml", "ini", "yaml", "yml", "md", "html", "htm"],
            "program": ["py", "js", "java", "c", "cpp", "h", "cs"],
            "obraz": ["jpg", "jpeg", "png", "gif", "bmp"],
            "bintekst": ["docx", "pdf"],
            "audio": ["mp3", "wav", "flac", "aac", "ogg"]
        }

    @abstractmethod
    def poprawnosc_pliku(self, sciezka_pliku: str) -> tuple[str, bool, str]:
        """Zwraca (rozszerzenie, czy_ok, komunikat)."""
        pass

    @abstractmethod
    def stworz_folder(self, adres: str, nazwa: str) -> None:
        pass

    @abstractmethod
    def edycja_folder(self, nazwa: str) -> None:
        pass

    @abstractmethod
    def przeszukiwanie(
        self,
        nazwa: str = "",
        od_konca: str = "",
        zaczyna_od: str = "C:/",
        liczba_wynikow: int = 10
    ) -> list[str]:
        pass

    @abstractmethod
    def zastap(self, stary_plik: str, nowy_plik: str) -> None:
        pass

    @abstractmethod
    def reset_plik(self, sciezka_pliku: str) -> None:
        pass

    @abstractmethod
    def odczytaj(self, sciezka_pliku: str) -> list[str]:
        pass

    @abstractmethod
    def dopisz(self, sciezka_pliku: str, zawartosc: list[str]) -> None:
        pass

class SciezkaPliku(__SciezkaPliku__):
    def __init__(self):
        super().__init__()

    def poprawnosc_pliku(self, sciezka_pliku):
        accept = False
        rpliki = self.rSciezek

        bin_ext = rpliki["obraz"] + rpliki["bintekst"] + rpliki["audio"]
        txt_ext = rpliki["tekst"] + rpliki["program"]

        _, ext = os.path.splitext(sciezka_pliku)

        ext = ext.lower().lstrip('.')

        try:
            if ext in bin_ext:
                with open(sciezka_pliku, "rb") as plik:
                    zawartosc = plik.read(10)
                    odczyt = f"Otwarto plik binarny ({ext}): {sciezka_pliku} |{zawartosc}...|"
                    accept = True

            elif ext in txt_ext:
                with open(sciezka_pliku, "r", encoding="utf-8") as plik:
                    zawartosc = plik.read(10)
                    odczyt = f"Otwarto plik tekstowy ({ext}): {sciezka_pliku} |{zawartosc}...|"
                    accept = True

            else:
                assert notUsePlikException(ext, sciezka_pliku)

        except Exception as e:
            assert unknownFileOpeningErrorException(e, sciezka_pliku)

        return ext, accept, odczyt

    def stworz_folder(self, adres, nazwa):
        try:
            sciezka = os.path.join(adres, nazwa)
            if not os.path.exists(sciezka):
                assert attemptToCreateAnExistingFileException(sciezka)
        except Exception as e:
            assert unknownFileCreateErrorException(e, adres, nazwa)

    def edycja_folder(self, nazwa):
        0

    def przeszukiwanie(self, nazwa="", od_konca="", zaczyna_od="C:/", liczba_wynikow=10):
        katalogi = []
        liczba = 0

        for root, _, files in os.walk(zaczyna_od):
            liczba += 1

            if liczba % 1000 == 0:
                print(f"sprawdzono {liczba} plików...")

            for plik in files:

                if nazwa in plik:

                    if od_konca == plik[-len(od_konca):]:
                        wynik = os.path.join(root, plik)
                        katalogi.append(wynik)
                        print("Znaleziono:", wynik)
                        if len(katalogi) >= liczba_wynikow:
                            return katalogi

        return katalogi

    def zastap(self, stary_plik, nowy_plik): # przepisać z dołu i to na dole usunąć.
        try:
            os.replace(stary_plik, nowy_plik)
        except Exception as e:
            assert failedFileReplacementException(e, stary_plik, nowy_plik)

    def reset_plik(self, sciezka_pliku):
        with open(sciezka_pliku, "w"):
            pass

    def odczytaj(self, sciezka_pliku): # niezrobione
        with open(sciezka_pliku, "a+") as plik:
            zawartosc = plik.readlines()
            return zawartosc

    def dopisz(self, sciezka_pliku: str, zawartosc):
        with open(sciezka_pliku, "a+") as plik:
            for linia in zawartosc:
                plik.write(linia)


class __pamiec_programu_txt__(ABC):
    """Abstrakcyjna klasa odpowiedzialna za operacje na plikach."""

    def __init__(self):
        self.dane_pliku = {
            "nazwa": "stronawww",
            "rodzaj": "txt",
            "zawartosc": None
        }

    @abstractmethod
    def zmien_dane(self) -> None:
        pass

    @abstractmethod
    def reset_pamiec(self) -> None:
        pass

    @abstractmethod
    def odczytaj(self) -> list[str]:
        pass

    @abstractmethod
    def wpisz(self, zawartosc: list[str]) -> None:
        pass

class PamiecProgramu(__pamiec_programu_txt__):
    def __init__(self):
        super().__init__()
        dane_p = self.dane_pliku
        nazwa_plik = dane_p["nazwa"] + "." + dane_p["rodzaj"]

    @abstractmethod
    def zmien_dane(self) -> None:
        pass

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

class __baza_danych__(ABC):
    @abstractmethod
    def BazadanychSprawdzOtworz(func):
        pass

    @abstractmethod
    def BazadanychsprawdzDodajElement(func):
        pass

    @abstractmethod
    def BazadanychsprawdzDodajPrzesten(func):
        pass
    
    @abstractmethod
    def BazadanychsprawdzUsun(func):
        pass
    
    @abstractmethod
    def BazadanychsprawdzEdytuj(func):
        pass
    
    @abstractmethod
    def BazadanychsprawdzZnajdz(func):
        pass
    
    def __init__(self, nazwa: str):
        self.nazwa = nazwa
        self.bazadanych: dict[tuple[int, str], dict[int, Any]]

    @abstractmethod
    def otworz(self, nazwa) -> None:
        pass

    @abstractmethod
    def dodaj_element(self, kolumna: int | str, wiersz: int | str,
                      autoWiersz: bool, wartosc: Any, bazadanych = None):
        pass

    @abstractmethod
    def dodaj_przesten(self, coDodac: Literal["kolumna", "wiersz"], nazwa: str):
        pass

    @abstractmethod
    def usun(self, coUsun: Literal["kolumna", "wiersz", "element"]):
        pass

    @abstractmethod
    def edytuj(self, kolumna: int | str, wiersz: int | str, nowyElement: int | str):
        pass

    @abstractmethod
    def znajdz(self, element: int | str, coZnajdz: Literal["kolumna", "wiersz", "element"], zwracaBool = False):
        pass 

class BazaDanychSprawdzOtworz(Exception):
    pass

# tu wyjątki SprawdzOtworz

class BazaDanychSprawdzDodajElementException(Exception): # zaktualizować 
    pass # z tyłu dodać Exception
class NoDatabaseProvidedException(BazaDanychSprawdzDodajElementException):
    def __init__(self, msg):
        super().__init__(f"Brak dostępu do bazy danych: {msg}")
class InvalidColumnTupleStructureException(BazaDanychSprawdzDodajElementException):
    def __init__(self, kolumna):
        super().__init__(f"Niepoprawna struktura klucza kolumny (oczekiwano tuple (int, str)): {kolumna}")
class ColumnIdNotFoundException(BazaDanychSprawdzDodajElementException):
    def __init__(self, kolumna_id):
        super().__init__(f"Nie znaleziono kolumny o ID: {kolumna_id}")
class ColumnNameNotFoundException(BazaDanychSprawdzDodajElementException):
    def __init__(self, kolumna_nazwa):
        super().__init__(f"Nie znaleziono kolumny o nazwie: {kolumna_nazwa}")
class InvalidColumnTypeException(BazaDanychSprawdzDodajElementException):
    def __init__(self, typ):
        super().__init__(f"Niepoprawny typ kolumny (oczekiwano int lub str): {typ}")
class InvalidRowContainerTypeException(BazaDanychSprawdzDodajElementException):
    def __init__(self, typ):
        super().__init__(f"Niepoprawny typ kontenera wierszy (oczekiwano dict): {typ}")
class AutoGeneratedRowIdConflictException(BazaDanychSprawdzDodajElementException):
    def __init__(self, wiersz_id):
        super().__init__(f"Konflikt ID wiersza wygenerowanego automatycznie: {wiersz_id}")
class MissingRowIdWhenAutoDisabledException(BazaDanychSprawdzDodajElementException):
    def __init__(self):
        super().__init__("Brak ID wiersza gdy autoWiersz jest wyłączone")
class InvalidRowIdInColumnException(BazaDanychSprawdzDodajElementException):
    def __init__(self, wiersz_id, kolumna):
        super().__init__(f"Niepoprawny ID wiersza {wiersz_id} w kolumnie {kolumna}")
class MissingRowNameException(BazaDanychSprawdzDodajElementException):
    def __init__(self, wiersz_nazwa):
        super().__init__(f"Nie znaleziono wiersza o nazwie: {wiersz_nazwa}")
class InvalidRowKeyTypeException(BazaDanychSprawdzDodajElementException):
    def __init__(self, typ):
        super().__init__(f"Niepoprawny typ klucza wiersza (oczekiwano int lub str): {typ}")
class InvalidAdditionElementNoneException(BazaDanychSprawdzDodajElementException):
    def __init__(self, wartosc):
        super().__init__(f"Niepoprawny element do dodania (None): {wartosc}")

class BazadanychsprawdzDodajPrzestenException(Exception):
    pass

# wyjątki sprawdzDodajPrzesten

class BazadanychsprawdzUsunException(Exception):
    pass

# pozostałe dodać

class Bazadanych(__baza_danych__):

    def BazadanychSprawdzOtworz(func):
        def wrapper(self, ):
            0 # sprawdza czy git WYJĄTKI NA GÓRZE TU TYLKO ASSERT
            return func(self, )
        return wrapper

    def BazadanychsprawdzDodajElement(func):
        def wrapper(self, kolumna, wiersz, autoWiersz, wartosc, bazadanych):
            if bazadanych is None:
                assert NoDatabaseProvidedException("bazadanych is None")

            if isinstance(kolumna, int):
                kolumna_key = None

                for key in bazadanych.keys():

                    if not (isinstance(key, tuple) and len(key) == 2 and isinstance(key[0], int) and isinstance(key[1], str)):
                        assert InvalidColumnTupleStructureException(str(key))

                    if key[0] == kolumna:
                        kolumna_key = key
                        break

                if kolumna_key is None:
                    assert ColumnIdNotFoundException(kolumna)

            elif isinstance(kolumna, str):
                kolumna_key = None

                for key in bazadanych.keys():

                    if not (isinstance(key, tuple) and len(key) == 2 and isinstance(key[0], int) and isinstance(key[1], str)):
                        assert InvalidColumnTupleStructureException(str(key))

                    if key[1] == kolumna:
                        kolumna_key = key
                        break

                if kolumna_key is None:
                    assert ColumnNameNotFoundException(kolumna)

            else:
                assert InvalidColumnTypeException(type(kolumna))

            wiersze = bazadanych.get(kolumna_key)
            if not isinstance(wiersze, dict):
                assert InvalidRowContainerTypeException(type(wiersze))

            if autoWiersz:

                if len(wiersze) == 0:
                    wiersz = 0

                else:
                    wiersz = max(wiersze.keys()) + 1

                if wiersz in wiersze:
                    assert AutoGeneratedRowIdConflictException(wiersz)
            else:

                if wiersz is None:
                    assert MissingRowIdWhenAutoDisabledException()

                if isinstance(wiersz, int):
                    if wiersz not in wiersze:
                        assert InvalidRowIdInColumnException(wiersz, kolumna_key)

                elif isinstance(wiersz, str):
                    znaleziono = False

                    for v in wiersze.values():
                        if v == wiersz:
                            znaleziono = True
                            break

                    if not znaleziono:
                        assert MissingRowNameException(wiersz)
                else:
                    assert InvalidRowKeyTypeException(type(wiersz))

            if wartosc is None:
                assert InvalidAdditionElementNoneException(wartosc)

            return func(self, kolumna_key, wiersz, autoWiersz, wartosc, bazadanych)

        return wrapper

    def BazadanychsprawdzDodajPrzesten(func):
        def wrapper(self, coDodac, nazwa):
            0 # sprawdza czy git
            return func(self, coDodac, nazwa)
        return wrapper
    
    def BazadanychsprawdzUsun(func):
        def wrapper(self, coUsun: Literal["kolumna", "wiersz", "element"], nazwa):
            0 # sprawdza czy git
            return func(self, coUsun, nazwa)
        return wrapper
    
    def BazadanychsprawdzEdytuj(func):
        def wrapper(self, kolumna, wiersz, nowyElement):
            0 # sprawdza czy git
            return func(self, kolumna, wiersz, nowyElement)
        return wrapper
    
    def BazadanychsprawdzZnajdz(func):
        def wrapper(self, ):
            0 # sprawdza czy git
            return func(self, )
        return wrapper

    def __init__(self, nazwa: str):
        super().__init__(nazwa)
        self.nazwa = nazwa
        self.bazadanych: dict[tuple[int, str], dict[int, Any]]

        self.bazadanych = {(0, "nameKolumna"): {0: "00War", 1: "01War"}, (1, "name1Kolumna1"): {0: "10War", 1: "11war"}}

    @BazadanychSprawdzOtworz
    def otworz(self, nazwa):
        0 # otwiera bazę danych i przepisuje do self.bazadanych żeby nie otwierać wiele razy

    @BazadanychsprawdzDodajElement
    def dodaj_element(self, kolumna, wiersz, autoWiersz, wartosc, bazadanych):
        self.bazadanych # to narazie nie zrobione ale nie przejmuj się

    @BazadanychsprawdzDodajPrzesten
    def dodaj_przesten(self, coDodac: Literal["kolumna", "wiersz"], nazwa: str):
        match coDodac:
            case "kolumna":
                0

            case "wiersz":
                0

    @BazadanychsprawdzUsun
    def usun(self, coUsun: Literal["kolumna", "wiersz", "element"], nazwa):
        match coUsun:
            case "kolumna":
                0

            case "wiersz":
                0

            case "element":
                0

            case _:
                if Bazadanych.znajdz(self, nazwa, coUsun, zwracaBool=True):
                    0
                else:
                    0 # nieistnieje to else bo jest w @BazadanychsprawdzUsun

    @BazadanychsprawdzEdytuj
    def edytuj(self, kolumna, wiersz, nowyElement): # narazie zrobić na słowniku
        0 # edytuje konkretny element

    @BazadanychsprawdzZnajdz
    def znajdz(self, element, coZnajdz: Literal["kolumna", "wiersz", "element"], zwracaBool = False):
        0 # przeszukuje coZnajdz
        match coZnajdz:
            case "kolumna":
                0

            case "wiersz":
                0

            case "element":
                0

            case _:
                assert invalidElementFindIncoZnajdzException(coZnajdz)

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
        super().__init__(f"numery musi być int lub list[int]")

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

class Czcionka(Chat):# do pytań z chata dodaje rodzaj czcionki
    def __init__(self, rodzaj):
        super().__init__(self.pytania, self.wynikUsunNawiasy) # wynikUsunNawiasy (nie wiem czy potrzebne)

        self.rodzaj = rodzaj

    def sprawdzCzcionki(self):
        0

    def ustawCzcionka(self):
        self.rodzaj = input("Podaj czcionkę: ")
    
    def dodajCzcionke(self):
        0
    
    def usunCzcionke(self):
        0

class __wiersz__(ABC): # stworzyć klase i podobną na dole tu ABC skupienie
    def __init__(self, zawartosc, aktualnyWiersz):
        self.zawartosc = zawartosc
        self.aktualnyWiersz = aktualnyWiersz

    @abstractmethod
    def dodaj(self):
        0

    @abstractmethod
    def edytuj(self):
        0

    @abstractmethod
    def usun(self):
        0

class Wiersz(__wiersz__, Czcionka): # edycja wierszy, jak są pytania to Chat, jak zmiana czcionki to Czcionka
    def __init__(self, zawartosc):
        super().__init__()
    
    def dodaj(self):
        0
    
    def edytuj(self):
        0

    def usun(self):
        0

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

class Strona(__strona__, Wiersz): # nie zrobione
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

class notUsePlikException(Exception):
    def __init__(self, ext, sciezka_pliku):
        super().__init__(f"Rodzaj {ext} w ścieżce {sciezka_pliku} jest nieobsługiwany.")
class unknownFileOpeningErrorException(Exception):
    def __init__(self, e, sciezka_pliku):
        super().__init__(f"Błąd {e} przy próbie otwarcia {sciezka_pliku} jest nieobsługiwany.")
class failedFileReplacementException(Exception):
    def __init__(self, e, staryPlik, nowyPlik):
        super().__init__(f"Błąd {e} przy próbie zastąpienia pliku {staryPlik} na {nowyPlik}.")
class unknownFileCreateErrorException(Exception):
    def __init__(self, e, adres, nazwa):
        super().__init__(f"Błąd {e} przy próbie stworzenia folderu {nazwa} na adresie {adres}.")
class attemptToCreateAnExistingFileException(Exception):
    def __init__(self, sciezka):
        super().__init__(f"Błąd przy próbie stworzenia folderu {sciezka}, taki już istnieje.")

# Przykład użycia
# sciezka_do_pliku = "dodatkiOSwyjatki.py"
# bezpieczne_otwarcie_pliku(sciezka_do_pliku)

plik = SciezkaPliku()
plik.przeszukiwanie("b", "", "C:/", 10)
plik.poprawnosc_pliku("tekstowy.txt")

