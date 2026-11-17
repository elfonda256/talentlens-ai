# TalentLens AI — Inventaris Teknologi

**Diaudit:** 18 November 2026, 01.30 WIB, dari kode di cabang `sprint-4` (commit `7c1a08e`).
**Yang sedang berjalan:** frontend di Vercel dari commit `d753937`; backend di Railway dari commit
`28e6c7b`. Kode backend di `7c1a08e` identik dengan `28e6c7b`.
**Bukti dari staging:** endpoint health melaporkan `environment: production`, `embedding_backend: e5`,
`llm_summary: true`; respons peringkat melaporkan model `multilingual-e5-small`.

Kolom **Aktif di staging**: *Ya* berarti dipakai oleh aplikasi yang sedang berjalan; *Cadangan* berarti
ada di kode dan dipakai hanya bila kondisi tertentu terjadi; *Tidak* berarti hanya untuk pengembangan
atau pengujian.

---

## Ringkasan satu halaman

| Pertanyaan | Jawaban |
|---|---|
| Frontend | Next.js 16.4.6 (App Router) + React 19.3, TypeScript, Tailwind CSS 4.3 |
| Backend | FastAPI (Python 3.12), Uvicorn, Pydantic v2 |
| Model AI untuk pencocokan | `intfloat/multilingual-e5-small` lewat sentence-transformers, berjalan di server sendiri (CPU) |
| Model AI untuk teks | Google Gemini: `gemini-3.5-flash-lite` (utama), `gemini-3.6-flash` (cadangan), lewat REST API |
| Penilaian | Aturan tetap dan bobot tetap (35/25/25/15). LLM tidak pernah memberi skor |
| FAISS | **Dipakai.** `faiss-cpu`, indeks `IndexFlatIP` (pencarian eksak, cosine), dibangun setiap penyaringan |
| TF-IDF | **Ada di kode, tidak aktif di staging.** Backend cadangan bila model E5 gagal dimuat; dipakai di tes dan benchmark |
| Database | **Tidak ada database.** Satu berkas JSON di volume Railway |
| Hosting | Vercel (frontend) dan Railway (backend, Docker), keduanya region AS Timur |
| CI | **Tidak ada pipeline CI.** Tes dijalankan manual sebelum setiap deploy |

---

## 1. Frontend framework

| Teknologi | Dipakai di | Alasan dipilih | Aktif di staging |
|---|---|---|---|
| Next.js 16.4.6, App Router, `cacheComponents` | `frontend/src/app` | Halaman dan relay API di satu proyek; deploy langsung ke Vercel | Ya |
| React 19.3 | Semua komponen UI | Bawaan Next.js | Ya |
| Tailwind CSS 4.3 (`@tailwindcss/turbopack`) | `globals.css`, semua komponen | Token desain di satu tempat, tanpa berkas CSS per komponen | Ya |
| Komponen UI buatan sendiri gaya shadcn (`class-variance-authority`, `clsx`, `tailwind-merge`) | `frontend/src/components/ui` | Komponen kecil yang dimiliki penuh, tanpa pustaka UI besar | Ya |
| lucide-react | Ikon di semua halaman | Ikon garis yang konsisten | Ya |
| Turbopack | Build dan dev server | Bawaan Next.js 16 | Ya (saat build) |

## 2. Backend framework

| Teknologi | Dipakai di | Alasan dipilih | Aktif di staging |
|---|---|---|---|
| FastAPI | `backend/app/main.py`, `app/api/v1/*` | API REST dengan validasi otomatis lewat Pydantic | Ya |
| Uvicorn | Perintah `CMD` di `Dockerfile` | Server ASGI standar untuk FastAPI | Ya |
| Pydantic v2 | `app/schemas/*` | Skema data yang tervalidasi untuk CV, lowongan, dan hasil | Ya |
| pydantic-settings | `app/core/config.py` | Konfigurasi dari variabel lingkungan, dengan validasi (misalnya `API_KEY` wajib di produksi) | Ya |

## 3. Bahasa pemrograman

| Bahasa | Dipakai di | Aktif di staging |
|---|---|---|
| Python 3.12 | Seluruh backend: pembacaan CV, pencocokan, penilaian, API | Ya |
| TypeScript 5 | Seluruh frontend dan relay API | Ya |
| CSS (lewat Tailwind) | Tampilan | Ya |

## 4. Model AI

