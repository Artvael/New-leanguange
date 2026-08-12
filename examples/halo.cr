# Contoh Program dalam Bahasa Pemrograman Core (.cr)
# Bahasa logika ramah pelajar Indonesia tanpa simbol {}, (), dan ;

cetak "=== SELAMAT DATANG DI BAHASA PEMROGRAMAN CORE ==="
cetak ""

# 1. Variabel dan Cetak
variabel nama = "Budi"
variabel umur = 16
variabel kota = "Jakarta"

cetak "Halo, nama saya", nama
cetak "Saya berumur", umur, "tahun dan tinggal di", kota
cetak ""

# 2. Percabangan Kondisi (jika, lainjika, selainitu)
cetak "--- Pengecekan Kelayakan KTP ---"
jika umur >= 17
    cetak nama, "sudah berhak memiliki KTP."
selainitu
    variabel sisa_tahun = 17 - umur
    cetak nama, "belum cukup umur. Tunggu", sisa_tahun, "tahun lagi."
cetak ""

# 3. Perulangan (selama)
cetak "--- Hitung Mundur Peluncuran ---"
variabel hitungan = 3
selama hitungan > 0
    cetak "Hitungan:", hitungan
    hitungan = hitungan - 1
cetak "Roket Meluncur!"
cetak ""

# 4. Definisi dan Pemanggilan Fungsi
cetak "--- Fungsi Penjumlahan Sederhana ---"
fungsi tambah a b
    variabel total = a + b
    kembalikan total

variabel angka1 = 25
variabel angka2 = 75
variabel hasil = panggil tambah angka1 angka2

cetak "Hasil dari", angka1, "+", angka2, "=", hasil

# 5. Fungsi Prosedur (Tanpa Nilai Kembalian)
fungsi sapa nama_teman
    cetak "Halo kawan seperjuangan,", nama_teman, "! Semangat belajar coding!"

sapa "Siti"
sapa "Andi"

cetak ""
cetak "=== PROGRAM CORE SELESAI DIJALANKAN DENGAN SUKSES ==="
