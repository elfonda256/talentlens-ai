# Deployment Report 01 — Staging (Vercel + Railway)

**Tanggal:** 17 November 2026 · **Cabang:** `sprint-4` · **Commit:** `3965831` · **Keputusan:** READY WITH MINOR FIX

## Deployment

| Hal | Frontend | Backend |
| --- | --- | --- |
| Platform | Vercel, proyek `talentlens-ai` | Railway, proyek `talentlens-ai`, environment `staging`, layanan `backend` |
| URL | https://talentlens-ai-azure.vercel.app | https://backend-staging-222b726d.up.railway.app |
| Status | READY | SUCCESS |
| Commit | `3965831` | `3965831`, dikunci (pin) ke commit ini |
| Durasi build | 15 detik | sekitar 2 menit (image dengan PyTorch CPU dan model E5) |
| Akses | Vercel Authentication untuk semua deployment | Kunci `X-API-Key`; hanya `/api/v1/health` yang terbuka |

Alamat `talentlens-ai.vercel.app`, `talentlensai.vercel.app`, dan `talentlens-ai-demo.vercel.app` sudah dipakai akun Vercel lain.

## Arsitektur staging

```
Peramban ──(Vercel Authentication)──> Next.js di Vercel
                                       └─ /api/backend/* (relay di server, menambah X-API-Key)
                                              └──> FastAPI di Railway (API_KEY wajib)
                                                     └─ volume /srv/storage (hasil screening)
```

Kunci API dan alamat backend hanya ada di server Vercel dan Railway. Lihat [TDR-0026](tdr/0026-server-side-relay-and-shared-key.md).

## Verifikasi

Uji otomatis dijalankan dari Vercel Sandbox (di luar kedua platform), lewat relay dengan akses Vercel
Authentication sementara, memakai fixture sintetis dari repo: 2 PDF, 1 DOCX, dan 5 teks yang meniru tata
letak CV nyata.

| Area | Pemeriksaan | Hasil |
| --- | --- | --- |
| Frontend | Halaman utama, halaman lowongan, halaman kandidat | PASS (200) |
| Frontend | 9 aset JS dan CSS termuat | PASS |
| Frontend | Tanpa login dialihkan ke Vercel Authentication | PASS (302) |
| Frontend | Galat konsol dan tampilan responsif di peramban sungguhan | Belum diuji |
| Backend | Health check | PASS, 37 ms |
| Backend | Unggah lowongan dan 8 dokumen (PDF, DOCX, TXT) lewat relay | PASS (201 dan 200) |
| Backend | Screening | PASS, 7,4 detik untuk 8 kandidat |
| AI | E5 (`multilingual-e5-small`) dipakai saat screening | PASS |
| AI | Catatan recruiter dari templat | PASS, susunan lengkap |
| AI | Catatan recruiter dari Gemini | **Belum diuji**: `GEMINI_API_KEY` belum diisi |
| Screening | Lulusan arsitektur berpengalaman di atas lulusan SMK yang masih kuliah | PASS |
| Explainable AI | Jumlah lima baris panel skor sama dengan skor akhir, 8 dari 8 kandidat | PASS |
| Candidate Insight | Persentase per komponen tersedia untuk semua kandidat | PASS |
| Match Breakdown | Status pendidikan, jabatan terbaca, keterampilan wajib | PASS |
| Lima CV perusahaan | Peringkat dan keputusan dengan E5 | **Belum diuji** (lihat Issue H-2) |
| Keamanan | Tanpa kunci atau kunci salah: 401 | PASS |
| Keamanan | `/docs`, `/redoc`, `/openapi.json` | PASS (404) |
| Keamanan | Kunci, alamat Railway, nama variabel tidak ada di HTML dan aset peramban | PASS |
| Keamanan | CORS menolak origin asing, menerima origin staging | PASS |
| Keamanan | Identitas tersembunyi bawaan; catatan AI tanpa email atau telepon | PASS |
| Keamanan | Log tanpa kunci dan tanpa data pribadi | PASS (diuji lokal; log Railway hanya ID dan hitungan) |

### Waktu

| Ukuran | Nilai |
| --- | --- |
| Build frontend (Vercel) | 15 detik |
| Build backend (Railway) | sekitar 2 menit |
| Muat halaman pertama (HTML, dari sandbox di region yang sama) | 47 ms |
| Unggah 8 dokumen | 193 ms |
| Screening 8 kandidat dengan E5 | 7,4 detik (termasuk memuat model pertama kali) |
| Rincian satu kandidat | 56–91 ms |
| Catatan recruiter (templat) | 55 ms |

## Issue

### High

