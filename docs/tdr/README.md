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
| [0012](0012-e5-default-tfidf-fallback.md) | Embedding E5 lokal sebagai default, TF-IDF sebagai cadangan otomatis | 3 |
| [0013](0013-faiss-flat-index.md) | FAISS `IndexFlatIP` dengan satu blok ID per kandidat | 3 |
| [0014](0014-reuse-scoring-pipeline.md) | Parser lowongan, pencocok, dan aturan keputusan dipindahkan tanpa mengubah logika | 3 |
| [0015](0015-gemini-explains-only.md) | Gemini hanya menjelaskan; REST dengan templat sebagai cadangan | 3 |
| [0016](0016-json-store-no-real-cvs-in-repo.md) | Penyimpanan JSON; CV asli dan dokumen perusahaan tidak masuk repositori | 3 |
| [0017](0017-jobs-api-blind-by-default.md) | API berpusat pada lowongan; identitas tersembunyi secara default | 3 |
| [0018](0018-three-routes-client-fetching.md) | Enam tampilan yang diminta ditempatkan pada tiga rute | 3 |
| [0019](0019-explanation-views-are-presentation-only.md) | Tampilan penjelasan dihitung terpisah dan tidak ikut menilai | 4 |
| [0020](0020-one-note-shape-for-gemini-and-template.md) | Catatan recruiter punya satu susunan, siapa pun penulisnya | 4 |
| [0021](0021-reject-cv-uploaded-as-job.md) | Dokumen yang tampak seperti CV ditolak saat diunggah sebagai lowongan | 4 |
| [0022](0022-ui-system-for-explanation.md) | Satu bahasa visual untuk penjelasan skor | 4 |
| [0023](0023-unread-section-is-unknown.md) | Bagian CV yang tidak terbaca berarti "tidak diketahui", bukan nol | QA 2 |
| [0024](0024-software-skills-are-never-implied.md) | Keterampilan perangkat lunak tidak pernah dianggap "tersirat" | QA 2 |
| [0025](0025-parser-hardening-from-real-layouts.md) | Parser diperkuat dari tata letak CV nyata, diuji dengan fixture sintetis | QA 2 |
| [0026](0026-server-side-relay-and-shared-key.md) | API dilindungi kunci bersama, dan peramban memanggilnya lewat relay di server frontend | Hardening |
| [0027](0027-assessment-panels-are-presentation-only.md) | Panel keputusan dan badge kandidat hanya menafsirkan hasil, tidak ikut menilai | 5 |

TDR baru memakai nomor berikutnya dan nama berkas `NNNN-ringkasan-singkat.md`. TDR yang sudah diterima tidak diubah isinya;
bila keputusan berganti, buat TDR baru yang menyatakan menggantikan yang lama.
