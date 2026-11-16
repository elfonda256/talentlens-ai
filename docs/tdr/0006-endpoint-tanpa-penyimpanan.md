# TDR-0006: Endpoint parse tidak menyimpan apa pun dan mengembalikan profil lengkap

**Status:** Diterima · **Tanggal:** 16 November 2026

## Konteks
Service perlu bisa dicoba dari Swagger dan nantinya dari frontend. Proyek belum punya penyimpanan.

## Keputusan
- `POST /api/v1/cvs/parse` menerima satu berkas, memprosesnya di folder sementara, lalu menghapusnya.
- Response adalah `CandidateProfile` utuh, termasuk `pii` dan `redacted_text`.
- Batas ukuran 5 MB (`MAX_UPLOAD_MB`). Kode status: 413, 415, 422.

## Alternatif yang ditolak
- **Menyembunyikan `pii` dari response:** pada tahap ini pengunggah melihat dokumennya sendiri, dan pemisahan `pii` dari `redacted_text` justru bahan demo redaksi.
- **Menambah penyimpanan sekarang:** di luar lingkup sprint integrasi.

## Konsekuensi
- Endpoint aman dipanggil berulang; tidak ada data kandidat yang tertinggal di server.
- **Perlu ditinjau lagi** saat tampilan peringkat dibuat: di sana identitas harus tersembunyi secara default, seperti pada PoC lama.
