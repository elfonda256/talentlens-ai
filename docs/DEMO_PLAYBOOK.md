# TalentLens AI — Panduan Demo

**Acara:** presentasi TalentLens AI untuk Allure Industries, 18 November 2026
**Audiens:** HR Director, Head of Talent Acquisition, CIO, CEO
**Alamat demo:** `https://talentlens-ai-azure.vercel.app`
**Kondisi staging (dicek 18 November, 01.45 WIB):** 1 lowongan (Junior Architect), 5 CV dari
perusahaan, 3 Direkomendasikan, 2 Perlu ditinjau, 0 Tidak lolos. Skor 91,3 · 87,8 · 83,4 · 66,5 · 46,3.
Kelima ringkasan AI sudah dibuat dan tersimpan, jadi terbuka seketika.

**Tiga kalimat yang perlu dihafal**

- "Aturan yang memberi skor. AI yang menjelaskan. HR yang memutuskan."
- "CV yang sama, lowongan yang sama, skornya selalu sama."
- "Setiap angka di layar ini bisa ditelusuri sampai ke kalimat di CV."

---

## Peta kandidat

Nama disembunyikan di layar. Sebut kandidat dengan nomor peringkatnya.

| Peringkat | Skor | Keputusan | Dipakai untuk menunjukkan |
|---|---|---|---|
| #1 | 91,3 | Direkomendasikan, "Paling cocok" | Penjelasan lengkap: skor, ringkasan AI, pertanyaan wawancara, alasan keputusan, rincian skor |
| #2 | 87,8 | Direkomendasikan | Kenapa 6,5 tahun pengalaman kalah dari 3,9 tahun |
| #3 | 83,4 | Direkomendasikan | Revit belum terlihat di CV: mengurangi skor, tetapi bukan syarat gugur |
| #4 | 66,5 | Perlu ditinjau | Zona tinjau, ditambah bidang dan jenjang pendidikan tidak sesuai |
| #5 | 46,3 | Perlu ditinjau | Hanya bila ditanya: pengalaman relevan 0,3 tahun, sedikit di atas batas 45 |

---

## Persiapan

### Malam ini atau pagi sebelum demo

1. **Baca kelima ringkasan AI dan pertanyaan wawancaranya.** Semuanya tersimpan, jadi yang Anda
   baca sama dengan yang dilihat audiens. Pastikan tidak ada yang bertentangan dengan angka di layar.
2. **Ambil screenshot cadangan** (lihat bagian "Rencana cadangan: internet lambat").
3. **Rekam layar 5 menit** dengan alur versi 5 menit. Ini cadangan terakhir.
4. **Latihan alur 10 menit sekali, bersuara, dengan timer.**

### 30 menit sebelum mulai

1. **Login ke Vercel** di browser demo, dengan akun pemilik proyek. Semua halaman dilindungi login
   Vercel. Ada tautan akses, tetapi **berakhir 18 November pukul 12.24 WIB**; jangan diandalkan.
2. **Panaskan sistem:** buka Dashboard, halaman lowongan, dan kelima kandidat sekali.
3. **Buka tab dengan urutan ini**, supaya Anda tinggal berpindah tab:
   Dashboard → Pengumpulan CV → Halaman lowongan → Kandidat #1 → Kandidat #2 → Kandidat #4.
4. Zoom browser 110–125% untuk proyektor. Tutup aplikasi lain dan notifikasi.
5. Pastikan **"Tampilkan nama kandidat" tidak dicentang**. Mereka pelamar sungguhan.
6. Siapkan hotspot ponsel.

### Halaman pertama yang dibuka

**Dashboard rekrutmen.** Satu layar langsung menunjukkan gambaran utuh: satu lowongan, lima
kandidat, tiga direkomendasikan, dua perlu ditinjau.

---

## Layar demi layar

Setiap layar berisi: apa yang diklik, apa yang diucapkan, pertanyaan HR yang mungkin muncul, dan
jawaban terbaiknya. Aturan menjawab: **satu atau dua kalimat, tunjukkan di layar, lalu berhenti.**

### Layar 1 — Dashboard rekrutmen

**Klik:** tidak ada. Biarkan audiens membaca empat angka di atas.

**Ucapkan:**
> "Membaca CV tahap pertama memakan waktu beberapa menit per CV, dan itu bagian pekerjaan recruiter
> yang paling sedikit nilainya. TalentLens mengerjakan tahap pertama itu dalam hitungan detik, dan
> menjelaskan setiap keputusannya. Ini satu lowongan sungguhan dari tim Bapak/Ibu, Junior Architect,
> dengan lima CV yang diberikan kepada kami: tiga direkomendasikan untuk wawancara, dua perlu keputusan
> HR."

