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

## Ringkasan HR (Gemini)

- Dibuat atas permintaan, per kandidat, lewat tombol di halaman rincian.
- Gemini menerima fakta yang sudah dihitung: posisi, skor, rekomendasi, kontribusi, keterampilan cocok dan tidak ditemukan, alasan, dan tiga kutipan CV yang sudah disamarkan. Nama, kontak, ID kandidat, dan atribut pribadi tidak dikirim.
- Prompt melarang Gemini menghitung atau mengubah skor, peringkat, dan rekomendasi.
- Bila kunci tidak ada atau panggilan gagal, narasi deterministik dikembalikan dengan `source: "template"` dan catatan penyebabnya. Antarmuka menampilkan sumbernya.
- Ringkasan dari Gemini disimpan; menjalankan ulang screening menghapusnya karena peringkat bisa berubah.

## API

| Method | Endpoint | Fungsi |
| --- | --- | --- |
| POST | `/api/v1/jobs` | Unggah lowongan, kembalikan kriteria |
| GET | `/api/v1/jobs`, `/api/v1/jobs/{job_id}` | Daftar lowongan; kriteria satu lowongan |
| POST | `/api/v1/jobs/{job_id}/candidates` | Unggah satu atau beberapa CV; hasil dilaporkan per berkas |
| GET | `/api/v1/jobs/{job_id}/candidates` | Daftar kandidat |
| POST | `/api/v1/jobs/{job_id}/screen` | Jalankan embedding, pencocokan, skor, dan peringkat |
| GET | `/api/v1/jobs/{job_id}/ranking` | Peringkat dengan skor dan alasan |
| GET | `/api/v1/jobs/{job_id}/candidates/{candidate_id}` | Rincian skor, bukti, dan profil |
| POST | `/api/v1/jobs/{job_id}/candidates/{candidate_id}/summary` | Ringkasan HR |
| POST | `/api/v1/cvs/parse` | Parsing satu CV tanpa menyimpan |

Identitas kandidat tersembunyi secara default; tambahkan `?reveal=true` untuk menampilkannya.
Kode status: 404 lowongan atau kandidat tidak ada, 409 belum ada CV atau screening belum dijalankan,
413 berkas terlalu besar, 415 format tidak didukung, 422 dokumen tidak terbaca.

## Antarmuka

| Halaman yang diminta | Lokasi |
| --- | --- |
| Upload Job Description | `/`, kartu "Unggah deskripsi lowongan" |
| Upload CV | `/jobs/[jobId]`, kartu "Unggah CV" |
| Run Screening | `/jobs/[jobId]`, tombol "Jalankan screening" |
| Candidate Ranking | `/jobs/[jobId]`, tabel "Peringkat kandidat" |
| Candidate Detail | `/jobs/[jobId]/candidates/[candidateId]` |
| AI Summary | `/jobs/[jobId]/candidates/[candidateId]`, kartu "Ringkasan AI untuk HR" |

## Batasan

- Belum pernah dijalankan pada CV nyata; semua pengujian memakai CV sintetis dengan format yang serupa.
- Mode E5 dan panggilan Gemini belum pernah dijalankan terhadap model dan API aslinya.
- Mengunggah CV baru menghapus hasil screening lowongan itu; screening harus dijalankan lagi.
- Tidak ada keputusan HR yang tersimpan (ubah rekomendasi) dan tidak ada audit bias; keduanya ada di PoC lama dan belum dibawa.
- Satu pengguna, tanpa autentikasi; penyimpanan berupa satu berkas JSON.
