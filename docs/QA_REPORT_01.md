# QA Report 01 — Real Data Validation

**Tanggal:** 17 November 2026 · **Cabang yang diuji:** `sprint-4` (commit `70d28c4`) · **Penguji:** Claude (peran: Senior QA Engineer / Technical Lead)

**Kesimpulan: aplikasi BELUM siap demo dengan data nyata.** Ada 3 temuan Critical, 7 High, 7 Medium, dan 7 Low.
Parser gagal mengenali bagian pengalaman kerja pada 4 dari 5 CV perusahaan, sehingga peringkat yang dihasilkan
hampir terbalik dari penilaian manual, dan satu kandidat yang memenuhi syarat ditolak otomatis.
Tidak ada kode yang diubah dalam fase ini.

Laporan ini tidak memuat nama, kontak, atau nama perusahaan dari CV. Kelima CV disebut CV 1 sampai CV 5
sesuai nama berkasnya, dan tidak ada berkas CV yang masuk ke repositori.

## Lingkup dan cara uji

| Hal | Keterangan |
| --- | --- |
| Data | `Vacancy.pdf` (Junior Architect) dan `CV_Sample_1.pdf` sampai `CV_Sample_5.pdf` dari perusahaan |
| Cara | Unggah lewat API yang sama dengan antarmuka, jalankan screening, lalu bandingkan setiap hasil dengan isi PDF yang dibaca manual |
| Uji kontrol | Lima CV yang sama diunggah ulang sebagai teks dengan **hanya judul bagian yang dirapikan**, untuk memisahkan kesalahan parser dari kesalahan penilaian |
| Antarmuka | Halaman peringkat dan tiga halaman kandidat dirender di peramban (1440 px), identitas disembunyikan |
| Mode | TF-IDF dan catatan templat. Lingkungan uji tidak dapat memuat model E5 maupun memanggil Gemini |

**Tidak diuji dalam fase ini:**

- Peringkat dengan embedding E5 (mode yang aktif di mesin Product Owner). E5 hanya mengubah komponen kesesuaian isi CV (25%) dan keterampilan tersirat; temuan parser di bawah tidak bergantung pada mode embedding.
- Catatan recruiter dari Gemini dengan prompt Sprint 4. Hanya templat yang diuji.
- OCR. Kelima CV berisi teks, sehingga jalur OCR tidak terpakai.

## Ringkasan hasil

Penilaian manual memakai syarat lowongan: gelar arsitektur atau desain interior, minimal 2 tahun pengalaman
desain dan bangun, serta AutoCAD, SketchUp, dan Revit.

| CV | Profil menurut pembacaan manual | Urutan wajar | Aplikasi (PDF asli) | Uji kontrol (judul dirapikan) |
| --- | --- | --- | --- | --- |
| CV 1 | Sarjana arsitektur, sekitar 6 tahun sebagai desainer interior dan arsitek, AutoCAD + SketchUp + Revit | 1–2 | **5** · 23,6 · Perlu ditinjau | 3 · 56,2 · Perlu ditinjau |
| CV 4 | Sarjana arsitektur (sedang S2), arsitek dan drafter sejak 2023 ditambah proyek lepas, ketiga perangkat lunak, menyebut building codes | 1–2 | **3** · 36,3 · **Tidak lolos** | 1 · 81,1 · Direkomendasikan |
| CV 2 | Sarjana arsitektur, arsitek lepas sejak 2022, AutoCAD + SketchUp, tanpa Revit | 3 | 2 · 45,9 · Perlu ditinjau | 2 · 68,0 · Perlu ditinjau |
| CV 3 | Lulusan SMK, masih kuliah arsitektur, drafter dan visualisasi 3D, tanpa Revit | 4 | **1** · 54,6 · Perlu ditinjau | 4 · 53,9 · Perlu ditinjau |
| CV 5 | Lulusan SMK, masih kuliah, drafter pengujian struktur, 6 bulan sebagai arsitek junior lepas, tanpa Revit | 5 | 4 · 30,7 · Perlu ditinjau | 5 · 31,4 · Tidak lolos |