**Tunjuk:** empat angka ringkasan, lalu bilah warna pada kartu lowongan (hijau direkomendasikan,
kuning perlu ditinjau).

**Pertanyaan HR:** "Berapa lama proses penyaringannya?"
**Jawaban:** "Beberapa detik untuk lima CV ini. Membaca setiap CV dan mencocokkannya dengan lowongan
dilakukan otomatis; HR tinggal meninjau hasilnya."

**Pertanyaan HR:** "Apa nilai bisnisnya?"
**Jawaban:** "Waktu membaca CV tahap pertama turun dari menit per CV menjadi detik per batch, semua
kandidat dinilai dengan aturan yang sama, dan hiring manager menerima ringkasan beralasan serta
pertanyaan wawancara, bukan tumpukan PDF. Berapa CV yang biasanya masuk untuk satu lowongan di sini?"
Jangan menyebut angka ROI yang belum diukur.

### Layar 2 — Pengumpulan CV

**Klik:** **Pengumpulan CV** di header.

**Ucapkan:**
> "Saat ini CV masuk lewat unggahan manual, dan itu yang kami pakai di demo ini. Halaman ini
> menunjukkan arah produk berikutnya: situs karier, kotak masuk email, folder bersama, LinkedIn,
> Jobstreet, Kalibrr, dan Indeed. Semuanya ditandai sebagai integrasi tahap produksi berikutnya. Semua
> akan terhubung lewat akses resmi, tidak dengan scraping, dan semua sumber masuk ke mesin penyaringan
> dan aturan yang sama."

**Tunjuk:** diagram Sumber lamaran → Lapisan integrasi (tahap berikutnya) → Mesin penyaringan
TalentLens (sudah berjalan), lalu empat prinsip integrasi di bawah.

**Jangan** mengatakan ada sumber yang sudah terhubung. Belum ada.

**Pertanyaan HR:** "Sekarang sudah tersambung ke LinkedIn atau Jobstreet?"
**Jawaban:** "Belum. Itu tahap produksi berikutnya. Saat ini CV masuk lewat unggahan. Halaman ini
menunjukkan cara tiap sumber akan terhubung dan apa yang dibutuhkan."

**Pertanyaan HR:** "Kenapa tidak di-scrape saja?"
**Jawaban:** "Scraping melanggar ketentuan penggunaan platform tersebut dan berisiko terhadap data
pribadi menurut UU PDP. Kami hanya menghubungkan lewat program mitra atau API resmi dari setiap
platform."

**Pertanyaan HR:** "Berapa lama integrasinya?"
**Jawaban:** Jangan menjanjikan tanggal. "Kotak masuk email dan folder bersama paling cepat, karena
hanya butuh akses dari tim IT. Portal lowongan bergantung pada persetujuan akses mitra dari setiap
platform."

### Layar 3 — Halaman lowongan: kriteria penilaian

**Klik:** **Dashboard** → kartu **Junior Architect** → buka **Kriteria penilaian**.

**Ucapkan:**
> "Sebelum menilai siapa pun, sistem membaca deskripsi lowongan dan mengubahnya menjadi kriteria:
> minimal dua tahun pengalaman, pendidikan arsitektur atau desain interior, delapan keterampilan wajib,
> dan dua keterampilan tambahan. HR bisa memeriksa kriteria ini sebelum memercayai peringkatnya. Kalau
> deskripsi lowongannya keliru, kelihatan di sini lebih dulu."

**Pertanyaan HR:** "Bisakah kriteria atau bobotnya diubah per posisi?"
**Jawaban:** "Kriteria diambil otomatis dari deskripsi lowongan dan ditampilkan sebelum penyaringan.
Bobotnya sengaja sama untuk semua kandidat, supaya hasilnya konsisten dan bisa diaudit. Pengaturan per
posisi adalah tahap berikutnya."

### Layar 4 — Halaman lowongan: peringkat dan cara keputusan dibuat

**Klik:** gulir ke **Peringkat kandidat**. Biarkan filter pada semua kandidat. Lalu gulir sedikit ke
bawah ke kartu **Cara keputusan dibuat**.

**Ucapkan (peringkat):**
> "Ini peringkatnya. Angka besar adalah skor AI dari 100. Peringkat satu mendapat badge 'Paling
> cocok'. Nama disembunyikan secara bawaan, jadi penilaian tahap pertama berlangsung tanpa melihat
> identitas. Setiap baris sudah menyebut satu hal yang perlu HR ketahui, misalnya berapa keterampilan
> wajib yang ditemukan dan berapa tahun pengalaman relevannya."

