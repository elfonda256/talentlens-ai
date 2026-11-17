# Sprint Report 05 — Demo Readiness

**Cabang:** `sprint-4` · **Commit:** `06a0224` · **Tanggal:** 17 November 2026

## Sprint Summary

Tampilan disiapkan untuk demo di depan tim rekrutmen: skor AI menjadi elemen paling menonjol,
kandidat terbaik mendapat badge, setiap kandidat punya panel rekomendasi tindak lanjut, keyakinan AI,
dan potensi risiko, dan dasbor kini merangkum seluruh lowongan. Semua istilah teknis (sumber
ringkasan, nama model, `GEMINI_API_KEY`, "templat", "kemiripan makna") dihapus dari layar.

Algoritma penilaian, parser, dan modul embedding tidak berubah. Skor, peringkat, dan keputusan lima
CV perusahaan identik sebelum dan sesudah sprint.

## Completed Tasks

| # | Prioritas | Hasil |
| --- | --- | --- |
| 1 | Alur Gemini tanpa pesan teknis | Ringkasan dibuat otomatis saat halaman dibuka. UI tidak lagi menampilkan sumber, label templat, atau pesan konfigurasi. Bila Gemini tidak tersedia, kalimat bawaan dengan nada yang sama dipakai. Penyebab teknis hanya tercatat di log server. **Gemini asli belum terverifikasi** karena `GEMINI_API_KEY` belum diatur di Railway. |
| 2 | Ringkasan bernada recruiter senior | Prompt Gemini ditulis ulang: hanya fakta CV dan lowongan, tanpa istilah sistem, maksimal 25 kata per butir. Kalimat bawaan juga diperbarui, misalnya "Kandidat kuat untuk Junior Architect: 3,9 tahun pengalaman relevan dan 7 dari 8 keterampilan wajib tertulis di CV." |
| 3 | Kartu kandidat | Cincin skor AI menjadi elemen pertama di setiap baris. Badge "Paling cocok" untuk peringkat 1 yang direkomendasikan dan "Sangat direkomendasikan" untuk kandidat yang jauh di atas batas dengan keyakinan tinggi. Baris juga menampilkan tingkat keyakinan AI. |
| 4 | Panel keputusan | Tiga panel di halaman kandidat: Rekomendasi tindak lanjut (dengan langkah bernomor), Keyakinan AI (tinggi/sedang/rendah beserta alasannya), dan Potensi risiko. Semuanya diturunkan dari hasil yang sudah ada ([TDR-0027](tdr/0027-assessment-panels-are-presentation-only.md)). |
| 5 | Dasbor enterprise | "Dasbor rekrutmen" dengan empat angka ringkas (lowongan, kandidat, direkomendasikan, perlu ditinjau), kartu lowongan dengan bilah sebaran keputusan, dan panduan tiga langkah saat belum ada data. |
| 6 | Audit istilah dan tampilan | Istilah teknis diganti ("Cara baca: OCR" → "Jenis dokumen: Hasil pindai"; "Kemiripan makna" → "Kesesuaian"). Baris CV yang terpotong oleh PDF digabung kembali. Diperiksa pada 1440 px dan 390 px. |
| 7 | Regression test | 171 tes backend lolos (8 tes baru), ruff bersih, lint dan build frontend bersih. Berkas algoritma tidak tersentuh. Lima CV perusahaan: hasil identik (tabel di bawah). |
| 8 | Deploy ulang staging | Railway disematkan ke commit `06a0224`; Vercel production dari commit yang sama. Hasil verifikasi di bagian Deployment. |

### Regression lima CV perusahaan

| Peringkat | Skor sebelum | Skor sesudah | Keputusan |
| --- | --- | --- | --- |
| 1 | 83,1 | 83,1 | Direkomendasikan |
| 2 | 77,2 | 77,2 | Direkomendasikan |
| 3 | 66,0 | 66,0 | Perlu ditinjau |
| 4 | 53,6 | 53,6 | Perlu ditinjau |
| 5 | 34,0 | 34,0 | Tidak lolos |

Diukur di lokal dengan berkas lowongan dan CV yang sama. Berkas aslinya tidak disimpan di repositori.

## Screenshot sebelum dan sesudah

- [Dasbor](screenshots/sprint-5/dasbor-sebelum-sesudah.png)
- [Peringkat kandidat](screenshots/sprint-5/peringkat-sebelum-sesudah.png)
- [Peringkat di ponsel](screenshots/sprint-5/ponsel-peringkat-sebelum-sesudah.png)

