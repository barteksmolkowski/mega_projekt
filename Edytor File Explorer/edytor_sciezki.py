# stronawww_sciezki:
# dopisać rodzaje błędów
# napisać klasy except
# dokończyć kod
# import do strona www (żeby tam można było używać)

import os
import time
from abc import ABC, abstractmethod

from edytor_sciezki_Exceptions import (
    DestinationFolderAlreadyExistsEdycjaFolderException,
    FileAppendOSErrorDopiszException,
    FileAppendPermissionDeniedDopiszException, FileNotFoundDopiszException,
    FileNotFoundOdczytajException, FileNotFoundPoprawnoscPlikuException,
    FileNotFoundResetPlikException, FileReadOSErrorOdczytajException,
    FileReadPermissionDeniedOdczytajException,
    FileResetOSErrorResetPlikException,
    FileResetPermissionDeniedResetPlikException,
    FolderAlreadyExistsStworzFolderException,
    FolderPermissionDeniedStworzFolderException,
    FolderRenameOSErrorEdycjaFolderException,
    FolderRenamePermissionDeniedEdycjaFolderException,
    FolderUnknownOSErrorStworzFolderException,
    InvalidSearchLimitPrzeszukanieException,
    ParentFolderNotFoundStworzFolderException,
    PathIsNotDirectoryStworzFolderException, PathIsNotFileDopiszException,
    PathIsNotFileOdczytajException, PathIsNotFileResetPlikException,
    PermissionDeniedPoprawnoscPlikuException, ReplaceOSErrorZastapException,
    ReplacePermissionDeniedZastapException,
    SearchPathIsNotDirectoryPrzeszukanieException,
    SearchPermissionDeniedPrzeszukanieException,
    SearchStartPathNotFoundPrzeszukanieException,
    SourceFileNotFoundZastapException,
    SourceFolderNotFoundEdycjaFolderException,
    SourcePathIsNotDirectoryEdycjaFolderException,
    SourcePathIsNotFileZastapException, UnicodeDecodePoprawnoscPlikuException,
    UnknownExtensionPoprawnoscPlikuException,
    UnsupportedFileExtensionDopiszException,
    UnsupportedFileExtensionOdczytajException,
    UnsupportedFileExtensionResetPlikException)

