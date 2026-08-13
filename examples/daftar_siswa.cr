# Program Pengelolaan Siswa dengan Tipe Data Daftar (List)

cetak "=== DAFTAR SISWA KELAS CODING CORE ==="

# 1. Membuat daftar awal
variabel siswa = ["Andi", "Budi", "Siti", "Vani"]
cetak "Siswa awal:", siswa
cetak "Jumlah siswa awal:", panggil panjang siswa
cetak ""

# 2. Menambah siswa baru
cetak "--- Menambahkan Siswa Baru ---"
tambah siswa "Juna"
tambah siswa "Dewi"
cetak "Setelah pendaftaran baru:", siswa
cetak ""

# 3. Menghapus siswa yang pindah (misal siswa pada indeks 1 / Budi)
cetak "--- Siswa Pindah Sekolah ---"
variabel siswa_pindah = panggil ambil siswa 1
hapus siswa 1
cetak "Siswa yang pindah:", siswa_pindah
cetak "Daftar siswa terbaru:", siswa
cetak ""

# 4. Melakukan perulangan untuk menyapa setiap siswa
cetak "--- Absensi Kelas Hari Ini ---"
variabel nomor = 1
untuk nama dalam siswa
    cetak nomor, ".", "Halo selamat pagi,", nama
    nomor = nomor + 1

cetak ""
cetak "Total siswa yang hadir:", panggil panjang siswa, "orang."
