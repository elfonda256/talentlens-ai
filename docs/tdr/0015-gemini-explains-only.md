# TDR-0015: Gemini hanya menjelaskan; dipanggil lewat REST dengan templat sebagai cadangan

**Status:** Diterima · **Sprint:** 3 · **Tanggal:** 17 November 2026

## Decision

Ringkasan HR dibuat oleh Gemini lewat endpoint REST `generateContent` memakai `httpx`, tanpa SDK. Gemini menerima fakta yang sudah dihitung pipeline dan hanya merangkainya menjadi narasi. Tanpa kunci API, atau bila panggilan gagal, narasi deterministik dikembalikan dan diberi label "template" beserta penyebabnya.

## Reason

LLM Policy pada governance: skor harus deterministik, dan LLM hanya untuk ringkasan dan penjelasan. Panggilan REST tunggal mudah dijelaskan dan mudah diuji dengan server tiruan. Cadangan templat menjaga demo tetap berjalan tanpa kunci atau internet.

## Impact

- Data yang dikirim ke Google dibatasi oleh `build_facts()`: tanpa nama, kontak, ID kandidat, atau atribut pribadi. Kutipan CV yang dikirim berasal dari teks yang sudah disamarkan.
- **Panggilan ke API Gemini asli belum pernah dijalankan**: tidak ada kunci, dan API tidak terjangkau dari lingkungan pembuatan. Bentuk request dan response diuji dengan server tiruan mengikuti dokumentasi resmi.
- Model default `gemini-3.6-flash` diambil dari dokumentasi Google per November 2026 dan dapat diganti lewat `GEMINI_MODEL`. Parameter sampling tidak dikirim karena model terbaru mengabaikannya.
- Google menyebut `generateContent` sebagai API lama (masih didukung) dan menganjurkan Interactions API untuk proyek baru.
- Ringkasan dari Gemini disimpan dan dihapus saat screening dijalankan ulang.

## Alternative Considered

- **SDK `google-genai`:** lebih ringkas, tetapi menambah dependensi dan lebih sulit diuji tanpa jaringan.
- **Interactions API:** antarmuka yang kini dianjurkan Google; bentuk response-nya belum dapat saya verifikasi tanpa akses, jadi dipilih endpoint yang bentuknya sudah mapan.
- **Menolak (galat) bila Gemini tidak tersedia:** membuat halaman rincian tidak berguna saat demo tanpa internet.
