# TalentLens AI — Synthetic Recruitment Benchmark Dataset

Synthetic but realistic recruitment documents for testing TalentLens AI: parsing, OCR, screening,
ranking, explanations and embedding quality. Every company, person, email address and phone number is
fictional. Universities, licensing bodies (LPJK, Dewan Arsitek Indonesia, GBC Indonesia, Kemnaker) and
Indonesian regulations are real, because a screening system has to recognise them.

This dataset is separate from the 5 company-provided CVs used for the live demo. Do not mix the two.

## Structure

```
dataset/
  <category>/
    Vacancy/          5 job vacancy PDFs
    CV/               20 candidate CV PDFs
    Expected_Result/  golden benchmark (one JSON per CV, one ranking per vacancy, summary CSV)
      regression/     regression fixtures: one JSON per CV + index.json + README.md
    README.md         category manifest
  regression_fixture.schema.json   JSON Schema for every regression fixture
  tools/run_pipeline.py            runs the unmodified pipeline over a category (baseline)
```

Categories (one per sprint, in this order): architecture, software-engineering, ui-ux, accounting,
finance, marketing, sales, purchasing, hr, warehouse, production, quality-control, project-manager,
business-analyst, customer-service.

| Category | Status |
|---|---|
| architecture | **Frozen: Golden Benchmark v1.0.0** (17 Nov 2026), see `architecture/DATASET_REPORT.md` |
| all others | Not started |

## How the benchmark is organised

Each category has 5 vacancies with 4 CVs aimed at each one. Every CV is scored against its **target
vacancy**, and the 4 CVs for a vacancy make up its ranking pool. A CV may also name an
`alternative_vacancy` where it would fit better. That field is a note, not a second graded result.

Reference date for all "present" / "sekarang" roles and experience calculations: **17 November 2026**.

### Decision bands

| Decision | Score |
|---|---|
| Recommended | 75 – 100 |
| Review | 50 – 74 |
| Reject | 0 – 49 |

Two overrides can move a decision outside its band, and each is recorded in `decision_override`:

- `overqualified`: the score may reach 75 or more, but the expected decision is Review. The system should flag the candidate and not auto-recommend.
- `incomplete_but_relevant`: a sparse CV whose few facts match the role. Expected decision is Review, with "request complete CV" as the action.

### How to grade a system against the benchmark

- **Decision:** must match exactly.
- **Score:** pass if the system score is inside `expected_score_range` (ranges are deliberately 6–13 points wide).
- **Ranking:** compare with `pool_order`. Adjacent swaps between CVs whose score ranges overlap are acceptable.
- **Skills:** `skills_found` is the set a good parser should recover. `missing_skills` is what the explanation should mention.
- **Years:** `years_of_relevant_experience.value`, with a tolerance of ±0.5 year. The `basis` field explains what was counted and what was excluded.
- **Parser traps:** `document.parser_traps` lists the specific extraction failures each CV is designed to provoke.

## Expected_Result file schema (`<CV-ID>.expected.json`)

| Field | Meaning |
|---|---|
| `cv_id`, `candidate_name`, `cv_file`, `target_vacancy`, `vacancy_file` | Identity and paths, relative to the category folder |
| `candidate_profile` | Difficulty class (Perfect, Overqualified, Career switch, …) |
| `test_tags` | Edge cases covered (scanned, no_headings, duplicated_sections, …) |
| `document` | Language, layout, whether a text layer exists, parser traps |
| `expected_ranking` | Rank, pool size and full pool order |
| `expected_score_range` | `min` and `max` on a 0–100 scale |
| `expected_decision`, `decision_override` | Recommended / Review / Reject and any override |
| `skills_found`, `missing_skills` | Against the target vacancy |
| `years_of_relevant_experience` | `value` plus domain sub-totals (`high_rise`, `healthcare`, `remote_site`) and `basis` |
| `education_match` | `Match` / `Exceeds` / `Partial` / `Mismatch` / `Unknown`, with detail |
| `semantic_match` | `High` / `Medium` / `Low`, with detail |
| `potential_risks`, `interview_focus`, `expected_explanation` | The reasoning a recruiter would expect to see |
| `alternative_vacancy` | Optional note about a better-fitting vacancy |

`<VAC-ID>.ranking.json` holds the structured vacancy requirements and the ordered pool.
`benchmark_summary.csv` is one row per CV for spreadsheet or regression use.
