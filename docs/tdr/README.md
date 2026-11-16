# Technical Decision Records

Satu berkas per keputusan penting, dengan empat bagian yang ditetapkan governance:
**Decision**, **Reason**, **Impact**, **Alternative Considered**.

| No | Keputusan | Sprint |
| --- | --- | --- |
| [0001](0001-browser-calls-api-directly.md) | Peramban memanggil API secara langsung | 1 |
| [0002](0002-system-fonts.md) | Font sistem, bukan Google Fonts | 1 |
| [0003](0003-shadcn-components-written-by-hand.md) | Komponen shadcn/ui ditulis langsung, tidak lewat CLI | 1 |
| [0004](0004-reuse-legacy-parser.md) | Memakai ulang parser lama, bukan menulis ulang | 2 |
| [0005](0005-golden-snapshot-as-contract.md) | Snapshot keluaran parser lama menjadi kontrak regresi | 2 |
| [0006](0006-cv-parsing-service-package.md) | Parser menjadi paket `services/cv_parsing` dengan satu pintu masuk | 2 |
| [0007](0007-explicit-configuration.md) | Tanggal acuan dan lokasi taksonomi diberikan dari `Settings` | 2 |
| [0008](0008-unused-code-not-migrated.md) | Kode yang belum dipakai tidak ikut dipindahkan | 2 |
| [0009](0009-stateless-parse-endpoint.md) | Endpoint `POST /api/v1/cvs/parse` sebagai komponen pendukung, tanpa penyimpanan | 2 |
| [0010](0010-tesseract-optional.md) | Tesseract menjadi dependensi opsional | 2 |
| [0011](0011-git-workflow.md) | Git menjadi sumber kebenaran, dengan satu cabang per sprint | Pra-Sprint 3 |

TDR baru memakai nomor berikutnya dan nama berkas `NNNN-ringkasan-singkat.md`. TDR yang sudah diterima tidak diubah isinya;
bila keputusan berganti, buat TDR baru yang menyatakan menggantikan yang lama.
