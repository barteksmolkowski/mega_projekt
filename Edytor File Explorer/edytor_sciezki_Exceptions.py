class FileNotFoundPoprawnoscPlikuException(Exception):
    def __init__(self, sciezka):
        super().__init__(f"Plik nie istnieje: {sciezka}")
class PermissionDeniedPoprawnoscPlikuException(Exception):
    def __init__(self, sciezka):
        super().__init__(f"Brak uprawnień do pliku: {sciezka}")
class UnicodeDecodePoprawnoscPlikuException(Exception):
    def __init__(self, sciezka):
        super().__init__(f"Błąd kodowania pliku tekstowego: {sciezka}")
class UnknownExtensionPoprawnoscPlikuException(Exception):
    def __init__(self, rozszerzenie):
        super().__init__(f"Nieznane rozszerzenie pliku: {rozszerzenie}")

class FolderAlreadyExistsStworzFolderException(Exception):
    def __init__(self, path):
        super().__init__(f"Folder już istnieje: {path}")
class ParentFolderNotFoundStworzFolderException(Exception):
    def __init__(self, path):
        super().__init__(f"Folder nadrzędny nie istnieje: {path}")
class PathIsNotDirectoryStworzFolderException(Exception):
    def __init__(self, path):
        super().__init__(f"Podana ścieżka nie jest folderem: {path}")
class FolderPermissionDeniedStworzFolderException(Exception):
    def __init__(self, path):
        super().__init__(f"Brak uprawnień do utworzenia folderu: {path}")
class FolderUnknownOSErrorStworzFolderException(Exception):
    def __init__(self, path, error):
        super().__init__(f"Błąd systemowy przy tworzeniu folderu '{path}': {error}")

class SourceFolderNotFoundEdycjaFolderException(Exception):
    def __init__(self, stara_sciezka):
        super().__init__(f"Folder źródłowy nie istnieje: {stara_sciezka}")
class DestinationFolderAlreadyExistsEdycjaFolderException(Exception):
    def __init__(self, nowa_sciezka):
        super().__init__(f"Folder docelowy już istnieje: {nowa_sciezka}")
class SourcePathIsNotDirectoryEdycjaFolderException(Exception):
    def __init__(self, stara_sciezka):
        super().__init__(f"Podana ścieżka źródłowa nie jest folderem: {stara_sciezka}")
class FolderRenamePermissionDeniedEdycjaFolderException(Exception):
    def __init__(self, stara_sciezka, nowa_sciezka):
        super().__init__(
            f"Brak uprawnień do zmiany nazwy folderu: {stara_sciezka} -> {nowa_sciezka}")
class FolderRenameOSErrorEdycjaFolderException(Exception):
    def __init__(self, stara_sciezka, nowa_sciezka, blad):
        super().__init__(f"Błąd systemowy przy zmianie nazwy folderu '{stara_sciezka}' -> '{nowa_sciezka}': {blad}")

class SearchStartPathNotFoundPrzeszukanieException(Exception):
    def __init__(self, zaczyna_od):
        super().__init__(f"Ścieżka początkowa nie istnieje: {zaczyna_od}")
class SearchPathIsNotDirectoryPrzeszukanieException(Exception):
    def __init__(self, zaczyna_od):
        super().__init__(f"Podana ścieżka początkowa nie jest folderem: {zaczyna_od}")
class SearchPermissionDeniedPrzeszukanieException(Exception):
    def __init__(self, sciezka):
        super().__init__(f"Brak uprawnień do przeszukiwania folderu: {sciezka}")
class InvalidSearchLimitPrzeszukanieException(Exception):
    def __init__(self, liczba_wynikow):
        super().__init__(f"Niepoprawna liczba wyników: {liczba_wynikow}")

class SourceFileNotFoundZastapException(Exception):
    def __init__(self, stary_plik):
        super().__init__(f"Plik źródłowy nie istnieje: {stary_plik}")
class SourcePathIsNotFileZastapException(Exception):
    def __init__(self, stary_plik):
        super().__init__(f"Podana ścieżka źródłowa nie jest plikiem: {stary_plik}")