**Ucapkan (cara keputusan dibuat):**
> "Dan ini aturannya. Setiap titik adalah satu kandidat pada skala 0 sampai 100. Skor 70 ke atas
> direkomendasikan, 45 sampai di bawah 70 perlu ditinjau, di bawah 45 tidak lolos. Skor tinggi pun
> tetap masuk tinjauan bila ada syarat gugur: pengalaman minimal, atau bidang dan jenjang pendidikan.
> Zona merah kosong karena tidak ada kandidat di lowongan ini yang skornya di bawah 45."

**Pertanyaan HR:** "Bisakah AI ini diskriminatif soal gender, usia, agama, atau kampus?"
**Jawaban:** "Skor hanya memakai empat hal: keterampilan, pengalaman relevan, bidang pendidikan, dan
kesesuaian isi CV dengan lowongan. Nama, foto, usia, gender, agama, dan alamat tidak pernah masuk ke
skor, dan nama disembunyikan di layar secara bawaan."

**Pertanyaan HR:** "Kenapa #5 tidak ditolak?"
**Jawaban:** "Skornya 46,3, sedikit di atas batas 45, jadi sistem menyerahkannya ke HR alih-alih
menolaknya. Alasannya tertulis di halaman kandidat: pengalaman relevan baru 0,3 tahun dan pendidikannya
belum sesuai. Batasnya adalah aturan bisnis yang bisa diperketat."
Jangan dibahas kalau tidak ditanya.

### Layar 5 — Kandidat #1 (layar utama)

**Klik:** baris **#1**. Telusuri halaman dari atas ke bawah:

1. **Skor dan keputusan.**
   > "91,3 dari 100, direkomendasikan, paling cocok. Bilah ini menunjukkan dari mana skornya."
2. **Ringkasan AI untuk hiring manager.**
   > "Inilah yang dibaca hiring manager sebagai pengganti CV: kesimpulan, kekuatan, kekurangan, dan
   > alasan rekomendasinya. AI menuliskan kalimatnya dari fakta yang sudah dihitung sistem. AI tidak
   > mengubah skor, dan nama serta kontak kandidat tidak pernah dikirim ke AI."
3. **Pertanyaan wawancara.**
   > "Ini pertanyaan wawancara yang disusun dari kekurangan kandidat ini sendiri, bukan daftar umum."
4. **Mengapa keputusannya seperti ini.**
   > "Di sini aturan keputusan diperiksa satu per satu untuk kandidat ini: CV terbaca lengkap, skor
   > mencapai batas 70, tidak ada syarat gugur yang dilanggar. Karena itu hasilnya Direkomendasikan.
   > AI tidak ikut menentukan keputusan ini."
5. **Tiga panel: Rekomendasi tindak lanjut, Keyakinan AI, Potensi risiko.**
   > "Langkah berikutnya untuk HR, seberapa yakin sistem dan kenapa, serta hal yang perlu diwaspadai."
6. **Dari mana skor ini berasal.**
   > "Bagian ini paling penting untuk kepercayaan. Lima komponen, masing-masing dengan bobot dan
   > poinnya, jumlahnya tepat 91,3. Tidak ada yang disembunyikan."
7. **Kecocokan dengan syarat lowongan,** lalu bagian atas **Bukti dari CV**.
   > "Setiap keterampilan wajib menunjukkan apakah tertulis di CV, hanya tersirat, atau belum
   > ditemukan. Dan ini kalimat dari CV yang menjadi bukti setiap kecocokan."

**Pertanyaan HR:** "ATS kami sudah bisa menyaring kata kunci. Apa bedanya?"
**Jawaban:** "Penyaringan kata kunci melewatkan orang yang menuliskan keterampilan yang sama dengan
kata berbeda. TalentLens mencocokkan makna, mengenali keterampilan yang tersirat dari pekerjaan yang
diceritakan, dan setiap kecocokan menunjukkan kalimat CV asalnya." Tunjuk keterampilan berlabel
"Tersirat".

**Pertanyaan HR:** "Apa arti 'Tersirat'?"
**Jawaban:** "CV tidak menyebut nama keterampilannya, tetapi pekerjaan yang diceritakan menunjukkannya.
Nilainya sebagian, dan HR diminta memastikannya saat wawancara."

**Pertanyaan HR:** "Bisakah ringkasan AI mengarang?"
**Jawaban:** "AI hanya merangkai kata dari fakta yang sudah dihitung sistem. AI tidak bisa mengubah
skor maupun keputusan, keterampilan yang tersirat ditandai perlu dikonfirmasi, dan bila layanan AI
gagal, ringkasan standar yang ditampilkan."

