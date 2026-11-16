# TalentLens AI

Enterprise AI Recruitment Copilot: Proof of Concept untuk menyaring dan memeringkat CV
terhadap sebuah lowongan, lengkap dengan alasan untuk setiap skor.

**Status: Sprint 2 selesai (integrasi parser CV).** Yang berjalan saat ini:

- Fondasi: API FastAPI dengan health check, frontend Next.js yang menampilkan status API, konfigurasi, logging, tes, Docker Compose.
- Parser CV: `POST /api/v1/cvs/parse` menerima PDF, DOCX, atau TXT dan mengembalikan profil terstruktur.
  Parser ini dipindahkan dari PoC sebelumnya tanpa mengubah logikanya. Belum ada tampilan frontend untuknya; coba lewat Swagger.

## Struktur

```
talentlens-ai/
├── backend/                  API (Python, FastAPI)
│   ├── app/
│   │   ├── main.py           perakitan aplikasi: middleware, CORS, router
│   │   ├── core/             config.py (pengaturan), logging.py (log + request ID)
│   │   ├── api/v1/           router.py dan satu berkas per kelompok endpoint
│   │   ├── schemas/          bentuk request/response (Pydantic)
│   │   └── services/         logika bisnis: cv_parsing/ dan taxonomy.py
│   ├── data/taxonomy/        daftar keterampilan dan aliasnya
│   ├── tests/                tes + fixtures/ (15 CV contoh sintetis, snapshot keluaran)
│   ├── requirements.txt      dependensi runtime
│   └── requirements-dev.txt  + pytest, httpx, ruff
├── frontend/                 antarmuka (Next.js, Tailwind, shadcn/ui)
│   └── src/
│       ├── app/              halaman dan layout
│       ├── components/       komponen fitur; ui/ berisi komponen dasar shadcn
│       └── lib/              api.ts (satu-satunya pintu ke backend), utils.ts
├── docs/                     arsitektur, panduan pengembangan, konvensi
├── docker-compose.yml
└── .env.example
```

## Prasyarat

| Kebutuhan | Versi yang dipakai saat membangun |
| --- | --- |
| Python | 3.12 atau lebih baru |
| Node.js | 22 |
| Tesseract OCR | opsional; hanya untuk CV hasil scan. Tanpa Tesseract, CV hasil scan ditolak dengan 422 |
| Docker + Docker Compose | opsional, untuk menjalankan dengan satu perintah (sudah menyertakan Tesseract) |

## Instalasi dependensi

```bash
# Backend
cd backend
python -m venv .venv && source .venv/bin/activate     # Windows: .venv\Scripts\activate
pip install -r requirements-dev.txt

# Frontend
cd ../frontend
npm install
```

Tesseract (opsional): `brew install tesseract tesseract-lang` di macOS, atau
`sudo apt install tesseract-ocr tesseract-ocr-ind` di Ubuntu/Debian.

## Menjalankan

### Tanpa Docker (dua terminal)

```bash
# Terminal 1
cd backend && source .venv/bin/activate
uvicorn app.main:app --reload

# Terminal 2
cd frontend
npm run dev
```

### Dengan Docker Compose

```bash
docker compose up --build
```

### Alamat

| Apa | Alamat |
| --- | --- |
| Frontend | http://localhost:3000 |
| Health check | http://localhost:8000/api/v1/health |
| Parse CV | `POST` http://localhost:8000/api/v1/cvs/parse |
| Swagger UI | http://localhost:8000/docs |
| Skema OpenAPI | http://localhost:8000/openapi.json |

Halaman frontend menampilkan lencana **Online** bila API terjangkau dan **Offline** bila tidak.

Mencoba parser dari terminal:

```bash
curl -F "file=@backend/tests/fixtures/cvs/cv_raka.pdf" http://localhost:8000/api/v1/cvs/parse
```

## Environment variables

Semua variabel punya nilai default, jadi aplikasi berjalan tanpa berkas `.env`.

| Variabel | Default | Dipakai oleh | Fungsi |
| --- | --- | --- | --- |
| `APP_ENV` | `development` | backend | Nama lingkungan: `development`, `test`, `production` |
| `LOG_LEVEL` | `INFO` | backend | Tingkat log |
| `CORS_ORIGINS` | `http://localhost:3000` | backend | Asal frontend yang diizinkan, dipisah koma |
| `MAX_UPLOAD_MB` | `5` | backend | Batas ukuran unggahan CV |
| `REFERENCE_DATE` | kosong | backend | Tanggal acuan untuk masa kerja "sampai sekarang"; kosong berarti hari ini |
| `NEXT_PUBLIC_API_URL` | `http://localhost:8000` | frontend | Alamat backend dilihat dari peramban |

Cara mengubah nilainya:

- **Docker Compose:** salin `.env.example` menjadi `.env` di akar proyek.
- **Backend tanpa Docker:** letakkan variabel di `backend/.env`.
- **Frontend tanpa Docker:** letakkan `NEXT_PUBLIC_API_URL` di `frontend/.env.local`.
  Nilai ini ditanam saat build, jadi jalankan ulang `npm run dev` atau `npm run build` setelah mengubahnya.

## Tes dan pemeriksaan kode

```bash
cd backend && pytest -q && ruff check . && ruff format --check .
cd frontend && npm run lint && npm run build
```

## Yang sudah diverifikasi dan yang belum

| Pemeriksaan | Hasil |
| --- | --- |
| `pytest` (42 tes) dan `ruff` | Lolos |
| Keluaran parser baru sama persis dengan parser lama pada 14 CV berbasis teks | Lolos |
| CV hasil scan lewat OCR (Tesseract 5.3.4) | Lolos |
| `POST /api/v1/cvs/parse` dicoba dengan unggahan nyata (PDF, hasil scan, format salah) | Lolos |
| `npm run lint` dan `npm run build` | Lolos |
| Backend dan frontend dijalankan bersama; lencana Online dan Offline diuji di peramban | Lolos |
| `docker compose config` (validasi sintaks) | Lolos |
| `docker compose up --build` | **Belum dijalankan**: lingkungan pembuatan tidak punya Docker daemon |
| Komponen shadcn/ui lewat CLI | **Belum**: registry shadcn tidak terjangkau dari lingkungan pembuatan, jadi `Button`, `Badge`, dan `Card` ditulis langsung mengikuti konvensi shadcn. Coba `npx shadcn@latest add <komponen>` di mesin Anda sebelum mengandalkannya |

## Dokumen lain

- [Arsitektur](docs/ARCHITECTURE.md)
- [Parser CV](docs/CV_PARSER.md)
- [Technical Decision Records](docs/tdr/README.md)
- [Panduan pengembangan](docs/DEVELOPMENT.md)
- [Konvensi commit, API, dan penamaan](docs/CONVENTIONS.md)
