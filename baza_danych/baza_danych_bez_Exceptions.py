from typing import Literal, Any
import sqlite3

class Bazadanych:
    def __init__(self, nazwa: str):
        self.nazwa = nazwa
        self.bazadanych: dict[tuple[int, str], dict[int, Any]]

        self.bazadanych = {(0, "nazwaKolumna"): {0: "00Wartość", 1: "01Wartość"}, (1, "name1Kolumna1"): {0: "10Wartość", 1: "11Wartość"}}

    def __str__(self):
        for klucz, wartosc in self.bazadanych.items():
            print(klucz, wartosc)


    def wyswietlBazeDanych(self, func):
        def wrapper(*args, **kwargs):
            print(f"Włączona funkcja: {func.__name__}")
            print(f"Baza danych przed zmianą:\n{self.bazadanych}")
            func(*args, **kwargs)
            print(f"Baza danych po zmianie:\n{self.bazadanych}")

            return wrapper

    def otworz(self, nazwa, czy_nowa=False):
        self.nazwa = nazwa
        self._tworzymy_nowy = czy_nowa

        if czy_nowa:
            self.bazadanych = {}
        else:
            conn = sqlite3.connect(nazwa)
            cursor = conn.cursor()
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            tabele = [row[0] for row in cursor.fetchall()]

            self.bazadanych = {}
            col_id_counter = 0

            for tabela in tabele:
                cursor.execute(f"PRAGMA table_info('{tabela}')")
                kolumny_info = cursor.fetchall()

                for kolumna_info in kolumny_info:
                    _, nazwa_kolumny, _, _, _, _ = kolumna_info
                    klucz = (col_id_counter, nazwa_kolumny)
                    col_id_counter += 1

                    cursor.execute(f"SELECT rowid, \"{nazwa_kolumny}\" FROM '{tabela}'")
                    wiersze = cursor.fetchall()

                    wiersze_slownik = {}
                    for rowid, wartosc in wiersze:
                        wiersze_slownik[rowid] = wartosc

                    self.bazadanych[klucz] = wiersze_slownik

            conn.close()

        self._tworzymy_nowy = False

    def zapisz(self):
        for (_, nazwa), wiersze in self.bazadanych.items():
            self.cursor.execute(
                f"""CREATE TABLE IF NOT EXISTS [{nazwa}] (
                    wiersz TEXT PRIMARY KEY,
                    wartosc TEXT
                )"""
            )

            for wiersz, wartosc in wiersze.items():
                self.cursor.execute(
                    f"""INSERT INTO [{nazwa}] (wiersz, wartosc)
                        VALUES (?, ?)
                        ON CONFLICT(wiersz) DO UPDATE SET wartosc=excluded.wartosc""",
                    (str(wiersz), str(wartosc))
                )

        self.conn.commit()

    def dodaj_element(self, kolumna, wiersz, autoWiersz, wartosc, bazadanych):
        self.bazadanych # nie zrobione

    @wyswietlBazeDanych
    def dodaj_przesten(self, coDodac: Literal["kolumna", "wiersz"], nazwa: str):
        match coDodac:
            case "kolumna":
                nowy_id = max((k[0] for k in self.bazadanych), default=-1) + 1
                nowy_klucz = (nowy_id, nazwa)
                self.bazadanych[nowy_klucz] = {}

            case "wiersz":
                if getattr(self, "autoWiersz", True):
                    wszystkie_wiersze = set()
                    for wiersze in self.bazadanych.values():
                        wszystkie_wiersze.update(k for k in wiersze.keys() if isinstance(k, int))
                    nowy_wiersz_id = max(wszystkie_wiersze, default=-1) + 1
                else:
                    nowy_wiersz_id = nazwa

                for wiersze in self.bazadanych.values():
                    wiersze[nowy_wiersz_id] = None

    @wyswietlBazeDanych
    def usun(self, coUsun: Literal["kolumna", "wiersz", "element"], nazwa):
        if coUsun == "kolumna":
            klucze_do_usuniecia = [k for k in self.bazadanych if k[0] == nazwa or k[1] == nazwa]
            for k in klucze_do_usuniecia:
                del self.bazadanych[k]

        elif coUsun == "wiersz":
            for wiersze in self.bazadanych.values():
                if nazwa in wiersze:
                    del wiersze[nazwa]

        elif coUsun == "element":
            kolumna, wiersz = nazwa
            for klucz, wiersze in self.bazadanych.items():
                if klucz[0] == kolumna or klucz[1] == kolumna:
                    if wiersz in wiersze:
                        del wiersze[wiersz]

    def edytuj(self, kolumna, wiersz, nowyElement): # narazie zrobić na słowniku
        0 # edytuje konkretny element

    @wyswietlBazeDanych()
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

bazadanych = Bazadanych()
bazadanych.otworz(nazwa="test", czy_nowa=True)
print(bazadanych)