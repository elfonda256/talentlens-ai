# TDR-0001: Peramban memanggil API secara langsung

**Status:** Diterima · **Sprint:** 1 · **Tanggal:** 16 November 2026

## Decision

Frontend memanggil backend FastAPI langsung dari peramban lewat `src/lib/api.ts`. Next.js hanya menyajikan antarmuka; tidak ada proxy atau route handler di tengah.

## Reason

Satu lompatan lebih sedikit untuk dijelaskan dan di-debug. CORS cukup satu baris konfigurasi, dan Swagger backend menjadi satu-satunya kontrak API.

## Impact

- Backend harus mengizinkan asal frontend lewat `CORS_ORIGINS`.
- `NEXT_PUBLIC_API_URL` ditanam saat build; mengubahnya berarti build ulang.
- Tidak ada tempat menyimpan rahasia di sisi frontend, yang memang tidak dibutuhkan PoC ini.

## Alternative Considered

- **Proxy lewat route handler Next.js:** menyembunyikan alamat backend, tetapi menambah lapisan yang tidak punya nilai demo.
- **Server Components yang mengambil data:** mengikat tampilan ke fitur cache Next.js 16 yang tidak perlu dijelaskan saat interview.