FileNotFoundPoprawnoscPlikuException
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

    @abstractmethod
    def sprawdz_poprawnosc_pliku(func):
        pass

    @abstractmethod
    def sprawdz_stworz_folder(func):
        pass

    @abstractmethod
    def sprawdz_edycja_folder(func):
        pass

    @abstractmethod
    def sprawdz_przeszukiwanie(func):
        pass

    @abstractmethod
    def sprawdz_zastap(func):
        pass

    @abstractmethod
    def sprawdz_reset_plik(func):
        pass

    @abstractmethod
    def sprawdz_odczytaj(func):
        pass

    @abstractmethod
    def sprawdz_dopisz(func):
        pass


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
    def edycja_folder(self, sciezka: str) -> None:
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
    def sprawdz_poprawnosc_pliku(func):
        def wrapper(self, sciezka_pliku, *args, **kwargs):
            _, ext = os.path.splitext(sciezka_pliku)
            ext = ext.lower().lstrip('.')
            
            assert ext, "Plik musi mieć rozszerzenie"
            if not any(ext in rozszerzenia for rozszerzenia in self.rSciezek.values()):
                raise UnknownExtensionPoprawnoscPlikuException(ext)

            try:
                return func(self, sciezka_pliku, *args, **kwargs)
            except FileNotFoundError:
                raise FileNotFoundPoprawnoscPlikuException(sciezka_pliku)
            except PermissionError:
                raise PermissionDeniedPoprawnoscPlikuException(sciezka_pliku)
            except UnicodeDecodeError:
                raise UnicodeDecodePoprawnoscPlikuException(sciezka_pliku)

        return wrapper
    
    def sprawdz_stworz_folder(func):
        def wrapper(self, adres, nazwa, *args, **kwargs):
            sciezka = os.path.join(adres, nazwa)

            if os.path.exists(sciezka):
                raise FolderAlreadyExistsStworzFolderException(sciezka)

            if not os.path.exists(adres):
                raise ParentFolderNotFoundStworzFolderException(adres)

            if not os.path.isdir(adres):
                raise PathIsNotDirectoryStworzFolderException(adres)

            try:
                return func(self, adres, nazwa, *args, **kwargs)
            except PermissionError:
                raise FolderPermissionDeniedStworzFolderException(sciezka)
            except OSError as e:
                raise FolderUnknownOSErrorStworzFolderException(sciezka, e)

        return wrapper

    def sprawdz_edycja_folder(func):
        def wrapper(self, stara_sciezka, nowa_sciezka, *args, **kwargs):

            if not os.path.exists(stara_sciezka):
                raise SourceFolderNotFoundEdycjaFolderException(stara_sciezka)

            if not os.path.isdir(stara_sciezka):
                raise SourcePathIsNotDirectoryEdycjaFolderException(stara_sciezka)

            if os.path.exists(nowa_sciezka):
                raise DestinationFolderAlreadyExistsEdycjaFolderException(nowa_sciezka)

            try:
                return func(self, stara_sciezka, nowa_sciezka, *args, **kwargs)
            except PermissionError:
                raise FolderRenamePermissionDeniedEdycjaFolderException(stara_sciezka, nowa_sciezka)
            except OSError as blad:
                raise FolderRenameOSErrorEdycjaFolderException(stara_sciezka, nowa_sciezka, blad)

        return wrapper


    def sprawdz_przeszukiwanie(func):
        def wrapper(self, nazwa="", od_konca="", zaczyna_od="C:/", liczba_wynikow=10, *args, **kwargs):
            if not os.path.exists(zaczyna_od):
                raise SearchStartPathNotFoundPrzeszukanieException(zaczyna_od)

            if not os.path.isdir(zaczyna_od):
                raise SearchPathIsNotDirectoryPrzeszukanieException(zaczyna_od)

            if liczba_wynikow <= 0:
                raise InvalidSearchLimitPrzeszukanieException(liczba_wynikow)

            try:
                return func(self,nazwa,od_konca,zaczyna_od,liczba_wynikow,*args,**kwargs)
            except PermissionError:
                raise SearchPermissionDeniedPrzeszukanieException(zaczyna_od)

        return wrapper

    def sprawdz_zastap(func):
        def wrapper(self, stary_plik, nowy_plik, *args, **kwargs):

            if not os.path.exists(stary_plik):
                raise SourceFileNotFoundZastapException(stary_plik)

            if not os.path.isfile(stary_plik):
                raise SourcePathIsNotFileZastapException(stary_plik)

            try:
                return func(self, stary_plik, nowy_plik, *args, **kwargs)
            except PermissionError:
                raise ReplacePermissionDeniedZastapException(stary_plik, nowy_plik)
            except OSError as blad:
                raise ReplaceOSErrorZastapException(stary_plik, nowy_plik, blad)

        return wrapper

    def sprawdz_reset_plik(func):
        def wrapper(self, sciezka_pliku, *args, **kwargs):

            if not os.path.exists(sciezka_pliku):
                raise FileNotFoundResetPlikException(sciezka_pliku)

            if not os.path.isfile(sciezka_pliku):
                raise PathIsNotFileResetPlikException(sciezka_pliku)

            rozszerzenie = os.path.splitext(sciezka_pliku)[1].lower().lstrip(".")

            obslugiwane = []
            for lista in self.rSciezek.values():
                obslugiwane.extend(lista)

            if rozszerzenie not in obslugiwane:
                raise UnsupportedFileExtensionResetPlikException(rozszerzenie)

            try:
                return func(self, sciezka_pliku, *args, **kwargs)
            except PermissionError:
                raise FileResetPermissionDeniedResetPlikException(sciezka_pliku)
            except OSError as blad:
                raise FileResetOSErrorResetPlikException(sciezka_pliku, blad)

        return wrapper

    def sprawdz_odczytaj(func):
        def wrapper(self, sciezka_pliku, *args, **kwargs):

            if not os.path.exists(sciezka_pliku):
                raise FileNotFoundOdczytajException(sciezka_pliku)

            if not os.path.isfile(sciezka_pliku):
                raise PathIsNotFileOdczytajException(sciezka_pliku)

            rozszerzenie = os.path.splitext(sciezka_pliku)[1].lower().lstrip(".")

            obslugiwane = []
            for lista in self.rSciezek.values():
                obslugiwane.extend(lista)

            if rozszerzenie not in obslugiwane:
                raise UnsupportedFileExtensionOdczytajException(rozszerzenie)

            try:
                return func(self, sciezka_pliku, *args, **kwargs)
            except PermissionError:
                raise FileReadPermissionDeniedOdczytajException(sciezka_pliku)
            except OSError as blad:
                raise FileReadOSErrorOdczytajException(sciezka_pliku, blad)

        return wrapper

    def sprawdz_dopisz(func):
        def wrapper(self, sciezka_pliku, zawartosc, *args, **kwargs):

            if not os.path.exists(sciezka_pliku):
                raise FileNotFoundDopiszException(sciezka_pliku)

            if not os.path.isfile(sciezka_pliku):
                raise PathIsNotFileDopiszException(sciezka_pliku)

            rozszerzenie = os.path.splitext(sciezka_pliku)[1].lower().lstrip(".")

            obslugiwane = []
            for lista in self.rSciezek.values():
                obslugiwane.extend(lista)

            if rozszerzenie not in obslugiwane:
                raise UnsupportedFileExtensionDopiszException(rozszerzenie)

            try:
                return func(self, sciezka_pliku, zawartosc, *args, **kwargs)
            except PermissionError:
                raise FileAppendPermissionDeniedDopiszException(sciezka_pliku)
            except OSError as blad:
                raise FileAppendOSErrorDopiszException(sciezka_pliku, blad)

        return wrapper


    def __init__(self):
        super().__init__()

    @sprawdz_poprawnosc_pliku
    def poprawnosc_pliku(self, sciezka_pliku):
        accept = False
        rpliki = self.rSciezek

        bin_ext = rpliki["obraz"] + rpliki["bintekst"] + rpliki["audio"]
        txt_ext = rpliki["tekst"] + rpliki["program"]

        _, ext = os.path.splitext(sciezka_pliku)

        ext = ext.lower().lstrip('.')

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

        return ext, accept, odczyt

    @sprawdz_stworz_folder
    def stworz_folder(self, adres, nazwa):
        sciezka = os.path.join(adres, nazwa)
        os.makedirs(sciezka)

    @sprawdz_edycja_folder
    def edycja_folder(self, stara_sciezka, nowa_sciezka):
        os.rename(stara_sciezka, nowa_sciezka)

    @sprawdz_przeszukiwanie
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

    @sprawdz_zastap
    def zastap(self, stary_plik, nowy_plik):
        os.replace(stary_plik, nowy_plik)

    @sprawdz_reset_plik
    def reset_plik(self, sciezka_pliku):
        rozszerzenie = os.path.splitext(sciezka_pliku)[1].lower().lstrip(".")
        
        kategoria = None
        for kat, rozszerzenia in self.rSciezek.items():
            if rozszerzenie in rozszerzenia:
                kategoria = kat
                break
        
        if kategoria in ["tekst", "program"]:
            tryb = "w"
        elif kategoria in ["obraz", "bintekst", "audio"]:
            tryb = "wb"

        with open(sciezka_pliku, tryb):
            pass
        
    @sprawdz_odczytaj
    def odczytaj(self, sciezka_pliku):
        rozszerzenie = os.path.splitext(sciezka_pliku)[1].lower().lstrip(".")
        
        kategoria = None
        for kat, rozszerzenia in self.rSciezek.items():
            if rozszerzenie in rozszerzenia:
                kategoria = kat
                break
        
        if kategoria in ["tekst", "program"]:
            with open(sciezka_pliku, "r", encoding="utf-8") as plik:
                return plik.readlines()
        
        elif kategoria == "bintekst":
            with open(sciezka_pliku, "rb") as plik:
                return plik.read()
        
        elif kategoria == "obraz" or kategoria == "audio":
            with open(sciezka_pliku, "rb") as plik:
                return plik.read()

    @sprawdz_dopisz
    def dopisz(self, sciezka_pliku: str, zawartosc):
        rozszerzenie = os.path.splitext(sciezka_pliku)[1].lower().lstrip(".")
        
        kategoria = None
        for kat, rozszerzenia in self.rSciezek.items():
            if rozszerzenie in rozszerzenia:
                kategoria = kat
                break

        match kategoria:
            case "tekst" | "program": tryb, encoding = "a", "utf-8"
            case "obraz" | "audio" | "bintekst": tryb, encoding = "ab", None

        if tryb == "a":
            with open(sciezka_pliku, tryb, encoding=encoding) as plik:
                if isinstance(zawartosc, str):
                    if not zawartosc.endswith("\n"):
                        zawartosc += "\n"
                    plik.write(zawartosc)

                else:
                    for linia in zawartosc:
                        if not linia.endswith("\n"):
                            linia += "\n"

                        plik.write(linia)
                        
        elif tryb == "ab":
            with open(sciezka_pliku, tryb) as plik:
                if isinstance(zawartosc, bytes):
                    plik.write(zawartosc)
                elif isinstance(zawartosc, (list, tuple)):
                    for element in zawartosc:
                        plik.write(element)

