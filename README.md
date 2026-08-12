# Bahasa Pemrograman Core (.cr)

<p align="center">
  <img src="assets/logo.jpg" alt="Logo Bahasa Pemrograman Core" width="220" style="border-radius: 20px; box-shadow: 0 8px 24px rgba(0,0,0,0.3);" />
</p>

**Core** adalah bahasa pemrograman edukatif berbahasa Indonesia yang dirancang khusus untuk membantu pemula dan pelajar di Indonesia memahami logika algoritma tanpa hambatan bahasa Inggris dan simbol sintaks yang rumit.

---

## Fitur Utama

- **Tanpa Simbol Rumit**: Tidak menggunakan kurung kurawal `{ }`, tanda kurung `( )`, atau titik koma `;`.
- **Berbasis Indentasi**: Struktur blok kode ditentukan oleh spasi indentasi (seperti Python).
- **Kata Kunci Berbahasa Indonesia**: Seluruh instruksi inti menggunakan istilah Bahasa Indonesia yang mudah dipahami.
- **Pesan Kesalahan Edukatif**: Error leksikal, sintaksis, dan waktu eksekusi dilaporkan secara jelas dalam Bahasa Indonesia beserta nomor barisnya.
- **Interpreter Ringan & Cepat**: Dibangun menggunakan Python murni tanpa dependensi eksternal.

---

## Kata Kunci (Keywords) & Sintaks

| Kata Kunci | Padanan Bahasa Inggris | Keterangan |
| :--- | :--- | :--- |
| `variabel` | `let` / `var` | Mendeklarasikan variabel baru |
| `cetak` | `print` | Menampilkan nilai ke layar |
| `jika` | `if` | Memulai blok percabangan kondisi |
| `lainjika` | `elif` / `else if` | Cabang kondisi lanjutan |
| `selainitu` | `else` | Cabang kondisi akhir |
| `selama` | `while` | Memulai perulangan logika |
| `fungsi` | `def` / `function` | Mendefinisikan fungsi baru |
| `kembalikan` | `return` | Mengembalikan nilai dari fungsi |
| `panggil` | `call` | Memanggil fungsi dalam ekspresi |
| `dan` | `and` | Operator logika AND |
| `atau` | `or` | Operator logika OR |
| `bukan` | `not` | Operator logika NOT |
| `benar` | `true` | Nilai boolean benar |
| `salah` | `false` | Nilai boolean salah |
| `kosong` | `null` / `None` | Nilai kosong |

---

## Contoh Program Core

### 1. Variabel dan Cetak
```python
variabel nama = "Budi"
variabel umur = 17

cetak "Halo nama saya", nama
cetak "Umur saya", umur, "tahun"
```

### 2. Percabangan Kondisi (`jika` - `selainitu`)
```python
jika umur >= 17
    cetak nama, "sudah memiliki KTP"
selainitu
    cetak nama, "belum cukup umur"
```

### 3. Perulangan (`selama`)
```python
variabel hitungan = 5
selama hitungan > 0
    cetak "Hitungan:", hitungan
    hitungan = hitungan - 1
cetak "Selesai!"
```

### 4. Definisi Fungsi
```python
fungsi tambah a b
    variabel total = a + b
    kembalikan total

variabel hasil = panggil tambah 25 75
cetak "Hasil 25 + 75 =", hasil
```

---

## Cara Menjalankan

### 1. Menjalankan File `.cr`
```bash
python main.py examples/halo.cr
python main.py examples/faktorial.cr
python main.py examples/logika.cr
```

### 2. Mode Interaktif (REPL)
Jalankan tanpa argumen untuk masuk ke prompt interaktif:
```bash
python main.py
```
```text
Core > variabel x = 10
Core > variabel y = 20
Core > cetak "Jumlah:", x + y
Jumlah: 30
Core > keluar
```

### 3. Menjalankan Unit Test
```bash
python tests/test_core.py
```

---

## Struktur Proyek

```
New leanguange/
├── src/
│   ├── __init__.py
│   ├── tokens.py        # Definisi Token & TokenType
│   ├── lexer.py         # Tokenizer dengan pelacak Indentasi
│   ├── ast_nodes.py     # Struktur pohon AST
│   ├── parser.py        # Recursive descent parser
│   └── interpreter.py   # Tree-walk interpreter & environment scope
├── examples/
│   ├── halo.cr          # Contoh sintaks lengkap
│   ├── faktorial.cr     # Contoh rekursi & perhitungan
│   └── logika.cr        # Contoh operator logika & branching
├── tests/
│   └── test_core.py     # Unit test suite
├── main.py              # Entry point CLI & REPL
└── README.md            # Dokumentasi panduan
```