| Model | Dipakai di | Fungsi | Alasan dipilih | Aktif di staging |
|---|---|---|---|---|
| `intfloat/multilingual-e5-small` | `app/services/embedding.py` (`E5Embedder`) | Mengubah kalimat CV dan lowongan menjadi vektor untuk kesesuaian makna dan keterampilan tersirat | Kecil, berjalan di CPU, multibahasa (CV Indonesia bisa cocok dengan lowongan berbahasa Inggris), tanpa biaya per CV | Ya (`EMBEDDING_BACKEND=e5`) |
| `gemini-3.5-flash-lite` | `app/services/hr_summary.py` | Menulis ringkasan untuk hiring manager dan pertanyaan wawancara dari fakta yang sudah dihitung | Menjawab dalam 4–10 detik di staging; model stabil | Ya (model utama) |
| `gemini-3.6-flash` | `app/services/hr_summary.py` | Sama, dicoba sekali bila model utama gagal | Model stabil kedua untuk ketahanan | Cadangan |

Model E5 diunduh saat image Docker dibangun, sehingga server tidak mengunduh apa pun saat berjalan
(`HF_HUB_OFFLINE=1`). Gemini tidak pernah memberi skor atau keputusan.

## 5. Pustaka AI

| Pustaka | Dipakai di | Alasan dipilih | Aktif di staging |
|---|---|---|---|
| sentence-transformers | `embedding.py` | Cara standar memuat dan menjalankan model E5 | Ya |
| PyTorch (build CPU) | Dipasang di `Dockerfile` bila `INSTALL_E5=true` | Dibutuhkan sentence-transformers; build CPU agar image tidak membawa pustaka GPU | Ya |
| faiss-cpu | `app/services/vector_index.py` | Pencarian vektor yang cepat dan teruji | Ya |
| NumPy | Embedding, indeks, perhitungan skor | Operasi vektor | Ya |
| scikit-learn | `TfidfEmbedder` di `embedding.py` | TF-IDF kata dan karakter untuk mode tanpa model | Cadangan |
| httpx | `hr_summary.py` | Memanggil Gemini REST API dengan timeout dan retry | Ya |
| Google GenAI SDK | — | **Tidak dipakai.** Gemini dipanggil langsung lewat REST dengan httpx | — |

## 6. Pembacaan CV (CV parsing)

| Teknologi | Dipakai di | Alasan dipilih | Aktif di staging |
|---|---|---|---|
| Parser berbasis aturan buatan sendiri | `app/services/cv_parsing/extractor.py` | Mengenali judul bagian (Indonesia dan Inggris), riwayat kerja dan tanggalnya, pendidikan, keterampilan; hasilnya dapat diperiksa dan diuji | Ya |
| Penyamaran data pribadi (regex) | `app/services/cv_parsing/pii.py` | Email, telepon, NIK 16 digit, tanggal lahir, nama kampus disamarkan sebelum penilaian dan sebelum dikirim ke Gemini | Ya |
| Taksonomi keterampilan | `backend/data/taxonomy/skills.json` (19 keterampilan) | Daftar keterampilan dan sinonimnya untuk pencocokan eksak | Ya |
| Glosarium Indonesia–Inggris | `backend/data/taxonomy/id_en_glossary.json` (49 istilah) | Membantu mode TF-IDF mencocokkan CV Indonesia dengan lowongan Inggris | Cadangan (hanya mode TF-IDF) |
| Parser lowongan berbasis aturan | `app/services/jd_parsing.py` | Membaca minimal pengalaman, bidang dan jenjang pendidikan, keterampilan wajib dan tambahan | Ya |
| python-docx | `cv_parsing/document_loader.py` | Membaca CV Word, termasuk tabel | Ya |

## 7. Algoritma pencocokan (matching)

Berkas: `app/services/matching.py`. Aktif di staging: **Ya.**

| Komponen | Bobot | Cara menghitung |
|---|---|---|
| Keterampilan | 35% | Tiap syarat dicek lewat taksonomi (nilai penuh bila tertulis). Bila tidak tertulis, dicari bukti makna di CV lewat FAISS; kemiripan ≥ 0,55 dihitung "tersirat" dengan setengah nilai. Perangkat lunak (AutoCAD, Revit, dll.) tidak pernah dianggap tersirat. Keterampilan wajib berbobot 1, tambahan 0,5 |
| Pengalaman relevan | 25% | Hanya pengalaman yang relevan dengan keterampilan lowongan yang dihitung (bobot 1; 0,6; 0,25; atau 0 per jabatan). Nilai = 0,85 × min(1, tahun ÷ minimal) + 0,15 × kelebihan tahun (maks. 3 tahun). Bila lowongan tanpa minimal, nilai 1 |
| Kesesuaian isi CV | 25% | Setiap kalimat syarat dan tanggung jawab lowongan mencari potongan CV yang paling mirip (FAISS, cosine), dikalibrasi ke 0–1, lalu dirata-rata |
| Pendidikan | 15% | Bidang sesuai 1,0; serumpun 0,6; lainnya 0,15; dikali 0,7 bila jenjang di bawah syarat |

