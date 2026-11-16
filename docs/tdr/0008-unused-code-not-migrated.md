# TDR-0008: Kode yang belum dipakai tidak ikut dipindahkan

**Status:** Diterima · **Sprint:** 2 · **Tanggal:** 16 November 2026

## Decision

Tidak dipindahkan pada Sprint 2: `text_utils.bilingual` dan glosarium ID-EN (milik embedder TF-IDF), `taxonomy.find_spans`/`label`/`describe` (milik parser lowongan dan pencocok), penggabungan hasil LLM (`_merge_llm`), serta deduplikasi dan penyimpanan kandidat.

## Reason

Bagian-bagian itu menempel pada parser lama tetapi bukan bagian dari parsing CV. Memindahkannya sekarang meninggalkan kode mati yang tidak teruji.

## Impact

- Setiap baris di proyek baru dipakai dan diuji.
- Sprint berikutnya mengambil bagian ini dari sumber lama saat modul pemakainya dibangun.
- `_merge_llm` kemungkinan tidak akan dibawa sama sekali: governance v1.1 tidak mengizinkan LLM untuk ekstraksi.

## Alternative Considered

- **Memindahkan semuanya sekaligus:** lebih cepat nanti, tetapi melanggar aturan tanpa placeholder.
