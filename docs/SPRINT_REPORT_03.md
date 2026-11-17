# Sprint Report 03 — Pipeline Screening Lengkap

**Tanggal:** 17 November 2026 · **Cabang Git:** `sprint-3` · **Status:** implementasi selesai; **Definition of Done belum terpenuhi** (3 dari 13 butir menunggu verifikasi di mesin Product Owner)

## Sprint Summary

Alur lengkap dari unggah lowongan sampai ringkasan HR sudah berjalan lewat antarmuka: parsing
lowongan, parsing CV, embedding, indeks FAISS, kemiripan semantik, skor berbobot, peringkat, rincian
kandidat, dan ringkasan. Logika penilaian dipindahkan dari PoC lama tanpa diubah dan hasilnya terbukti
sama lewat tes snapshot.

Tiga hal tidak dapat diselesaikan dari lingkungan pembuatan, karena bergantung pada sumber daya yang
tidak tersedia di sana: 5 CV perusahaan (berkasnya tidak ada), model E5 (tidak dapat diunduh), dan API
Gemini (tidak ada kunci dan host tidak terjangkau). Kode untuk E5 dan Gemini sudah ditulis dan diuji
dengan pengganti, tetapi belum pernah dijalankan terhadap aslinya.

## Definition of Done

| Butir | Status | Bukti atau penyebab |
| --- | --- | --- |
| 5 CV perusahaan dapat diproses | **Belum** | Berkas tidak tersedia. Diuji dengan 14 CV sintetis |
| Job Description dapat diproses | Selesai | Tes parser dan alur API; diuji di peramban |
| Embedding berjalan | **Sebagian** | TF-IDF berjalan. E5 belum dijalankan dengan model asli |
| FAISS berjalan | Selesai | `test_vector_index.py`; dipakai pada setiap screening |
| Similarity berjalan | Selesai | Hasil sama dengan PoC lama (snapshot) |
| Weighted Score berjalan | Selesai | Hasil sama dengan PoC lama (snapshot) |
| Candidate Ranking berjalan | Selesai | Tes API dan peramban |
| Gemini Summary berjalan | **Belum terverifikasi** | Diuji dengan server tiruan; belum pernah memanggil API asli |
| Frontend menampilkan hasil dengan benar | Selesai | Alur lengkap dijalankan di peramban |
| Build berhasil | Selesai | `npm run build` |
| Tes berhasil | Selesai | 71 tes, `ruff`, `eslint` |
| Perubahan di-commit dan di-push | Selesai | Cabang `sprint-3` |
| Sprint Report dibuat | Selesai | Dokumen ini |

## Completed Tasks

| # | Fitur | Hasil |
| --- | --- | --- |
| 1 | CV Parsing | Dipakai ulang dari Sprint 2; kini terhubung ke alur lowongan dengan unggahan banyak berkas |
| 2 | Job Description Parsing | `jd_parsing.py`, dipindahkan dari PoC lama |
| 3 | Candidate JSON | `CandidateProfile` disimpan per lowongan di penyimpanan JSON |
| 4 | Embedding | `multilingual-e5-small` sebagai default, TF-IDF sebagai cadangan otomatis |
| 5 | FAISS Vector Index | `IndexFlatIP` dengan pencarian per kandidat |
| 6 | Semantic Similarity | Bukti terbaik per kalimat lowongan |
| 7 | Weighted Scoring | Empat komponen, dipindahkan tanpa diubah |
| 8 | Candidate Ranking | Peringkat dengan tiga zona keputusan dan alasan |
| 9 | Gemini HR Summary | Hanya menjelaskan; templat sebagai cadangan |
| 10 | Frontend Integration | Tiga rute yang memuat enam tampilan yang diminta |

**Komponen di luar daftar fitur (dependensi teknis, sesuai Sprint Policy):**

- Penyimpanan JSON (`store.py`): peringkat membutuhkan daftar kandidat per lowongan. [TDR-0016](tdr/0016-json-store-no-real-cvs-in-repo.md)
- Penyembunyian identitas dengan `?reveal=true`: menutup utang teknis dari Sprint 2. [TDR-0017](tdr/0017-jobs-api-blind-by-default.md)
- `scripts/check_ai_backends.py`: memeriksa E5 dan Gemini di mesin tujuan. [TDR-0012](tdr/0012-e5-default-tfidf-fallback.md)
- `api/v1/uploads.py`: validasi unggahan yang dipakai bersama oleh endpoint CV dan lowongan.
- Field `embedding_backend` dan `llm_summary` pada health check, untuk strip status di antarmuka.

## Modified Files

- Akar: `.env.example`, `.gitignore`, `README.md`, `docker-compose.yml`
- Backend: `Dockerfile`, `pyproject.toml`, `requirements.txt`, `requirements-dev.txt`, `app/core/config.py`, `app/api/v1/{cvs,health,router}.py`, `app/schemas/health.py`, `app/services/taxonomy.py`, `tests/conftest.py`, `tests/test_health.py`
- Frontend: `src/app/{globals.css,layout.tsx,page.tsx}`, `src/components/system-status.tsx`, `src/components/ui/{badge,button}.tsx`, `src/lib/api.ts`
- Dokumentasi: `docs/ARCHITECTURE.md`, `docs/CV_PARSER.md`, `docs/tdr/README.md`

## Added Files