Bila suatu bagian CV tidak terbaca, komponennya tidak dinilai (bukan dianggap nol) dan bobotnya
dibagi ke komponen lain. Syarat gugur: pengalaman di bawah minimal, bidang pendidikan tidak sesuai,
jenjang pendidikan di bawah syarat.

## 8. Algoritma peringkat dan keputusan (ranking)

Berkas: `app/services/screening.py`, `app/services/explanation.py`. Aktif di staging: **Ya.**

| Langkah | Cara kerja |
|---|---|
| Skor | Jumlah poin keempat komponen, 0–100, dibulatkan satu desimal |
| Urutan | Skor tertinggi lebih dulu; bila sama, diurutkan menurut ID kandidat agar hasilnya selalu sama |
| Keputusan | Bagian CV tidak terbaca → Perlu ditinjau. Skor ≥ 70 tanpa syarat gugur → Direkomendasikan; ≥ 70 dengan syarat gugur → Perlu ditinjau. Skor 45 sampai di bawah 70 → Perlu ditinjau. Di bawah 45 → Tidak lolos, kecuali dokumen hasil pindai atau sulit dibaca → Perlu ditinjau |
| Sifat | Deterministik: CV dan lowongan yang sama selalu menghasilkan skor dan keputusan yang sama |

Tahap "recall" FAISS (`recall_candidates`, 50 teratas) hanya menentukan urutan pemrosesan. Semua
kandidat tetap dinilai; tidak ada yang tersaring di tahap ini.

## 9. Explainable AI

Dibangun dengan aturan yang transparan, bukan dengan metode penjelasan model. **SHAP dan LIME tidak
dipakai.** Aktif di staging: **Ya.**

| Bagian | Dipakai di | Yang dijelaskan |
|---|---|---|
| Rincian skor per komponen | `match_breakdown.py`, kartu "Dari mana skor ini berasal" | Bobot dan poin tiap komponen; jumlahnya tepat sama dengan skor |
| Status tiap syarat | `match_breakdown.py`, kartu "Kecocokan dengan syarat lowongan" | Tertulis, tersirat, atau belum ditemukan, beserta kata yang ditemukan |
| Bukti dari CV | `matching.py` (FAISS `best_match`), kartu "Bukti dari CV" | Kalimat CV yang paling mendukung setiap syarat lowongan |
| Alasan dan narasi | `explanation.py` | Kontributor skor terbesar, keterampilan yang cocok dan hilang, syarat gugur |
| Penilaian lanjutan | `assessment.py` | Rekomendasi tindak lanjut, tingkat keyakinan (dari kelengkapan pembacaan dan jarak skor dari batas), potensi risiko |
| Penjelasan keputusan | `frontend/src/lib/decision.ts`, `components/decision-explainer.tsx` | Aturan keputusan diperiksa satu per satu untuk tiap kandidat, dan posisi skor pada zona 0–100 |
| Ringkasan untuk hiring manager | `hr_summary.py` (Gemini, dengan templat cadangan) | Kalimat yang dirangkai dari fakta yang sudah dihitung |

## 10. Database dan penyimpanan

| Teknologi | Dipakai di | Alasan dipilih | Aktif di staging |
|---|---|---|---|
| Berkas JSON (`JsonStore`) | `app/services/store.py`, berkas `state.json` | Cukup untuk proof of concept satu server; tanpa layanan database tambahan | Ya |
| Volume Railway `screening-data` | Dipasang di `/srv/storage` | Data tetap ada saat container dimulai ulang | Ya |
| Database (PostgreSQL, dll.) | — | **Tidak dipakai.** | — |

Yang disimpan: profil lowongan, profil kandidat hasil parsing (data pribadi disimpan terpisah dari
teks yang dinilai), hasil penyaringan, dan ringkasan Gemini yang berhasil. **Berkas CV asli tidak
disimpan**; berkas hanya ada di folder sementara selama dibaca.

## 11. Platform deployment