class ReplacePermissionDeniedZastapException(Exception):
    def __init__(self, stary_plik, nowy_plik):
        super().__init__(f"Brak uprawnień do zastąpienia pliku: {stary_plik} -> {nowy_plik}")
class ReplaceOSErrorZastapException(Exception):
    def __init__(self, stary_plik, nowy_plik, blad):
        super().__init__(f"Błąd systemowy przy zastępowaniu pliku '{stary_plik}' -> '{nowy_plik}': {blad}")

class FileNotFoundResetPlikException(Exception):
    def __init__(self, sciezka_pliku):
        super().__init__(f"Plik nie istnieje: {sciezka_pliku}")
class PathIsNotFileResetPlikException(Exception):
    def __init__(self, sciezka_pliku):
        super().__init__(f"Podana ścieżka nie jest plikiem: {sciezka_pliku}")
class UnsupportedFileExtensionResetPlikException(Exception):
    def __init__(self, rozszerzenie):
        super().__init__(f"Nieobsługiwane rozszerzenie pliku: .{rozszerzenie}")
class FileResetPermissionDeniedResetPlikException(Exception):
    def __init__(self, sciezka_pliku):
        super().__init__(f"Brak uprawnień do resetowania pliku: {sciezka_pliku}")
class FileResetOSErrorResetPlikException(Exception):
    def __init__(self, sciezka_pliku, blad):
        super().__init__(f"Błąd systemowy podczas resetowania pliku '{sciezka_pliku}': {blad}")
class FileReadPermissionDeniedResetPlikException(Exception):
    def __init__(self, sciezka_pliku):
        super().__init__(f"Brak uprawnień do odczytu pliku: {sciezka_pliku}")
class FileReadOSErrorResetPlikException(Exception):
    def __init__(self, sciezka_pliku, blad):
        super().__init__(f"Błąd systemowy podczas odczytu pliku '{sciezka_pliku}': {blad}")

class FileNotFoundOdczytajException(Exception):
    def __init__(self, sciezka_pliku):
        super().__init__(f"Plik do odczytu nie istnieje: {sciezka_pliku}")
class PathIsNotFileOdczytajException(Exception):
    def __init__(self, sciezka_pliku):
        super().__init__(f"Ścieżka do odczytu nie jest plikiem: {sciezka_pliku}")
class UnsupportedFileExtensionOdczytajException(Exception):
    def __init__(self, rozszerzenie):
        super().__init__(f"Nieobsługiwane rozszerzenie pliku do odczytu: .{rozszerzenie}")
class FileReadPermissionDeniedOdczytajException(Exception):
    def __init__(self, sciezka_pliku):
        super().__init__(f"Brak uprawnień do odczytu pliku: {sciezka_pliku}")
class FileReadOSErrorOdczytajException(Exception):
    def __init__(self, sciezka_pliku, blad):
        super().__init__(f"Błąd systemowy podczas odczytu pliku '{sciezka_pliku}': {blad}")

class FileNotFoundDopiszException(Exception):
    def __init__(self, sciezka_pliku):
        super().__init__(f"Plik do dopisania nie istnieje: {sciezka_pliku}")
class PathIsNotFileDopiszException(Exception):
    def __init__(self, sciezka_pliku):
        super().__init__(f"Ścieżka do dopisania nie jest plikiem: {sciezka_pliku}")
class UnsupportedFileExtensionDopiszException(Exception):
    def __init__(self, rozszerzenie):
        super().__init__(f"Nieobsługiwane rozszerzenie pliku do dopisania: .{rozszerzenie}")
class FileAppendPermissionDeniedDopiszException(Exception):
    def __init__(self, sciezka_pliku):
        super().__init__(f"Brak uprawnień do dopisywania do pliku: {sciezka_pliku}")
class FileAppendOSErrorDopiszException(Exception):
    def __init__(self, sciezka_pliku, blad):
        super().__init__(f"Błąd systemowy podczas dopisywania do pliku '{sciezka_pliku}': {blad}")

FileNotFoundPoprawnoscPlikuException