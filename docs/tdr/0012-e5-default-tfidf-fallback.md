# TDR-0012: Embedding E5 lokal sebagai default, TF-IDF sebagai cadangan otomatis

**Status:** Diterima · **Sprint:** 3 · **Tanggal:** 17 November 2026

## Decision

Embedding memakai `intfloat/multilingual-e5-small` yang berjalan lokal. Bila model tidak dapat dimuat (paket belum terpasang, tidak ada internet saat unduhan pertama), sistem otomatis beralih ke TF-IDF dan mencatat peringatan. Backend yang benar-benar dipakai disimpan bersama hasil screening dan ditampilkan di antarmuka. Embedding lewat Gemini tidak dibuat.

## Reason

Spesifikasi Sprint 3 menetapkan E5 sebagai pilihan utama dan TF-IDF sebagai cadangan terakhir. E5 multibahasa, sehingga CV berbahasa Indonesia dapat dicocokkan dengan lowongan berbahasa Inggris, dan teks CV tidak meninggalkan mesin. Cadangan otomatis menjaga demo tetap berjalan tanpa internet.

## Impact

- `sentence-transformers` (dengan PyTorch, sekitar 2 GB) dipisah ke `requirements-e5.txt` agar instalasi dasar dan image Docker tetap ringan.
- **Jalur E5 belum pernah dijalankan dengan model asli**: lingkungan pembuatan tidak dapat mengunduhnya. Pembungkusnya diuji dengan model pengganti (awalan `query:`/`passage:`, normalisasi, kalibrasi).
- Rentang kalibrasi E5 (0,75 sampai 0,88) adalah nilai awal. Skor semantik pada mode E5 belum divalidasi; `scripts/check_ai_backends.py` menampilkan nilainya.
- Skor pada mode E5 dan TF-IDF tidak identik, jadi peringkat bisa berbeda antar-mode.

## Alternative Considered

- **Embedding Gemini:** tanpa unduhan model, tetapi mengirim teks CV ke pihak ketiga dan menambah satu jalur lagi yang tidak dapat diuji di sini. Spesifikasi hanya memintanya bila model lokal dilarang.
- **BGE-M3:** lebih akurat tetapi unduhannya sekitar 2 GB; terlalu berat untuk demo di laptop.
- **Gagal keras bila E5 tidak ada:** lebih jujur terhadap konfigurasi, tetapi membuat demo bergantung pada internet. Mode `EMBEDDING_BACKEND=e5` menyediakan perilaku ini bagi yang menginginkannya.
