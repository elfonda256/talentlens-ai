# Konvensi

## Konvensi commit

Format [Conventional Commits](https://www.conventionalcommits.org/):

```
<tipe>(<lingkup>): <ringkasan dalam kalimat perintah, huruf kecil, tanpa titik>
```

| Tipe | Dipakai untuk |
| --- | --- |
| `feat` | Fitur baru yang terlihat pengguna |
| `fix` | Perbaikan galat |
| `refactor` | Perubahan struktur tanpa mengubah perilaku |
| `test` | Menambah atau memperbaiki tes |
| `docs` | Dokumentasi |
| `chore` | Dependensi, konfigurasi, perkakas |

Lingkup: `backend`, `frontend`, `docs`, atau `infra`.

```
feat(backend): add health check endpoint
chore(infra): add docker compose for backend and frontend
docs: describe environment variables in readme
```

Satu commit satu perubahan logis. Ringkasan paling panjang 72 karakter.

## Konvensi API

| Aturan | Contoh |
| --- | --- |
| Semua endpoint di bawah `/api/v1` | `/api/v1/health` |
| Nama resource jamak, huruf kecil, kebab-case | `/api/v1/candidates`, `/api/v1/interview-questions` |
| Kata kerja dinyatakan oleh metode HTTP | `POST /candidates`, bukan `/create-candidate` |
| Aksi yang bukan CRUD memakai sub-resource kata kerja | `POST /jobs/{job_id}/screen` |
| Field JSON memakai snake_case | `app_name`, `created_at` |
| Waktu dalam ISO 8601 UTC | `2026-11-16T11:15:27Z` |
| Setiap endpoint punya `response_model`, `summary`, dan `tags` | terlihat rapi di Swagger |

Kode status:

| Kode | Arti |
| --- | --- |
| 200 | Berhasil membaca atau memproses |
| 201 | Resource dibuat |
| 404 | Resource tidak ditemukan |
| 415 | Format berkas tidak didukung |
| 422 | Input tidak lolos validasi |

Galat memakai bentuk bawaan FastAPI, `{"detail": "..."}`, dengan pesan yang bisa ditampilkan ke pengguna.
Setiap response membawa header `X-Request-ID`.

## Konvensi penamaan

### Python

| Hal | Aturan | Contoh |
| --- | --- | --- |
| Modul dan paket | snake_case | `cv_parser.py` |
| Fungsi dan variabel | snake_case, diawali kata kerja untuk fungsi | `parse_cv`, `candidate_id` |
| Kelas | PascalCase | `CandidateProfile` |
| Konstanta | UPPER_SNAKE_CASE | `REQUEST_ID_HEADER` |
| Skema response dan request | akhiran `Response` atau `Request` | `HealthResponse` |
| Tes | `test_<perilaku yang diharapkan>` | `test_health_reports_ok_with_app_metadata` |

### TypeScript

| Hal | Aturan | Contoh |
| --- | --- | --- |
| Berkas | kebab-case | `system-status.tsx` |
| Komponen | PascalCase, ekspor bernama | `SystemStatus` |
| Fungsi dan variabel | camelCase | `getHealth` |
| Tipe | PascalCase | `HealthResponse` |
| Handler peristiwa | awalan `handle` | `handleCheckAgain` |

### Umum

- Kode, komentar, nama, dan pesan commit berbahasa Inggris. Dokumen di `docs/` dan README berbahasa Indonesia.
- Environment variable: UPPER_SNAKE_CASE; yang dibaca peramban berawalan `NEXT_PUBLIC_`.
- Hindari singkatan kecuali yang baku di bidangnya (`cv`, `jd`, `api`, `id`).