**Pertanyaan HR:** "Kenapa keyakinan AI 'Sedang' untuk semua kandidat?"
**Jawaban:** "Keyakinan diukur dari kelengkapan pembacaan CV dan jarak skor dari batas keputusan.
Setiap kandidat ini punya setidaknya satu keterampilan yang hanya tersirat, jadi sistem memilih
'sedang' daripada terlalu yakin. Peringkatnya tidak berubah."

**Pertanyaan HR:** "Bisakah sistem mendeteksi CV palsu?"
**Jawaban:** "Tidak ada penyaring CV yang benar-benar bisa. Yang dilakukan sistem ini: menunjukkan
kalimat yang mendukung setiap klaim, memisahkan keterampilan yang tertulis dari yang tersirat, dan
memberi pertanyaan wawancara untuk menguji klaim itu."

**Pertanyaan HR:** "Bagaimana dengan kandidat bagus yang CV-nya kurang rapi?"
**Jawaban:** "Ada tiga pengaman: keterampilan yang tersirat tetap dinilai sebagian, bagian CV yang
tidak terbaca tidak dihitung nol, dan kandidat di zona tengah masuk 'Perlu ditinjau', bukan ditolak."
Tunjuk kartu **Pembacaan dokumen**.

### Layar 6 — Kandidat #2 (momen "aha" yang direncanakan)

**Klik:** kembali → baris **#2**.

**Ucapkan:**
> "Mungkin Bapak/Ibu bertanya: kenapa yang berpengalaman 6,5 tahun ada di bawah yang 3,9 tahun?
> Pengalaman dihitung sampai syaratnya jelas terpenuhi; setelah itu tambahan tahun hanya menambah
> sedikit. Keduanya lolos syarat minimal dua tahun, jadi poin pengalamannya hampir sama. Peringkat
> satu unggul di keterampilan yang tertulis jelas di CV dan di kesesuaian isi CV dengan lowongan.
> Semua poinnya terlihat di sini."

**Tunjuk:** **Dari mana skor ini berasal**, bandingkan baris *Pengalaman* dan *Kesesuaian isi CV*
dengan kandidat #1. Lalu **Potensi risiko**: sistem mencatat pengalamannya jauh di atas syarat,
sehingga ekspektasi peran dan gaji perlu dipastikan.

**Pertanyaan HR:** "Apakah pertanyaan wawancaranya generik?"
**Jawaban:** "Tidak. Bandingkan dengan kandidat #1: pertanyaannya berbeda, karena disusun dari
kekurangan masing-masing kandidat."

### Layar 7 — Kandidat #4 (HR tetap memutuskan)

**Klik:** kembali → baris **#4**. Gulir ke **Mengapa keputusannya seperti ini**.

**Ucapkan:**
> "Kandidat ini punya pengalaman drafting yang baik, tetapi skornya 66,5, di zona tinjau, dan
> pendidikannya belum sesuai syarat, baik bidang maupun jenjangnya. Sistem tidak menolaknya. Kandidat
> ini diserahkan ke HR sebagai 'Perlu ditinjau', dengan keputusan yang harus diambil tertulis jelas:
> apakah kekurangan pendidikan ini bisa diterima? Keputusan itu milik manusia."

**Tunjuk:** tanda centang dan silang pada **Mengapa keputusannya seperti ini**, lalu langkah
"Putuskan apakah ini dapat ditoleransi" di **Rekomendasi tindak lanjut**.

**Pertanyaan HR:** "Siapa yang membuat keputusan akhir?"
**Jawaban:** "Selalu HR. Sistem merekomendasikan dan menjelaskan; sistem tidak menolak siapa pun
dengan sendirinya."

**Pertanyaan HR:** "Kenapa #3 tetap direkomendasikan padahal Revit belum terlihat?"
**Jawaban:** "Keterampilan wajib yang tidak terlihat mengurangi skor, tetapi bukan syarat gugur. Skor
#3 tetap 83,4, di atas batas 70, dan kartu keputusannya mencatat Revit sebagai hal yang perlu
dipastikan saat wawancara." Buka #3 bila perlu.

### Layar 8 — Penutup (di Dashboard)

**Klik:** **Dashboard**.

