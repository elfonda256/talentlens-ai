# TDR-0024: Keterampilan perangkat lunak tidak pernah dianggap "tersirat"

**Status:** Diterima · **Sprint:** QA Phase 2 · **Tanggal:** 17 November 2026

## Decision

Kecocokan tersirat (setengah nilai dari kemiripan makna) tidak lagi diberikan untuk syarat yang seluruhnya berkategori `software` di taksonomi. Perangkat lunak hanya dihitung bila namanya tertulis di CV. Catatan recruiter memisahkan keterampilan yang tertulis dari yang hanya terindikasi, dan prompt Gemini melarang menyebut kandidat menguasai keterampilan di luar daftar yang tertulis.

## Reason

Dua CV perusahaan yang tidak menyebut Revit mendapat "Revit / BIM (tersirat)", karena kalimat lowongan yang menyebut tiga perangkat lunak mirip dengan kalimat CV yang menyebut dua di antaranya. Catatan lalu menulis "Menguasai Revit". Sistem tidak boleh mengarang kemampuan.

## Impact

- Perubahan aturan pencocokan yang disengaja dan diminta pada QA Phase 2. Pada 13 CV sintetis tidak ada skor yang berubah karenanya; pada data perusahaan, dua kandidat kehilangan setengah nilai untuk Revit.
- Keterampilan non-perangkat-lunak (misalnya Technical Drawing) masih dapat tersirat, dan ditampilkan terpisah sebagai "perlu dikonfirmasi".
- Bergantung pada kategori di taksonomi; keterampilan yang salah kategori akan mengikuti aturan yang salah.

## Alternative Considered

- **Menghapus kecocokan tersirat sepenuhnya:** paling aman, tetapi mengubah lebih banyak skor dan menghilangkan sinyal yang berguna untuk keterampilan yang jarang ditulis harfiah.
- **Menaikkan ambang kemiripan:** tidak menyelesaikan akar masalah dan nilainya berbeda antara TF-IDF dan E5.