Dua hal terbaca dari tabel ini:

1. **Mesin penilaian pada dasarnya masuk akal.** Begitu judul bagian terbaca, urutannya mendekati penilaian manual. Masalah utama ada di parser, bukan di rumus skor.
2. **Masih ada kesalahan lapis kedua.** Pada uji kontrol pun CV 1 hanya dihitung 0,5 tahun pengalaman relevan dari sekitar 6 tahun (lihat H-1).

### Hasil parser per CV (PDF asli)

| CV | Pengalaman terbaca | Pendidikan terbaca | Peringatan | Penyebab utama |
| --- | --- | --- | --- | --- |
| CV 1 | 0 dari 6 jabatan | Tidak | 2 | Format Jobstreet: judul bagian satu baris dengan isinya ("Riwayat karier …", "Pendidikan …") |
| CV 2 | 0 dari 2 jabatan | Ya, ditambah 1 entri palsu | 1 | Judul "EXPERIENCES" (jamak) dan "ORGANIZATIONAL EXPERIENCE" tidak dikenali |
| CV 3 | 2 dari 2 jabatan (jabatan dan perusahaan tertukar) | Ya, tetapi keliru (lihat H-4) | 0 | — |
| CV 4 | 0 dari 3 jabatan | Tidak | 2 | Judul "Work Experiences", "Education Level", "Organisational Experience" tidak dikenali |
| CV 5 | 0 dari 2 jabatan | Tidak | 2 | Judul berspasi per huruf ("W O R K  E X P E R I E N C E") dan tata letak dua kolom |

## Yang lolos

- Kelima PDF terbaca sebagai teks tanpa galat, dan tidak ada galat di konsol peramban.
- Nama dan email tersamarkan pada kelima CV; identitas tersembunyi secara bawaan di antarmuka.
- Lowongan terbaca benar untuk judul, minimal 2 tahun, jenjang S1, dan bidang arsitektur serta desain interior.
- Hitungan skor konsisten dengan rumus: bobot 35/25/25/15 diterapkan sama untuk semua kandidat.
- Catatan templat selalu terbentuk dengan susunan lengkap, dan labelnya menyebut sumbernya.
- Deteksi keterampilan eksplisit (AutoCAD, SketchUp, Revit) benar pada 14 dari 15 kasus; satu yang luput karena salah ketik di CV.

## Critical

### C-1 · Bagian CV tidak dikenali pada 4 dari 5 CV nyata

- **Gejala:** masa kerja 0 bulan untuk CV 1, 2, 4, 5; pendidikan tidak terbaca untuk CV 1, 4, 5; pada CV 1 komponen kesesuaian isi CV bernilai 0 dan tidak ada satu pun kutipan bukti.
- **Akar penyebab:** `split_sections` di `cv_parsing/extractor.py` hanya mengenali judul bagian yang berdiri sendiri pada satu baris dan persis cocok dengan daftar kata yang sempit. Lima pola nyata gagal: bentuk jamak ("Experiences"), judul dengan kata tambahan ("Education Level", "Organizational Experience"), sinonim yang tidak terdaftar ("Riwayat karier"), judul yang sebaris dengan isinya (Jobstreet), dan judul berspasi per huruf. Teks yang tidak masuk bagian mana pun jatuh ke bagian "header", yang tidak ikut dipotong menjadi kutipan, sehingga CV 1 tidak punya bahan untuk pencocokan makna.
- **Mengapa lolos dari tes:** 15 CV sintetis di `tests/fixtures` semuanya memakai judul bagian yang rapi. Tes snapshot hanya membuktikan keluaran sama dengan PoC lama, bukan bahwa keluaran itu benar untuk CV nyata.
- **Rekomendasi:** normalisasi baris sebelum dicocokkan (rapatkan huruf berspasi, buang tanda baca), izinkan bentuk jamak dan kata tambahan, tambah sinonim, kenali judul di awal baris yang diikuti isi, dan bila bagian pengalaman tidak ditemukan, cari rentang tanggal di seluruh dokumen. Tambahkan lima fixture sintetis yang meniru kelima tata letak ini.

