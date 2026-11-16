# Sprint Report 01 — Fondasi Proyek

**Tanggal:** 16 November 2026 · **Tag Git:** `sprint-1` · **Status:** selesai, menunggu satu verifikasi (Docker)

Laporan ini ditulis setelah sprint berakhir, saat governance v1.1 mulai berlaku.

## Sprint Summary

Kerangka proyek dua layanan: backend FastAPI dan frontend Next.js. Tidak ada fitur bisnis.
Backend punya health check, pengaturan dari environment, dan log per request. Frontend punya satu
halaman yang menampilkan apakah API terjangkau.

## Completed Tasks

| # | Deliverable | Hasil |
| --- | --- | --- |
| 1-2 | Struktur folder dan inisialisasi proyek | `backend/`, `frontend/`, `docs/` |
| 3 | FastAPI | `app/main.py` dengan `create_app()` |
| 4-6 | Next.js, Tailwind, shadcn/ui | Next.js 16.4.6, Tailwind 4.3.3, tiga komponen bergaya shadcn |
| 7-8 | Environment variables dan konfigurasi | `core/config.py` (pydantic-settings), `.env.example` |
| 9 | Logging | Satu baris per request dengan `X-Request-ID` |
| 10 | Docker Compose | Dua layanan dengan health check; **belum dijalankan** |
| 11 | Health check | `GET /api/v1/health` |
| 12-19 | README dan dokumentasi | README, `ARCHITECTURE.md`, `DEVELOPMENT.md`, `CONVENTIONS.md` |
| 20 | Swagger | `/docs` dan `/openapi.json` |

Verifikasi: 5 tes dan `ruff` lolos; `npm run lint` dan `npm run build` lolos; kedua layanan dijalankan
bersama dan lencana Online serta Offline diuji di peramban.

## Modified Files

Tidak ada (sprint pertama).

## Added Files

44 berkas. Per kelompok:

| Kelompok | Berkas |
| --- | --- |
| Akar | `.env.example`, `.gitignore`, `README.md`, `docker-compose.yml` |
| Backend, aplikasi | `app/main.py`, `app/core/config.py`, `app/core/logging.py`, `app/api/v1/router.py`, `app/api/v1/health.py`, `app/schemas/health.py`, lima `__init__.py` |
| Backend, lainnya | `Dockerfile`, `.dockerignore`, `pyproject.toml`, `requirements.txt`, `requirements-dev.txt`, `tests/test_health.py` |
| Frontend, kode | `src/app/{layout.tsx,page.tsx,globals.css,favicon.ico}`, `src/components/system-status.tsx`, `src/components/ui/{button,badge,card}.tsx`, `src/lib/{api,utils}.ts` |
| Frontend, konfigurasi | `package.json`, `package-lock.json`, `tsconfig.json`, `next.config.ts`, `eslint.config.mjs`, `components.json`, `Dockerfile`, `.dockerignore`, `.gitignore`, `AGENTS.md` |
| Dokumentasi | `docs/ARCHITECTURE.md`, `docs/DEVELOPMENT.md`, `docs/CONVENTIONS.md` |

Daftar lengkap: `git ls-tree -r --name-only sprint-1`.

## Deleted Files

Tidak ada. Berkas bawaan template Next.js (logo SVG, README template) dibuang sebelum commit pertama.

## Known Issues

- `docker compose up --build` belum pernah dijalankan; hanya sintaksnya yang tervalidasi.
- CLI shadcn belum pernah berhasil dijalankan pada proyek ini.

## Technical Debt

- Tiga komponen UI ditulis tangan; komponen yang lebih rumit (dialog, tabel, unggah) akan butuh CLI shadcn atau pustaka primitif.
- Frontend belum punya tes.
- Tidak ada CI; tes dan lint dijalankan manual.

## Risks

| Risiko | Dampak | Mitigasi |
| --- | --- | --- |
| Build Docker gagal di mesin Product Owner | Demo satu perintah tidak tersedia | Jalankan sekali sebelum Sprint 3; cara tanpa Docker sudah teruji |
| Next.js 16 berbeda dari versi yang umum dikenal | Waktu frontend membengkak | Baca dokumen di `node_modules/next/dist/docs/` sebelum memakai API baru |
| Frontend menyerap waktu yang seharusnya untuk pipeline AI | Fitur inti tidak selesai | Batasi frontend pada satu halaman per fitur |

## Technical Decision Records

- [TDR-0001](tdr/0001-browser-calls-api-directly.md): peramban memanggil API secara langsung
- [TDR-0002](tdr/0002-system-fonts.md): font sistem, bukan Google Fonts
- [TDR-0003](tdr/0003-shadcn-components-written-by-hand.md): komponen shadcn/ui ditulis langsung

## Recommended Next Sprint

Integrasi parser CV dari PoC sebelumnya. (Sudah dikerjakan sebagai Sprint 2.)

## Suggested Git Commit Message

```
chore: set up project foundation with fastapi and next.js
```
