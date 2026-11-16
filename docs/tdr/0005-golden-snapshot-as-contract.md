# TDR-0005: Snapshot keluaran parser lama menjadi kontrak regresi

**Status:** Diterima · **Sprint:** 2 · **Tanggal:** 16 November 2026

## Decision

Sebelum kode dipindahkan, parser lama dijalankan pada 15 CV contoh dan hasilnya disimpan sebagai `tests/fixtures/golden_profiles.json`. Tes membandingkan parser baru dengan snapshot ini field demi field untuk 14 CV berbasis teks. CV hasil scan diperiksa lebih longgar.

## Reason

Syarat sprint adalah keluaran tetap konsisten. Tanpa pembanding dari kode lama, konsistensi tidak bisa dibuktikan. Teks OCR berbeda tipis antarversi Tesseract, sehingga perbandingan persis untuk CV hasil scan akan rapuh.

## Impact

- Setiap perubahan perilaku langsung menggagalkan tes.
- Mengubah logika parser berarti membuat ulang snapshot dan meninjau selisihnya.
- 15 CV sintetis (372 KB) tersimpan di repositori.

## Alternative Considered

- **Hanya tes unit baru:** membuktikan kode baru benar menurut tes baru, bukan bahwa ia sama dengan yang lama.
- **Menyertakan parser lama di repositori sebagai pembanding:** kode ganda yang harus dirawat.