- Backend, aplikasi: `app/api/v1/jobs.py`, `app/api/v1/uploads.py`, `app/schemas/screening.py`, `app/services/{jd_parsing,embedding,vector_index,matching,explanation,hr_summary,store,screening}.py`
- Backend, lainnya: `requirements-e5.txt`, `scripts/check_ai_backends.py`, `data/taxonomy/id_en_glossary.json`
- Backend, tes: `tests/test_{jd_parsing,embedding,vector_index,screening_golden,hr_summary,jobs_api}.py`, `tests/fixtures/golden_screening.json`, `tests/fixtures/jobs/junior_architect.txt`
- Frontend: `src/app/jobs/[jobId]/page.tsx`, `src/app/jobs/[jobId]/candidates/[candidateId]/page.tsx`, `src/hooks/use-api.ts`, `src/lib/labels.ts`, `src/components/{page-shell,file-picker,job-criteria,cv-upload,ranking-table,recommendation-badge,score-bar,ai-summary}.tsx`
- Dokumentasi: `docs/SCREENING.md`, `docs/SPRINT_REPORT_03.md`, `docs/tdr/0012` sampai `0018`

## Deleted Files

Tidak ada.

## Known Issues

- **Mode E5 belum pernah dijalankan.** Rentang kalibrasi kemiripan (0,75 sampai 0,88) adalah nilai awal; bila tidak cocok, skor semantik semua kandidat bisa mengumpul di 0 atau 1.
- **Panggilan Gemini belum pernah dijalankan.** Nama model default (`gemini-3.6-flash`) diambil dari dokumentasi; bila tidak tersedia untuk kunci Anda, ringkasan jatuh ke templat dengan catatan galat.
- **Parser belum pernah melihat CV nyata.** Kelemahan yang diwarisi (nama dari baris pertama, CV dua kolom, tata letak tanpa judul bagian) tercatat di `docs/CV_PARSER.md`.
- Pada mode TF-IDF, kemiripan bukti sering tampil 100% karena kalibrasinya jenuh.
- Rincian kandidat menampilkan ID keterampilan (`technical_drawing`), bukan labelnya.
- Tag `sprint-1` dan `sprint-2` belum ada di GitHub: push tag ditolak (HTTP 403) dari lingkungan pembuatan.
- `docker compose up --build` tetap belum dijalankan.

## Technical Debt

- Frontend tanpa tes otomatis.
- Keputusan HR (mengubah rekomendasi) dan audit bias dari PoC lama belum dibawa.
- Bobot skor belum dapat diubah lewat antarmuka.
- Penyimpanan satu berkas JSON, tanpa penguncian antarproses.
- `generateContent` disebut Google sebagai API lama; migrasi ke Interactions API ditunda.
- `document_loader` berada di paket `cv_parsing` tetapi kini dipakai juga untuk lowongan.

## Risks

| Risiko | Dampak | Mitigasi |
| --- | --- | --- |
| CV perusahaan terbaca buruk oleh parser berbasis aturan | Skor dan peringkat demo tidak masuk akal | Uji kelima CV hari ini; perbaikan parser menjadi isi sprint berikutnya bila perlu |
| Kalibrasi E5 tidak cocok | Skor semantik tidak membedakan kandidat | Jalankan `check_ai_backends.py`; sesuaikan dua konstanta |
| Gemini gagal saat demo (kuota, model, jaringan) | Ringkasan tampil sebagai templat | Sudah ditangani otomatis; uji kunci sebelum demo |
| CV asli ter-commit ke repositori publik | Kebocoran data pribadi | `backend/storage/` di-ignore; CV hanya diunggah lewat antarmuka; jangan menyalin CV ke folder proyek |
| Sisa waktu sampai Kamis 16.30 | Perbaikan setelah uji data nyata tidak selesai | Uji data nyata lebih dulu, sebelum menambah fitur apa pun |

## Technical Decision Records

- [TDR-0012](tdr/0012-e5-default-tfidf-fallback.md): embedding E5 lokal, TF-IDF sebagai cadangan
- [TDR-0013](tdr/0013-faiss-flat-index.md): FAISS `IndexFlatIP`
- [TDR-0014](tdr/0014-reuse-scoring-pipeline.md): penilaian dipindahkan tanpa mengubah logika
- [TDR-0015](tdr/0015-gemini-explains-only.md): Gemini hanya menjelaskan
- [TDR-0016](tdr/0016-json-store-no-real-cvs-in-repo.md): penyimpanan JSON; CV asli tidak masuk repositori
- [TDR-0017](tdr/0017-jobs-api-blind-by-default.md): API berpusat pada lowongan; identitas tersembunyi
- [TDR-0018](tdr/0018-three-routes-client-fetching.md): tiga rute untuk enam tampilan

## Recommended Next Sprint

**Sprint 4: verifikasi dengan data nyata dan persiapan demo.** Tanpa fitur baru sampai tiga langkah pertama selesai.

1. Di mesin Product Owner: `pip install -r requirements-e5.txt`, isi `GEMINI_API_KEY`, jalankan `python scripts/check_ai_backends.py`.
2. Unggah lowongan dan 5 CV perusahaan lewat antarmuka; catat CV yang terbaca salah.
3. Perbaiki parser dan kalibrasi E5 berdasarkan temuan langkah 2.
4. Bila waktu tersisa: keputusan HR dan audit bias dari PoC lama, lalu skrip demo dan penyelarasan slide.

## Suggested Git Commit Message

```
feat: add end-to-end screening pipeline with faiss, weighted scoring and hr summary
```
