# TDR-0014: Parser lowongan, pencocok, dan aturan keputusan dipindahkan tanpa mengubah logika

**Status:** Diterima · **Sprint:** 3 · **Tanggal:** 17 November 2026

## Decision

`jd_parser`, `matcher`, dan `explainer` dari PoC lama dipindahkan menjadi `jd_parsing.py`, `matching.py`, dan `explanation.py`. Perubahan dibatasi pada jalur impor, komentar, pemanggilan indeks (FAISS menggantikan penyimpanan NumPy), parameter `kind` pada embedding, dan ambang keputusan yang kini diberikan sebagai argumen. Sebelum dipindahkan, keluaran pipeline lama disimpan sebagai `tests/fixtures/golden_screening.json`.

## Reason

Reuse Policy pada governance. Logika penilaian sudah teruji, dan snapshot membuktikan pemindahan tidak mengubah hasil: kriteria lowongan identik, dan skor, peringkat, keputusan, serta alasan 13 kandidat sama.

## Impact

- Perubahan perilaku penilaian apa pun akan menggagalkan tes snapshot.
- `matching.py` dan `explanation.py` dikecualikan dari aturan panjang baris karena templat pesannya tidak dipecah.
- Penggabungan hasil LLM ke ekstraksi (`_merge_llm`) dan penulisan ulang narasi oleh LLM di dalam `explainer` tidak dibawa; narasi LLM kini berada di `hr_summary.py` sebagai langkah terpisah.
- Keputusan HR (mengubah rekomendasi) dan audit bias dari PoC lama tidak dibawa karena di luar spesifikasi sprint ini.

## Alternative Considered

- **Menulis ulang penilaian agar lebih sederhana:** berisiko mengubah hasil tanpa manfaat demo.
- **Normalisasi skor semantik relatif terhadap kandidat lain:** menghilangkan kebutuhan kalibrasi per backend, tetapi mengubah logika dan membuat skor seorang kandidat bergantung pada pelamar lain.
