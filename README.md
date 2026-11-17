# TalentLens AI

AI Recruitment Copilot: Proof of Concept yang menyaring dan memeringkat CV terhadap sebuah
lowongan, lengkap dengan skor, alasan, bukti dari CV, dan ringkasan untuk HR.

**Status: Sprint 3 (pipeline screening lengkap), menunggu verifikasi di mesin Product Owner.**
Alur dari unggah lowongan sampai ringkasan HR berjalan dan teruji. Dua komponen yang butuh
internet, model embedding E5 dan Gemini, sudah ditulis dan diuji dengan pengganti, tetapi belum
pernah dijalankan terhadap layanan aslinya. Lihat [Yang sudah diverifikasi dan yang belum](#yang-sudah-diverifikasi-dan-yang-belum).

## Alur

```
Lowongan (PDF/DOCX/TXT) ─> parser lowongan ─> kriteria
CV (PDF/DOCX/TXT/scan)  ─> parser CV ─> Candidate JSON (data pribadi dipisahkan)
        │
        └─> embedding ─> indeks FAISS ─> kemiripan semantik ─> skor berbobot ─> peringkat
                                                                    │
                                              ringkasan HR (Gemini) ┘  hanya menjelaskan, tidak menilai
```

Skor dihitung secara deterministik dari empat komponen: keterampilan (35%), pengalaman relevan (25%),
kesesuaian semantik (25%), dan pendidikan (15%). Rinciannya ada di [docs/SCREENING.md](docs/SCREENING.md).

## Mulai cepat

```bash
# Terminal 1: backend
cd backend
python -m venv .venv && source .venv/bin/activate     # Windows: .venv\Scripts\activate
pip install -r requirements-dev.txt
pip install -r requirements-e5.txt                    # opsional: model embedding E5 (+2 GB)
uvicorn app.main:app --reload

# Terminal 2: frontend
cd frontend
npm install
npm run dev
```

Buka http://localhost:3000, lalu:

1. Unggah deskripsi lowongan.
2. Unggah CV (boleh beberapa berkas sekaligus).
3. Klik **Jalankan screening**.
4. Buka seorang kandidat untuk melihat rincian skor, bukti, dan **Ringkasan AI**.

Dengan Docker: `docker compose up --build` (tambahkan `INSTALL_E5=true` di `.env` untuk menyertakan E5).

| Apa | Alamat |
| --- | --- |
| Antarmuka | http://localhost:3000 |
| Swagger UI | http://localhost:8000/docs |
| Health check | http://localhost:8000/api/v1/health |

## Mengaktifkan komponen AI

| Komponen | Cara mengaktifkan | Tanpa itu |
| --- | --- | --- |
| Embedding `multilingual-e5-small` | `pip install -r requirements-e5.txt`; unduhan model sekitar 470 MB saat pertama dipakai | Otomatis memakai TF-IDF (lemah untuk CV Indonesia terhadap lowongan Inggris) |
| Ringkasan HR oleh Gemini | Isi `GEMINI_API_KEY` di `backend/.env` (kunci dari Google AI Studio) | Ringkasan memakai templat deterministik, diberi label "Templat" |
| OCR untuk CV hasil scan | Pasang Tesseract (`brew install tesseract tesseract-lang` atau `apt install tesseract-ocr tesseract-ocr-ind`) | CV hasil scan ditolak dengan pesan galat |

Periksa keduanya sebelum demo:

```bash
cd backend && python scripts/check_ai_backends.py
```

Skrip ini memuat model E5, membandingkan satu syarat berbahasa Inggris dengan baris CV berbahasa
Indonesia, dan memanggil Gemini satu kali. Antarmuka selalu menampilkan backend embedding yang
benar-benar dipakai dan sumber setiap ringkasan.

## Data demo dan data pribadi

- Repositori ini publik. **Jangan pernah meng-commit CV asli atau dokumen perusahaan.**
- CV diunggah lewat antarmuka. Berkasnya tidak disimpan; yang disimpan hanya hasil parsing di
  `backend/storage/state.json`, yang sudah masuk `.gitignore`.
- CV di `backend/tests/fixtures/` seluruhnya sintetis (nama dan data fiktif) dan hanya dipakai oleh tes.
- Di peringkat, kandidat tampil sebagai ID. Nama baru terlihat bila "Tampilkan identitas kandidat" dicentang.
- Ke Gemini hanya dikirim fakta hasil hitung (skor, keterampilan, alasan, kutipan CV yang sudah disamarkan). Nama, kontak, dan atribut pribadi tidak dikirim.

## Struktur

```
talentlens-ai/
├── backend/
│   ├── app/
│   │   ├── main.py             perakitan aplikasi
│   │   ├── core/               config.py, logging.py
│   │   ├── api/v1/             health.py, cvs.py, jobs.py, uploads.py, router.py
│   │   ├── schemas/            cv.py, screening.py, health.py
│   │   └── services/
│   │       ├── cv_parsing/     baca dokumen, redaksi data pribadi, ekstraksi
│   │       ├── jd_parsing.py   lowongan menjadi kriteria
│   │       ├── taxonomy.py     normalisasi keterampilan
│   │       ├── embedding.py    E5 dan TF-IDF di balik satu antarmuka
│   │       ├── vector_index.py indeks FAISS
│   │       ├── matching.py     kemiripan semantik dan skor berbobot
│   │       ├── explanation.py  aturan keputusan dan alasan
│   │       ├── hr_summary.py   ringkasan HR lewat Gemini
│   │       ├── store.py        penyimpanan JSON
│   │       └── screening.py    orkestrasi pipeline
│   ├── data/taxonomy/          keterampilan dan glosarium Indonesia-Inggris
│   ├── scripts/                check_ai_backends.py
│   └── tests/                  71 tes + fixtures sintetis
├── frontend/src/
│   ├── app/                    /, /jobs/[jobId], /jobs/[jobId]/candidates/[candidateId]
│   ├── components/             komponen fitur; ui/ berisi komponen dasar
│   ├── hooks/                  use-api.ts
│   └── lib/                    api.ts, labels.ts, utils.ts
├── docs/                       arsitektur, panduan, TDR, laporan sprint
└── docker-compose.yml
```

## Environment variables

Semua punya nilai default. Untuk menjalankan tanpa Docker, letakkan di `backend/.env`
(dan `NEXT_PUBLIC_API_URL` di `frontend/.env.local`); untuk Docker Compose, di `.env` pada akar proyek.

| Variabel | Default | Fungsi |
| --- | --- | --- |
| `EMBEDDING_BACKEND` | `auto` | `auto` = E5 bila bisa dimuat, selain itu TF-IDF; `e5` = wajib E5; `tfidf` = selalu TF-IDF |
| `GEMINI_API_KEY` | kosong | Kunci Google AI Studio untuk ringkasan HR |
| `GEMINI_MODEL` | `gemini-3.6-flash` | Nama model Gemini; ganti bila tidak tersedia untuk kunci Anda |
| `SHORTLIST_THRESHOLD` | `70` | Skor minimal untuk "Lolos" |
| `REJECT_THRESHOLD` | `45` | Skor di bawah ini "Tidak lolos" |
| `REFERENCE_DATE` | kosong | Tanggal acuan masa kerja "sampai sekarang"; kosong berarti hari ini |
| `MAX_UPLOAD_MB` | `5` | Batas ukuran unggahan |
| `CORS_ORIGINS` | `http://localhost:3000` | Asal frontend yang diizinkan |
| `APP_ENV`, `LOG_LEVEL` | `development`, `INFO` | Lingkungan dan tingkat log |
| `NEXT_PUBLIC_API_URL` | `http://localhost:8000` | Alamat backend dilihat dari peramban (ditanam saat build) |

## Tes dan pemeriksaan kode

```bash
cd backend && pytest -q && ruff check . && ruff format --check .
cd frontend && npm run lint && npm run build
```

## Yang sudah diverifikasi dan yang belum

| Pemeriksaan | Hasil |
| --- | --- |
| `pytest` (71 tes), `ruff`, `npm run lint`, `npm run build` | Lolos |
| Keluaran parser CV sama dengan PoC lama pada 14 CV sintetis | Lolos |
| Kriteria lowongan, skor, peringkat, dan alasan sama dengan PoC lama (13 kandidat, mode TF-IDF) | Lolos |
| Alur lengkap di peramban: unggah lowongan, unggah CV termasuk hasil scan dan duplikat, screening, peringkat, rincian, ringkasan | Lolos, dengan TF-IDF dan ringkasan templat |
| Indeks FAISS dan pencarian per kandidat | Lolos |
| **5 CV dari perusahaan** | **Belum**: berkasnya belum tersedia di lingkungan pembuatan |
| **Embedding `multilingual-e5-small` dengan model asli** | **Belum**: model tidak dapat diunduh di lingkungan pembuatan. Pembungkusnya diuji dengan model pengganti; rentang kalibrasinya masih nilai awal |
| **Ringkasan oleh Gemini dengan API asli** | **Belum**: tidak ada kunci dan API tidak terjangkau dari lingkungan pembuatan. Diuji dengan server tiruan |
| `docker compose up --build` | **Belum**: lingkungan pembuatan tidak punya Docker daemon; hanya sintaksnya tervalidasi |

## Dokumen lain

- [Arsitektur](docs/ARCHITECTURE.md)
- [Pipeline screening dan cara skor dihitung](docs/SCREENING.md)
- [Parser CV](docs/CV_PARSER.md)
- [Panduan pengembangan](docs/DEVELOPMENT.md) dan [konvensi](docs/CONVENTIONS.md)
- [Governance](docs/GOVERNANCE.md)
- [Technical Decision Records](docs/tdr/README.md)
- Laporan sprint: [01](docs/SPRINT_REPORT_01.md), [02](docs/SPRINT_REPORT_02.md), [03](docs/SPRINT_REPORT_03.md)