| Platform | Dipakai untuk | Konfigurasi | Aktif |
|---|---|---|---|
| Vercel | Frontend Next.js | Proyek `talentlens-ai`, root `frontend`, alias `talentlens-ai-azure.vercel.app`, region `iad1` (AS Timur), Vercel Authentication di semua deployment | Ya |
| Railway | Backend FastAPI | Builder Dockerfile, environment `staging`, health check `/api/v1/health`, volume `/srv/storage`, memori 1 GB, region AS Timur, disematkan ke satu commit | Ya |
| Docker | Image backend (`python:3.12-slim`, Tesseract, model E5 di dalam image) | `backend/Dockerfile` | Ya (di Railway) |
| Docker Compose | Menjalankan frontend dan backend di mesin lokal | `docker-compose.yml`, `frontend/Dockerfile` | Tidak (hanya lokal) |

## 12. CI dan pengujian

| Teknologi | Dipakai di | Alasan dipilih | Aktif |
|---|---|---|---|
| pytest | `backend/tests` (14 berkas, 113 fungsi tes, **178 kasus uji**, semuanya lolos) | Tes unit, API, keamanan, dan golden | Dijalankan manual sebelum deploy |
| Ruff | `backend/pyproject.toml` | Lint dan format Python | Manual |
| ESLint (`eslint-config-next`) dan Prettier | `frontend` | Lint dan format TypeScript | Manual |
| Pemeriksaan tipe TypeScript | `next build` | Build gagal bila tipe salah | Ya, di setiap build Vercel |
| Pipeline CI (GitHub Actions, dll.) | — | **Tidak ada di repositori.** | — |
| Tes otomatis frontend | — | **Tidak ada.** Frontend diperiksa dengan screenshot Playwright saat pengembangan | — |

## 13. Kerangka regresi

| Teknologi | Dipakai di | Fungsi | Aktif |
|---|---|---|---|
| Snapshot golden | `tests/test_cv_parsing_golden.py`, `tests/test_screening_golden.py`, `tests/fixtures/golden_*.json` | Hasil parsing dan penyaringan harus identik dengan snapshot yang disetujui | Ya, bagian dari 178 tes |
| Fixture tata letak CV nyata | `tests/test_real_cv_layouts.py`, `tests/fixtures/real_layouts/*.txt` | Tata letak dari CV perusahaan, tanpa data pribadi | Ya, bagian dari 178 tes |
| Architecture Golden Benchmark v1.0.0 | Cabang `dataset/architecture-v1` (commit `92cc4e0`): 5 lowongan, 20 CV, 20 fixture regresi, JSON Schema, `dataset/tools/run_pipeline.py` | Benchmark beku dengan hasil yang diharapkan ditulis sebelum sistem dijalankan; dijalankan dalam mode TF-IDF | Dijalankan manual. **Belum digabung ke `sprint-4`** dan tidak ikut di-deploy |

## 14. API eksternal

| API | Dipakai di | Fungsi | Aktif di staging |
|---|---|---|---|
| Google Gemini API (`generativelanguage.googleapis.com/v1beta`, `generateContent`) | `hr_summary.py` | Ringkasan hiring manager dan pertanyaan wawancara. Thinking `low`, keluaran JSON, timeout 15 detik, 3 percobaan pada model utama lalu 1 pada cadangan, templat bila semua gagal | Ya |
| Hugging Face Hub | `Dockerfile`, saat build | Mengunduh model E5 sekali ke dalam image | Hanya saat build |
| LinkedIn, Jobstreet, Kalibrr, Indeed, email, folder bersama | Halaman "Pengumpulan CV" | **Belum terhubung.** Hanya ditampilkan sebagai integrasi tahap berikutnya | Tidak |

## 15. Autentikasi

| Teknologi | Dipakai di | Fungsi | Aktif di staging |
|---|---|---|---|
| Vercel Authentication (Deployment Protection) | Semua deployment Vercel | Hanya akun tim Vercel (atau tautan akses sementara) yang bisa membuka aplikasi | Ya |
| Kunci API bersama (`X-API-Key`) | `app/core/security.py`; relay `frontend/src/app/api/backend/[...path]/route.ts` | Backend menolak permintaan tanpa kunci (perbandingan waktu konstan). Kunci hanya ada di server Next.js (`BACKEND_API_KEY`), tidak pernah sampai ke browser | Ya |
| Pembatasan CORS dan dokumentasi API | `app/main.py` | CORS hanya untuk domain Vercel; `/docs` dan `/openapi.json` dimatikan di produksi; galat tidak menampilkan stack trace | Ya |
| Akun pengguna dan peran | — | **Tidak ada.** Masuk tahap produksi | — |

