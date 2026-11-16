# TDR-0004: Memakai ulang parser lama, bukan menulis ulang

**Status:** Diterima · **Sprint:** 2 · **Tanggal:** 16 November 2026

## Decision

Tiga modul parser dari `cv-screening-poc` (`document_loader`, `pii`, `extractor`) dipindahkan apa adanya. Perubahan dibatasi pada jalur impor, penerjemahan komentar ke bahasa Inggris, pemformatan otomatis, satu nama variabel (`l` menjadi `line`), dan kelas galat khusus untuk format yang tidak didukung.

## Reason

Parser lama sudah berjalan dan teruji pada 15 CV contoh. Menulis ulang tidak menambah nilai demo dan membuang perilaku yang sudah terbukti (Reuse Policy).

## Impact

- Integrasi selesai dalam satu sprint dengan risiko rendah.
- Kelemahan parser lama ikut terbawa; daftarnya ada di `docs/CV_PARSER.md`.
- `extractor.py` dan `pii.py` dikecualikan dari aturan panjang baris karena ekspresi regulernya tidak dipecah.

## Alternative Considered

- **Menulis ulang dengan desain baru:** tidak ada manfaat rekayasa yang jelas.
- **Mengganti dengan ekstraksi LLM:** tidak deterministik, dan saat itu belum ada LLM yang disetujui.
