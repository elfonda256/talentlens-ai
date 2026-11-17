# Pipeline Screening

Dari dokumen yang diunggah sampai daftar kandidat berperingkat. Logika penilaian berasal dari PoC
sebelumnya dan dipindahkan tanpa diubah; yang baru adalah indeks FAISS, pilihan backend embedding,
ringkasan HR, penyimpanan, API, dan antarmuka.

## Langkah

| # | Langkah | Modul | Keluaran |
| --- | --- | --- | --- |
| 1 | Parsing lowongan | `services/jd_parsing.py` | `JobProfile`: pengalaman minimal, bidang pendidikan, keterampilan wajib dan nilai tambah, kalimat syarat |
| 2 | Parsing CV | `services/cv_parsing/` | `CandidateProfile` (Candidate JSON); data pribadi terpisah di `pii` |
| 3 | Embedding | `services/embedding.py` | Satu vektor ternormalisasi per potongan teks CV dan per kalimat lowongan |
| 4 | Indeks vektor | `services/vector_index.py` | Indeks FAISS `IndexFlatIP` atas semua potongan CV |
| 5 | Kemiripan semantik | `services/matching.py` | Untuk tiap kalimat lowongan, potongan CV yang paling mirip milik kandidat itu |
| 6 | Skor berbobot | `services/matching.py` | Skor 0-100 dan kontribusi tiap komponen |
| 7 | Keputusan dan alasan | `services/explanation.py` | Lolos, Perlu ditinjau, atau Tidak lolos, dengan alasan tertulis |
| 8 | Peringkat | `services/screening.py` | Urutan menurut skor |
| 9 | Ringkasan HR | `services/hr_summary.py` | Narasi oleh Gemini, atau templat bila Gemini tidak tersedia |

## Cara skor dihitung

`skor = 100 x (0,35 x keterampilan + 0,25 x pengalaman + 0,25 x semantik + 0,15 x pendidikan)`

| Komponen | Cara menghitung |
| --- | --- |
| Keterampilan | Tiap syarat keterampilan dicari di CV. Cocok persis lewat taksonomi = nilai penuh; cocok tersirat lewat embedding (kemiripan terkalibrasi >= 0,55) = setengah. Syarat wajib berbobot 1, nilai tambah 0,5. Syarat "A / B" dihitung sebagai satu syarat alternatif |
| Pengalaman relevan | Hanya masa kerja yang isinya menyentuh keterampilan lowongan. Dibandingkan dengan pengalaman minimal; kelebihan sampai 3 tahun memberi sedikit tambahan |
| Kesesuaian semantik | Rata-rata kemiripan terbaik untuk tiap kalimat lowongan. Potongan CV yang terpilih ditampilkan sebagai bukti |
| Pendidikan | Bidang sesuai = 1,0; serumpun = 0,6; lainnya = 0,15. Jenjang di bawah syarat dikali 0,7 |

Bobot tersimpan per lowongan (`JobProfile.weights`).

## Aturan keputusan

| Kondisi | Keputusan |
| --- | --- |
| Skor >= 70 dan tidak ada syarat wajib yang dilanggar | Lolos |
| Skor >= 70 tetapi ada syarat wajib yang dilanggar | Perlu ditinjau |
| Skor 45 sampai di bawah 70 | Perlu ditinjau |
| Skor < 45, tetapi dokumen dibaca dengan OCR atau keyakinan ekstraksi < 0,7 | Perlu ditinjau |
| Skor < 45 | Tidak lolos |

Syarat wajib yang diperiksa: pengalaman relevan minimal, bidang pendidikan, dan jenjang pendidikan.
Ambang 70 dan 45 dapat diubah lewat `SHORTLIST_THRESHOLD` dan `REJECT_THRESHOLD`.

## Embedding

| Backend | Kapan dipakai | Catatan |
| --- | --- | --- |
| `multilingual-e5-small` | Default bila `sentence-transformers` terpasang dan model dapat dimuat | Berjalan lokal; teks CV tidak keluar dari mesin. Kalimat lowongan diberi awalan `query:`, potongan CV `passage:` |
| TF-IDF | Cadangan otomatis, atau `EMBEDDING_BACKEND=tfidf` | Kata dan n-gram karakter, dibantu glosarium Indonesia-Inggris kecil. Lemah bila CV dan lowongan berbeda bahasa |

Kemiripan mentah dipetakan ke rentang 0-1 oleh `calibrate()` milik tiap backend, supaya skor sebanding.
**Rentang kalibrasi E5 (0,75 sampai 0,88) adalah nilai awal yang belum divalidasi dengan data nyata.**
Jalankan `python scripts/check_ai_backends.py` untuk melihat nilainya di mesin Anda.

## Indeks FAISS

- `IndexFlatIP`: pencarian eksak dengan inner product. Karena vektor ternormalisasi, hasilnya sama dengan cosine similarity.
- Potongan CV tiap kandidat ditambahkan sebagai satu blok berurutan. Pencarian "bukti terbaik milik kandidat X" dibatasi ke blok itu dengan `IDSelectorRange`.
- Indeks dibangun ulang setiap screening dijalankan dan tidak disimpan ke disk.

## Tampilan penjelasan (tidak ikut menilai)

`services/match_breakdown.py` menyusun ulang hasil yang sudah ada menjadi bentuk yang mudah ditampilkan.
Modul ini tidak menghitung skor apa pun.

