# TDR-0017: API berpusat pada lowongan; identitas kandidat tersembunyi secara default

**Status:** Diterima · **Sprint:** 3 · **Tanggal:** 17 November 2026

## Decision

Alur screening diekspos di bawah `/api/v1/jobs`: unggah lowongan, unggah CV, jalankan screening, peringkat, rincian, ringkasan. Peringkat, daftar kandidat, dan rincian menyembunyikan nama, kontak, dan nama berkas kecuali diminta dengan `?reveal=true`. Unggahan beberapa CV melaporkan hasil per berkas; satu berkas rusak tidak menggagalkan yang lain.

## Reason

Semua langkah bergantung pada satu lowongan, jadi lowongan menjadi resource induk. Menyembunyikan identitas adalah perilaku PoC lama dan menutup catatan pada TDR-0009: penilai melihat skor dan bukti sebelum melihat siapa orangnya.

## Impact

- Antarmuka menampilkan ID kandidat; nama muncul setelah kotak "Tampilkan identitas kandidat" dicentang.
- Nama berkas ikut disembunyikan karena sering memuat nama orang.
- `POST /api/v1/cvs/parse` dari Sprint 2 tetap ada dan tetap mengembalikan data pribadi; endpoint itu untuk mencoba parser, bukan bagian alur screening.
- Tidak ada pencatatan siapa yang membuka identitas, karena tidak ada pengguna.

## Alternative Considered

- **Selalu menampilkan nama:** lebih praktis untuk demo, tetapi melemahkan cerita mitigasi bias.
- **Satu endpoint yang menerima lowongan dan semua CV lalu langsung mengembalikan peringkat:** lebih sedikit panggilan, tetapi langkah-langkahnya tidak bisa ditunjukkan terpisah saat demo.
