"""
Test Suite untuk Interpreter Bahasa Core.
Menguji Lexer, Parser, Interpreter, Operator, Logika, Perulangan, Fungsi, dan Penanganan Error.
"""

import sys
import os
import unittest

# Tambahkan direktori root ke sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.lexer import Lexer, CoreLexerError
from src.parser import Parser, CoreParserError
from src.interpreter import Interpreter, CoreRuntimeError


def execute_source(code: str) -> Interpreter:
    lexer = Lexer(code)
    tokens = lexer.tokenize()
    parser = Parser(tokens)
    ast = parser.parse()
    interpreter = Interpreter()
    interpreter.run(ast)
    return interpreter


class TestCoreLanguage(unittest.TestCase):

    def test_variables_and_math(self):
        code = """
variabel a = 10
variabel b = 20
variabel c = a + b * 2
variabel d = (a + b) # diuji tanpa kurung
"""
        # Dalam Core tanpa kurung: a + b * 2 = 10 + 40 = 50
        interp = execute_source("""
variabel a = 10
variabel b = 20
variabel c = a + b * 2
variabel d = c / 10
""")
        self.assertEqual(interp.global_env.get("a", 1), 10)
        self.assertEqual(interp.global_env.get("b", 1), 20)
        self.assertEqual(interp.global_env.get("c", 1), 50)
        self.assertEqual(interp.global_env.get("d", 1), 5)

    def test_if_elif_else(self):
        code = """
variabel nilai = 75
variabel hasil = ""

jika nilai >= 85
    hasil = "A"
lainjika nilai >= 70
    hasil = "B"
selainitu
    hasil = "C"
"""
        interp = execute_source(code)
        self.assertEqual(interp.global_env.get("hasil", 1), "B")

    def test_while_loop(self):
        code = """
variabel total = 0
variabel i = 1
selama i <= 5
    total = total + i
    i = i + 1
"""
        interp = execute_source(code)
        self.assertEqual(interp.global_env.get("total", 1), 15)
        self.assertEqual(interp.global_env.get("i", 1), 6)

    def test_functions_and_recursion(self):
        code = """
fungsi faktorial n
    jika n <= 1
        kembalikan 1
    selainitu
        variabel sisa = n - 1
        variabel rekursif = panggil faktorial sisa
        kembalikan n * rekursif

variabel hasil = panggil faktorial 5
"""
        interp = execute_source(code)
        self.assertEqual(interp.global_env.get("hasil", 1), 120)

    def test_logical_operators(self):
        code = """
variabel x = 10
variabel y = 20
variabel kondisi1 = x < 15 dan y > 15
variabel kondisi2 = x > 15 atau y > 15
variabel kondisi3 = bukan benar
"""
        interp = execute_source(code)
        self.assertTrue(interp.global_env.get("kondisi1", 1))
        self.assertTrue(interp.global_env.get("kondisi2", 1))
        self.assertFalse(interp.global_env.get("kondisi3", 1))

    def test_indentation_error(self):
        # Indentasi tidak terduga di luar blok
        code_unexpected = """
variabel a = 1
  variabel b = 2
"""
        with self.assertRaises(CoreParserError):
            execute_source(code_unexpected)

        # Indentasi tidak cocok (mismatched unindent)
        code_mismatch = """
jika benar
    variabel a = 1
        variabel b = 2
  variabel c = 3
"""
        with self.assertRaises(CoreLexerError):
            execute_source(code_mismatch)

    def test_undefined_variable_error(self):
        code = """
cetak variabel_gaib
"""
        with self.assertRaises(CoreRuntimeError):
            execute_source(code)

    def test_division_by_zero_error(self):
        code = """
variabel salah_hitung = 10 / 0
"""
        with self.assertRaises(CoreRuntimeError):
            execute_source(code)


if __name__ == "__main__":
    unittest.main()
