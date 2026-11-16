# Panduan Pengembangan

## Prinsip

1. Bila tidak menambah nilai demo, jangan dibuat.
2. Setiap berkas harus bisa dijelaskan dalam satu kalimat; bila tidak, pecah atau sederhanakan.
3. Tidak ada placeholder, tidak ada implementasi palsu. Kode yang masuk harus berjalan dan teruji.
4. Satu tanggung jawab per modul. Endpoint tipis, logika di service.
5. Batasan ditulis terbuka di README.

## Menambah endpoint backend

1. Definisikan bentuk request dan response di `app/schemas/<fitur>.py`.
2. Tulis logikanya di `app/services/<fitur>.py` sebagai fungsi biasa yang bisa diuji tanpa HTTP.
3. Buat `app/api/v1/<fitur>.py` dengan `APIRouter(tags=["<Fitur>"])`; endpoint hanya memanggil service.
4. Daftarkan router di `app/api/v1/router.py`.
5. Tulis tes di `tests/test_<fitur>.py`: minimal satu jalur berhasil dan satu jalur gagal.
6. Periksa tampilannya di Swagger (`/docs`): ringkasan, tag, dan contoh harus terbaca.

## Menambah tampilan frontend

1. Tambahkan fungsi pemanggil dan tipe response di `src/lib/api.ts`.
2. Buat komponen fitur di `src/components/`; pakai komponen dasar dari `src/components/ui/`.
3. Pasang di halaman pada `src/app/`.
4. Tangani tiga keadaan: memuat, berhasil, gagal.
5. Next.js yang dipakai adalah versi 16. Sebelum memakai API yang belum pernah dipakai di proyek ini,
   baca panduannya di `frontend/node_modules/next/dist/docs/`.

## Konfigurasi

Pengaturan baru ditambahkan sebagai field di `Settings` (`app/core/config.py`) dengan nilai default,
lalu dicatat di `.env.example` dan tabel environment variables pada README. Jangan membaca
`os.environ` di tempat lain.

## Logging

```python
import logging

logger = logging.getLogger(__name__)
logger.info("Parsed CV %s in %.0f ms", candidate_id, duration_ms)
```

- `INFO` untuk peristiwa yang ingin terlihat saat demo, `WARNING` untuk fallback, `ERROR` untuk kegagalan.
- Jangan mencatat isi CV atau data pribadi kandidat.
- Jangan memakai `print`.

## Definisi selesai

- [ ] `pytest -q`, `ruff check .`, dan `ruff format --check .` lolos di `backend/`.
- [ ] `npm run lint` dan `npm run build` lolos di `frontend/`.
- [ ] Fitur dicoba sendiri lewat antarmuka atau Swagger.
- [ ] README dan dokumen terkait diperbarui.
- [ ] Tidak ada kode mati, TODO, atau berkas yang tidak dipakai.

## Alur kerja Git

Git adalah sumber kebenaran proyek ([TDR-0011](tdr/0011-git-workflow.md)).

1. Buat cabang dari `main` untuk setiap sprint: `git switch -c sprint-3`.
2. Commit kecil mengikuti [konvensi commit](CONVENTIONS.md#konvensi-commit).
3. Sprint ditutup dengan `docs/SPRINT_REPORT_NN.md` dan TDR untuk setiap keputusan penting.
4. Setelah Product Owner menyetujui, gabung ke `main` dan beri tag: `git tag sprint-3`.

ZIP hanya dibuat atas permintaan Product Owner, sebagai cadangan milestone, atau untuk penyerahan akhir.