**Ucapkan:**
> "Kesimpulannya: tahap pertama yang biasanya memakan waktu berjam-jam kini selesai dalam hitungan
> detik. Semua kandidat dinilai dengan aturan yang sama. Setiap skor bisa ditelusuri sampai ke kalimat
> di CV, dan setiap keputusan dijelaskan dengan aturannya. AI menuliskan penjelasannya, HR yang
> memutuskan. Langkah menuju produksi: validasi untuk lebih banyak jenis posisi, hosting di Indonesia
> dengan kebijakan perlindungan data, peran pengguna dan jejak audit, serta menghubungkan sumber CV
> yang tadi Bapak/Ibu lihat."

**Pertanyaan:** "Apa yang dibutuhkan untuk masuk produksi?"
**Jawaban:** "Empat langkah: validasi lebih banyak jenis posisi, termasuk dibandingkan dengan
keputusan rekrutmen Anda sebelumnya; hosting di Indonesia dengan kebijakan perlindungan data; peran
pengguna dan jejak audit; dan integrasi sumber CV serta ATS Anda." Jangan menjanjikan tanggal.

**Pertanyaan:** "Apakah ini akan menggantikan recruiter?"
**Jawaban:** "Tidak. Yang dihilangkan adalah pekerjaan membaca, bukan penilaian. Recruiter
menghabiskan waktunya untuk shortlist dan wawancara."

---

## "Di mana kandidat yang ditolak?"

Pertanyaan ini hampir pasti muncul, karena angka **Tidak lolos** di halaman lowongan adalah 0.

**Jawaban terbaik:**
> "Di lowongan ini memang tidak ada. Kelima CV yang diberikan semuanya relevan untuk posisi arsitek,
> dan skor terendahnya 46,3, sedikit di atas batas tolak 45. Kami sengaja tidak menambahkan CV palsu
> hanya untuk memperlihatkan penolakan. Aturannya terlihat di sini."

**Lalu tunjukkan, dalam urutan ini:**

1. **Halaman lowongan → Cara keputusan dibuat.** Zona merah "Tidak lolos, di bawah 45" kosong, dan
   kalimat di bawahnya menyatakan tidak ada kandidat yang skornya di bawah 45.
2. Bila ditanya lebih lanjut, klik angka **Tidak lolos** di ringkasan atas. Daftar kosong itu
   menjelaskan sendiri: tidak ada kandidat di bawah 45, dan kandidat yang belum memenuhi syarat ada di
   kelompok Perlu ditinjau.
3. Buka **kandidat #5**:
   > "Ini yang paling dekat dengan penolakan: pengalaman relevan 0,3 tahun dari syarat dua tahun,
   > pendidikan belum sesuai, skor 46,3. Sistem menandai semua kekurangan itu, tetapi karena skornya
   > masih di atas 45, keputusan akhir diserahkan ke HR."

**Kalimat penutup bila mereka masih ragu:**
> "Sistem ini memang dirancang untuk tidak menolak kandidat di zona abu-abu. Lebih baik HR melihat satu
> kandidat tambahan daripada kehilangan kandidat bagus karena keputusan otomatis. 'Tidak lolos' hanya
> untuk skor di bawah 45 dari CV yang terbaca dengan baik, dan itu pun tetap berupa rekomendasi dengan
> alasan tertulis."

**Jangan:** mengunggah CV yang tidak relevan saat demo hanya untuk memunculkan penolakan, atau
mengatakan sistem "belum bisa menolak". Aturan penolakan ada dan teruji; datanya saja yang tidak
memicunya.

---

## Pertanyaan teknis dari CIO

**"Data kandidat disimpan di mana? Sesuai UU PDP?"**
"Untuk proof of concept ini, aplikasi berjalan di layanan cloud terkelola di balik login, dengan berkas
di volume penyimpanan privat. Untuk produksi kami akan menempatkannya di region Indonesia atau di server
Anda sendiri, dengan kebijakan retensi dan penghapusan serta persetujuan kandidat. Aplikasinya dikemas
dalam container, jadi mudah dipindahkan." Bila ditanya langsung: backend demo berjalan di region AS.

**"Apakah data kami dikirim ke Google?"**
"Penilaian berjalan sepenuhnya di server kami dengan model bahasa kami sendiri; tidak ada CV yang
dikirim keluar untuk dinilai. Hanya langkah ringkasan yang memanggil Gemini, dan yang dikirim hanya
fakta tanpa nama, email, atau nomor telepon."

**"Seberapa aman?"**
"Semua halaman dilindungi login. Backend memerlukan kunci rahasia yang hanya ada di server dan tidak
pernah sampai ke browser, halaman dokumentasi API dimatikan di produksi, dan permintaan dari situs tak
dikenal ditolak. Peran pengguna dan log audit masuk tahap produksi."

**"Bagaimana kalau layanan AI mati?"**
"Penilaian tidak bergantung pada AI. Hanya ringkasan tertulis yang beralih ke versi standar, setelah
sistem mencoba model AI kedua."

