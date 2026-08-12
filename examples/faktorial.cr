# Contoh Rekursi dan Perhitungan Faktorial dalam Bahasa Core (.cr)

fungsi hitung_faktorial n
    jika n <= 1
        kembalikan 1
    selainitu
        variabel n_kurang_satu = n - 1
        variabel hasil_sebelumnya = panggil hitung_faktorial n_kurang_satu
        kembalikan n * hasil_sebelumnya

cetak "=== Program Menghitung Faktorial ==="

variabel angka = 5
variabel hasil = panggil hitung_faktorial angka

cetak "Faktorial dari", angka, "! adalah:", hasil

angka = 6
hasil = panggil hitung_faktorial angka
cetak "Faktorial dari", angka, "! adalah:", hasil
