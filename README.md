# TalentLens AI

Enterprise AI Recruitment Copilot: Proof of Concept untuk menyaring dan memeringkat CV
terhadap sebuah lowongan, lengkap dengan alasan untuk setiap skor.

**Status: Sprint 1 selesai (fondasi proyek).** Belum ada fitur bisnis. Yang berjalan saat ini:
API FastAPI dengan health check, frontend Next.js yang menampilkan status API, dan
konfigurasi, logging, tes, serta Docker Compose di sekelilingnya.

## Struktur

```
talentlens-ai/
├── backend/                  API (Python, FastAPI)
│   ├── app/
│   │   ├── main.py           perakitan aplikasi: middleware, CORS, router
│   │   ├── core/             config.py (pengaturan), logging.py (log + request ID)
│   │   ├── api/v1/           router.py dan satu berkas per kelompok endpoint
│   │   └── schemas/          bentuk request/response (Pydantic)
│   ├── tests/
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
| Docker + Docker Compose | opsional, untuk menjalankan dengan satu perintah |

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
| Swagger UI | http://localhost:8000/docs |
| Skema OpenAPI | http://localhost:8000/openapi.json |

Halaman frontend menampilkan lencana **Online** bila API terjangkau dan **Offline** bila tidak.

## Environment variables

Semua variabel punya nilai default, jadi aplikasi berjalan tanpa berkas `.env`.

| Variabel | Default | Dipakai oleh | Fungsi |
| --- | --- | --- | --- |
| `APP_ENV` | `development` | backend | Nama lingkungan: `development`, `test`, `production` |
| `LOG_LEVEL` | `INFO` | backend | Tingkat log |
| `CORS_ORIGINS` | `http://localhost:3000` | backend | Asal frontend yang diizinkan, dipisah koma |
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
| `pytest` (5 tes) dan `ruff` | Lolos |
| `npm run lint` dan `npm run build` | Lolos |
| Backend dan frontend dijalankan bersama; lencana Online dan Offline diuji di peramban | Lolos |
| `docker compose config` (validasi sintaks) | Lolos |
| `docker compose up --build` | **Belum dijalankan**: lingkungan pembuatan tidak punya Docker daemon |
| Komponen shadcn/ui lewat CLI | **Belum**: registry shadcn tidak terjangkau dari lingkungan pembuatan, jadi `Button`, `Badge`, dan `Card` ditulis langsung mengikuti konvensi shadcn. Coba `npx shadcn@latest add <komponen>` di mesin Anda sebelum mengandalkannya |

## Dokumen lain

- [Arsitektur](docs/ARCHITECTURE.md)
- [Panduan pengembangan](docs/DEVELOPMENT.md)
- [Konvensi commit, API, dan penamaan](docs/CONVENTIONS.md)
