# TDR-0007: Tesseract menjadi dependensi opsional

**Status:** Diterima · **Tanggal:** 16 November 2026

## Konteks
OCR hanya dibutuhkan untuk CV hasil scan. Tesseract adalah program sistem, bukan paket Python, sehingga
tidak semua mesin memilikinya.

## Keputusan
- Image Docker backend memasang Tesseract beserta data bahasa Indonesia.
- Di luar Docker, Tesseract bersifat opsional. Tanpa Tesseract, CV berbasis teks tetap diproses dan CV hasil scan ditolak dengan `UnreadableDocumentError` (422).
- Tes OCR dilewati otomatis bila Tesseract tidak ada.

## Alternatif yang ditolak
- **Mewajibkan Tesseract:** menambah langkah instalasi untuk fitur yang jarang dipakai saat pengembangan.
- **Mengganti dengan PaddleOCR atau layanan cloud:** lebih berat, dan itu perubahan logika.

## Konsekuensi
- Demo yang menampilkan CV hasil scan sebaiknya dijalankan lewat Docker, atau dengan Tesseract terpasang.
- Pesan galat untuk "Tesseract tidak ada" dan "berkas rusak" sama; penyebab pastinya tercatat di log.
