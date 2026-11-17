# TDR-0019: Tampilan penjelasan dihitung terpisah dan tidak ikut menilai

**Status:** Diterima · **Sprint:** 4 · **Tanggal:** 17 November 2026

## Decision

Rincian skor, kecocokan per syarat, relevansi tiap jabatan, dan kata kunci yang cocok disusun oleh modul baru `services/match_breakdown.py` dari hasil screening yang sudah tersimpan. Modul ini tidak dipanggil oleh pipeline penilaian dan tidak mengubah `ScreeningResult`. Komponen keterampilan ditampilkan sebagai dua baris (wajib dan tambahan) dengan pembagian 1 : 0,5 per syarat, sama seperti cara pencocok menimbangnya.

## Reason

Spesifikasi Sprint 4 meminta Explainable AI, Match Breakdown, dan penanda kata kunci tanpa mengubah penilaian. Menyusun penjelasan dari keluaran yang ada menjamin angka yang ditampilkan sama dengan angka yang dipakai untuk memeringkat. "Bonus Score" yang diminta tidak ada sebagai komponen tersendiri di rumus; memecah komponen keterampilan adalah cara menampilkannya tanpa mengarang angka.

## Impact

- Tes snapshot skor dari Sprint 3 tidak berubah dan tetap lolos.
- Tes baru memastikan jumlah lima baris sama dengan skor akhir, dan baris wajib ditambah tambahan sama dengan komponen keterampilan.
- Relevansi jabatan diperoleh dengan menanyakan aturan `relevant_months` milik pencocok satu jabatan demi satu, bukan dengan menyalin aturannya.
- Satu fungsi privat pencocok diganti namanya menjadi publik (`requirement_units`) agar dapat dipakai ulang; logikanya tidak berubah.
- Penjelasan dihitung pada setiap permintaan. Untuk puluhan kandidat biayanya dapat diabaikan; pemindaian kata kunci dilewati pada daftar peringkat karena tidak ditampilkan di sana.
- Penanda kata kunci bekerja per kata, sehingga nama perusahaan yang memuat kata kunci ikut ditandai.

## Alternative Considered

- **Menambah field penjelasan ke `ScreeningResult` di dalam pencocok:** satu kali hitung, tetapi mengubah pipeline yang sudah tervalidasi dan membuat hasil tersimpan milik Product Owner tidak cocok lagi.
- **Menambah "Bonus Score" sebagai komponen kelima di rumus:** mengubah skor dan peringkat, bertentangan dengan spesifikasi.
- **Menghitung penjelasan di frontend:** menduplikasi aturan bisnis dalam TypeScript.