| Tampilan | Isi | Sumber |
| --- | --- | --- |
| Rincian skor | Lima baris: keterampilan wajib, keterampilan tambahan, pengalaman, pendidikan, kesesuaian isi CV; masing-masing dengan poin, batas poin, dan alasannya | `contributions` dan bobot lowongan |
| Kecocokan per syarat | Status tiap keterampilan (ditemukan, tersirat, tidak ditemukan) beserta kata yang tertulis di CV | daftar keluaran pencocok dan taksonomi |
| Relevansi tiap jabatan | Relevan, sebagian relevan, atau tidak dihitung | aturan `relevant_months` milik pencocok, ditanyakan per jabatan |
| Syarat yang belum terpenuhi | Syarat wajib yang dilanggar dan keterampilan wajib yang tidak ditemukan | `knockout_flags`, `missing_must_skills` |

Skor punya empat komponen. Komponen keterampilan ditampilkan sebagai dua baris, wajib dan tambahan,
dengan membaginya seperti pencocok menimbangnya: 1 untuk tiap keterampilan wajib dan 0,5 untuk tiap
keterampilan tambahan. Jumlah kedua baris itu sama dengan poin komponen keterampilan.

Penanda kata kunci di antarmuka memakai daftar kata dari taksonomi. Karena pencocokannya per kata,
nama perusahaan yang kebetulan memuat kata kunci juga ikut ditandai.

## Catatan recruiter (Gemini)

- Dibuat atas permintaan, per kandidat, lewat tombol di halaman rincian.
- Susunannya tetap: kesimpulan, kecocokan terhadap posisi, kekuatan, kekurangan, risiko, hal yang perlu digali saat wawancara, dan alasan rekomendasi.
- Gemini diminta membalas dalam JSON dengan susunan itu. Templat bawaan mengisi susunan yang sama dari fakta yang sama, sehingga tampilannya tidak berubah bila Gemini tidak tersedia; hanya label sumbernya yang berbeda.
- Gemini menerima fakta yang sudah dihitung: posisi, skor, rekomendasi, keterampilan ditemukan dan tidak ditemukan, pengalaman relevan, jabatan yang relevan, status pendidikan, dan tiga kutipan CV yang sudah disamarkan. Nama, kontak, ID kandidat, dan atribut pribadi tidak dikirim.
- Prompt melarang Gemini menghitung atau mengubah skor, peringkat, dan rekomendasi, dan memintanya mengabaikan instruksi di dalam kutipan CV.
- Templat dipakai bila kunci tidak ada, panggilan gagal, jawaban bukan JSON, atau ada bagian yang kosong.
- Catatan dari Gemini disimpan; menjalankan ulang screening menghapusnya karena peringkat bisa berubah.

## API

| Method | Endpoint | Fungsi |
| --- | --- | --- |
| POST | `/api/v1/jobs` | Unggah lowongan, kembalikan kriteria. Dokumen yang tampak seperti CV ditolak (422) |
| GET | `/api/v1/jobs`, `/api/v1/jobs/{job_id}` | Daftar lowongan; kriteria satu lowongan |
| POST | `/api/v1/jobs/{job_id}/candidates` | Unggah satu atau beberapa CV; hasil dilaporkan per berkas |
| GET | `/api/v1/jobs/{job_id}/candidates` | Daftar kandidat |
| POST | `/api/v1/jobs/{job_id}/screen` | Jalankan embedding, pencocokan, skor, dan peringkat |
| GET | `/api/v1/jobs/{job_id}/ranking` | Peringkat dengan skor, alasan, dan ringkasan kecocokan tiap kandidat |
| GET | `/api/v1/jobs/{job_id}/candidates/{candidate_id}` | Rincian skor, kecocokan per syarat, relevansi jabatan, bukti, dan profil |
| POST | `/api/v1/jobs/{job_id}/candidates/{candidate_id}/summary` | Catatan recruiter |
| POST | `/api/v1/cvs/parse` | Parsing satu CV tanpa menyimpan |

Identitas kandidat tersembunyi secara default; tambahkan `?reveal=true` untuk menampilkannya.
Kode status: 404 lowongan atau kandidat tidak ada, 409 belum ada CV atau screening belum dijalankan,
413 berkas terlalu besar, 415 format tidak didukung, 422 dokumen tidak terbaca.

## Antarmuka

| Rute | Isi |
| --- | --- |
| `/` | Daftar lowongan dan unggah deskripsi lowongan |
| `/jobs/[jobId]` | Kriteria penilaian, unggah CV, tombol screening, ringkasan (total, direkomendasikan, perlu ditinjau, tidak lolos) yang juga menyaring daftar, dan peringkat dengan bilah susunan skor |
| `/jobs/[jobId]/candidates/[candidateId]` | Catatan recruiter, asal skor, kecocokan per syarat, bukti dari CV dengan kata kunci ditandai, tingkat kecocokan, dan kualitas pembacaan dokumen |

Setiap bagian punya keadaan memuat (kerangka), kosong (petunjuk langkah berikutnya), dan galat (pesan yang menjelaskan penyebabnya).

## Batasan

- Belum pernah dijalankan pada CV nyata; semua pengujian memakai CV sintetis dengan format yang serupa.
- Mode E5 dan panggilan Gemini belum pernah dijalankan terhadap model dan API aslinya.
- Mengunggah CV baru menghapus hasil screening lowongan itu; screening harus dijalankan lagi.
- Tidak ada keputusan HR yang tersimpan (ubah rekomendasi) dan tidak ada audit bias; keduanya ada di PoC lama dan belum dibawa.
- Satu pengguna, tanpa autentikasi; penyimpanan berupa satu berkas JSON.
