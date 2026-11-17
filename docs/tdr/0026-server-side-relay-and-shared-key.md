# TDR-0026: API dilindungi kunci bersama, dan peramban memanggilnya lewat relay di server frontend

**Status:** Diterima · **Sprint:** Production Hardening · **Tanggal:** 17 November 2026

## Decision

1. Backend mewajibkan header `X-API-Key` pada semua endpoint kecuali `/api/v1/health`. Kuncinya dibaca dari variabel `API_KEY`, dibandingkan dengan `secrets.compare_digest`, dan disimpan sebagai `SecretStr`. Dengan `APP_ENV=production`, aplikasi menolak berjalan tanpa kunci.
2. Peramban tidak lagi memanggil backend langsung. Semua permintaan masuk ke `/api/backend/*` di aplikasi Next.js, yang di server menambahkan kunci dari `BACKEND_API_KEY` lalu meneruskannya ke `BACKEND_URL`. `NEXT_PUBLIC_API_URL` dihapus.
3. Dalam mode production, `/docs`, `/redoc`, dan `/openapi.json` tidak dipublikasikan; galat tak terduga dijawab dengan pesan umum tanpa detail internal; CORS dibatasi ke origin yang dikonfigurasi, metode `GET` dan `POST`, serta tiga header.

## Reason

Backend staging dapat dijangkau dari internet, dan endpoint rincian kandidat mengembalikan nama, email, dan nomor telepon bila `reveal=true`. Kunci yang dikirim langsung dari peramban harus berupa variabel `NEXT_PUBLIC_*`, yang tertanam di JavaScript yang diunduh setiap pengunjung, sehingga siapa pun dapat menyalinnya. Dengan relay, kunci tidak pernah meninggalkan server, dan akses ke frontend tetap dijaga Vercel Authentication.

## Impact

- Tidak ada perubahan pada algoritma, skor, atau isi response. Tes lama tetap lolos; 17 tes keamanan baru.
- Unggahan melewati fungsi Vercel, sehingga satu permintaan dibatasi sekitar 4,5 MB oleh platform. Lima CV perusahaan berjumlah sekitar 400 KB.
- Setiap permintaan menempuh satu lompatan jaringan tambahan (Vercel ke Railway).
- Kunci bersama bukan autentikasi pengguna: siapa pun yang memegang kuncinya punya akses penuh. Untuk demo itu cukup; untuk pemakaian nyata diperlukan login dan peran (di luar cakupan, DO NOT IMPLEMENT).
- Pengembangan lokal tanpa kunci tetap berjalan seperti sebelumnya.

## Alternative Considered

- **`NEXT_PUBLIC_API_KEY` dikirim dari peramban:** paling sederhana, tetapi kuncinya publik.
- **Rewrites di `next.config` ke backend:** tidak dapat menambahkan header rahasia per permintaan.
- **Jaringan privat Railway:** peramban tetap harus menjangkau backend lewat sesuatu yang publik, dan frontend berada di Vercel, bukan di Railway.
- **Login pengguna:** di luar cakupan proyek ini.
