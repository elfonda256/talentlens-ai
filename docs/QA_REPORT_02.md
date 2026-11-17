# QA Report 02 — Parser Hardening

**Tanggal:** 17 November 2026 · **Cabang:** `sprint-4` · **Dasar:** temuan [QA Report 01](QA_REPORT_01.md)

**Kesimpulan: tiga temuan Critical dan tujuh temuan High dari QA Phase 1 sudah tertutup pada uji TF-IDF.**
Seluruh pengalaman kerja pada lima CV perusahaan kini terbaca (15 dari 15 jabatan, sebelumnya 2), dan
peringkatnya sama dengan urutan dari penilaian manual. Yang belum diuji: peringkat dengan embedding E5 dan
catatan recruiter dari Gemini; keduanya hanya dapat dijalankan di mesin Product Owner.

Tidak ada fitur baru dan tidak ada perubahan arsitektur. Laporan ini tidak memuat nama atau kontak dari CV,
dan tidak ada berkas CV asli di repositori.

## Sebelum dan sesudah pada lima CV perusahaan

Mode TF-IDF, tanggal acuan hari ini, berkas dan lowongan yang sama dengan QA Phase 1.

| CV | Urutan wajar (manual) | Sebelum | Sesudah |
| --- | --- | --- | --- |
| CV 4 | 1–2 | 3 · 36,3 · **Tidak lolos** | **1** · 83,1 · Direkomendasikan |
| CV 1 | 1–2 | 5 · 23,6 · Perlu ditinjau | **2** · 77,2 · Direkomendasikan |
| CV 2 | 3 | 2 · 45,9 · Perlu ditinjau | **3** · 66,0 · Perlu ditinjau |
| CV 3 | 4 | 1 · 54,6 · Perlu ditinjau | **4** · 53,6 · Perlu ditinjau |
| CV 5 | 5 | 4 · 30,7 · Perlu ditinjau | **5** · 34,0 · Tidak lolos |

Kriteria penerimaan C-3 terpenuhi: CV 1 dan CV 4 di dua teratas, CV 5 terbawah, dan tidak ada peringatan
"tidak ditemukan" pada kelima CV.

| Ukuran | Sebelum | Sesudah |
| --- | --- | --- |
| Jabatan yang terbaca | 2 dari 15 | 15 dari 15 |
| CV dengan bagian pengalaman terbaca | 1 dari 5 | 5 dari 5 |
| Jabatan dan perusahaan di kolom yang benar | 0 dari 2 | 14 dari 15 (satu jabatan lepas tanpa nama perusahaan) |
| Pendidikan selesai dan yang masih ditempuh terbaca benar | 1 dari 5 | 5 dari 5 |
| Nomor telepon tersamarkan | 2 dari 5 | 5 dari 5 |
| Tanggal lahir, alamat, nama kampus pada teks yang tersimpan | Ada pada 5 CV | Tidak ditemukan pada pemeriksaan pola |
| "Revit" dianggap tersirat padahal tidak tertulis | 2 CV | 0 |
| Jumlah baris panel skor sama dengan skor akhir | 2 dari 5 | 5 dari 5 |
| CV ditolak bila diunggah sebagai lowongan | 1 dari 2 yang diuji | 5 dari 5 |

Rincian pengalaman relevan sesudah perbaikan: CV 1 6,5 tahun, CV 2 4,8 tahun, CV 3 3,5 tahun, CV 4 3,9 tahun,
CV 5 0,3 tahun. Angka ini dihitung sampai hari ini; lihat batasan nomor 1.

## Yang dikerjakan, menurut prioritas

