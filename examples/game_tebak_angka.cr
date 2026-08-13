# ==========================================
# GAME TEBAK ANGKA INTERAKTIF BAHASA CORE
# ==========================================

cetak "=== SELAMAT DATANG DI GAME TEBAK ANGKA ==="
cetak "Komputer telah memilih angka rahasia antara 1 sampai 10."
cetak "Kamu memiliki 3 kesempatan untuk menebak!"
cetak ""

variabel angka_rahasia = panggil acak 1 10
variabel status_menang = salah

untuk putaran dari 1 hingga 3
    cetak "--- Percobaan ke-", putaran, "dari 3 ---"
    variabel tebakan = masukan "Masukkan angka tebakanmu (1-10): "
    
    jika tebakan == angka_rahasia
        cetak "🎉 LUAR BIASA! Tebakanmu TEPAT! Kamu Menang!"
        status_menang = benar
    lainjika tebakan < angka_rahasia
        cetak "💡 Petunjuk: Tebakanmu terlalu KECIL."
    selainitu
        cetak "💡 Petunjuk: Tebakanmu terlalu BESAR."
    cetak ""

jika status_menang == salah
    cetak "😢 Yah, kesempatan habis! Angka rahasia sebenarnya adalah:", angka_rahasia
selainitu
    cetak "🏆 Hebat! Kamu berhasil mengalahkan komputer!"
