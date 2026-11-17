# Category: Architecture (Sprint 1)

**Golden Benchmark v1.0.0, frozen on 17 November 2026.** Validation results, pipeline baseline and known failures are in [DATASET_REPORT.md](DATASET_REPORT.md).

Building architects in Indonesia, covering five industries, from fresh-graduate drafters to licensed
senior architects. Reference date is 17 November 2026.

## Vacancies

| ID | Role | Employer (fictional) | Industry | Location | Salary (IDR/month) | Min. exp. | Language |
|---|---|---|---|---|---|---|---|
| ARC-VAC-01 | Senior Architect — High-Rise & Mixed-Use | PT Arsitama Griya Konsultan | Architecture consulting | Jakarta Selatan, hybrid | 28 – 38 jt | 8 y | English |
| ARC-VAC-02 | Junior Architect / Drafter Arsitektur | PT Baja Konstruksi Nusantara | EPC / steel structure | Cikarang | 6.0 – 7.5 jt | 0 – 2 y | Indonesian |
| ARC-VAC-03 | Healthcare Facility Architect | PT Husada Prima Medika | Hospital group | Surabaya | 18 – 24 jt | 5 y | English |
| ARC-VAC-04 | Site Architect — Township & Support Facilities | PT Tanjung Kerta Mining | Coal mining | Kutai Timur, roster 8/2 | 20 – 27 jt + 25% site | 5 y | Indonesian / English |
| ARC-VAC-05 | Architectural Designer (Residential) | Griyakarya (PT Griyakarya Digital Nusantara) | PropTech startup | Bandung, hybrid | 9 – 13 jt + ESOP | 2 – 4 y | English |

Each vacancy uses a different document style: corporate letterhead, job-fair poster, two-column
brief, HR form with tables, and a startup post.

## CVs and expected outcome

| CV | Candidate | Target | Profile | Layout | Lang | Rank | Score | Decision |
|---|---|---|---|---|---|---|---|---|
| ARC-CV-01 | Raditya Mahendra Wibisono | VAC-01 | Perfect candidate | ATS | EN | 1 | 90–96 | Recommended |
| ARC-CV-03 | Nadia Paramitha Kusuma | VAC-01 | Very good, employment gap | Canva 2-col | Mixed | 2 | 80–88 | Recommended |
| ARC-CV-02 | Hendrawan Sutanto | VAC-01 | Overqualified, own firm | Word serif | EN | 3 | 70–80 | Review (override) |
| ARC-CV-04 | Kevin Halim | VAC-01 | Wrong major / industry | Minimalist | EN | 4 | 28–40 | Reject |
| ARC-CV-07 | Rizky Ramadhan Pratama | VAC-02 | Good, scanned | Scanned image | ID | 1 | 78–87 | Recommended |
| ARC-CV-05 | Salsabila Putri Anggraini | VAC-02 | Fresh graduate, internship only | Word "Daftar Riwayat Hidup" | ID | 2 | 75–83 | Recommended |
| ARC-CV-08 | Bambang Wicaksono | VAC-02 | Career switch, military | Tables | Mixed | 3 | 58–68 | Review |
| ARC-CV-06 | Agus Setiawan | VAC-02 | Wrong major, typos, no dates | Bad formatting | ID | 4 | 50–60 | Review |
| ARC-CV-09 | Dewi Kartikasari Simanjuntak | VAC-03 | Very good | Tables | Mixed | 1 | 86–94 | Recommended |
| ARC-CV-10 | Fajar Nugroho | VAC-03 | Good, missing domain skill | 2-col + icons | EN | 2 | 64–74 | Review |
| ARC-CV-11 | Grace Natalia Wenas | VAC-03 | Duplicated sections | Messy spacing | Mixed | 3 | 56–66 | Review |
| ARC-CV-12 | Muhammad Ilham Saputra | VAC-03 | Underqualified | Minimalist | EN | 4 | 30–42 | Reject |
| ARC-CV-13 | Andi Muhammad Rais | VAC-04 | Perfect candidate | ATS serif | EN | 1 | 85–93 | Recommended |
| ARC-CV-15 | Stefanus Hartono | VAC-04 | Very good, no headings | Broken PDF text | ID/EN | 2 | 76–86 | Recommended |
| ARC-CV-14 | I Putu Gede Wirawan | VAC-04 | Overlapping jobs, freelance | Icons + bands | Mixed | 3 | 55–66 | Review |
| ARC-CV-16 | Yudi Firmansyah | VAC-04 | Incomplete, no education | Bare text | ID | 4 | 50–58 | Review (override) |
| ARC-CV-17 | Alya Rahmania Hakim | VAC-05 | Excellent portfolio | Canva 2-col + QR | EN | 1 | 88–95 | Recommended |
| ARC-CV-20 | Dimas Aryo Baskoro | VAC-05 | Average, unusual headings | Quirky | EN | 2 | 60–70 | Review |
| ARC-CV-18 | Teguh Prasetyo | VAC-05 | Career switch, volunteer | Word blue headings | ID | 3 | 58–68 | Review |
| ARC-CV-19 | Clarissa Tanoto | VAC-05 | No experience, wrong major | Minimalist condensed | EN | 4 | 15–28 | Reject |

