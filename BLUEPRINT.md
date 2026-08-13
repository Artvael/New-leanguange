# 🗺️ Blueprint & Roadmap Pengembangan Bahasa Pemrograman Core (.cr)

Dokumen ini berisi analisis mendalam mengenai status bahasa **Core saat ini**, visi jangka panjang, serta daftar **PR (Pekerjaan Rumah / Action Items)** yang terstruktur ke dalam 4 fase pengembangan.

---

## 📊 1. Analisis Status Saat Ini (Core v1.1.0)

### ✅ Keunggulan yang Sudah Berhasil Dibangun:
1. **Sintaks Humanis Tanpa Simbol**: Bebas `{ }`, `( )`, dan `;`.
2. **Sistem Indentasi Python-like**: Penanganan otomatis `INDENT` dan `DEDENT`.
3. **Kata Kunci 100% Bahasa Indonesia**: `variabel`, `masukan`, `cetak`, `jika`, `lainjika`, `selainitu`, `selama`, `untuk ... dari ... hingga`, `fungsi`, `kembalikan`.
4. **Fungsi Bawaan Logika & Game**: `acak`, `panjang`, `angka`, `teks`.
5. **Developer Experience**: Launcher `core.bat`, `core.ps1`, unit test suite terotomatisasi, serta Ekstensi VS Code / Antigravity IDE (Logo resmi + Syntax Highlighting).

---

## 🎯 2. Blueprint & Rencana Upgrade (PR Roadmap)

```
┌──────────────────────────────────────────────────────────────────────────┐
│                             CORE ROADMAP                                 │
├──────────────┬──────────────┬────────────────────────┬───────────────────┤
│    FASE 1    │    FASE 2    │         FASE 3         │      FASE 4       │
│ Struktur Data│ Fitur Web &  │ Modularitas & Deteksi  │ Transpiler &      │
│   & File     │ Jaringan     │     Error Pintar       │ Ekosistem         │
└──────────────┴──────────────┴────────────────────────┴───────────────────┘
```

---

### 📌 FASE 1: Struktur Data & Manajemen Berkas (Prioritas Tinggi)
> **Tujuan**: Memungkinkan pelajar mengelola banyak data sekaligus dan menyimpan data ke file komputer.

- [ ] **PR 1.1: Tipe Data `daftar` (List / Array)**
  - Sintaks: `variabel nilai = [80, 90, 75, 100]`
  - Operasi: `tambah nilai 95`, `ambil nilai 0`, `panjang nilai`
  - Perulangan: `untuk item dalam nilai`
- [ ] **PR 1.2: Tipe Data `kamus` (Dictionary / Map / Objek)**
  - Sintaks: `variabel siswa = { nama: "Budi", umur: 17, kota: "Jakarta" }`
- [ ] **PR 1.3: Manajemen File (File I/O)**
  - Membaca file: `variabel teks = baca_file "catatan.txt"`
  - Menulis file: `tulis_file "skor.txt" "Pemenang: Juna"`

---

### 🌐 FASE 2: Fitur Web & Komunikasi Jaringan
> **Tujuan**: Membuka kemampuan Core agar bisa langsung digunakan membuat website dan aplikasi interaktif.

- [ ] **PR 2.1: Mini Web Server (`buka_web`)**
  - Perintah bawaan: `buka_web 8080 konten_html`
  - Memungkinkan browser membuka `http://localhost:8080` dan menampilkan hasil olah logika Core.
- [ ] **PR 2.2: Online Web Playground (Bisa Koding di Browser & HP)**
  - Membuat web app di mana siswa bisa menulis kode Core dan melihat hasilnya langsung secara online tanpa install Python.
- [ ] **PR 2.3: Pemanggilan API Eksternal (`ambil_web`)**
  - Mengambil data cuaca, kurs rupiah, atau berita via API: `variabel data = panggil ambil_web "https://api.example.com"`

---

### 🧠 FASE 3: Modularitas & Pesan Error Cerdas
> **Tujuan**: Membuat pengalaman koding bebas stres dengan diagnostik ramah pemula.

- [ ] **PR 3.1: Sistem Impor Antar-File (`muat`)**
  - Memecah program besar ke beberapa file: `muat "rumus_matematika.cr"`
- [ ] **PR 3.2: Detektor Typo Cerdas (*"Apakah maksud Anda...?"*)**
  - Jika siswa mengetik `cetakk` atau `varriabel`, interpreter otomatis menyarankan:
    `❌ [Kesalahan] Kata 'cetakk' tidak dikenali. Apakah maksud Anda 'cetak'?`
- [ ] **PR 3.3: Penunjuk Visual Baris Kode pada Error**
  - Menampilkan cuplikan baris kode yang salah dengan tanda panah `^` tepat di bawah karakter penyebab error.

---

### ⚡ FASE 4: Transpiler, Kompilasi & Ekosistem Nasional
> **Tujuan**: Mengintegrasikan Core ke industri dan menjadikannya standar kurikulum nasional.

- [ ] **PR 4.1: Transpiler Otomatis (Core ➔ Python & Core ➔ JavaScript)**
  - Perintah: `core ekspor game.cr --ke python`
  - Membuktikan bahwa logika di Core 100% kompatibel dengan bahasa industri.
- [ ] **PR 4.2: Installer Mandiri (`core.exe` & `pip install core-lang`)**
  - Pengguna di seluruh dunia bisa menginstall cukup dengan: `pip install core-lang`.
- [ ] **PR 4.3: Dokumentasi Interaktif & Modul Ajar Sekolah**
  - Buku panduan kurikulum logika komputasi untuk guru dan siswa di Indonesia.

---

## 🏆 Kesimpulan & Langkah Selanjutnya
Dengan menyelesaikan **Fase 1 (Struktur Data & File I/O)** dan **Fase 2 (Web Server & Playground)**, bahasa **Core** akan melompat dari sekadar bahasa mainan (*toy language*) menjadi **bahasa edukasi fungsional sekelas Python dan Lua**, tetapi jauh lebih ramah untuk bangsa Indonesia!