| # | Prioritas | Hasil | Temuan yang ditutup |
| --- | --- | --- | --- |
| 1 | Pengenalan judul bagian | Judul dicocokkan tanpa memandang kapitalisasi, tanda baca, bentuk jamak, dan spasi antarhuruf; sekitar 100 frasa Indonesia dan Inggris; judul yang sebaris dengan isinya dikenali | C-1 |
| 2 | Confidence per bagian | `section_confidence` untuk pengalaman, pendidikan, keterampilan, ringkasan: 0 tidak ditemukan, 0,3 judul ada tetapi isinya tidak terbaca, 0,6–1,0 terbaca. Tampil di halaman kandidat | — |
| 3 | "Tidak terbaca" dibedakan dari "tidak memenuhi" | Komponen yang bagiannya tidak terbaca tidak dihitung, bobotnya dibagi ke komponen lain, tidak ada syarat yang dilaporkan gagal, hasilnya selalu "Perlu ditinjau" dengan skor berlabel sementara | C-2, H-6, M-6 |
| 4 | Ekstraksi pengalaman kerja | Jabatan dan perusahaan dibaca dari baris yang benar; durasi dalam kurung diabaikan; "PROJECT :" tidak memutus bagian; ejaan jamak ("technical drawings") dikenali | H-1, H-2, sebagian M-2 |
| 5 | Tidak mengarang keterampilan | Perangkat lunak hanya dihitung bila tertulis; catatan recruiter memisahkan yang tertulis dari yang terindikasi; kata "Menguasai" dihapus; prompt Gemini diberi larangan yang sama | H-3, H-6 |
| 6 | Penyamaran data pribadi | Telepon berbagai format, tanggal lahir dalam kalimat, baris kontak beserta alamatnya, dan nama kampus utuh; kutipan disamarkan sekali lagi sebelum dikirim ke Gemini | H-5 |
| 7 | Algoritma dipertahankan | Rumus, bobot, embedding, FAISS, dan alur tidak berubah untuk CV yang terbaca. Dua aturan berubah atas permintaan fase ini; lihat di bawah | — |
| 8 | Tes regresi | 60 tes baru dan lima fixture berisi karangan yang meniru lima tata letak nyata. Total 149 tes lolos | — |
| 9 | QA ulang | Tabel di atas | C-3 |

Ikut diperbaiki karena murah dan terkait: pendidikan yang masih ditempuh tidak lagi dihitung sebagai gelar
(H-4), pengaman unggah lowongan (H-7), selisih pembulatan panel skor (M-4), dan teks catatan (L-4, L-5, L-6).

## Perubahan pada penilaian

Permintaan fase ini meminta algoritma dipertahankan, tetapi juga meminta dua hal yang tidak mungkin
dipenuhi tanpa menyentuh aturan. Keduanya saya batasi sesempit mungkin dan saya catat sebagai keputusan.

| Perubahan | Kapan berlaku | Dampak pada 13 CV sintetis | Catatan |
| --- | --- | --- | --- |
| Komponen yang bagiannya tidak terbaca tidak dihitung | Hanya bila parser tidak menemukan entri pengalaman atau pendidikan | Tidak ada | [TDR-0023](tdr/0023-unread-section-is-unknown.md) |
| Perangkat lunak tidak pernah "tersirat" | Selalu | Tidak ada | [TDR-0024](tdr/0024-software-skills-are-never-implied.md) |
| Pendidikan yang masih ditempuh bukan gelar | Selalu (di parser) | Tidak ada | [TDR-0025](tdr/0025-parser-hardening-from-real-layouts.md) |
| Ejaan baru di taksonomi | Selalu | Satu skor bergeser 0,1 poin (6,5 menjadi 6,4); peringkat dan keputusan tetap | Dicatat di tes snapshot |

Profil hasil parser untuk 13 CV sintetis lama identik dengan sebelumnya, termasuk teks yang disamarkan.

## Status seluruh temuan QA Phase 1

| ID | Temuan | Status |
| --- | --- | --- |
| C-1 | Bagian CV tidak dikenali | Tertutup |
| C-2 | Dokumen gagal baca dinilai nol dan dapat ditolak | Tertutup |
| C-3 | Peringkat tidak dapat dipertanggungjawabkan | Tertutup pada TF-IDF; E5 belum diuji |
| H-1 | Jabatan dan perusahaan dari baris yang salah | Tertutup |
| H-2 | "PROJECT :" memutus bagian pengalaman | Tertutup |
| H-3 | Revit dianggap tersirat | Tertutup |
| H-4 | Pendidikan berjalan dihitung sebagai gelar | Tertutup |
| H-5 | Penyamaran data pribadi bocor | Tertutup untuk pola yang ditemukan; batasan nomor 4 |
| H-6 | Catatan templat menyampaikan gagal baca sebagai fakta | Tertutup |
| H-7 | CV diterima sebagai lowongan | Tertutup |
| M-1 | "Sampai sekarang" dihitung sampai hari ini | **Terbuka** |
| M-2 | Keterampilan keliru atau luput | Sebagian: jamak, salah ketik, dan "accurate" diperbaiki; "Java" dari nama provinsi masih terbaca sebagai pemrograman |
| M-3 | Pembacaan lowongan terlalu harfiah | **Terbuka** |
| M-4 | Selisih 0,1 pada panel skor | Tertutup |
| M-5 | Kandidat tidak dapat diunggah ulang atau dihapus | **Terbuka** |
| M-6 | Antarmuka menampilkan gagal baca sebagai kekurangan | Tertutup |
| M-7 | Tata letak dua kolom | **Terbuka** |
| L-1, L-2, L-3, L-7 | Titik desimal, keterangan terpotong, judul kosong, teks kaki halaman | **Terbuka** |
| L-4, L-5, L-6 | Teks catatan, ketelitian poin, status pengalaman | Tertutup |

