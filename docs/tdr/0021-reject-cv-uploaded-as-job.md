# TDR-0021: Dokumen yang tampak seperti CV ditolak saat diunggah sebagai lowongan

**Status:** Diterima · **Sprint:** 4 · **Tanggal:** 17 November 2026

## Decision

`POST /api/v1/jobs` menolak dokumen (422, dengan pesan yang menjelaskan) bila dokumen itu memuat email atau nomor telepon dan tidak punya satu pun judul bagian lowongan seperti Requirements, Kualifikasi, Syarat, atau Tanggung Jawab. Parser lowongan tidak diubah; pemeriksaan dilakukan sebelum parser dipanggil.

## Reason

Saat validasi Sprint 3, sebuah CV terunggah sebagai lowongan. Sistem menerimanya, memberi judul lowongan dengan nama pelamar, dan menghasilkan peringkat yang tidak sah tanpa peringatan apa pun. Kesalahan ini mudah terjadi saat demo.

## Impact

- Kesalahan unggah yang sama kini dihentikan dengan pesan yang menyuruh mengunggah berkas lowongan.
- Lowongan yang memuat alamat email tetap diterima selama punya judul bagian; lowongan tanpa judul bagian tetap diterima selama tidak memuat kontak. Tiga kasus ini diuji.
- Lowongan tanpa judul bagian yang sekaligus memuat email atau telepon akan ditolak. Itu harga dari aturan sederhana ini.
- Belum ada cara menghapus lowongan yang salah dari antarmuka.

## Alternative Considered

- **Hanya memberi peringatan dan tetap menyimpan:** tidak mencegah peringkat yang tidak sah.
- **Klasifikasi dokumen dengan LLM:** lebih andal, tetapi menambah ketergantungan dan mengirim isi dokumen ke pihak ketiga hanya untuk validasi.
- **Menolak semua dokumen tanpa judul bagian:** terlalu ketat untuk lowongan yang ditulis sebagai paragraf.
