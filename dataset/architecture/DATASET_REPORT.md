# Architecture Dataset Report — Golden Benchmark v1.0.0

**Status:** Golden Benchmark v1.0.0 (Approved by the Product Owner, 17 November 2026) · frozen on 17 November 2026 · **Baseline:** commit `ea2345f` (`sprint-4`), TF-IDF, reference date 2026-11-17

This is the first golden benchmark for TalentLens AI. Any change to it from here needs a new version
number. The test and benchmark data is separate from the 5 company CVs used in the demo.

## Contents

| Item | Count |
|---|---|
| Vacancies (PDF) | 5 |
| CVs (PDF) | 20 (4 per vacancy) |
| Golden benchmark files | 20 `.expected.json`, 5 `.ranking.json`, 1 summary CSV |
| Regression fixtures | 20 `.regression.json` + `index.json` + `validation_report.json` |
| JSON Schema | `dataset/regression_fixture.schema.json` |
| Expected decisions | 8 Recommended, 9 Review, 3 Reject |

## Coverage

| Area | CVs |
|---|---|
| Parser edge cases (15 kinds) | Section without headings (15), duplicated sections (11), overlapping jobs (14), no dates (06), years-only dates (16), typos in headings and skills (06), unusual headings (20), broken text layer with ligatures and hyphenation (15), missing education (16), work history in a table (08), biodata key-value table (05), icon glyphs in contact lines (10, 14), photo/QR placeholders (03, 17), academic titles in the name (02, 08, 09, 18), headings in the name position (05, 06, 07) |
| OCR | 1 — ARC-CV-07, an image-only scan with no text layer |
| Multilingual | Indonesian 5, English 9, mixed 6; vacancies are 2 Indonesian/mixed and 3 English |
| Two-column layouts | 3 — ARC-CV-03, ARC-CV-10, ARC-CV-17 |
| Difficulty profiles | Perfect, very good, good, average, junior, fresh graduate, no experience, overqualified, underqualified, career switch, wrong major, wrong industry, incomplete |
| Special cases | Military, volunteer, freelance, side business, internship only, employment gap, portfolio links |
| Industries | Consulting, EPC/steel, hospital, coal mining, PropTech startup |

## Final validation

| Check | Result |
|---|---|
| JSON Schema | 20/20 fixtures valid |
| Fixture vs benchmark (decision, rank, score range, file paths) | 0 inconsistencies |
| Parser expectations: every evidence string is in the extracted text (the scanned CV via Tesseract) | Pass |
| Experience years vs benchmark (±0.5 y) | Pass |
| Expected ranking: each pool's order is consistent with its score ranges | 5/5 pools |
| Explanation consistency: requirement counts, negative factors vs statuses, decision stated in the HR text, `must_mention` covered, no PII | 0 issues |
| Scoring weights | Confirmed from source: skills 0.35, experience 0.25, semantic 0.25, education 0.15 |
| Component ranges | Recomputed with the real formulas. Where they don't reproduce a benchmark score range, the cause is documented (11 CVs, 0 undocumented) |

## Pipeline baseline (current build vs benchmark)

| Measure | Result |
|---|---|
| Decision matches benchmark | 14/20 |
| Rank matches benchmark | 12/20 |
| Score inside benchmark range | 8/20 (TF-IDF semantic calibrates low; the ranges are E5 targets) |
| Full pool order matches | 1/5 (top candidate correct in 3/5) |
| Name extracted correctly | 12/20 |
| Experience entries found | 11/20 |

## Findings: parser defects and business rule decisions

The baseline differences above have two different causes, and they are handled differently.

- **Group A — Parser defects.** The application misreads a document. These are bugs, and they go to
  the backlog for future parser work.
- **Group B — Business rule decisions.** The application reads the document correctly and scores it
  as its rules intend. The benchmark expects a different outcome. These rules are intentional and stay
  unchanged until after the demo.

Every item is also recorded in `pipeline_baseline.known_failures` in the fixtures. They are not
fixture errors.

### Group A — Parser defects (backlog)

| ID | Defect | Affects | Where |
|---|---|---|---|
| PD-01 | Vacancy misclassified as a CV: VAC-05 is refused at upload as "looks like a CV" | ARC-VAC-05 | `screening._looks_like_cv` |
| PD-02 | Vacancy headings not recognised: "Kualifikasi Wajib" is missed, so VAC-04's requirements are not read (minimum years becomes 0, no degree required) | ARC-VAC-04 | `jd_parsing.parse_job` |
| PD-03 | Master's degree read as mandatory: "A Master's degree is an advantage" becomes minimum level S2, so every S1 candidate is flagged and the perfect CV goes to Review | ARC-VAC-01 → CV-01, 03 | `jd_parsing` level rule |
| PD-04 | "East/West Java" read as the skill "programming" (open issue M-2) | ARC-VAC-03, -05, CV-10 | taxonomy |
| PD-05 | Work experience not extracted: 0 entries in 9 CVs — two-column (03, 17); "Work", "Pengalaman Kerja Praktik", tables, "Where I've Worked" (04, 05, 08, 19, 20); no dates (06); no headings (15) | 9 CVs | `cv_parsing` (M-7 and others) |
| PD-06 | Candidate name extracted incorrectly: taken from a heading ("Data Pribadi", "Curiculum Vitae", "Riwayat Hidup"), academic titles kept (Ir., S.Ars., S.T.), or missing | 8 CVs | `cv_parsing` name rule |
| PD-07 | "D3/S1" read as minimum S1, so the D3 candidate is flagged | ARC-VAC-02 → CV-07 | `jd_parsing` level rule |
| PD-08 | "2–4 years" not read as a minimum | ARC-VAC-05 | `MIN_YEARS` regex |
| PD-09 | Education not found in two-column sidebars and under unusual headings | CV-10, 20 (15: no headings) | `cv_parsing` |

PD-01 to PD-06 were classified by the Product Owner. PD-07 to PD-09 are the same kind of defect (the
document is misread), so they are listed here too.

### Group B — Business rule decisions (unchanged until after the demo)

**Decision (Product Owner, 17 November 2026):** keep the current scoring rules for the demo. Do not
tune the scoring model before the demo.

| Rule | Current behaviour (kept) |
|---|---|
| Decision thresholds | Recommended at 70 or above, Review from 45 to below 70, Reject below 45. The benchmark's 75/50 bands are reference only; each fixture keeps both views. |
| Related major | A related field of study gets 0.6 education credit, with no knockout flag |
| Minimum experience = 0 | When a vacancy sets no minimum, the experience component scores 100 |

Related scoring questions found by the benchmark, left for the same post-demo discussion:

- No overqualification rule (CV-02).
- Domain experience (hospitals, remote sites) is not modelled.
- Missing mandatory certificates and portfolios are not knockouts.

### How the two groups interact

With correctly parsed input, the current rules would score 7 benchmark "Review" candidates as
Recommended: CV-06, 08, 10, 11, 14, 18 and 20. CV-02 is the same case through its overqualified
override. Today they mostly land in Review only because parser defects lower their scores.

**Fixing Group A without revisiting Group B will therefore move these candidates to Recommended.**
Plan the parser backlog together with the post-demo scoring discussion, and re-run this benchmark
after each parser fix.

## Reproduce

```
cd backend && pip install -r requirements.txt
python ../dataset/tools/run_pipeline.py . ../dataset/architecture /tmp/run.json
```

`run_pipeline.py` drives the unmodified `ScreeningService` in TF-IDF mode with reference date 2026-11-17. When a vacancy is refused at upload, it records the refusal and then parses the vacancy directly, so its CVs can still be scored.
