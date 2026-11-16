# TDR-0009: Endpoint `POST /api/v1/cvs/parse` sebagai komponen pendukung, tanpa penyimpanan

**Status:** Diterima · **Sprint:** 2 · **Tanggal:** 16 November 2026

## Decision

Ditambahkan endpoint yang menerima satu berkas, memprosesnya di folder sementara, lalu menghapusnya. Response adalah `CandidateProfile` utuh, termasuk `pii` dan `redacted_text`. Batas ukuran 5 MB; kode status 413, 415, 422.

## Reason

Endpoint ini tidak ada di spesifikasi Sprint 2. Ia ditambahkan sebagai dependensi teknis (Sprint Policy): tanpa endpoint, service tidak bisa dicoba dari Swagger maupun dipakai frontend. Proyek belum punya penyimpanan, jadi endpoint dibuat stateless.

## Impact

- Parser dapat didemokan lewat Swagger.
- Tidak ada data kandidat yang tertinggal di server.
- **Perlu ditinjau lagi** saat tampilan peringkat dibuat: di sana identitas harus tersembunyi secara default.

## Alternative Considered

- **Tidak membuat endpoint:** patuh pada spesifikasi secara harfiah, tetapi hasil sprint tidak bisa didemokan.
- **Menyembunyikan `pii` dari response:** pada tahap ini pengunggah melihat dokumennya sendiri, dan pemisahan `pii` justru bahan demo redaksi.
- **Menambah penyimpanan:** di luar lingkup sprint integrasi.
