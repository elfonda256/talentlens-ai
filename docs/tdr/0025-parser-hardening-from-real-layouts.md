# TDR-0025: Parser diperkuat dari tata letak CV nyata, diuji dengan fixture sintetis

**Status:** Diterima · **Sprint:** QA Phase 2 · **Tanggal:** 17 November 2026

## Decision

1. Judul bagian dicocokkan lewat kunci ternormalisasi (huruf kecil, tanpa spasi dan tanda baca, bentuk jamak diabaikan) terhadap daftar frasa Indonesia dan Inggris, sehingga "EXPERIENCES", "Work Experience:", dan "W O R K  E X P E R I E N C E" bermuara ke entri yang sama. Judul yang sebaris dengan isinya dikenali untuk frasa ekspor portal kerja berbahasa Indonesia.
2. Jabatan dan perusahaan diambil dari baris yang tepat: baris di atas tanggal, baris di bawah tanggal, atau pola "Perusahaan, Jabatan". Durasi dalam kurung diabaikan, dan "PROJECT :" di dalam pengalaman tidak memutus bagian.
3. Pendidikan yang masih ditempuh disimpan terpisah (`education_in_progress`) dan tidak dihitung sebagai gelar.
4. Penyamaran data pribadi diperluas (format telepon, tanggal lahir dalam kalimat, baris kontak, nama kampus utuh) dan diulang pada setiap kutipan sebelum dikirim ke Gemini.
5. Lima fixture di `tests/fixtures/real_layouts/` meniru tata letak yang gagal, dengan isi karangan. CV asli tidak disimpan.

## Reason

QA Phase 1: pengalaman kerja tidak terbaca pada 4 dari 5 CV perusahaan. Fixture lama semuanya memakai judul bagian yang rapi, sehingga kegagalan ini tidak pernah terlihat.

## Impact

- 13 CV sintetis lama: profil hasil parser identik. Satu skor berubah 0,1 poin (6,5 menjadi 6,4) karena ejaan baru di taksonomi menggeser kosakata TF-IDF; dicatat di tes snapshot.
- Skor kelima CV perusahaan berubah karena isinya sekarang terbaca. Itu tujuan fase ini.
- `extraction_confidence` lama dipertahankan agar keluaran tetap sebanding dengan PoC; `section_confidence` adalah ukuran baru yang lebih rinci.
- Heuristik "baris pendek di bawah tanggal adalah jabatan" dapat keliru pada butir uraian yang sangat pendek.
- Belum ditangani: tata letak dua kolom yang terbaca berselang-seling, dan CV tanpa judul bagian sama sekali (jatuh ke TDR-0023).

## Alternative Considered

- **Mengganti parser aturan dengan ekstraksi LLM:** lebih tahan terhadap variasi, tetapi mengirim isi CV ke pihak ketiga, tidak deterministik, dan melanggar batas "tanpa perubahan arsitektur".
- **Menyimpan CV asli sebagai fixture:** paling setia, tetapi repositori ini publik.
