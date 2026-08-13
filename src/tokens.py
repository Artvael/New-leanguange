"""
Definisi tipe token dan struktur Token untuk bahasa pemrograman Core.
"""

from enum import Enum, auto
from dataclasses import dataclass
from typing import Any, Optional


class TokenType(Enum):
    # Kata Kunci (Keywords)
    KEYWORD_VARIABEL = auto()   # variabel
    KEYWORD_CETAK = auto()      # cetak
    KEYWORD_JIKA = auto()       # jika
    KEYWORD_LAINJIKA = auto()   # lainjika
    KEYWORD_SELAINITU = auto()  # selainitu
    KEYWORD_SELAMA = auto()     # selama
    KEYWORD_FUNGSI = auto()     # fungsi
    KEYWORD_KEMBALIKAN = auto() # kembalikan
    KEYWORD_DAN = auto()        # dan
    KEYWORD_ATAU = auto()       # atau
    KEYWORD_BUKAN = auto()      # bukan
    KEYWORD_BENAR = auto()      # benar (True)
    KEYWORD_SALAH = auto()      # salah (False)
    KEYWORD_KOSONG = auto()     # kosong (None)
    KEYWORD_PANGGIL = auto()    # panggil (pemanggilan fungsi)
    KEYWORD_MASUKAN = auto()    # masukan (input pengguna)
    KEYWORD_UNTUK = auto()      # untuk (for loop)
    KEYWORD_DARI = auto()       # dari (range start)
    KEYWORD_HINGGA = auto()     # hingga (range end)
    KEYWORD_DALAM = auto()      # dalam (for-in loop)
    KEYWORD_TAMBAH = auto()     # tambah (list append)
    KEYWORD_HAPUS = auto()      # hapus (list remove)

    # Literal & Identifier
    IDENTIFIER = auto()
    NUMBER = auto()
    STRING = auto()

    # Tanda Kurung Siku (Daftar / List)
    LBRACKET = auto()       # [
    RBRACKET = auto()       # ]

    # Operator Matematika & Perbandingan
    PLUS = auto()           # +
    MINUS = auto()          # -
    MULTIPLY = auto()       # *
    DIVIDE = auto()         # /
    MODULO = auto()         # %
    ASSIGN = auto()         # =
    EQUAL = auto()          # ==
    NOT_EQUAL = auto()      # !=
    GREATER = auto()        # >
    LESS = auto()           # <
    GREATER_EQUAL = auto()  # >=
    LESS_EQUAL = auto()     # <=

    # Pemisah
    COMMA = auto()          # ,

    # Struktur & Indentasi
    INDENT = auto()
    DEDENT = auto()
    NEWLINE = auto()
    EOF = auto()


KEYWORDS = {
    "variabel": TokenType.KEYWORD_VARIABEL,
    "cetak": TokenType.KEYWORD_CETAK,
    "jika": TokenType.KEYWORD_JIKA,
    "lainjika": TokenType.KEYWORD_LAINJIKA,
    "selainitu": TokenType.KEYWORD_SELAINITU,
    "selama": TokenType.KEYWORD_SELAMA,
    "untuk": TokenType.KEYWORD_UNTUK,
    "dari": TokenType.KEYWORD_DARI,
    "hingga": TokenType.KEYWORD_HINGGA,
    "dalam": TokenType.KEYWORD_DALAM,
    "tambah": TokenType.KEYWORD_TAMBAH,
    "hapus": TokenType.KEYWORD_HAPUS,
    "fungsi": TokenType.KEYWORD_FUNGSI,
    "kembalikan": TokenType.KEYWORD_KEMBALIKAN,
    "dan": TokenType.KEYWORD_DAN,
    "atau": TokenType.KEYWORD_ATAU,
    "bukan": TokenType.KEYWORD_BUKAN,
    "benar": TokenType.KEYWORD_BENAR,
    "salah": TokenType.KEYWORD_SALAH,
    "kosong": TokenType.KEYWORD_KOSONG,
    "panggil": TokenType.KEYWORD_PANGGIL,
    "masukan": TokenType.KEYWORD_MASUKAN,
}


@dataclass
class Token:
    type: TokenType
    value: Any
    line: int
    column: int

    def __repr__(self) -> str:
        return f"Token({self.type.name}, {repr(self.value)}, baris={self.line}, kolom={self.column})"
