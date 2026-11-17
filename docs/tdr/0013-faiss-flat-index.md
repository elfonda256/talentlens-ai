# TDR-0013: FAISS `IndexFlatIP` dengan satu blok ID per kandidat

**Status:** Diterima · **Sprint:** 3 · **Tanggal:** 17 November 2026

## Decision

Indeks vektor memakai FAISS `IndexFlatIP`. Potongan CV tiap kandidat ditambahkan sebagai satu blok berurutan; pencarian "bukti terbaik milik kandidat ini" dibatasi ke blok itu dengan `IDSelectorRange`. Indeks dibangun ulang pada setiap screening dan tidak disimpan ke disk.

## Reason

Spesifikasi Sprint 3 mewajibkan FAISS. Indeks flat melakukan pencarian eksak, sehingga hasilnya sama dengan penyimpanan NumPy pada PoC lama; ini dibuktikan oleh tes snapshot skor. Vektor sudah ternormalisasi, jadi inner product sama dengan cosine similarity.

## Impact

- Satu dependensi native baru (`faiss-cpu`).
- Pemetaan ID ke teks dan kandidat disimpan di sisi Python karena FAISS hanya menyimpan vektor.
- Membangun ulang indeks setiap screening memakan waktu sebanding dengan jumlah potongan; untuk puluhan CV kurang dari satu detik dengan TF-IDF.

## Alternative Considered

- **NumPy seperti PoC lama:** rekomendasi saya sebelum spesifikasi keluar; ditolak karena FAISS diminta secara eksplisit.
- **Indeks aproksimasi (IVF, HNSW):** hanya berguna pada jutaan vektor dan membuat hasil tidak eksak.
- **Satu indeks per kandidat:** menyederhanakan penyaringan tetapi menghilangkan pencarian lintas kandidat untuk tahap recall.
