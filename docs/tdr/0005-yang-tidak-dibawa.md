# TDR-0005: Kode yang belum dipakai tidak ikut dipindahkan

**Status:** Diterima · **Tanggal:** 16 November 2026

## Konteks
Beberapa bagian PoC lama menempel pada parser tetapi bukan bagian dari parsing CV.

## Keputusan
Tidak dipindahkan pada sprint ini:

| Bagian | Alasan | Kapan dibawa |
| --- | --- | --- |
| `text_utils.bilingual` dan glosarium ID-EN | Hanya dipakai embedder TF-IDF | Bersama embedding |
| `taxonomy.find_spans`, `label`, `describe` | Dipakai parser lowongan dan pencocok | Bersama modul tersebut |
| Penggabungan hasil LLM (`_merge_llm`) | Belum pernah dijalankan; akses LLM belum diputuskan | Setelah keputusan LLM |
| Deduplikasi dan penyimpanan kandidat | Butuh penyimpanan, yang belum ada | Bersama fitur daftar kandidat |

## Alternatif yang ditolak
- **Memindahkan semuanya sekaligus:** meninggalkan kode mati yang tidak teruji di proyek baru.

## Konsekuensi
- Setiap baris di proyek baru dipakai dan diuji.
- Sprint berikutnya mengambil bagian-bagian ini dari sumber lama, bukan menulis ulang.