## Batasan yang masih ada

1. **Masa kerja dihitung sampai hari ini (M-1).** CV perusahaan dibuat sekitar 2024, sehingga jabatan yang "sampai sekarang" bertambah sekitar dua tahun. Urutan peringkat tidak berubah karenanya pada data ini, tetapi angka tahunnya lebih besar dari yang tertulis di CV. `REFERENCE_DATE` di `.env` dapat diisi untuk demo.
2. **Pembacaan lowongan (M-3) tidak disentuh.** "Design & Build" tetap menjadi keterampilan wajib yang tidak tertulis pada kelima CV, dan AutoCAD, SketchUp, Revit tetap tiga syarat terpisah.
3. **Tata letak dua kolom (M-7).** Pada CV 5, baris keterampilan dan pendidikan terbaca berselang-seling. Hasil akhirnya benar pada CV ini, tetapi bagian keterampilannya hanya terbaca 70%.
4. **Penyamaran data pribadi tidak menyeluruh.** Nama sekolah menengah, alamat di tengah paragraf, serta jenis kelamin atau agama yang ditulis di dalam kalimat tidak disamarkan. Yang berlabel ("Agama: …") tetap disamarkan seperti sebelumnya.
5. **CV tanpa judul bagian sama sekali** tidak diurai; hasilnya "Perlu ditinjau" dengan skor sementara.
6. **Jumlah "keterampilan wajib" di daftar peringkat menghitung yang tersirat**, sedangkan catatan recruiter hanya menghitung yang tertulis (7 dan 6 pada CV 1).
7. **Heuristik jabatan:** baris pendek tepat di bawah tanggal dianggap jabatan atau perusahaan. Butir uraian yang sangat pendek dapat terbaca keliru.

## Belum diuji

- **Embedding E5.** Semua angka di laporan ini memakai TF-IDF. E5 mengubah komponen kesesuaian isi CV (25%) dan keterampilan tersirat.
- **Catatan recruiter dari Gemini.** Prompt mendapat tiga aturan baru dan dua kunci fakta berganti nama; hanya diuji dengan tiruan.
- **OCR, tablet, navigasi keyboard, pembaca layar, Docker:** tidak berubah sejak laporan sebelumnya.

## Verifikasi

| Pemeriksaan | Hasil |
| --- | --- |
| `pytest` | 149 lolos (89 lama, 60 baru) |
| `ruff check`, `ruff format --check` | Lolos |
| `npm run lint`, `npm run build` | Lolos |
| Lima CV perusahaan lewat API dan peramban | Lolos, tanpa galat konsol |
| Keadaan "CV tidak terbaca" di peramban | Lolos, diuji dengan CV karangan tanpa judul bagian |

## Rekomendasi

Proyek dapat masuk ke **Demo Preparation** setelah satu langkah verifikasi di mesin Product Owner:

1. `git pull` cabang `sprint-4`, lalu `npm install` di `frontend`.
2. Hapus `backend/storage/state.json` (hasil lama tidak diurai ulang otomatis).
3. Unggah Vacancy dan lima CV, jalankan screening dengan E5.
4. Bandingkan urutannya dengan tabel "Sebelum dan sesudah". Urutan yang sama berarti C-3 tertutup penuh.
5. Buat catatan recruiter untuk satu kandidat dan periksa labelnya "Ditulis oleh Gemini" serta tidak ada keterampilan yang tidak tertulis di CV.

Untuk Demo Preparation saya sarankan dua keputusan kecil: isi `REFERENCE_DATE` atau jelaskan batasan nomor 1
saat presentasi, dan tentukan apakah M-3 (pembacaan lowongan) perlu dirapikan atau cukup disebut sebagai
batasan.
