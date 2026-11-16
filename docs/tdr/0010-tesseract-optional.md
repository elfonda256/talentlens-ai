# TDR-0010: Tesseract menjadi dependensi opsional

**Status:** Diterima · **Sprint:** 2 · **Tanggal:** 16 November 2026

## Decision

Image Docker backend memasang Tesseract dengan data bahasa Indonesia. Di luar Docker, Tesseract opsional: CV berbasis teks tetap diproses, CV hasil scan ditolak dengan `UnreadableDocumentError` (422). Tes OCR dilewati otomatis bila Tesseract tidak ada.

## Reason

OCR hanya dibutuhkan untuk CV hasil scan, dan Tesseract adalah program sistem yang tidak dimiliki semua mesin.

## Impact

- Pengembangan lokal tidak terhambat instalasi Tesseract.
- Demo CV hasil scan sebaiknya lewat Docker atau dengan Tesseract terpasang.
- Pesan galat untuk "Tesseract tidak ada" dan "berkas rusak" sama; penyebab pastinya ada di log.

## Alternative Considered

- **Mewajibkan Tesseract:** menambah langkah instalasi untuk fitur yang jarang dipakai saat pengembangan.
- **PaddleOCR atau layanan cloud:** lebih berat, dan itu perubahan logika.
