import unittest
import sys
import os
from io import StringIO
from contextlib import redirect_stdout

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from main import run_code


class TestCoreLists(unittest.TestCase):
    def run_capture(self, code: str) -> str:
        f = StringIO()
        with redirect_stdout(f):
            success = run_code(code)
        self.assertTrue(success)
        return f.getvalue().strip()

    def test_list_creation_and_print(self):
        code = '''variabel angka = [10, 20, 30]
cetak angka'''
        output = self.run_capture(code)
        self.assertEqual(output, "[10, 20, 30]")

    def test_list_string_elements(self):
        code = '''variabel nama = ["Andi", "Budi", "Siti"]
cetak nama'''
        output = self.run_capture(code)
        self.assertEqual(output, '["Andi", "Budi", "Siti"]')

    def test_list_append(self):
        code = '''variabel buah = ["Apel", "Jeruk"]
tambah buah "Mangga"
cetak buah'''
        output = self.run_capture(code)
        self.assertEqual(output, '["Apel", "Jeruk", "Mangga"]')

    def test_list_remove(self):
        code = '''variabel buah = ["Apel", "Jeruk", "Mangga"]
hapus buah 1
cetak buah'''
        output = self.run_capture(code)
        self.assertEqual(output, '["Apel", "Mangga"]')

    def test_list_ambil_and_panjang(self):
        code = '''variabel buah = ["Apel", "Jeruk", "Mangga"]
cetak panggil panjang buah
cetak panggil ambil buah 0
cetak panggil ambil buah 2'''
        output = self.run_capture(code)
        self.assertEqual(output, "3\nApel\nMangga")

    def test_for_in_loop(self):
        code = '''variabel siswa = ["Andi", "Budi", "Siti"]
untuk nama dalam siswa
    cetak "Halo,", nama'''
        output = self.run_capture(code)
        expected = "Halo, Andi\nHalo, Budi\nHalo, Siti"
        self.assertEqual(output, expected)

    def test_gabung_builtin(self):
        code = '''variabel kata = ["Saya", "Belajar", "Core"]
cetak panggil gabung kata " - "'''
        output = self.run_capture(code)
        self.assertEqual(output, "Saya - Belajar - Core")


if __name__ == "__main__":
    unittest.main()
