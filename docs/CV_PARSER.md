# Parser CV

Mengubah satu berkas CV menjadi profil terstruktur. Kodenya berasal dari PoC sebelumnya
(`cv-screening-poc`) dan dipindahkan tanpa mengubah logika; keputusan di baliknya ada di
[docs/tdr/](tdr/README.md).

## Alur

```
berkas CV ──> document_loader ──> pii ──> extractor ──> CandidateProfile
              teks (atau OCR)     redaksi   aturan + taksonomi
```

| Langkah | Modul | Masuk | Keluar |
| --- | --- | --- | --- |
| 1. Baca dokumen | `cv_parsing/document_loader.py` | PDF, DOCX, TXT | teks dan metode (`text` atau `ocr`) |
| 2. Redaksi data pribadi | `cv_parsing/pii.py` | teks | teks tersamarkan dan data pribadi terpisah |
| 3. Ekstraksi | `cv_parsing/extractor.py` | teks tersamarkan | pengalaman, pendidikan, keterampilan, potongan teks |
| Orkestrasi | `cv_parsing/service.py` | path berkas | `CandidateProfile` |

PDF yang teksnya kurang dari 80 karakter dianggap hasil scan dan dibaca dengan Tesseract.
Keterampilan dikenali lewat `services/taxonomy.py`, yang membaca `backend/data/taxonomy/skills.json`.

## Pemakaian

```python
from pathlib import Path
from app.services.cv_parsing import parse_cv

profile = parse_cv(Path("cv.pdf"))
print(profile.total_experience_months, profile.skills)
```

Lewat API: `POST /api/v1/cvs/parse` dengan field multipart `file`. Tidak ada yang disimpan;
salinan sementara dihapus setelah diproses.

## Keluaran (`CandidateProfile`)

| Field | Isi |
| --- | --- |
| `candidate_id` | ID stabil dari hash email; orang yang sama mendapat ID yang sama di setiap unggahan |
| `file_name`, `source` | Nama berkas asli dan asal dokumen |
| `extraction_method` | `text` atau `ocr` |
| `pii` | Nama, email, telepon, gender, tanggal lahir, agama, status, alamat, institusi |
| `redacted_text` | Teks CV setelah data pribadi dibuang |
| `summary` | Bagian profil atau ringkasan, paling banyak 400 karakter |
| `experiences` | Jabatan, perusahaan, tahun mulai dan selesai, lama dalam bulan, deskripsi |
| `total_experience_months` | Total masa kerja; periode tumpang tindih dihitung sekali |
| `education` | Jenjang (3 = D3, 4 = S1/D4, 5 = S2, 6 = S3) dan bidang |
| `skills` | ID keterampilan kanonik dari taksonomi |
| `chunks` | Potongan teks hingga 170 karakter, untuk embedding pada sprint berikutnya |
| `extraction_confidence` | 0,4 sampai 1,0; dikali 0,85 untuk hasil OCR |
| `warnings` | Bagian yang tidak terbaca, atau catatan bahwa dokumen dibaca dengan OCR |

Field `pii` tidak boleh dipakai sebagai fitur penilaian. Modul berikutnya (embedding, pencocokan)
hanya membaca `redacted_text`, `chunks`, dan field terstruktur.

## Galat

| Kondisi | Di service | Di API |
| --- | --- | --- |
| Ekstensi tidak dikenal | `UnsupportedFormatError` | 415 |
| Berkas rusak, kosong, atau butuh OCR padahal Tesseract tidak terpasang | `UnreadableDocumentError` | 422 |
| Berkas melebihi `MAX_UPLOAD_MB` | tidak sampai ke service | 413 |

## Logging

Satu baris `INFO` per CV berisi ID kandidat, metode, jumlah pengalaman, pendidikan, keterampilan,
keyakinan, jumlah peringatan, dan durasi. Nama berkas dan isi CV tidak dicatat karena dapat
mengidentifikasi orang. Berkas yang gagal dibaca dicatat sebagai `WARNING` dengan jenis galatnya saja.

## Tes

| Berkas | Yang dijaga |
| --- | --- |
| `tests/test_cv_parsing_golden.py` | Keluaran sama persis dengan parser lama pada 14 CV berbasis teks; jalur OCR pada 1 CV hasil scan |
| `tests/test_cv_parsing_units.py` | Redaksi, perhitungan masa kerja, CV berbahasa Indonesia, pemuatan format, galat, isi log |
| `tests/test_cvs_api.py` | Kode status 200, 413, 415, 422 dan dokumentasi OpenAPI |

`tests/fixtures/golden_profiles.json` dibuat dengan menjalankan parser lama, sebelum dipindahkan,
pada berkas di `tests/fixtures/cvs/`. Bila logika parser sengaja diubah, snapshot ini harus dibuat
ulang dan perubahannya ditinjau baris demi baris.

## Batasan yang diwarisi dari parser lama

Tidak diperbaiki pada sprint ini karena memperbaikinya berarti mengubah logika:

- Nama diambil dari baris pertama yang tidak kosong (paling banyak lima kata). CV dengan judul lain di baris pertama akan salah dibaca.
- Baris berlabel `Status:` selalu dianggap status pernikahan dan dibuang, termasuk bila maksudnya status kerja.
- Bagian dikenali dari judul yang umum (`Experience`, `Pengalaman Kerja`, `Pendidikan`, dan sejenisnya). Tata letak tanpa judul bagian menghasilkan keyakinan rendah.
- CV dua kolom dapat terbaca dengan urutan baris yang tercampur.
- Semua CV contoh adalah data sintetis dengan format yang serupa; ketahanan pada CV nyata belum diukur.