**H-1 · Batas memori Railway 1 GB.** Paket Railway saat ini tidak mengizinkan lebih dari 1 GB per layanan.
Setelah model E5 dimuat, pemakaian sekitar 0,77 GB. Sebelum perbaikan konfigurasi, screening memakan
lebih dari 3 menit karena memori penuh dan thread PyTorch berebut 2 vCPU.
*Sudah ditangani dengan variabel:* `OMP_NUM_THREADS=2`, `MKL_NUM_THREADS=2`, `MALLOC_ARENA_MAX=2`,
`TOKENIZERS_PARALLELISM=false`, `HF_HUB_OFFLINE=1`, `HF_HOME` ke cache di image.
*Rekomendasi:* naikkan paket Railway ke Hobby (memori hingga 8 GB) sebelum demo, atau hindari screening
bersamaan dari beberapa pengguna.

**H-2 · Lima CV perusahaan belum diuji di staging.** Berkasnya tidak dapat dikirim ke klien uji tanpa
risiko salah salin, dan tidak boleh masuk repo publik.
*Rekomendasi:* Product Owner mengunggah Vacancy dan lima CV lewat antarmuka staging; hasilnya diverifikasi
lewat API. Peringkat E5 dapat berbeda angkanya dari TF-IDF di QA Report 02.

### Medium

**M-1 · Gemini belum aktif.** Catatan recruiter memakai templat.
*Rekomendasi:* isi `GEMINI_API_KEY` (kunci baru) di Variables layanan Railway, lalu uji satu catatan.

**M-2 · Sumber Railway sempat berpindah ke cabang `main`.** Saat variabel diubah pertama kali, Railway
men-deploy `main` (kode Sprint 2, tanpa kunci API) selama sekitar 3 menit. Log HTTP menunjukkan tidak ada
permintaan dari luar selama jendela itu.
*Sudah ditangani:* layanan dikunci ke commit `3965831`. Pembaruan berikutnya harus menyambungkan ulang
sumber ke commit baru secara sengaja.

**M-3 · Data uji sintetis ada di staging.** Lowongan "Junior Architect" sintetis dan 8 kandidat uji
tersimpan di volume. Judulnya sama dengan lowongan perusahaan.
*Rekomendasi:* kosongkan volume sebelum demo (hapus dan buat ulang volume `screening-data`).

**M-4 · Container berjalan sebagai root.** `RAILWAY_RUN_UID=0` diperlukan agar volume dapat ditulis.
*Rekomendasi:* terima untuk staging.

### Low

**L-1 · Cabang production Vercel adalah `main`.** Push ke `main` akan menimpa alias production dengan
versi lama sampai `sprint-4` digabung.

**L-2 · Hitungan keterampilan wajib berbeda antara daftar peringkat dan catatan recruiter.** Daftar
menghitung yang tersirat, catatan hanya yang tertulis (sudah tercatat di QA Report 02).

**L-3 · Log Railway berlabel `error`.** Uvicorn menulis ke stderr, sehingga baris informasi tampil
sebagai galat di dashboard. Hanya kosmetik.

## Konfigurasi (runbook)

**Railway, layanan `backend`:** root directory `/backend`, builder Dockerfile, health check
`/api/v1/health`, volume di `/srv/storage`, domain ke port 8000.

| Variabel | Nilai |
| --- | --- |
| `APP_ENV` | `production` |
| `API_KEY` | rahasia, sama dengan `BACKEND_API_KEY` di Vercel |
| `INSTALL_E5` | `true` (argumen build) |
| `EMBEDDING_BACKEND` | `e5` |
| `PORT` | `8000` |
| `CORS_ORIGINS` | `https://talentlens-ai-azure.vercel.app,https://talentlens-ai-git-sprint-4-atn6.vercel.app` |
| `RAILWAY_RUN_UID` | `0` |
| `HF_HOME` | `/home/appuser/.cache/huggingface` |
| `HF_HUB_OFFLINE` | `1` |
| `OMP_NUM_THREADS`, `MKL_NUM_THREADS` | `2` |
| `MALLOC_ARENA_MAX` | `2` |
| `TOKENIZERS_PARALLELISM` | `false` |
| `GEMINI_API_KEY` | belum diisi |

**Vercel, proyek `talentlens-ai`:** root directory `frontend`, framework Next.js, Vercel Authentication
untuk semua deployment. Variabel `BACKEND_URL` dan `BACKEND_API_KEY` (sensitive) untuk Production dan
Preview.

**Memperbarui backend:** sambungkan ulang sumber layanan Railway ke commit baru (pin), lalu pastikan
daftar deployment menunjukkan cabang dan commit yang benar.