**"Seberapa akurat?"**
Jangan menyebut persentase. "Kami mengujinya dengan benchmark tetap: 20 CV arsitektur untuk 5 lowongan,
dengan hasil yang diharapkan ditulis sebelum sistem dijalankan. Setiap perubahan harus menghasilkan
ulang benchmark itu sebelum dirilis, dan 178 tes otomatis berjalan di setiap perubahan." Batasannya:
benchmark baru mencakup posisi arsitektur.

**"Bisakah hasilnya diulang untuk audit?"**
"Bisa. CV dan lowongan yang sama selalu menghasilkan skor yang sama, setiap skor terurai menjadi
komponen yang jumlahnya tepat, dan setiap keputusan dijelaskan dengan aturan yang sama." Ucapkan dengan
yakin.

**"Bisa diintegrasikan dengan ATS atau HRIS kami?"**
"Semua yang Bapak/Ibu lihat berjalan lewat API: membuat lowongan, unggah, penyaringan, peringkat. Jadi
integrasinya berupa konektor, bukan membangun ulang. Itu di luar cakupan proof of concept."

**"Teknologinya apa? Siapa yang bisa memeliharanya?"**
"Frontend Next.js; backend Python dan FastAPI dalam Docker; model bahasa multibahasa yang berjalan di
server sendiri untuk pencocokan; aturan biasa untuk penilaian; Gemini untuk ringkasan. Dipelihara di
Git dengan keputusan teknis yang terdokumentasi, 178 tes otomatis, dan benchmark yang wajib lolos."

**"Berapa biaya operasionalnya?"**
"Penilaian berjalan di server kecil tanpa biaya AI per CV. Satu-satunya biaya berbasis pemakaian
adalah ringkasan AI, yang dibuat sekali per kandidat lalu disimpan." Jangan menyebut angka.

**"Bisa dipakai untuk posisi keuangan, sales, atau IT?"**
"Mesinnya membaca lowongan dan CV apa pun. Kami memvalidasinya satu rumpun posisi per tahap dengan
benchmark tetap; arsitektur sudah, yang lain sudah direncanakan." Jangan mengklaim posisi lain sudah
tervalidasi.

---

## Fitur yang perlu ditonjolkan

Urut dari yang paling penting:

1. **Keputusan yang bisa dijelaskan.** Kartu "Mengapa keputusannya seperti ini" dan "Cara keputusan
   dibuat": aturan yang sama, diperiksa satu per satu untuk setiap kandidat.
2. **Skor yang bisa ditelusuri.** Lima komponen yang jumlahnya tepat, plus kalimat CV di balik setiap
   kecocokan.
3. **Konsisten dan bisa diaudit.** Input sama, skor sama. AI tidak pernah menilai.
4. **AI dengan pagar pengaman.** Ringkasan dan pertanyaan wawancara dari fakta yang sudah dihitung;
   data pribadi disamarkan; ringkasan standar bila AI tidak tersedia.
5. **Siap untuk langkah HR berikutnya.** Pertanyaan wawancara per kandidat, langkah tindak lanjut,
   risiko.
6. **HR tetap memutuskan.** Zona abu-abu masuk "Perlu ditinjau" dengan keputusan yang jelas.
7. **Penilaian tanpa identitas.** Nama disembunyikan secara bawaan.
8. **Peta jalan yang masuk akal.** Halaman Pengumpulan CV: satu mesin, banyak sumber, akses resmi.

---

## Yang TIDAK boleh didemokan

| Jangan | Alasan | Bila diminta |
|---|---|---|
| Menekan **Susun ulang** pada ringkasan | Memanggil AI secara langsung, bisa 15–60 detik, dan menghasilkan kalimat baru yang belum Anda baca | "Itu menulis ulang ringkasan; yang tersimpan adalah yang ditinjau HR." |
| Mencentang **Tampilkan nama kandidat** | Nama pelamar sungguhan akan tampil di proyektor | "Nama tersedia untuk HR, disembunyikan secara bawaan agar penilaian tidak bias." |
| Mengunggah CV baru atau **Tambah lowongan** | Mengubah angka yang sudah dilatih, dan ringkasan pertama untuk CV baru butuh 7–18 detik | Tunjukkan tombolnya saja; unggah hanya bila mereka memaksa, dengan CV yang mereka berikan |
| Mengunggah CV tidak relevan untuk memunculkan "Tidak lolos" | Terkesan dibuat-buat | Gunakan jawaban "Di mana kandidat yang ditolak?" |
| Menekan **Saring ulang** | Tidak perlu, dan menambah waktu tunggu | "Hasilnya identik; sudah kami cek setelah pembaruan terakhir." |
| Mengatakan ada sumber di **Pengumpulan CV** yang sudah terhubung | Belum ada | "Itu tahap produksi berikutnya." |
| Menggulir ke bagian bawah **Bukti dari CV** | Beberapa pasangan bukti di bawah terlihat janggal | Tetap di butir-butir teratas |
| Membuka Railway, Vercel, GitHub, log, atau URL API | Keluar dari pesan utama dan membuka infrastruktur | Tawarkan sesi teknis terpisah |
| Membahas kandidat #5 tanpa ditanya | Kasus yang paling sulit dijelaskan dalam waktu singkat | Lihat jawaban "Di mana kandidat yang ditolak?" |
| Menyebut persentase akurasi, ROI, atau tanggal | Tidak bisa dibuktikan di panggung | Gunakan jawaban di bagian CIO dan Layar 8 |

