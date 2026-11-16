# TDR-0002: Font sistem, bukan Google Fonts

**Status:** Diterima · **Sprint:** 1 · **Tanggal:** 16 November 2026

## Decision

Template Next.js memuat font Geist dari Google Fonts. Pemuatan itu dihapus; antarmuka memakai tumpukan font sistem.

## Reason

`next/font/google` mengunduh font saat build. Build dan demo tidak boleh bergantung pada internet.

## Impact

- `npm run build` dan `docker compose build` untuk frontend tidak butuh akses ke Google Fonts.
- Tampilan huruf sedikit berbeda antar sistem operasi.

## Alternative Considered

- **Menyimpan berkas font di repositori (`next/font/local`):** tampilan seragam, tetapi menambah berkas biner untuk manfaat kosmetik.
