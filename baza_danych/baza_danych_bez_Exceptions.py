import sqlite3
from typing import Any, Literal, TypeAlias


class Bazadanych:
    def __init__(self, nazwa: str):
        self.nazwa = nazwa
        {("idKol", "naKol"):{("idWiersz", "naWier"):("rodEl", "cos")}}

        self.bazadanych:dict[
            tuple[int, str],
            dict[
                tuple[int, str],
                tuple[str, Any]
                ]
                ]

        self.bazadanych = {(0, "nazwaKolumna"): {0: "00Wartość", 1: "01Wartość"}, (1, "name1Kolumna1"): {0: "10Wartość", 1: "11Wartość"}}

    def __str__(self):
        print(self.bazadanych)
        # for klucz, wartosc in self.bazadanych.items():
        #     print(klucz, wartosc)


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

# [("wieksze", 5), ("mniejsze", 8)] np
#         self.bazadanych:dict[tuple[int, str],dict[tuple[int, str],tuple[str, Any]]]
    PobierzTyp: TypeAlias = Literal["kolumna", "wiersz", "element"]

    Operator: TypeAlias = Literal[
        "==", "!=", ">", ">=", "<", "<=","in", "between",
        "like", "startswith", "endswith", "ilike",
        "is_null", "not_null","fuzzy"
    ]

    Warunek: TypeAlias = tuple[Operator,Any]
      
    def pobierz(
        self,
        coPobierz: list[PobierzTyp],
        walidacja: list[Warunek]) -> Any:

        """
        Porównania
        == to równe, != to różne, > to większe, < to mniejsze
        Zakres / zbiór, between to zakres wartości, in to w zbiorze
        Tekst
        like zawiera tekst
        startswith zaczyna się
        endswith kończy się
        like bez dużych liter
        Logika
        or to jeden warunek
        not to negacja NIE
        Braki danych
        is_null to brak wartości
        not_null to ma wartość
        Kolejność / ilość
        order_by to sortuj dane
        limit to ogranicz ilość
        offset to pomiń początek
        Podobieństwo
        fuzzy to toleruj literówki
        """
        0 # można pobrać np dane z kolumny czy z wiersza
        # warunki liczbowe
        # wymień te które są zwykle w bazadanych sql żebym mógł większość zaimplementować
        # też warto dać stopień pomylenia że jest do tego jakaś biblitoeka cn
        for operator, wartosc in walidacja:
            match operator:
                case "==":
                    ...
                case ">=":
                    ...
                case "between":
                    a, b = wartosc
                case "fuzzy":
                    tekst, prog = wartosc


    def znajdz(self, element, coZnajdz: Literal["kolumna", "wiersz", "element"], zwracaBool = False):
        0 # przeszukuje coZnajdz
        self.bazadanych = {(0, "nazwaKolumna"):
                           {0: "00Wartość", 1: "01Wartość"}, (1, "name1Kolumna1"): {0: "10Wartość", 1: "11Wartość"}}
        match coZnajdz:
            case "kolumna":
                for el, _ in self.bazadanych.items():
                    if el[1] == element:
                        return True

            case "wiersz":
                0

            case "element":
                0

            case _:
                assert invalidElementFindIncoZnajdzException(coZnajdz)

bazadanych = Bazadanych("test")
bazadanych.otworz(nazwa="test", czy_nowa=True)
bazadanych.dodaj_przesten(coDodac="kolumna", nazwa= "testKolumna")
print(bazadanych)
# dodajel edytuj znajdź zrobić potem chatgpt niech zrobi print i sprawdzi czy wszystko git
# potem exceptions