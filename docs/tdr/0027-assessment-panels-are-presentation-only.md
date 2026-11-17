# TDR-0027: Panel keputusan dan badge kandidat hanya menafsirkan hasil, tidak ikut menilai

**Status:** Diterima · **Sprint:** 5 — Demo Readiness · **Tanggal:** 17 November 2026

## Decision

1. Backend menambahkan objek `assessment` pada baris peringkat dan rincian kandidat. Isinya dibangun oleh `services/assessment.py` hanya dari hasil penyaringan yang sudah ada: rekomendasi tindak lanjut, tingkat keyakinan AI, daftar potensi risiko, dan penanda `highly_recommended`.
2. Aturannya tetap dan dapat diperiksa:
   - **Keyakinan rendah** bila ada bagian CV yang belum dapat dinilai.
   - **Keyakinan sedang** bila CV hasil pindai, ada bagian yang hanya terbaca sebagian (keyakinan bagian di bawah 0,6), skor berada dalam 5 poin dari batas 70 atau 45, atau ada keterampilan wajib yang hanya tersirat.
   - **Keyakinan tinggi** untuk selain itu.
   - **"Sangat direkomendasikan"** bila keputusan *Direkomendasikan*, keyakinan tinggi, dan skor minimal 10 poin di atas batas shortlist.
   - **"Paling cocok"** untuk peringkat 1 yang berstatus *Direkomendasikan*.
3. Gemini tetap hanya menyusun kalimat ringkasan dari fakta yang sudah dihitung. Bila Gemini tidak tersedia, ringkasan disusun dari kalimat bawaan dengan nada yang sama, dan UI tidak menampilkan sumber teknisnya.

## Reason

Sprint 5 meminta panel Hiring Recommendation, AI Confidence, dan Potential Risks serta badge Best Match dan Highly Recommended tanpa mengubah algoritma penilaian. Menurunkan semuanya dari hasil yang sudah ada membuat skor, peringkat, dan keputusan tetap identik, dan setiap badge dapat dijelaskan dengan satu kalimat saat wawancara.

## Impact

- Skor, peringkat, dan keputusan untuk lima CV perusahaan identik sebelum dan sesudah (83,1 / 77,2 / 66,0 / 53,6 / 34,0). Tes golden tidak berubah.
- "Keyakinan AI" mengukur kelengkapan pembacaan CV dan jarak dari batas keputusan, bukan probabilitas statistik. Hal ini dituliskan di panelnya.
- Response API bertambah satu objek kecil per kandidat. Klien lama tidak terpengaruh karena field lain tidak berubah.

## Alternative Considered

- **Meminta Gemini menilai keyakinan atau risiko:** melanggar aturan bahwa LLM tidak pernah menilai, dan hasilnya tidak dapat diulang.
- **Menghitung badge di frontend:** aturan akan tersebar di dua tempat dan tidak teruji oleh tes backend.
- **Probabilitas keyakinan dari model:** tidak ada data berlabel untuk mengkalibrasinya, sehingga angkanya akan menyesatkan.
