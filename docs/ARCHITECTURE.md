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

## Pipeline screening (Sprint 3)

```
Lowongan -> jd_parsing -> JobProfile
CV       -> cv_parsing -> CandidateProfile -> embedding -> vector_index (FAISS)
                                                   -> matching (skor berbobot) -> explanation (keputusan)
                                                   -> screening (peringkat) -> hr_summary (Gemini)
```

| Modul di `app/services/` | Tanggung jawab | Bergantung pada |
| --- | --- | --- |
| `cv_parsing/` | Berkas CV menjadi `CandidateProfile` | `taxonomy` |
| `jd_parsing.py` | Teks lowongan menjadi `JobProfile` | `taxonomy`, konstanta jenjang dari `cv_parsing` |
| `embedding.py` | Teks menjadi vektor; E5 atau TF-IDF | pengaturan |
| `vector_index.py` | Indeks FAISS dan pencarian per kandidat | tidak ada |
| `matching.py` | Kemiripan semantik dan skor berbobot | `embedding`, `vector_index`, `taxonomy` |
| `explanation.py` | Aturan keputusan dan alasan tertulis | tidak ada |
| `match_breakdown.py` | Tampilan penjelasan: rincian skor, kecocokan per syarat, relevansi jabatan. Tidak ikut menilai | `matching`, `taxonomy` |
| `hr_summary.py` | Catatan recruiter lewat Gemini, dengan templat bersusunan sama | pengaturan |
| `store.py` | Penyimpanan JSON | skema |
| `screening.py` | Orkestrasi; satu-satunya modul yang dipanggil API | semua di atas |

Skor kandidat deterministik. Gemini hanya menulis ringkasan dari fakta yang sudah dihitung.
Rincian langkah, rumus skor, dan API ada di [SCREENING.md](SCREENING.md).

**Frontend.** Tiga rute: `/` (lowongan), `/jobs/[jobId]` (kriteria, unggah CV, screening, peringkat),
dan `/jobs/[jobId]/candidates/[candidateId]` (rincian dan ringkasan AI). Semua halaman adalah Client
Component yang mengambil data lewat `src/lib/api.ts` dan hook `useApi`.

**Penyimpanan.** `backend/storage/state.json` berisi lowongan, profil kandidat (termasuk data pribadi),
hasil screening, dan ringkasan. Berkas CV asli tidak disimpan. Folder ini tidak masuk Git.

## Sengaja tidak dibuat

Autentikasi, otorisasi, manajemen peran, notifikasi, email, Redis, RabbitMQ, Kubernetes,
Terraform, Helm, LangGraph, microservices, deployment cloud, dan monitoring.
