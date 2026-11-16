# TDR-0003: Parser menjadi paket `services/cv_parsing` dengan satu pintu masuk

**Status:** Diterima · **Tanggal:** 16 November 2026

## Konteks
Di PoC lama, urutan muat, redaksi, ekstraksi, dan penyesuaian OCR ditulis di dalam metode
`ScreeningService.ingest_file`, bercampur dengan deduplikasi dan penyimpanan.

## Keputusan
- Tiga modul lama tetap terpisah: `document_loader.py`, `pii.py`, `extractor.py`.
- Urutan langkahnya diangkat menjadi satu fungsi, `parse_cv(path)`, di `service.py`.
- Paket hanya mengekspor `parse_cv`, dua kelas galat, dan daftar ekstensi yang didukung.
- Rumus `candidate_id` dan penalti keyakinan OCR dipindahkan tanpa diubah.
- `taxonomy.py` diletakkan di `services/`, bukan di dalam paket parser, karena parser lowongan dan pencocok akan memakainya juga.

## Alternatif yang ditolak
- **Kelas `CVParser` dengan dependency injection:** tidak ada state yang perlu disimpan; fungsi lebih mudah dijelaskan dan diuji.
- **Satu berkas besar:** tiga langkah dengan tanggung jawab berbeda lebih mudah dibaca terpisah.

## Konsekuensi
- Pemanggil cukup tahu satu fungsi.
- Service bisa diuji tanpa HTTP; endpoint hanya menerjemahkan galat menjadi kode status.