### C-2 · Dokumen yang gagal dibaca dinilai nol dan dapat ditolak otomatis

- **Gejala:** CV 4, kandidat yang pada uji kontrol menjadi peringkat 1 dengan skor 81,1, mendapat **Tidak lolos** (36,3) dengan alasan "Bidang pendidikan tidak sesuai" dan "0,0 tahun pengalaman", padahal kedua bagian itu hanya tidak terbaca.
- **Akar penyebab:** pengaman "kualitas pembacaan meragukan, tidak ditolak otomatis" di `explanation.py` bergantung pada angka keyakinan. Rumusnya (`0,4 + 0,15 ×` jumlah bagian yang terisi) memberi 0,70 kepada CV 4 karena keterampilannya terdeteksi, sehingga pengaman tidak aktif walaupun ada dua peringatan. Selain itu, "pendidikan tidak terbaca" diperlakukan sama dengan "bidang pendidikan tidak sesuai".
- **Rekomendasi:** bila ada peringatan bagian pengalaman atau pendidikan tidak terbaca, hasil tidak boleh "Tidak lolos"; jadikan "Perlu ditinjau" dengan alasan "dokumen tidak terbaca lengkap". Bedakan "tidak terbaca" dari "tidak sesuai" pada alasan dan syarat wajib.

### C-3 · Peringkat untuk data perusahaan tidak dapat dipertanggungjawabkan

- **Gejala:** kandidat terlemah kedua menjadi peringkat 1, dua kandidat terkuat menjadi peringkat 3 dan 5.
- **Akar penyebab:** akibat langsung C-1 dan C-2. Satu-satunya CV yang bagian pengalamannya terbaca otomatis unggul 15,5 poin.
- **Rekomendasi:** setelah C-1, C-2, H-1, dan H-2 diperbaiki, ulangi tabel "Ringkasan hasil" sebagai uji penerimaan. Kriteria lolos: CV 1 dan CV 4 di dua teratas, CV 5 terbawah, dan tidak ada peringatan "tidak ditemukan" pada kelima CV.

## High

### H-1 · Jabatan dan perusahaan diambil dari baris yang salah, sehingga relevansi pengalaman keliru

- **Gejala (uji kontrol):** pada CV 1, keenam jabatan terbaca dengan judul "1 tahun", "9 bulan", "5 tahun 8 bulan", dan seterusnya; jabatan sebagai arsitek interior selama 67 bulan dinilai "tidak dihitung", dan pengalaman relevan hanya 0,5 tahun. Pada CV 3 dan CV 4, nama perusahaan masuk ke kolom jabatan.
- **Akar penyebab:** `parse_experiences` mengambil judul dari sisa teks pada baris tanggal. Pada format Jobstreet, jabatan ada di baris sebelum tanggal dan sisa baris tanggal adalah durasi dalam kurung. Jabatan pertama juga hilang karena baris sebelum tanggal hanya diambil bila sisa baris kosong. Relevansi (`relevant_months`) lalu hanya melihat istilah taksonomi pada judul dan deskripsi, dan judul yang benar sudah hilang.
- **Rekomendasi:** abaikan sisa baris berupa durasi dalam kurung dan ambil baris sebelumnya sebagai judul; kenali pola "Perusahaan, Jabatan" dan "Perusahaan - Kota"; tambahkan istilah jabatan ke taksonomi (interior architect, drafter, architectural designer).

### H-2 · Subjudul "PROJECT :" di dalam pengalaman kerja memutus bagian pengalaman

