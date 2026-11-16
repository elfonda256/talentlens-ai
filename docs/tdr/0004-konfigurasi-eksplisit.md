# TDR-0004: Tanggal acuan dan lokasi taksonomi diberikan dari `Settings`

**Status:** Diterima · **Tanggal:** 16 November 2026

## Konteks
Parser lama membaca modul `config` global di tiga tempat. Masa kerja "sampai sekarang" bergantung
pada tanggal hari ini, sehingga hasilnya berubah setiap bulan.

## Keputusan
- `extractor.extract` tidak lagi membaca konfigurasi; tanggal acuan diteruskan sebagai argumen `today` oleh pemanggil.
- `Settings` mendapat tiga field: `taxonomy_path`, `reference_date`, `max_upload_mb`.
- Bila `REFERENCE_DATE` kosong, tanggal hari ini dipakai (perilaku yang sama dengan parser lama).

## Alternatif yang ditolak
- **Membiarkan modul parser membaca `Settings` sendiri:** menyembunyikan ketergantungan dan menyulitkan tes.

## Konsekuensi
- Tes dan demo dapat dikunci pada satu tanggal sehingga angkanya tetap.
- Ini satu-satunya perubahan pada tanda tangan fungsi lama; logikanya tidak berubah.
