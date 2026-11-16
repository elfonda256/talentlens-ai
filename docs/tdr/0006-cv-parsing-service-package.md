# TDR-0006: Parser menjadi paket `services/cv_parsing` dengan satu pintu masuk

**Status:** Diterima · **Sprint:** 2 · **Tanggal:** 16 November 2026

## Decision

Tiga modul lama tetap terpisah. Urutan langkahnya diangkat menjadi satu fungsi, `parse_cv(path)`, di `service.py`. Paket hanya mengekspor `parse_cv`, dua kelas galat, dan daftar ekstensi. Rumus `candidate_id` dan penalti keyakinan OCR dipindahkan tanpa diubah. `taxonomy.py` diletakkan di `services/` karena akan dipakai modul lain.

## Reason

Di PoC lama, urutan langkah parser tertanam di `ScreeningService.ingest_file`, bercampur dengan deduplikasi dan penyimpanan. Memisahkannya membuat parser bisa dipanggil dan diuji sendiri.

## Impact

- Pemanggil cukup tahu satu fungsi.
- Service bisa diuji tanpa HTTP; endpoint hanya menerjemahkan galat menjadi kode status.

## Alternative Considered

- **Kelas `CVParser` dengan dependency injection:** tidak ada state yang perlu disimpan; fungsi lebih mudah dijelaskan.
- **Satu berkas besar:** tiga langkah dengan tanggung jawab berbeda lebih mudah dibaca terpisah.
