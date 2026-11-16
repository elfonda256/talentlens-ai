# Technical Decision Records

Satu berkas per keputusan penting. Format: konteks, keputusan, alternatif yang ditolak, konsekuensi.

| No | Keputusan | Status |
| --- | --- | --- |
| [0001](0001-reuse-parser-lama.md) | Memakai ulang parser lama, bukan menulis ulang | Diterima |
| [0002](0002-snapshot-keluaran-sebagai-kontrak.md) | Snapshot keluaran parser lama menjadi kontrak regresi | Diterima |
| [0003](0003-struktur-service.md) | Parser menjadi paket `services/cv_parsing` dengan satu pintu masuk | Diterima |
| [0004](0004-konfigurasi-eksplisit.md) | Tanggal acuan dan lokasi taksonomi diberikan dari `Settings` | Diterima |
| [0005](0005-yang-tidak-dibawa.md) | Kode yang belum dipakai tidak ikut dipindahkan | Diterima |
| [0006](0006-endpoint-tanpa-penyimpanan.md) | Endpoint parse tidak menyimpan apa pun dan mengembalikan profil lengkap | Diterima |
| [0007](0007-ocr-dependensi-opsional.md) | Tesseract menjadi dependensi opsional | Diterima |
