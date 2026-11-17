# TDR-0020: Catatan recruiter punya satu susunan, siapa pun penulisnya

**Status:** Diterima · **Sprint:** 4 · **Tanggal:** 17 November 2026

## Decision

`HRSummary` berubah dari satu paragraf menjadi susunan tetap: kesimpulan, kecocokan, kekuatan, kekurangan, risiko, hal yang perlu digali saat wawancara, dan alasan rekomendasi. Gemini diminta membalas dalam JSON dengan kunci tersebut; jawabannya divalidasi. Templat bawaan mengisi susunan yang sama dari fakta yang sama dan dipakai bila kunci tidak ada, panggilan gagal, jawaban bukan JSON, atau ada bagian wajib yang kosong.

## Reason

Spesifikasi Sprint 4 meminta catatan bergaya recruiter dan cadangan yang "hampir identik". Susunan yang sama membuat halaman tidak berubah bentuk saat Gemini tidak tersedia, dan memudahkan HR memindai kekuatan serta kekurangan. Validasi mencegah jawaban setengah jadi tampil di layar.

## Impact

- **Prompt baru dengan keluaran JSON belum diuji terhadap API Gemini asli.** Panggilan uji sederhana sudah terbukti berjalan di mesin Product Owner; bila model menjawab di luar format, templat yang tampil dan labelnya menyebut penyebabnya.
- Butir "hal yang perlu digali saat wawancara" adalah saran fokus, bukan fitur daftar pertanyaan wawancara yang dikeluarkan dari lingkup pada Sprint 3.
- Catatan tersimpan dengan bentuk lama diabaikan dan dibuat ulang.
- Templat memakai aturan sederhana untuk risiko (CV hasil scan, banyak keterampilan wajib belum terbukti, pengalaman jauh di atas syarat); ini penanda untuk diperiksa, bukan penilaian.
- Field `text` pada response dihapus; frontend diperbarui bersamaan.

## Alternative Considered

- **Tetap satu paragraf bebas:** lebih "alami", tetapi tampilan Gemini dan templat akan berbeda jauh dan sulit dipindai.
- **`responseMimeType: application/json` pada request:** memaksa JSON di sisi API, tetapi menambah parameter yang belum dapat diuji dari lingkungan pembuatan. Dipilih instruksi di prompt ditambah pengurai yang toleran.
- **Memakai Gemini untuk menilai risiko secara bebas:** berisiko menambah dugaan di luar data.
