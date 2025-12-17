class BazaDanychSprawdzOtworz(Exception):
    pass
class FileNotFoundException(Exception):
    pass
class InvalidDatabaseTypeException(BazaDanychSprawdzOtworz):
    def __init__(self, typ):
        super().__init__(f"Typ bazy danych jest nieprawidłowy (oczekiwano dict): {typ}")
class EmptyDatabaseException(BazaDanychSprawdzOtworz):
    def __init__(self):
        super().__init__("Baza danych jest pusta")
class InvalidColumnKeyException(BazaDanychSprawdzOtworz):
    def __init__(self, key):
        super().__init__(f"Klucz kolumny nie jest krotką (int, str): {key}")
class InvalidColumnIndexException(BazaDanychSprawdzOtworz):
    def __init__(self, idx):
        super().__init__(f"Pierwszy element klucza kolumny nie jest int: {idx}")
class InvalidColumnNameException(BazaDanychSprawdzOtworz):
    def __init__(self, name):
        super().__init__(f"Drugi element klucza kolumny nie jest str: {name}")
class DuplicateColumnKeyException(BazaDanychSprawdzOtworz):
    def __init__(self, key):
        super().__init__(f"Duplikat klucza kolumny: {key}")
class InvalidColumnNameCharactersException(BazaDanychSprawdzOtworz):
    def __init__(self, name):
        super().__init__(f"Nazwa kolumny zawiera niedozwolone znaki: {name}")
class InvalidColumnValuesException(BazaDanychSprawdzOtworz):
    def __init__(self, key):
        super().__init__(f"Wartości kolumny nie są dict: {key}")
class InvalidRowKeyException(BazaDanychSprawdzOtworz):
    def __init__(self, key):
        super().__init__(f"Klucz wiersza nie jest int lub str: {key}")
class DuplicateRowKeyException(BazaDanychSprawdzOtworz):
    def __init__(self, key, kolumna):
        super().__init__(f"Duplikat klucza wiersza {key} w kolumnie {kolumna}")
class NoneValueException(BazaDanychSprawdzOtworz):
    def __init__(self, kolumna, wiersz):
        super().__init__(f"Wartość w kolumnie {kolumna} wiersz {wiersz} nie może być None")
class UnsupportedValueTypeException(BazaDanychSprawdzOtworz):
    def __init__(self, typ, kolumna, wiersz):
        super().__init__(f"Niewspierany typ wartości {typ} w kolumnie {kolumna} wiersz {wiersz}")
class DatabaseOperationalException(BazaDanychSprawdzOtworz):
    pass
class DatabaseOpenException(Exception):
    pass

class BazaDanychSprawdzZapisz(Exception):
    pass
class ConnectionClosedFromSaveException(BazaDanychSprawdzZapisz):
    def __init__(self):
        super().__init__("Brak otwartego połączenia z bazą (self.conn is None)")
class InvalidDatabaseTypeFromSaveException(BazaDanychSprawdzZapisz):
    def __init__(self, actual_type):
        super().__init__(f"self.bazadanych musi być typu dict, a jest {actual_type}")
class EmptyDatabasFromSaveeException(BazaDanychSprawdzZapisz):
    def __init__(self):
        super().__init__("Brak danych do zapisu (pusta baza)")
class InvalidColumnKeyFromSaveException(BazaDanychSprawdzZapisz):
    def __init__(self, key):
        super().__init__(f"Klucz {key} musi być krotką (int, str)")
class InvalidColumnFormatFromSaveException(BazaDanychSprawdzZapisz):
    def __init__(self, key):
        super().__init__(f"Niepoprawny format klucza kolumny {key}")
class InvalidColumnValuesFromSaveException(BazaDanychSprawdzZapisz):
    def __init__(self, key):
        super().__init__(f"Wartości kolumny {key} muszą być dict")
class InvalidRowKeyFromSaveException(BazaDanychSprawdzZapisz):
    def __init__(self, row_key):
        super().__init__(f"Klucz wiersza {row_key} musi być int lub str")
class NoneValueFromSaveException(BazaDanychSprawdzZapisz):
    def __init__(self, key, row_key):
        super().__init__(f"Wartość w kolumnie {key} wiersz {row_key} nie może być None")
class UnsupportedValueTypeFromSaveException(BazaDanychSprawdzZapisz):
    def __init__(self, value, key, row_key):
        super().__init__(f"Niewspierany typ wartości {value} w {key} {row_key}")