- **Gejala (uji kontrol):** CV 5 hanya terbaca satu dari dua jabatan; jabatan sebagai arsitek junior hilang.
- **Akar penyebab:** kata "project" terdaftar sebagai judul bagian "lainnya", sehingga baris "PROJECT :" menutup bagian pengalaman.
- **Rekomendasi:** jangan perlakukan "project" sebagai judul bagian bila bagian yang sedang aktif adalah pengalaman.

### H-3 · Keterampilan "tersirat" memberi nilai untuk Revit pada CV yang tidak menyebut Revit

- **Gejala:** CV 2 dan CV 5 mendapat "Revit / BIM (tersirat)" dan setengah nilai, padahal keduanya tidak menulis Revit. Catatan templat lalu menulis "Menguasai … Revit / BIM".
- **Akar penyebab:** kecocokan tersirat diberikan bila kalimat lowongan yang memuat keterampilan itu mirip dengan sebuah kalimat CV. Kalimat lowongan "AutoCAD, Sketchup, Revit" mirip dengan kalimat CV yang menyebut AutoCAD dan SketchUp, sehingga Revit ikut dianggap tersirat.
- **Rekomendasi:** jangan beri kecocokan tersirat untuk keterampilan berupa nama perangkat lunak; perangkat lunak hanya dihitung bila tertulis. Ini mengubah skor, jadi butuh persetujuan.

### H-4 · Pendidikan yang masih berjalan dihitung sebagai gelar, dan baris lain terbaca sebagai pendidikan

- **Gejala:** CV 3 mendapat nilai pendidikan penuh (15 dari 15) dari "Bachelor of Architecture 2021 - Present", padahal pendidikan yang sudah selesai adalah SMK. Baris mata kuliah terbaca sebagai bidang "management"; pada CV 2, kalimat tentang kepanitiaan terbaca sebagai entri pendidikan.
- **Akar penyebab:** `parse_education` menilai tiap baris yang memuat kata jenjang atau bidang tanpa melihat tanggal maupun konteks.
- **Rekomendasi:** tandai entri dengan "Present", "Expected", atau "sekarang" sebagai sedang ditempuh dan jangan hitung sebagai gelar yang dimiliki; abaikan baris tanpa kata jenjang kecuali melengkapi entri sebelumnya. Ini mengubah skor CV 3, jadi butuh persetujuan.

### H-5 · Penyamaran data pribadi bocor pada data nyata

- **Gejala:** nomor telepon tidak tersamarkan pada 3 dari 5 CV (format `+62 8…`, `+62-8…`); kalimat tempat dan tanggal lahir pada CV 5 tetap ada; alamat dan kode pos tetap ada pada CV 2 dan CV 3; nama kampus hanya tersamarkan sebagian (kata sebelum "University" tetap tampil). Penyamaran kampus juga menghapus sisa baris, sehingga tanggal dan bidang studi ikut hilang (CV 4, CV 5).
- **Dampak:** teks ini menjadi sumber kutipan bukti yang tampil di antarmuka dan dikirim ke Gemini, sedangkan antarmuka menyatakan "data pribadi kandidat tidak dikirim". Tanggal lahir adalah penanda usia.
- **Akar penyebab:** pola telepon di `cv_parsing/pii.py` tidak mengizinkan spasi atau tanda hubung setelah kode negara; tidak ada pola untuk tanggal lahir di dalam kalimat; pola institusi hanya mencakup teks setelah kata kuncinya.
- **Rekomendasi:** perluas pola telepon; samarkan kalimat yang memuat "born", "lahir", atau tanggal lahir; samarkan nama kampus termasuk kata di depannya tanpa menghapus sisa baris; samarkan baris kontak di kepala CV seluruhnya.

### H-6 · Catatan templat menyampaikan kegagalan baca sebagai fakta tentang kandidat