---

## Rencana cadangan: Gemini sedang gangguan

**Yang akan terlihat:** tidak ada yang mengkhawatirkan. Ringkasan kelima kandidat demo sudah tersimpan
dan terbuka tanpa memanggil Gemini. Untuk CV yang baru diunggah, aplikasi mencoba dua model Gemini
dengan beberapa percobaan; bila keduanya gagal, ringkasan standar dengan tata letak yang sama muncul
dalam waktu paling lama sekitar satu menit. Tidak ada pesan error di layar.

**Yang dilakukan:**

1. **Tetap di kelima kandidat yang tersimpan.** Ringkasan mereka tidak bisa gagal.
2. **Jangan menekan Susun ulang.** Hanya tombol itu yang memicu panggilan AI langsung pada kandidat
   yang tersimpan.
3. Bila Anda sempat mengunggah CV baru dan ringkasannya lambat, terus berbicara beberapa detik, lalu
   pindah ke **Mengapa keputusannya seperti ini** atau **Dari mana skor ini berasal**. Keduanya tidak
   bergantung pada AI.
4. **Bila ada yang memperhatikan kalimatnya lebih sederhana:**
   > "Layanan AI sedang sibuk, jadi sistem memakai ringkasan standarnya. Perhatikan bahwa skor,
   > peringkat, keputusan, dan buktinya tidak berubah. Penilaian memang tidak bergantung pada AI;
   > itu disengaja."
5. Jadikan kekuatan: ini membuktikan jawaban "Bagaimana kalau layanan AI mati?".

---

## Rencana cadangan: internet lambat

**Siapkan malam ini:**

- **Screenshot** dalam satu folder di desktop, dinamai sesuai urutan demo:
  `01-dashboard`, `02-pengumpulan-cv`, `03-kriteria`, `04-peringkat`, `05-cara-keputusan-dibuat`,
  `06-kandidat-1-skor-ringkasan`, `07-kandidat-1-mengapa-keputusan`, `08-kandidat-1-rincian-skor`,
  `09-kandidat-2-rincian-skor`, `10-kandidat-4-mengapa-keputusan`. Pastikan nama tersembunyi di semua
  gambar.
- **Rekaman layar 5 menit** dengan alur versi 5 menit.
- **Hotspot ponsel** terisi penuh dan sudah dicoba dengan laptop demo.

**Saat demo, naikkan langkah demi langkah:**

1. **Halaman lambat (3–10 detik):** gunakan tab yang sudah dibuka 30 menit sebelumnya; pindah tab,
   jangan klik tautan. Isi jeda dengan poin berikutnya.
2. **Wi-Fi tempat acara tidak stabil:** pindah ke hotspot ponsel. Halamannya ringan; 4G cukup.
3. **Tidak ada koneksi sama sekali:** buka folder screenshot layar penuh dan bawakan naskah yang sama.
   Ucapkan sekali: "Koneksinya sedang tidak stabil, jadi saya tunjukkan layar yang sama dari tangkapan
   layar."
4. **Waktu tinggal sedikit:** putar rekaman 5 menit dan sisakan waktu untuk tanya jawab.

Jangan pernah menunggu halaman sambil diam. Terus berbicara, atau pindah ke screenshot berikutnya.

---

## Alur 5 menit

Untuk sesi eksekutif. Satu pesan: *penyaringan AI yang bisa dijelaskan, dengan HR tetap memegang
keputusan.*

