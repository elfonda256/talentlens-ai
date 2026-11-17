# TDR-0016: Penyimpanan berkas JSON; CV asli dan dokumen perusahaan tidak masuk repositori

**Status:** Diterima · **Sprint:** 3 · **Tanggal:** 17 November 2026

## Decision

Lowongan, profil kandidat, hasil screening, dan ringkasan disimpan di `backend/storage/state.json`, yang tidak masuk Git. Berkas CV yang diunggah tidak disimpan; hanya hasil parsing. Data demo (5 CV dari perusahaan) dimasukkan lewat antarmuka, bukan disertakan di repositori. Tes memakai CV sintetis dan satu deskripsi lowongan sintetis.

## Reason

Repositori `elfonda256/talentlens-ai` bersifat publik. CV asli memuat data pribadi orang lain, dan berkas lowongan adalah materi tes milik perusahaan. Peringkat membutuhkan daftar kandidat per lowongan, dan satu berkas JSON adalah penyimpanan paling sederhana yang bertahan setelah restart.

## Impact

- Demo dimulai dengan mengunggah lowongan dan 5 CV; hasilnya tersimpan lokal sehingga tidak perlu diulang.
- `state.json` berisi data pribadi kandidat dan harus diperlakukan sebagai data sensitif di mesin demo.
- Kandidat disimpan per lowongan; CV yang sama untuk dua lowongan diparsing dua kali.
- Mengunggah CV baru menghapus hasil screening lowongan itu.
- Tidak aman untuk beberapa proses sekaligus; cukup untuk satu pengguna.

## Alternative Considered

- **Menyertakan 5 CV perusahaan sebagai data contoh:** mempermudah demo, tetapi mempublikasikan data pribadi kandidat.
- **SQLite atau PostgreSQL:** tepat untuk produksi; menambah skema dan migrasi tanpa nilai demo.
- **Hanya di memori:** data hilang setiap backend dimulai ulang, termasuk di tengah demo.
