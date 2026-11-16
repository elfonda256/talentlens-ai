# TDR-0003: Komponen shadcn/ui ditulis langsung, tidak lewat CLI

**Status:** Diterima · **Sprint:** 1 · **Tanggal:** 16 November 2026

## Decision

`Button`, `Badge`, dan `Card` ditulis langsung di `src/components/ui/` mengikuti konvensi shadcn/ui (token CSS, `cva`, `cn`). `components.json` disertakan agar CLI dapat dipakai nanti.

## Reason

Registry shadcn tidak terjangkau dari lingkungan tempat fondasi dibangun, sehingga `npx shadcn init` gagal. shadcn/ui pada dasarnya menyalin kode komponen ke proyek, jadi hasil akhirnya setara.

## Impact

- Tiga komponen ini tidak memakai Radix/Base UI; cukup untuk kebutuhan saat ini.
- `npx shadcn@latest add <komponen>` belum pernah diuji terhadap `components.json` ini. Bila gagal, jalankan `npx shadcn@latest init` di mesin pengembang dan terima perubahannya.

## Alternative Considered

- **Menunda frontend sampai CLI bisa dijalankan:** menghambat Sprint 1 untuk masalah yang bisa diselesaikan manual.
- **Tanpa shadcn, Tailwind polos:** bertentangan dengan tech stack yang disetujui.
