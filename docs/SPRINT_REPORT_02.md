# Sprint Report 02 — Integrasi Parser CV

**Tanggal:** 16 November 2026 · **Tag Git:** `sprint-2` · **Status:** selesai, menunggu review

Laporan ini ditulis setelah sprint berakhir, saat governance v1.1 mulai berlaku.

## Sprint Summary

Parser CV dari `cv-screening-poc` dipindahkan ke arsitektur baru sebagai service `parse_cv()` tanpa
mengubah logikanya. Keluaran parser baru sama persis dengan parser lama pada 14 CV berbasis teks;
CV hasil scan diperiksa lebih longgar karena hasil OCR bergantung pada versi Tesseract.

## Completed Tasks

| # | Tugas | Hasil |
| --- | --- | --- |
| 1 | Analisis parser lama | Tiga modul, sekitar 430 baris, bergantung pada konfigurasi global di tiga tempat |
| 2 | Menentukan bagian yang dipakai ulang | `document_loader`, `pii`, `extractor`, taksonomi, skema `CandidateProfile` |
| 3 | Refactor seperlunya | Jalur impor, komentar, format, `today` sebagai argumen, kelas galat |
| 4 | Logika bisnis tidak diubah | Dibuktikan oleh tes snapshot |
| 5 | Service yang bersih | `app/services/cv_parsing/` dengan satu pintu masuk |
| 6 | Keluaran konsisten | 14 dari 14 CV berbasis teks identik field demi field |
| 7 | Unit test | 37 tes baru; total 42 lolos |
| 8 | Logging | Satu baris per CV, tanpa nama berkas atau isi CV |
| 9 | Dokumentasi | `docs/CV_PARSER.md`, README, `ARCHITECTURE.md` |
| 10 | TDR | Tujuh keputusan (TDR-0004 sampai TDR-0010) |

**Komponen di luar spesifikasi:** endpoint `POST /api/v1/cvs/parse`. Ditambahkan sebagai dependensi
teknis agar service bisa dicoba dari Swagger; alasannya ada di [TDR-0009](tdr/0009-stateless-parse-endpoint.md).

## Modified Files

- `.env.example`
- `README.md`
- `docker-compose.yml`
- `backend/Dockerfile`
- `backend/pyproject.toml`
- `backend/requirements.txt`
- `backend/app/api/v1/router.py`
- `backend/app/core/config.py`
- `docs/ARCHITECTURE.md`

## Added Files

- `backend/app/api/v1/cvs.py`
- `backend/app/schemas/cv.py`
- `backend/app/services/__init__.py`
- `backend/app/services/taxonomy.py`
- `backend/app/services/cv_parsing/__init__.py`
- `backend/app/services/cv_parsing/document_loader.py`
- `backend/app/services/cv_parsing/extractor.py`
- `backend/app/services/cv_parsing/pii.py`
- `backend/app/services/cv_parsing/service.py`
- `backend/app/services/cv_parsing/text_utils.py`
- `backend/data/taxonomy/skills.json`
- `backend/tests/__init__.py`
- `backend/tests/conftest.py`
- `backend/tests/test_cv_parsing_golden.py`
- `backend/tests/test_cv_parsing_units.py`
- `backend/tests/test_cvs_api.py`
- `backend/tests/fixtures/golden_profiles.json`
- `backend/tests/fixtures/cvs/` (15 CV contoh sintetis)
- `docs/CV_PARSER.md`
- `docs/tdr/` (delapan berkas; dinomori ulang dan diseragamkan setelah sprint, lihat catatan di bawah)

## Deleted Files

Tidak ada.

**Catatan:** setelah sprint ini, berkas TDR ditulis ulang ke format governance dan dinomori ulang
secara kronologis. TDR Sprint 2 yang semula 0001-0007 kini menjadi 0004-0010.

## Known Issues

Diwarisi dari parser lama dan sengaja tidak diperbaiki:

- Nama diambil dari baris pertama yang tidak kosong; CV dengan judul lain di baris pertama salah dibaca.
- Baris berlabel `Status:` selalu dianggap status pernikahan dan dibuang.
- Tata letak tanpa judul bagian menghasilkan keyakinan ekstraksi rendah.
- CV dua kolom dapat terbaca dengan urutan baris yang tercampur.

Baru:

- Tanpa Tesseract, CV hasil scan ditolak dengan 422 dan pesannya sama dengan berkas rusak.
- `docker compose up --build` tetap belum dijalankan, termasuk pemasangan Tesseract di image.

## Technical Debt

- Response endpoint memuat `pii` secara utuh; harus disembunyikan saat tampilan peringkat dibuat.
- Pesan `warnings` dan pesan galat berbahasa Indonesia tertanam di kode (dipertahankan demi konsistensi keluaran).
- `extractor.py` dan `pii.py` dikecualikan dari aturan panjang baris.
- Glosarium ID-EN, fungsi taksonomi untuk parser lowongan, dan deduplikasi masih di repositori PoC lama.
- Belum ada tampilan frontend untuk parser.

## Risks

| Risiko | Dampak | Mitigasi |
| --- | --- | --- |
| Parser hanya diuji pada CV sintetis dengan format serupa | CV nyata saat demo bisa terbaca buruk | Uji dengan beberapa CV nyata sebelum demo; siapkan CV contoh sebagai jalur aman |
| Arsitektur governance memakai FAISS dan embedding, tetapi sumber embedding belum ditetapkan | Sprint 3 terhambat keputusan | Putuskan di spesifikasi Sprint 3 (lihat rekomendasi) |
| Penguji mengunggah CV hasil scan di mesin tanpa Tesseract | Galat 422 saat demo | Demo lewat Docker, atau pasang Tesseract |
| Sisa waktu sekitar 2,5 hari untuk parser lowongan, pencocokan, peringkat, penjelasan, dan dashboard | Lingkup tidak selesai | Pindahkan modul lama alih-alih menulis ulang; batasi frontend |

## Technical Decision Records

- [TDR-0004](tdr/0004-reuse-legacy-parser.md): memakai ulang parser lama
- [TDR-0005](tdr/0005-golden-snapshot-as-contract.md): snapshot keluaran sebagai kontrak regresi
- [TDR-0006](tdr/0006-cv-parsing-service-package.md): paket `services/cv_parsing`
- [TDR-0007](tdr/0007-explicit-configuration.md): konfigurasi eksplisit
- [TDR-0008](tdr/0008-unused-code-not-migrated.md): kode yang belum dipakai tidak dipindahkan
- [TDR-0009](tdr/0009-stateless-parse-endpoint.md): endpoint parse tanpa penyimpanan
- [TDR-0010](tdr/0010-tesseract-optional.md): Tesseract opsional

## Recommended Next Sprint

**Sprint 3: parser lowongan, pencocokan, dan peringkat (backend saja).**

Pindahkan `jd_parser`, `matcher`, dan aturan keputusan dari PoC lama dengan pola yang sama
(snapshot dulu, lalu pindahkan). Spesifikasinya perlu menjawab tiga hal:

1. **Sumber embedding.** Governance menolak unduhan model lokal, sehingga pilihannya embedding lewat Gemini API (teks CV yang sudah disamarkan dikirim ke layanan luar) atau TF-IDF dari PoC lama (offline, lemah lintas bahasa).
2. **FAISS atau NumPy.** Untuk puluhan CV, hasil keduanya sama; FAISS menambah satu dependensi native. Rekomendasi: NumPy di balik antarmuka yang sama, kecuali FAISS memang ingin ditunjukkan saat interview.
3. **Penyimpanan.** Peringkat butuh daftar kandidat per lowongan. Rekomendasi: berkas JSON seperti PoC lama.

## Suggested Git Commit Message

```
feat(backend): integrate legacy cv parser as a service
```