Totals: 8 Recommended, 9 Review, 3 Reject.

## Edge-case coverage

| Requirement | CV(s) |
|---|---|
| Perfect / very good / good / average | 01, 13 / 03, 09, 15 / 07, 10, 14 / 11, 20 |
| Junior / fresh graduate / no experience | 12 / 05 / 19 |
| Overqualified / underqualified | 02 / 12 |
| Career switch / multiple careers | 08, 18 / 08 (military → architecture), 18 (QS → design) |
| Wrong major / wrong industry | 04, 06, 18, 19 / 04 |
| Missing skills | 03 (licence level), 10 (healthcare), 14 (K3 cert) |
| Incomplete CV / missing education | 16 |
| Scanned CV, OCR noise, no text layer | 07 |
| Broken PDF text, ligatures, hyphenation | 15 |
| CV without headings | 15 |
| Unusual headings | 20 |
| Typos | 06 |
| Duplicated sections | 11 |
| No dates | 06 |
| Overlapping jobs | 14 |
| Employment gap | 03 (career break), 16 (nothing after 2024) |
| Freelance work | 06, 08, 14, 19 |
| Internship only | 05 |
| Military experience | 08 |
| Volunteer work | 18, 19 |
| Side business | 02 (own firm), 18 (own design-build company), 20 (3D asset shop) |
| Portfolio links | 10, 17, 19, 20 |
| QR code placeholder | 17 |
| Image / photo placeholder | 03, 17 |
| Two columns / tables / icons | 03, 10, 17 / 05, 08, 09 / 10, 14 |
| ATS / minimalist / Canva / Word style | 01, 13 / 04, 12, 19 / 03, 17 / 02, 05, 18 |
| Bad formatting / messy spacing | 06, 11 |
| Indonesian / English / mixed | 05, 06, 07, 16, 18 / 01, 02, 04, 10, 12, 13, 17, 19, 20 / 03, 08, 09, 11, 14, 15 |

## Known traps worth testing first

1. **ARC-CV-07** has no text layer. A pipeline without OCR sees an empty document and must route it to manual review, not reject it.
2. **ARC-CV-11** repeats its experience and skills sections. Years must stay 7.3, not double.
3. **ARC-CV-14** has three concurrent date ranges. Years must be 8.8, not the sum of all ranges.
4. **ARC-CV-04** and **ARC-CV-19** share many keywords with their vacancies. Keyword overlap alone should not lift them out of Reject.
5. **ARC-CV-02** scores high on raw requirements. The expected output is Review with an overqualification flag.
