# TDR-0023: Bagian CV yang tidak terbaca berarti "tidak diketahui", bukan nol

**Status:** Diterima · **Sprint:** QA Phase 2 · **Tanggal:** 17 November 2026

## Decision

Bila lowongan mensyaratkan pengalaman atau pendidikan tetapi parser tidak menemukan satu pun entri pada bagian itu, komponen tersebut ditandai `unassessed`. Komponen itu tidak ikut dihitung: bobotnya dibagi rata-proporsional ke komponen yang dapat dinilai, tidak ada syarat wajib yang dilaporkan gagal, dan rekomendasinya selalu "Perlu ditinjau" dengan skor berlabel sementara. Parser juga melaporkan `section_confidence` per bagian (0 = tidak ditemukan, 0,3 = judul ada tetapi isinya tidak terbaca, 0,6–1,0 = terbaca).

## Reason

Pada QA Phase 1, satu kandidat yang memenuhi syarat ditolak otomatis dengan alasan "bidang pendidikan tidak sesuai" padahal bagiannya hanya tidak terbaca. Kegagalan sistem tidak boleh dicatat sebagai kekurangan kandidat.

## Impact

- Ini satu-satunya perubahan pada cara skor dijumlahkan, dan hanya berlaku ketika sebuah bagian tidak terbaca. Untuk CV yang terbaca, rumus dan bobotnya tidak berubah; tes snapshot membuktikannya.
- Skor sementara tidak sebanding penuh dengan skor kandidat lain, karena dihitung dari komponen yang lebih sedikit. Karena itu hasilnya tidak pernah "Direkomendasikan" maupun "Tidak lolos" secara otomatis.
- Kandidat tanpa pengalaman kerja sama sekali (lulusan baru tanpa bagian pengalaman) juga jatuh ke "Perlu ditinjau". Sistem tidak dapat membedakannya dari bagian yang gagal dibaca.
- Pengaman lama berbasis `extraction_confidence` tetap ada untuk CV hasil scan.
- Antarmuka, panel skor, dan catatan recruiter menampilkan "Belum dinilai", bukan 0.

## Alternative Considered

- **Tetap nol tetapi hanya diberi peringatan:** peringkat tetap menyesatkan dan kandidat tenggelam di bawah.
- **Mengeluarkan kandidat dari peringkat:** HR bisa tidak melihatnya sama sekali.
- **Mengisi komponen dengan nilai tengah:** mengarang angka yang tidak punya dasar.