Tangkapan halaman rincian kandidat memuat riwayat kerja dari CV asli, sehingga tidak disimpan di
repositori publik. Gambarnya dikirim langsung ke Product Owner.

## Skill dan plugin Claude yang digunakan

| Skill | Dipakai untuk |
| --- | --- |
| `frontend-design` | Arah visual: skor sebagai satu elemen utama, warna brand dari logo, tidak ada kartu seragam atau label huruf kapital |
| `ui-design-review:ui-review` | Meninjau tangkapan layar hasil render di desktop dan ponsel |
| `design:accessibility-review` | Struktur semantik (judul, `aria-label` pada cincin skor dan bilah sebaran, `role="status"` saat memuat) |
| `engineering:code-review` | Memastikan perubahan tidak menyentuh algoritma dan tidak menambah kebocoran data |

## Modified Files

- Backend: `app/api/v1/jobs.py`, `app/schemas/screening.py`, `app/services/{hr_summary,match_breakdown}.py`, `tests/test_hr_summary.py`, `tests/test_jobs_api.py`
- Frontend: `src/app/{globals.css,page.tsx}`, `src/app/jobs/[jobId]/page.tsx`, `src/app/jobs/[jobId]/candidates/[candidateId]/page.tsx`, `src/components/{ai-summary,cv-evidence,page-shell,ranking-table,system-status}.tsx`, `src/components/ui/badge.tsx`, `src/lib/{api,labels}.ts`
- Dokumentasi: `docs/tdr/README.md`

## Added Files

- Backend: `app/services/assessment.py`, `tests/test_assessment.py`
- Frontend: `src/components/{assessment-panels,candidate-badges,score-ring}.tsx`
- Dokumentasi: `docs/SPRINT_REPORT_05.md`, `docs/tdr/0027-assessment-panels-are-presentation-only.md`, `docs/screenshots/sprint-5/` (3 gambar)

## Deleted Files

Tidak ada.

## Known Issues

- **Gemini belum terverifikasi di staging** karena `GEMINI_API_KEY` belum diatur. Sampai diatur, ringkasan memakai kalimat bawaan (tetap rapi, tanpa pesan teknis).
- **Data staging masih data uji sintetis** (lowongan "Junior Architect" dengan 8 kandidat). Lima CV perusahaan belum diunggah ke staging.
- Response API ringkasan masih memuat field `source` dan `note` untuk keperluan diagnosis; field ini tidak ditampilkan di UI.
- Mode gelap, tablet (768 px), dan pembaca layar belum diuji.

## Technical Debt

- Frontend belum punya tes otomatis; alur diverifikasi dengan skrip peramban.
- Ambang badge dan keyakinan berupa konstanta di `assessment.py`, belum dapat diatur lewat konfigurasi.

## Risks

| Risiko | Dampak | Mitigasi |
| --- | --- | --- |
| Gemini menjawab di luar format saat demo | Ringkasan memakai kalimat bawaan | Atur kunci hari ini dan uji satu kandidat sebelum demo |
| Memori Railway 1 GB (pemakaian sekitar 0,77 GB) | Layanan dapat restart saat beban puncak | Pertimbangkan paket Hobby; hindari unggahan besar saat demo |
| "Keyakinan AI" dibaca sebagai probabilitas | Salah tafsir oleh penonton | Panel menjelaskan cara mengukurnya; siapkan satu kalimat penjelasan saat demo |

## Technical Decision Records

- [TDR-0027](tdr/0027-assessment-panels-are-presentation-only.md): panel keputusan dan badge hanya menafsirkan hasil, tidak ikut menilai

Tidak ada perubahan arsitektur. Satu modul service dan satu field response ditambahkan.

## Recommended Next Sprint

**Gladi demo dan penggabungan ke `main`.**

1. Product Owner mengatur `GEMINI_API_KEY` (kunci baru) di Railway Variables.
2. Ganti data uji di staging dengan lima CV perusahaan.
3. Uji satu ringkasan Gemini, lalu gladi alur demo dari dasbor sampai rincian kandidat.
4. Gabungkan `sprint-4` ke `main` dan buat tag rilis.

## Suggested Git Commit Message

```
docs(sprint-5): sprint report, regression results and staging verification
```