| Waktu | Layar | Klik | Ucapkan (inti) |
|---|---|---|---|
| 0:00–0:40 | Layar 1 · Dashboard | — | Masalah dan hasil: 5 CV sungguhan, 3 direkomendasikan, 2 perlu ditinjau |
| 0:40–1:40 | Layar 4 · Peringkat dan Cara keputusan dibuat | Kartu lowongan, gulir | Skor dari 100, "Paling cocok", nama disembunyikan; aturan 70/45 dan zona merah yang kosong |
| 1:40–3:50 | Layar 5 · Kandidat #1 | Baris #1: skor → Ringkasan AI → Pertanyaan wawancara → Mengapa keputusannya seperti ini → Dari mana skor ini berasal | "Aturan yang memberi skor, AI yang menjelaskan; lima komponen jumlahnya tepat 91,3" |
| 3:50–4:25 | Layar 2 · Pengumpulan CV | Header | "Hari ini unggahan; berikutnya situs karier, email, dan portal lowongan, lewat akses resmi" |
| 4:25–5:00 | Layar 8 · Dashboard | Header | Penutup dengan tiga kalimat hafalan dan langkah menuju produksi |

Lewati: kriteria, kandidat #2 dan #4, detail panel. Tanya jawab setelahnya.

---

## Alur 10 menit

Alur bawaan yang disarankan.

| Waktu | Layar | Klik |
|---|---|---|
| 0:00–1:00 | Layar 1 · Dashboard | — |
| 1:00–1:45 | Layar 2 · Pengumpulan CV, singkat | Pengumpulan CV di header |
| 1:45–2:30 | Layar 3 · Kriteria penilaian | Dashboard → Junior Architect → Kriteria penilaian |
| 2:30–3:45 | Layar 4 · Peringkat dan Cara keputusan dibuat | Gulir |
| 3:45–6:45 | Layar 5 · Kandidat #1, ketujuh bagian | Baris #1 |
| 6:45–7:45 | Layar 6 · Kandidat #2, momen "aha" | Kembali → baris #2 |
| 7:45–8:45 | Layar 7 · Kandidat #4, HR memutuskan | Kembali → baris #4 |
| 8:45–10:00 | Layar 8 · Penutup | Dashboard |

---

## Alur 15 menit

Untuk audiens campuran HR dan IT yang ingin lebih dalam. Termasuk waktu tanya jawab.

| Waktu | Layar | Klik | Tambahan dibanding versi 10 menit |
|---|---|---|---|
| 0:00–1:15 | Layar 1 · Dashboard | — | Tanyakan: "Berapa CV yang masuk untuk satu lowongan?" |
| 1:15–3:00 | Layar 2 · Pengumpulan CV, lengkap | Pengumpulan CV | Diagram, dua kelompok sumber, empat prinsip integrasi |
| 3:00–3:45 | Layar 3 · Kriteria penilaian | Junior Architect → Kriteria penilaian | — |
| 3:45–5:00 | Layar 4 · Peringkat dan Cara keputusan dibuat | Gulir; klik angka Tidak lolos | Tunjukkan pesan daftar kosong yang menjelaskan sendiri |
| 5:00–8:15 | Layar 5 · Kandidat #1 | Baris #1 | Tambah kartu **Pembacaan dokumen** (jenis dokumen dan seberapa lengkap terbaca) |
| 8:15–9:15 | Layar 6 · Kandidat #2 | Baris #2 | — |
| 9:15–10:30 | Layar 7 · Kandidat #4, lalu #3 sebentar | Baris #4, lalu #3 | #3: Revit belum terlihat mengurangi skor, bukan syarat gugur |
| 10:30–11:30 | Dashboard, tanpa layar baru | — | Cara sistem divalidasi: benchmark 20 CV dengan hasil yang ditulis lebih dulu, 178 tes otomatis, kode penilaian tidak berubah sejak benchmark, AI tidak pernah menilai |
| 11:30–12:00 | Layar 8 · Penutup | — | Langkah menuju produksi |
| 12:00–15:00 | Tanya jawab | — | Jawab singkat, tunjukkan di layar, berhenti |

---

## Kartu ringkas

- Halaman pertama: **Dashboard**. Layar utama: **Kandidat #1**. Momen "aha": **#2 dibanding #1**.
  HR memutuskan: **#4**. Pertanyaan penolakan: **Cara keputusan dibuat** dan **#5**.
- Jangan: Susun ulang, menampilkan nama, unggah, Saring ulang, mengklaim integrasi sudah aktif.
- Gemini gangguan: tetap di lima kandidat yang tersimpan; penilaian tidak bergantung pada AI.
- Internet lambat: tab → hotspot → screenshot → rekaman.
- Penutup: "Aturan yang memberi skor. AI yang menjelaskan. HR yang memutuskan."