import os
import shutil


def test_systemu_plikow():
    print(f"\n=> ROZPOCZYNAM TESTY METOD: SciezkaPliku (Status 2026) <=")
    
    # Konfiguracja środowiska testowego
    sp = SciezkaPliku()
    root_test = "TEST_DIR_REMOVABLE"
    test_file = os.path.join(root_test, "test_unit.txt")
    target_file = os.path.join(root_test, "test_replaced.txt")
    
    try:
        # 1. Test stworz_folder
        try:
            sp.stworz_folder(".", root_test)
            print("[OK] stworz_folder")
        except Exception as e: print(f"[FAIL] stworz_folder: {e}")

        # 2. Test dopisz
        try:
            sp.dopisz(test_file, ["Linia 1", "Linia 2"])
            print("[OK] dopisz")
        except Exception as e: print(f"[FAIL] dopisz: {e}")

        # 3. Test poprawnosc_pliku
        try:
            ext, ok, msg = sp.poprawnosc_pliku(test_file)
            if ok and ext == "txt": print("[OK] poprawnosc_pliku")
            else: raise ValueError(msg)
        except Exception as e: print(f"[FAIL] poprawnosc_pliku: {e}")

        # 4. Test odczytaj
        try:
            dane = sp.odczytaj(test_file)
            if len(dane) == 2: print("[OK] odczytaj")
            else: raise ValueError("Błędna liczba linii")
        except Exception as e: print(f"[FAIL] odczytaj: {e}")

        # 5. Test zastap (Rename/Move)
        try:
            sp.zastap(test_file, target_file)
            if os.path.exists(target_file): print("[OK] zastap")
        except Exception as e: print(f"[FAIL] zastap: {e}")

        # 6. Test przeszukiwanie
        try:
            wyniki = sp.przeszukiwanie(nazwa="test", zaczyna_od=root_test)
            if len(wyniki) > 0: print("[OK] przeszukiwanie")
        except Exception as e: print(f"[FAIL] przeszukiwanie: {e}")

        # 7. Test reset_plik
        try:
            sp.reset_plik(target_file)
            if len(sp.odczytaj(target_file)) == 0: print("[OK] reset_plik")
        except Exception as e: print(f"[FAIL] reset_plik: {e}")

    finally:
        # CZYSZCZENIE (Cleanup) - Usuwamy wszystko, co stworzył test
        print(f"\n=> CZYSZCZENIE ŚRODOWISKA... <=")
        if os.path.exists(root_test):
            shutil.rmtree(root_test)
            print(f"Usunięto folder testowy: {root_test}")
        print("Status: System plików przywrócony do stanu początkowego.")

if __name__ == "__main__":
    test_systemu_plikow()