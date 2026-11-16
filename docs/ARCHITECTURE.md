# Arsitektur

## Gambaran

```
Peramban ──HTTP──> Frontend (Next.js, :3000)
    │
    └────JSON────> Backend (FastAPI, :8000) ──> pipeline AI (Sprint 2 dan seterusnya)
```

Dua layanan, tanpa basis data, tanpa antrean. Peramban memanggil backend secara langsung;
Next.js hanya menyajikan antarmuka. Ini pilihan paling sederhana yang masih memisahkan
antarmuka dari logika, sehingga keduanya bisa dijelaskan dan diuji sendiri-sendiri.

## Backend

| Lapisan | Lokasi | Tanggung jawab | Boleh mengimpor |
| --- | --- | --- | --- |
| Perakitan | `app/main.py` | Membuat aplikasi, memasang middleware dan router | semua lapisan |
| API | `app/api/v1/` | Menerima request, memvalidasi, memanggil service, mengembalikan response | `schemas`, `core`, `services` |
| Service | `app/services/` | Logika bisnis sebagai fungsi biasa, tanpa pengetahuan tentang HTTP | `schemas`, `core` |
| Skema | `app/schemas/` | Bentuk data request dan response | tidak ada |
| Inti | `app/core/` | Pengaturan dan logging | tidak ada |

Aturan arah: endpoint tidak berisi logika bisnis, dan `core` serta `schemas` tidak mengimpor apa pun dari lapisan lain.

**Alur satu request:** middleware `log_requests` memberi request ID dan mencatat waktu,
CORS memeriksa asal, router v1 meneruskan ke endpoint, endpoint mengembalikan model Pydantic,
FastAPI mengubahnya menjadi JSON. Satu baris log ditulis per request.

**Pengaturan** dibaca sekali dari environment oleh `get_settings()` dan disuntikkan ke endpoint
lewat `Depends`, sehingga tes dapat menggantinya tanpa mengubah kode.

## Frontend

| Lokasi | Tanggung jawab |
| --- | --- |
| `src/app/` | Halaman dan layout (App Router) |
| `src/components/ui/` | Komponen dasar bergaya shadcn/ui; tidak tahu apa pun tentang API |
| `src/components/` | Komponen fitur yang menggabungkan komponen dasar dengan data |
| `src/lib/api.ts` | Satu-satunya tempat `fetch` ke backend dan tipe response-nya |

Warna dan radius didefinisikan sebagai variabel CSS di `globals.css`; komponen hanya memakai
nama token (`bg-primary`, `text-muted-foreground`), bukan nilai warna.

## Keputusan yang diambil di Sprint 1

Tiga keputusan pertama dicatat lengkap sebagai TDR-0001 sampai TDR-0003 di [docs/tdr/](tdr/README.md).

| Keputusan | Alasan |
| --- | --- |
| Peramban memanggil backend langsung, tanpa proxy Next.js | Satu lompatan lebih sedikit untuk dijelaskan dan di-debug; CORS cukup satu baris konfigurasi |
| Font sistem, bukan Google Fonts | Build dan demo tidak bergantung pada internet |
| Logging dengan `logging` bawaan Python | Cukup untuk PoC; tanpa dependensi tambahan |
| Request ID di header `X-Request-ID` | Satu baris log dapat dicocokkan dengan satu klik di antarmuka saat demo |
| Versi API di path (`/api/v1`) | Kontrak eksplisit; Swagger tetap rapi |
| Tidak ada folder kosong untuk fitur mendatang | Folder dibuat bersama kode pertamanya, bukan sebagai placeholder |

## Pipeline target (governance v1.1)

```
Deterministic Pipeline -> Candidate JSON -> Embedding -> FAISS Similarity
    -> Weighted Scoring -> Ranking -> Gemini Summary -> Dashboard
```

Yang sudah ada hanya dua langkah pertama (parser CV menghasilkan `CandidateProfile`).
Skor kandidat harus tetap deterministik; Gemini hanya menulis ringkasan dan penjelasan.

## Rencana penempatan fitur (belum dibuat)

Tabel ini rencana, bukan kode yang ada. Tiap baris dibuat pada sprint-nya.

| Fitur | Backend | Frontend |
| --- | --- | --- |
| Unggah dan parsing CV | **Sudah ada (Sprint 2):** `api/v1/cvs.py`, `services/cv_parsing/` | halaman kandidat (belum) |
| Unggah dan parsing lowongan | `api/v1/jobs.py`, `services/jd_parser.py` | halaman lowongan |
| Embedding dan pencocokan semantik | `services/embedder.py`, `services/matcher.py` | tidak ada |
| Peringkat, penjelasan, rekomendasi | `services/ranker.py`, `services/explainer.py` | tabel peringkat dan panel rincian |
| Ringkasan dan penjelasan oleh Gemini | `services/llm.py` | panel pada rincian kandidat |
| Dashboard | endpoint ringkasan | halaman utama |

Pembaca dokumen, redaksi data pribadi, dan ekstraktor dari PoC sebelumnya (`cv-screening-poc`)
sudah dipindahkan ke `services/cv_parsing/`; lihat [CV_PARSER.md](CV_PARSER.md). Parser lowongan,
pencocok, dan audit bias akan dipindahkan dengan cara yang sama, bukan ditulis ulang.

## Sengaja tidak dibuat

Autentikasi, otorisasi, manajemen peran, notifikasi, email, Redis, RabbitMQ, Kubernetes,
Terraform, Helm, LangGraph, microservices, deployment cloud, dan monitoring.
