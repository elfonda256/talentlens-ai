# TDR-0011: Git menjadi sumber kebenaran, dengan satu cabang per sprint

**Status:** Diterima · **Sprint:** Pra-Sprint 3 · **Tanggal:** 16 November 2026

## Decision

Repositori Git dibuat dengan `main` sebagai cabang utama. Sprint 1 dan 2 dicatat sebagai dua commit bertanda `sprint-1` dan `sprint-2`. Mulai Sprint 3, pekerjaan dilakukan di cabang `sprint-N`, digabung ke `main` setelah disetujui Product Owner, lalu diberi tag.

## Reason

Governance v1.1 menetapkan Git sebagai sumber kebenaran dan membatasi ZIP. Sprint 1 dan 2 dikerjakan sebelum repositori ada, jadi riwayatnya disusun dari dua arsip sprint.

## Impact

- Riwayat Sprint 1 dan 2 **disusun belakangan**: isi tiap commit sama dengan arsip sprint-nya, tetapi waktu commit adalah saat repositori dibuat, bukan saat kode ditulis.
- Setiap commit membawa baris `Co-Authored-By: Claude`, sehingga keterlibatan AI terlihat di riwayat.
- Selama GitHub belum terhubung ke sesi kerja, penyerahan memakai `git bundle`, bukan ZIP.

## Alternative Considered

- **Satu commit awal berisi semuanya:** lebih sederhana, tetapi menghapus batas antara Sprint 1 dan Sprint 2.
- **Memundurkan tanggal commit agar tampak bertahap:** ditolak karena memalsukan riwayat.
- **Git Flow dengan cabang develop dan release:** berlebihan untuk satu pengembang dan tiga hari.
