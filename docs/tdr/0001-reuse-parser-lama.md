# TDR-0001: Memakai ulang parser lama, bukan menulis ulang

**Status:** Diterima · **Tanggal:** 16 November 2026

## Konteks
PoC sebelumnya punya parser CV yang berjalan: pembaca dokumen, redaksi data pribadi, dan ekstraktor
berbasis aturan (sekitar 430 baris, sudah teruji pada 15 CV contoh). Arsitektur baru dari Sprint 1
belum punya parser.

## Keputusan
Tiga modul parser dipindahkan apa adanya ke proyek baru. Perubahan dibatasi pada: jalur impor,
penerjemahan komentar ke bahasa Inggris, pemformatan otomatis, satu nama variabel (`l` menjadi `line`),
dan kelas galat khusus untuk format yang tidak didukung. Ekspresi reguler, urutan langkah, dan semua
teks keluaran tidak disentuh.

## Alternatif yang ditolak
- **Menulis ulang dengan desain baru:** tidak menambah nilai demo dan membuang perilaku yang sudah teruji.
- **Mengganti dengan ekstraksi LLM:** bergantung pada akses LLM yang belum diputuskan, dan hasilnya tidak deterministik.

## Konsekuensi
- Integrasi selesai dalam satu sprint dengan risiko rendah.
- Kelemahan parser lama ikut terbawa; daftarnya ada di `docs/CV_PARSER.md`.
- Dua berkas dikecualikan dari aturan panjang baris karena ekspresi regulernya tidak dipecah.
