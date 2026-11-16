# TDR-0007: Tanggal acuan dan lokasi taksonomi diberikan dari `Settings`

**Status:** Diterima · **Sprint:** 2 · **Tanggal:** 16 November 2026

## Decision

`extractor.extract` tidak lagi membaca konfigurasi global; tanggal acuan diteruskan sebagai argumen `today`. `Settings` mendapat `taxonomy_path`, `reference_date`, dan `max_upload_mb`. Bila `REFERENCE_DATE` kosong, tanggal hari ini dipakai, sama seperti parser lama.

## Reason

Parser lama membaca modul `config` global di tiga tempat. Masa kerja "sampai sekarang" bergantung pada tanggal hari ini, sehingga hasil tes dan demo berubah setiap bulan.

## Impact

- Tes dan demo dapat dikunci pada satu tanggal.
- Ini satu-satunya perubahan pada tanda tangan fungsi lama; logikanya tidak berubah.

## Alternative Considered

- **Membiarkan modul parser membaca `Settings` sendiri:** menyembunyikan ketergantungan dan menyulitkan tes.
