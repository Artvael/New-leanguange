import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from main import run_code

print("=" * 60)
print("TEST 1: TYPO KATA KUNCI")
print("=" * 60)
run_code('cetakk "Halo Dunia"')

print("\n" + "=" * 60)
print("TEST 2: TYPO NAMA VARIABEL")
print("=" * 60)
run_code('''variabel nama_pengguna = "Andi"
cetak nama_penggun''')

print("\n" + "=" * 60)
print("TEST 3: STRUKTUR PERCABANGAN DUA SELAINITU")
print("=" * 60)
run_code('''jika tebakan == 10
    cetak "Benar"
selainitu
    cetak "Sedang"
selainitu
    cetak "Terlalu besar"''')