## 16. Penanganan berkas

| Teknologi | Dipakai di | Fungsi | Aktif di staging |
|---|---|---|---|
| python-multipart (unggahan FastAPI) | `app/api/v1/jobs.py`, `cvs.py` | Unggah lowongan dan beberapa CV sekaligus | Ya |
| Validasi unggahan | `app/api/v1/uploads.py` | Hanya `.pdf`, `.docx`, `.txt`, `.md`; maksimal 5 MB per berkas (`MAX_UPLOAD_MB`) | Ya |
| Salinan sementara | `uploads.py` (`tempfile.TemporaryDirectory`) | Berkas hanya ada di disk selama dibaca, lalu dihapus | Ya |
| Relay Next.js | `frontend/src/app/api/backend/[...path]/route.ts` | Meneruskan unggahan dan permintaan dari browser ke backend | Ya |

## 17. Pemrosesan PDF

| Teknologi | Dipakai di | Fungsi | Aktif di staging |
|---|---|---|---|
| pdfplumber | `cv_parsing/document_loader.py` | Mengambil teks dari PDF digital | Ya |
| pypdfium2 + Pillow | `document_loader.py` | Merender halaman PDF menjadi gambar untuk OCR | Ya (hanya untuk PDF hasil pindai) |
| Tesseract OCR (`tesseract-ocr`, `tesseract-ocr-ind`) + pytesseract | `Dockerfile`, `document_loader.py` | Membaca PDF hasil pindai, bahasa Inggris dan Indonesia | Ya (hanya bila teks PDF kurang dari 80 karakter) |

## 18. Pencarian vektor: FAISS

**Dipakai di implementasi akhir.**

| Hal | Keterangan |
|---|---|
| Pustaka | `faiss-cpu` |
| Berkas | `app/services/vector_index.py` (`FaissIndex`), dipanggil dari `screening.py` dan `matching.py` |
| Jenis indeks | `IndexFlatIP` pada vektor yang sudah dinormalisasi, jadi inner product sama dengan cosine. Pencarian eksak, bukan perkiraan |
| Dipakai untuk | (1) mencari kalimat CV yang paling mendukung setiap syarat lowongan, dibatasi per kandidat dengan `IDSelectorRange`; (2) bukti untuk keterampilan tersirat; (3) urutan recall awal |
| Kapan dibangun | Di memori, setiap kali penyaringan dijalankan; tidak disimpan ke disk |
| Aktif di staging | Ya |

## 19. TF-IDF

**Ada di kode, tetapi tidak aktif di aplikasi yang sedang berjalan.**

| Hal | Keterangan |
|---|---|
| Berkas | `app/services/embedding.py` (`TfidfEmbedder`): TF-IDF kata (1–2 gram) dan karakter (3–5 gram) dengan scikit-learn, plus glosarium Indonesia–Inggris; LSA hanya bila korpus ≥ 300 dokumen |
| Peran | Cadangan bila model E5 tidak bisa dimuat (`EMBEDDING_BACKEND=auto`), mode tanpa model untuk pengembangan, dan mode yang dipakai tes dan Golden Benchmark agar hasilnya bisa diulang tanpa mengunduh model |
| Aktif di staging | Tidak. Staging memakai `EMBEDDING_BACKEND=e5`, yang tidak jatuh ke TF-IDF: bila model E5 gagal dimuat, penyaringan berhenti dengan galat, bukan diam-diam berganti metode |

## 20. Model embedding

| Hal | Keterangan |
|---|---|
| Model | `intfloat/multilingual-e5-small` |
| Dimuat oleh | sentence-transformers, PyTorch CPU |
| Cara pakai | Prefiks `query:` untuk kalimat lowongan dan `passage:` untuk potongan CV, vektor dinormalisasi, kemiripan dikalibrasi ke 0–1 (rentang 0,75–0,88) |
| Lokasi | Di dalam image Docker backend; tidak memanggil layanan luar saat berjalan |
| Aktif di staging | Ya |

---

## Batasan yang perlu disebut bila ditanya

- Tidak ada database; data disimpan dalam satu berkas JSON di satu server.
- Tidak ada pipeline CI dan tidak ada tes otomatis frontend.
- Server backend memiliki memori 1 GB dan berada di region AS Timur.
- Golden Benchmark berada di cabang terpisah dan dijalankan dalam mode TF-IDF, sedangkan staging memakai E5.
- Belum ada akun pengguna, peran, maupun jejak audit.
