# TDR-0002: Snapshot keluaran parser lama menjadi kontrak regresi

**Status:** Diterima · **Tanggal:** 16 November 2026

## Konteks
Syarat sprint: keluaran harus tetap konsisten. Tanpa pembanding, "konsisten" tidak bisa dibuktikan.

## Keputusan
Sebelum memindahkan kode, parser lama dijalankan pada 15 CV contoh dan hasilnya disimpan sebagai
`tests/fixtures/golden_profiles.json`. Tes membandingkan keluaran parser baru dengan snapshot ini,
field demi field, untuk 14 CV berbasis teks.

CV hasil scan diperiksa lebih longgar (metode, keterampilan inti, masa kerja, bidang pendidikan),
karena teks hasil OCR berbeda tipis antarversi Tesseract.

## Alternatif yang ditolak
- **Hanya tes unit baru:** membuktikan kode baru benar menurut tes baru, bukan bahwa ia sama dengan yang lama.
- **Menyertakan parser lama di repositori sebagai pembanding:** kode ganda yang harus dirawat.

## Konsekuensi
- Setiap perubahan perilaku, sengaja atau tidak, langsung menggagalkan tes.
- Mengubah logika parser berarti membuat ulang snapshot dan meninjau selisihnya.
- 15 CV sintetis (372 KB) ikut tersimpan di repositori.
