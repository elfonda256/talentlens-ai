# Regression fixtures — architecture

There is one JSON fixture per CV (`ARC-CV-NN.regression.json`) and an `index.json` that lists the
fixtures, the assertion levels and the test suites. Every fixture validates against
`dataset/regression_fixture.schema.json`.

These fixtures extend the golden benchmark (`../ARC-CV-NN.expected.json`) with the fields an
automated test can assert on. Decision, rank and score range are identical in both files.

## What each fixture contains

| Block | What to assert |
|---|---|
| `parser_output` | Extraction method (text/OCR), language, layout, contact (phone in E.164), detected sections with raw and canonical headings, every job and education entry with normalised dates, certifications, languages, volunteer and side-business entries, expected parser warnings, and PII fields to mask |
| `extracted_skills` | `explicit`: each skill with a category and an evidence string copied verbatim from the CV. `must_not_extract`: known false positives such as "Java" from "East Java", photo-placeholder labels, and "Ir." as a skill |
| `experience` | Total years, relevant years with tolerance, the basis (what was counted and what was excluded), and domain sub-totals (high-rise, healthcare, remote site) |
| `education` | Highest degree, field, status, GPA and match class |
| `confidence` | Expected `section_confidence` range per section (pipeline convention: 0 not found, 0.3 heading only, 0.6–1.0 read), parse quality, and screening confidence (Tinggi/Sedang/Rendah) with a reason |
| `explainability` | Status of every vacancy requirement (`met` / `partial` / `not_met` / `unknown`) with evidence, a mandatory summary, expected component ranges at weights 35/25/25/15, top positive and negative factors, risks and a reference explanation |
| `recommendation` | Decision (English and Indonesian label), score range, rank, pool order, override, provisional-score flag, decisions that must never appear, and the next action |
| `interview_questions` | 1–5 questions each, in the vacancy's language, with purpose, the requirement or risk they test, good-answer signals and red flags |
| `hr_summary` | Indonesian reference summary (≤120 words), concepts it must mention, claims it must not make, and PII strings that must not appear |

## Assertion levels

These are defined in `index.json`.

- **Hard:** contact fields, extraction method, job dates, relevant years (± `tolerance_years`), highest education, software skills, `must_not_extract`, status of mandatory requirements, decision, `never_decision`, `provisional_score`, and the absence of `forbidden_strings` from any generated summary.
- **Soft** (warn, don't fail): score range, rank (adjacent swaps are fine when score ranges overlap), component ranges, confidence values, non-software skills, section list, and the `must_mention` concepts.
- **Reference only:** reference texts, `must_not_claim` (for manual or LLM-judge review), and interview questions.

## Matching rules

- **Evidence strings:** apply Unicode NFKC, collapse whitespace and casefold before checking that the evidence is a substring of the extracted text. NFKC also turns ligatures such as `ﬁ` into `fi`. Evidence for ARC-CV-07 comes from OCR, so match it with a token-overlap threshold (≥ 60%), not exact substrings.
- **`must_mention`:** the summary passes a concept if it contains any phrase in `any_of` (case-insensitive).
- **`forbidden_strings`:** match whole words only, case-insensitive. Use these for PII leak tests on Gemini or template output.
- **Dates:** `YYYY-MM`, a bare `YYYY` (treated as January), or `present`. `present` is the reference date, 2026-11-17, not the day the test runs. This avoids open issue M-1.
- **`unknown` vs `not_met`:** `unknown` means the CV is silent, and it must never be reported as a failed requirement (TDR-0023).

## Scoring rules (confirmed from source at `ea2345f`)

- **Weights** (`DEFAULT_WEIGHTS` in `backend/app/schemas/screening.py`): skills 0.35, experience 0.25, semantic 0.25, education 0.15.
- **Formulas** (`matching.py`):
  - experience = 0.85·min(1, years/min) + 0.15·min(1, excess/3), or 1.0 when the job's minimum is 0;
  - education = 1.0 for a matching field, 0.6 for a related field, 0.15 otherwise, then ×0.7 if the degree level is below the minimum.
- **Decision** (`explanation.decide`, `config.py`): SHORTLIST at 70 or more, unless a knockout flag is raised; REJECT below 45, unless the CV went through OCR or extraction confidence is under 0.7. If a section can't be read, the result is always REVIEW.

`explainability.score_components.expected_ranges` follow these formulas, given a correctly parsed CV and vacancy. The semantic range is the E5 target and wasn't verified here; `semantic_tfidf_range` is what TF-IDF gives. Where formula-correct components don't reproduce the benchmark score range, `scoring_model_gap` gives the cause. The benchmark range stays the target.

## Pipeline baseline

`pipeline_baseline` records what the unmodified pipeline produced at commit `ea2345f` (branch `sprint-4`, TF-IDF, reference date 2026-11-17):
- the observed score, rank, decision, components, parsed contact, experience, education and skills;
- a set of checks against this fixture, plus `known_failures`.

Use it to detect *unintended* change at a later commit. It is not the target. `validation_report.json` holds the aggregate results.

## Benchmark band vs app thresholds

The benchmark labels decisions with bands of 75/50. The app shortlists at 70 and rejects below 45. `recommendation.pipeline_rules` shows the decision the app's own rules give for the target components, so both views are available. Aligning the two is a Product Owner decision.
