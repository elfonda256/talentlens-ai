# TDR-0022: Satu bahasa visual untuk penjelasan skor

**Status:** Diterima · **Sprint:** 4 · **Tanggal:** 17 November 2026

## Decision

Antarmuka dibangun ulang di atas token warna yang sama dengan empat aturan: (1) tiap komponen skor punya satu warna yang dipakai di semua tempat, dan bilah susunan skor menjadi elemen penjelas utama di daftar peringkat dan halaman rincian; (2) vonis selalu ditampilkan dengan ikon dan kata, tidak hanya warna; (3) setiap bagian punya keadaan memuat, kosong, dan galat; (4) teks antarmuka memakai bahasa HR, bukan istilah sistem. Komponen dasar baru ditulis langsung: `Skeleton`, `Notice`, `EmptyState`, `Meter`, `ScoreComposition`, `HighlightedText`. Prettier ditambahkan sebagai dependensi pengembangan.

## Reason

Spesifikasi Sprint 4 meminta tampilan yang siap dipresentasikan kepada HR dan transparansi AI. Bilah susunan skor menjawab "mengapa skornya segini" sebelum halaman rincian dibuka, dan warna yang konsisten membuat rincian di halaman berikutnya langsung terbaca.

## Impact

- Kontras teks pada semua pasangan token minimal 4,5 : 1 dan elemen grafis minimal 3 : 1 (dihitung dari nilai token); satu warna komponen digelapkan agar lolos.
- Tombol utama setinggi 44 px; fokus keyboard terlihat pada semua elemen interaktif; animasi dimatikan bila sistem meminta gerak dikurangi.
- Ringkasan hasil (total, direkomendasikan, perlu ditinjau, tidak lolos) sekaligus berfungsi sebagai penyaring daftar.
- Di ponsel, tingkat kecocokan tampil paling atas; daftar peringkat menjadi kartu bertumpuk.
- Garis tepi kartu berkontras rendah (1,3 : 1); garis itu dekoratif, bukan satu-satunya penanda kontrol.
- Belum diuji: tablet, mode gelap (belum ada), navigasi keyboard penuh, dan pembaca layar.
- Frontend tetap tanpa tes otomatis.

## Alternative Considered

- **Pustaka komponen lengkap (shadcn lewat CLI, Radix):** registry tidak terjangkau dari lingkungan pembuatan (TDR-0003), dan enam komponen kecil tidak membenarkan dependensi baru.
- **Grafik radar atau donat untuk kecocokan:** lebih mencolok, tetapi lebih sulit dibaca dan dibandingkan antarkandidat daripada bilah.
- **Mempertahankan tabel peringkat Sprint 3:** berfungsi, tetapi tidak menunjukkan dari mana skor berasal.
