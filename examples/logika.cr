# Contoh Logika Percabangan dan Operator dalam Bahasa Core (.cr)

variabel nilai_ujian = 82
variabel kehadiran = 90
variabel ikut_ekskul = benar

cetak "=== Evaluasi Nilai Siswa ==="
cetak "Nilai Ujian:", nilai_ujian
cetak "Tingkat Kehadiran:", kehadiran
cetak "Mengikuti Ekstrakurikuler:", ikut_ekskul
cetak ""

# Penggunaan 'dan', 'atau', 'bukan'
jika nilai_ujian >= 85 dan kehadiran >= 80
    cetak "Predikat: Sangat Memuaskan (A)"
lainjika nilai_ujian >= 75 dan kehadiran >= 75
    cetak "Predikat: Memuaskan (B)"
lainjika nilai_ujian >= 60 atau ikut_ekskul == benar
    cetak "Predikat: Cukup (C)"
selainitu
    cetak "Predikat: Perlu Remedial (D)"

cetak ""
variabel rajin = bukan salah
cetak "Status rajin siswa:", rajin