class DatabaseIntegrityFromSaveException(BazaDanychSprawdzZapisz):
    def __init__(self, original_msg):
        super().__init__(f"Naruszenie ograniczeń integralności bazy (unikalność, klucze obce): {original_msg}")
class DatabaseOperationalFromSaveException(BazaDanychSprawdzZapisz):
    def __init__(self, original_msg):
        super().__init__(f"Błędy SQL podczas zapisu (np. błędne zapytania, brak tabel): {original_msg}")
class DatabaseFileFromSaveException(BazaDanychSprawdzZapisz):
    def __init__(self, original_msg):
        super().__init__(f"Problemy z plikiem bazy (uszkodzenie, brak miejsca): {original_msg}")
class DatabasePermissionFromSaveException(BazaDanychSprawdzZapisz):
    def __init__(self, original_msg):
        super().__init__(f"Brak uprawnień do zapisu pliku: {original_msg}")
class EmptyDatabaseFromSaveException(BazaDanychSprawdzZapisz):
    def __init__(self):
        super().__init__("Brak danych do zapisu (pusta baza)")

class BazaDanychSprawdzDodajElementException(Exception):
    pass
class NoDatabaseProvidedFromAddException(BazaDanychSprawdzDodajElementException):
    def __init__(self, msg):
        super().__init__(f"Brak dostępu do bazy danych: {msg}")
class InvalidColumnTupleStructureFromAddException(BazaDanychSprawdzDodajElementException):
    def __init__(self, kolumna):
        super().__init__(f"Niepoprawna struktura klucza kolumny (oczekiwano tuple (int, str)): {kolumna}")
class ColumnIdNotFoundFromAddException(BazaDanychSprawdzDodajElementException):
    def __init__(self, kolumna_id):
        super().__init__(f"Nie znaleziono kolumny o ID: {kolumna_id}")
class ColumnNameNotFoundFromAddException(BazaDanychSprawdzDodajElementException):
    def __init__(self, kolumna_nazwa):
        super().__init__(f"Nie znaleziono kolumny o nazwie: {kolumna_nazwa}")
class InvalidColumnTypeFromAddException(BazaDanychSprawdzDodajElementException):
    def __init__(self, typ):
        super().__init__(f"Niepoprawny typ kolumny (oczekiwano int lub str): {typ}")
class InvalidRowContainerTypeFromAddException(BazaDanychSprawdzDodajElementException):
    def __init__(self, typ):
        super().__init__(f"Niepoprawny typ kontenera wierszy (oczekiwano dict): {typ}")
class AutoGeneratedRowIdConflictFromAddException(BazaDanychSprawdzDodajElementException):
    def __init__(self, wiersz_id):
        super().__init__(f"Konflikt ID wiersza wygenerowanego automatycznie: {wiersz_id}")
class MissingRowIdWhenAutoDisabledFromAddException(BazaDanychSprawdzDodajElementException):
    def __init__(self):
        super().__init__("Brak ID wiersza gdy autoWiersz jest wyłączone")
class InvalidRowIdInColumnFromAddException(BazaDanychSprawdzDodajElementException):
    def __init__(self, wiersz_id, kolumna):
        super().__init__(f"Niepoprawny ID wiersza {wiersz_id} w kolumnie {kolumna}")
class MissingRowNameFromAddException(BazaDanychSprawdzDodajElementException):
    def __init__(self, wiersz_nazwa):
        super().__init__(f"Nie znaleziono wiersza o nazwie: {wiersz_nazwa}")
class InvalidRowKeyTypeFromAddException(BazaDanychSprawdzDodajElementException):
    def __init__(self, typ):
        super().__init__(f"Niepoprawny typ klucza wiersza (oczekiwano int lub str): {typ}")
class InvalidAdditionElementNoneFromAddException(BazaDanychSprawdzDodajElementException):
    def __init__(self, wartosc):
        super().__init__(f"Niepoprawny element do dodania (None): {wartosc}")

class BazaDanychSprawdzDodajPrzestrzenException(Exception):
    pass
class NoDatabaseProvidedDodajPrzestrzenException(BazaDanychSprawdzDodajPrzestrzenException):
    def __init__(self, msg):
        super().__init__(f"Brak dostępu do bazy danych: {msg}")
class InvalidColumnTupleStructureDodajPrzestrzenException(BazaDanychSprawdzDodajPrzestrzenException):
    def __init__(self, kolumna):
        super().__init__(f"Niepoprawna struktura klucza kolumny (oczekiwano tuple(int, str)): {kolumna}")