- **Gejala:** "memiliki sekitar 0,0 tahun pengalaman relevan" untuk kandidat berpengalaman bertahun-tahun; "Bidang pendidikan berbeda dari yang diminta (tidak terbaca)"; "Menguasai …" untuk keterampilan yang hanya tersirat; CV 4 tidak mendapat peringatan "struktur CV sulit dibaca" walaupun dua bagiannya tidak terbaca.
- **Akar penyebab:** `template_note` di `hr_summary.py` tidak memeriksa peringatan parser sebelum menulis kalimat pengalaman dan pendidikan, dan aturan risikonya memakai angka keyakinan yang sama dengan C-2.
- **Rekomendasi:** bila bagian tidak terbaca, tulis "belum dapat dinilai dari CV ini" dan jadikan pemeriksaan manual sebagai butir pertama; pisahkan keterampilan tertulis dari yang tersirat; ganti "Menguasai" dengan "Tertulis di CV".

### H-7 · Pengaman "CV diunggah sebagai lowongan" tidak menghentikan kasus yang memicunya

- **Gejala:** CV 1 diunggah sebagai lowongan dan **diterima** (201). CV 4 ditolak dengan benar (422). CV 1 adalah berkas yang kemarin salah terunggah sebagai lowongan.
- **Akar penyebab:** `_looks_like_cv` menganggap dokumen sebagai lowongan bila ada baris pendek yang memuat kata seperti "requirements". CV 1 punya baris isi yang berakhir dengan kata itu. Tes Sprint 4 hanya memakai CV sintetis.
- **Rekomendasi:** judul bagian lowongan harus berada di awal baris; tambahkan syarat kedua, yaitu dokumen dengan beberapa rentang tanggal pekerjaan diperlakukan sebagai CV.

## Medium

| ID | Temuan | Akar penyebab | Rekomendasi |
| --- | --- | --- | --- |
| M-1 | Jabatan "sampai sekarang" dihitung sampai hari ini (November 2026). CV 1 menulis "1 tahun" untuk jabatan terakhirnya, aplikasi menghitung 38 bulan; semua jabatan aktif bertambah sekitar 2 tahun | Tanggal acuan bawaan adalah hari ini, sedangkan CV dibuat sekitar 2024 | Isi `REFERENCE_DATE` untuk demo dan sebutkan di antarmuka "dihitung per tanggal …" |
| M-2 | Keterampilan keliru: "Java" dari nama provinsi menjadi pemrograman; "accurate" menjadi akuntansi; Photoshop dihitung sebagai Creative Visualization. Yang luput: "Skechup" (salah ketik), "technical drawings" (jamak) | Alias taksonomi terlalu longgar di satu sisi dan terlalu ketat di sisi lain | Rapikan alias: hapus yang ambigu, tambah bentuk jamak dan salah ketik umum |
| M-3 | Lowongan: "or a related field" diabaikan; "such as AutoCAD, Sketchup, Revit" menjadi tiga syarat wajib terpisah; "Design & Build" menjadi keterampilan wajib yang tidak ditemukan pada 4 dari 5 CV; satu kalimat tanggung jawab terbelah karena ganti baris; "Available join ASAP" ikut dicocokkan | Aturan `jd_parsing` membaca tiap frasa secara harfiah | Tampilkan kriteria untuk dikonfirmasi HR; pertimbangkan "such as" sebagai kelompok alternatif; gabungkan baris bersambung. Mengubah skor, butuh persetujuan |
| M-4 | Pada 3 dari 5 kandidat, jumlah lima baris di panel skor berselisih 0,1 dari skor akhir (36,2 terhadap 36,3) | Tiap baris dibulatkan sendiri di `match_breakdown.py` | Bulatkan dengan cara yang menjaga jumlah, atau tampilkan catatan pembulatan |
| M-5 | Kandidat yang sama tidak dapat diunggah ulang, diganti, atau dihapus. Setelah parser diperbaiki, hasil lama tetap dipakai | Deduplikasi berdasarkan identitas, tanpa jalur ganti | Untuk demo: hapus `backend/storage/state.json` sebelum mengunggah ulang, dan catat di panduan demo |
| M-6 | Antarmuka menampilkan dokumen yang gagal dibaca sebagai kekurangan kandidat: silang merah "0,0 tahun", "Bidang pendidikan tidak sesuai", sedangkan peringatan baca hanya ada di kolom samping. Daftar peringkat tidak menampilkan peringatan sama sekali | Tampilan tidak membedakan "tidak terbaca" dari "tidak memenuhi" | Tampilkan peringatan di bagian atas halaman kandidat dan sebagai penanda pada baris peringkat |
| M-7 | Tata letak dua kolom (CV 5): baris pendidikan dan keterampilan terbaca berselang-seling | `pdfplumber` membaca per baris melintasi kolom | Deteksi kolom saat ekstraksi, atau terima sebagai batasan yang diketahui dan arahkan ke tinjauan manual |

