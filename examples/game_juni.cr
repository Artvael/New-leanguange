cetak "Selamat datang di game yang diadakan oleh Juni"
cetak "Game ini dibuat oleh Juni karena mereka sudah menikah sekarang"
cetak "Selamat bermain"
cetak ""

variabel angka_rahasia = panggil acak 1 20
variabel status_menang = salah

untuk putaran dari 1 hingga 10
    cetak "--- Percobaan ke-", putaran, "dari 10 ---"
    variabel tebakan = masukan "Masukkan angka tebakanmu (1-20): "
    
    jika tebakan == angka_rahasia
        cetak "Wow, mommy Vani sangat bangga kepada Juna"
        status_menang = benar
    lainjika tebakan < angka_rahasia
        cetak "💡 Petunjuk: jancok"
    lainjika tebakan == angka_rahasia + 1 atau tebakan == angka_rahasia - 1
        cetak "💡 Petunjuk: Anda mabuk"
    selainitu
        cetak "💡 Petunjuk: Tidur aja"
    cetak ""

jika status_menang == salah
    cetak "😢 Noo!, Juna kena spanking dari Vani"
selainitu
    cetak "🏆 Good! Juna mencintai mommy Vani!"