# TDR-0018: Enam tampilan yang diminta ditempatkan pada tiga rute

**Status:** Diterima · **Sprint:** 3 · **Tanggal:** 17 November 2026

## Decision

Frontend punya tiga rute. `/` memuat unggah lowongan dan daftar lowongan. `/jobs/[jobId]` memuat kriteria, unggah CV, tombol screening, dan tabel peringkat. `/jobs/[jobId]/candidates/[candidateId]` memuat rincian kandidat dan ringkasan AI. Semua halaman adalah Client Component yang mengambil data lewat `lib/api.ts` dan hook `useApi`.

## Reason

Spesifikasi meminta antarmuka sederhana dengan enam tampilan. Unggah CV, screening, dan peringkat adalah satu alur kerja pada satu lowongan; memecahnya ke halaman terpisah menambah navigasi tanpa menambah nilai demo. Pengambilan data di sisi klien konsisten dengan TDR-0001.

## Impact

- Demo berjalan dalam tiga layar.
- Next.js 16 mewajibkan batas `Suspense` di sekitar komponen yang membaca URL di klien; kedua halaman dinamis memilikinya.
- Tiga komponen dasar baru ditulis langsung (varian lencana, bilah skor, pemilih berkas), melanjutkan TDR-0003.
- Teks antarmuka berbahasa Indonesia.
- Frontend tetap tanpa tes otomatis; alurnya diverifikasi dengan skrip peramban sekali jalan.

## Alternative Considered

- **Enam rute terpisah:** mengikuti daftar secara harfiah, tetapi memecah satu alur menjadi banyak klik.
- **Server Components dengan pengambilan data di server:** mengikat tampilan ke mekanisme cache Next.js 16 dan membutuhkan alamat backend kedua di dalam Docker.