## Low

| ID | Temuan | Rekomendasi |
| --- | --- | --- |
| L-1 | Angka dari pipeline memakai titik desimal ("0.0 tahun") di samping teks baru yang memakai koma | Format saat ditampilkan |
| L-2 | Keterangan baris peringkat terpotong dan sama untuk semua kandidat ("Pengalaman di bawah syarat …") | Persingkat dan pilih alasan pembeda |
| L-3 | Judul "Kalimat CV yang paling mendukung tiap syarat" tampil tanpa isi bila tidak ada bukti | Sembunyikan atau beri keterangan kosong |
| L-4 | Catatan templat: nama bidang berbahasa Inggris ("architecture dan management") dan frasa ganda ("posisi ini untuk posisi Junior Architect") | Pakai label Indonesia; rapikan kalimat |
| L-5 | Batas poin dibulatkan ("dari 31", "dari 4") sedangkan poin memakai satu desimal | Samakan ketelitian |
| L-6 | Status pengalaman yang belum memenuhi syarat dibacakan sebagai "Tidak ditemukan" | Ganti menjadi "Belum memenuhi" |
| L-7 | Teks kaki halaman dari situs pembuat CV masuk ke deskripsi pekerjaan (CV 1) | Buang baris kaki halaman yang berulang |

## Catatan proses

Sprint 2 dan Sprint 3 menyatakan parser "tervalidasi" berdasarkan kesamaan keluaran dengan PoC lama pada CV
sintetis. Validasi itu tidak pernah menyentuh tata letak CV nyata, dan lima CV perusahaan baru tersedia untuk
diuji langsung pada fase ini. Aturan "jangan ubah parser" selama Sprint 4 dengan demikian mempertahankan
parser yang belum pernah benar-benar diuji.

## Rekomendasi

**Jangan masuk ke Demo Preparation dulu.** Syarat "tanpa temuan kritis" tidak terpenuhi.

Usulan: **QA Phase 2 — perbaikan temuan**, tanpa fitur baru, dengan urutan berikut. Semua butir menyentuh
parser atau aturan keputusan, sehingga butuh persetujuan Product Owner dan Technical Lead.

| Urutan | Temuan | Mengubah skor? | Perkiraan |
| --- | --- | --- | --- |
| 1 | C-1, H-2: pengenalan bagian | Ya, untuk CV yang sebelumnya gagal dibaca | 2–3 jam termasuk fixture |
| 2 | H-1: judul jabatan dan relevansi | Ya | 2 jam |
| 3 | C-2, H-6, M-6: "tidak terbaca" bukan "tidak sesuai" | Hanya keputusan dan teks | 1–2 jam |
| 4 | H-5, H-7: penyamaran data pribadi dan pengaman unggah | Tidak | 1–2 jam |
| 5 | H-3, H-4: keterampilan tersirat dan pendidikan berjalan | Ya | 1–2 jam |
| 6 | Uji ulang lima CV (kriteria C-3), lalu uji E5 dan Gemini di mesin Product Owner | — | 1 jam |

Temuan Medium dan Low selain M-6 dapat ditunda atau dicatat sebagai batasan yang diketahui saat presentasi.
Tes snapshot skor akan berubah pada butir 1, 2, dan 5; perubahan itu disengaja dan perlu dicatat dalam TDR.