class ColumnIdNotFoundDodajPrzestrzenException(BazaDanychSprawdzDodajPrzestrzenException):
    def __init__(self, kolumna_id):
        super().__init__(f"Nie znaleziono kolumny o ID: {kolumna_id}")
class ColumnNameNotFoundDodajPrzestrzenException(BazaDanychSprawdzDodajPrzestrzenException):
    def __init__(self, kolumna_nazwa):
        super().__init__(f"Nie znaleziono kolumny o nazwie: {kolumna_nazwa}")
class InvalidColumnTypeDodajPrzestrzenException(BazaDanychSprawdzDodajPrzestrzenException):
    def __init__(self, typ):
        super().__init__(f"Niepoprawny typ kolumny (oczekiwano int lub str): {typ}")
class InvalidRowContainerTypeDodajPrzestrzenException(BazaDanychSprawdzDodajPrzestrzenException):
    def __init__(self, typ):
        super().__init__(f"Niepoprawny typ kontenera wierszy (oczekiwano dict): {typ}")
class AutoGeneratedRowIdConflictDodajPrzestrzenException(BazaDanychSprawdzDodajPrzestrzenException):
    def __init__(self, wiersz_id):
        super().__init__(f"Konflikt ID wiersza wygenerowanego automatycznie: {wiersz_id}")
class MissingRowIdWhenAutoDisabledDodajPrzestrzenException(BazaDanychSprawdzDodajPrzestrzenException):
    def __init__(self):
        super().__init__("Brak ID wiersza gdy autoWiersz jest wyłączone")
class InvalidRowIdInColumnDodajPrzestrzenException(BazaDanychSprawdzDodajPrzestrzenException):
    def __init__(self, wiersz_id, kolumna):
        super().__init__(f"Niepoprawny ID wiersza {wiersz_id} w kolumnie {kolumna}")
class MissingRowNameDodajPrzestrzenException(BazaDanychSprawdzDodajPrzestrzenException):
    def __init__(self, wiersz_nazwa):
        super().__init__(f"Nie znaleziono wiersza o nazwie: {wiersz_nazwa}")
class InvalidRowKeyTypeDodajPrzestrzenException(BazaDanychSprawdzDodajPrzestrzenException):
    def __init__(self, typ):
        super().__init__(f"Niepoprawny typ klucza wiersza (oczekiwano int lub str): {typ}")
class InvalidAdditionElementNoneDodajPrzestrzenException(BazaDanychSprawdzDodajPrzestrzenException):
    def __init__(self, wartosc):
        super().__init__(f"Niepoprawny element do dodania: {wartosc}")

class BazadanychSprawdzUsunException(Exception):
    pass
class NoDatabaseProvidedUsunException(BazadanychSprawdzUsunException):
    def __init__(self, msg):
        super().__init__(f"Brak bazy danych: {msg}")
class InvalidDatabaseTypeUsunException(BazadanychSprawdzUsunException):
    def __init__(self, typ):
        super().__init__(f"Niepoprawny typ bazy danych (oczekiwano dict): {typ}")
class InvalidRemovalTypeUsunException(BazadanychSprawdzUsunException):
    def __init__(self, wartosc):
        super().__init__(f"Nieprawidłowy typ usuwania: {wartosc}")
class InvalidRemovalNameTypeUsunException(BazadanychSprawdzUsunException):
    def __init__(self, typ):
        super().__init__(f"Niepoprawny typ nazwy do usunięcia (oczekiwano str, int lub tuple): {typ}")
class ColumnNotFoundUsunException(BazadanychSprawdzUsunException):
    def __init__(self, nazwa):
        super().__init__(f"Nie znaleziono kolumny do usunięcia: {nazwa}")
class RowNotFoundUsunException(BazadanychSprawdzUsunException):
    def __init__(self, nazwa):
        super().__init__(f"Nie znaleziono wiersza do usunięcia: {nazwa}")
class InvalidElementKeyUsunException(BazadanychSprawdzUsunException):
    def __init__(self, wartosc):
        super().__init__(f"Nieprawidłowy klucz elementu do usunięcia (oczekiwano krotkę (kolumna, wiersz)): {wartosc}")
class InvalidColumnTupleStructureUsunException(BazadanychSprawdzUsunException):
    def __init__(self, wartosc):
        super().__init__(f"Niepoprawna struktura klucza kolumny (oczekiwano tuple (int, str)): {wartosc}")
class InvalidColumnTypeUsunException(BazadanychSprawdzUsunException):
    def __init__(self, wartosc):
        super().__init__(f"Niepoprawny typ klucza kolumny (oczekiwano int i str): {wartosc}")

0