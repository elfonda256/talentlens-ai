# Golden Benchmark Policy v1.0

This policy governs every golden benchmark in `dataset/`. It applies alongside
[GOVERNANCE.md](GOVERNANCE.md). When the two conflict, GOVERNANCE.md wins.

Current benchmarks:

| Category | Version | Status | Report |
| --- | --- | --- | --- |
| Architecture | 1.0.0 | Approved, frozen | [DATASET_REPORT.md](../dataset/architecture/DATASET_REPORT.md) |

## 1. Purpose of golden benchmarks

A golden benchmark is a frozen set of synthetic vacancies and CVs with agreed expected results. It
answers one question: **did a code change make screening better, worse, or just different?**

It is used to:

- detect unintended changes in parsing, ranking, decisions and explanations;
- measure progress on known parser defects;
- give the Product Owner a fixed reference for business rule decisions.

A benchmark is not:

- a training set: the scoring model is deterministic and is never fitted to it;
- the demo data: the 5 company CVs are kept apart and never added to `dataset/`;
- a description of current behaviour: expected results are the target. What the app does today is
  recorded separately in `pipeline_baseline`.

## 2. Versioning policy

Each benchmark has its own version, `MAJOR.MINOR.PATCH`, recorded in the Frozen Benchmark Metadata
section of its Dataset Report.

| Bump | When | Examples |
| --- | --- | --- |
| **MAJOR** | Any change to what a test must pass | A changed expected decision, rank, score range or hard assertion; a CV or vacancy added or removed; a new reference date; a schema change that breaks existing fixtures |
| **MINOR** | Additions that leave existing expectations intact | New optional fixture fields; new soft or reference-only assertions; a refreshed `pipeline_baseline` after an approved application change |
| **PATCH** | No assertion changes | Report wording, metadata, typos in reference texts that no test reads |

Rules:

- A frozen version is never edited in place. A change produces a new version in a new commit.
- Every version can be found again from its commit, and from its tag once the tag exists. The tag
  name is `<category>-golden-benchmark-v<version>`, for example
  `architecture-golden-benchmark-v1.0.0`.
- A missing tag does not block a version, as long as the branch and commit are recorded in the
  Dataset Report.

## 3. Approval workflow

1. **Proposal.** Whoever wants the change (usually Claude, during a sprint) writes what will change,
   why, which files, the version bump, and the expected effect on validation results.
2. **Validation.** Run the checks in section 5 on the proposed version and attach the results.
3. **Product Owner decision.** Approve, reject or request changes. Without explicit approval, the
   current version stays in force.
4. **Release.** Commit on the dataset branch, update the metadata (Status, Version, Last Updated),
   add an entry to the Dataset Report, and create the tag.

The status of a version is one of: **Draft** (being built, may change freely), **Approved** (frozen,
in force), **Superseded** (replaced by a newer approved version, kept for history).

PATCH changes still need Product Owner approval, but can be grouped into the next sprint report.

## 4. When to create a new version

Create a new version when:

- a fixture is proven wrong against its source PDF (for example, evidence text that is not in the
  document, or wrong dates);
- the Product Owner changes a business rule, and the benchmark's expected outcome should follow it;
- coverage is extended with new layouts, languages or edge cases;
- an approved application change makes the recorded `pipeline_baseline` obsolete.

Do not create a new version:

- to make a failing test pass;
- because the application's output differs from the expected result (that difference is the
  finding the benchmark exists to show);
- to match a parser defect that has not been fixed yet.

## 5. Regression validation requirements

Run the benchmark before merging any change to parsing (`cv_parsing/`, `jd_parsing.py`), skill
taxonomy, embedding, scoring (`matching.py`, `screening.py`, `explanation.py`) or the HR summary.

```
cd backend && pip install -r requirements.txt
python ../dataset/tools/run_pipeline.py . ../dataset/<category> /tmp/run.json
```

Use TF-IDF mode and the benchmark's reference date (17 November 2026 for Architecture v1.0.0).

| Requirement | Rule |
| --- | --- |
| Schema | Every fixture validates against `dataset/regression_fixture.schema.json` |
| Hard assertions | No new failures compared with `pipeline_baseline` |
| Decisions | Every decision that changes against `pipeline_baseline` is listed in the sprint report with its cause: a parser defect fixed (PD-ID) or an approved business rule change |
| Soft assertions | Reported, do not block the merge |
| Privacy | No `forbidden_strings` (PII) in any generated summary |
| Demo data | The 5 company CVs give the same ranking and decisions, unless the sprint was approved to change them |

The sprint report states which benchmark version was used, the commit, and the results table.

## 6. Rules for modifying benchmark datasets

- Benchmark data is synthetic only. Real CVs, company documents and real personal data are never
  added to `dataset/`.
- Frozen files (`CV/`, `Vacancy/`, `Expected_Result/`, regression fixtures, schema) are not edited
  in place. Changes go through the workflow in section 3.
- Expected results describe the desired outcome, decided by the Product Owner. They are never copied
  from the application's output.
- A correction to a fixture needs evidence from the source PDF, quoted in the proposal.
- `pipeline_baseline` is a snapshot of application behaviour at a named commit. Refreshing it is a
  MINOR version and needs approval, so that a regression cannot be hidden by re-recording it.
- The reference date is fixed per version. Tests never use the day they run.
- Tools in `dataset/tools/` may only drive the unmodified application. They must not patch
  application code.

## 7. Parser defects and business rule decisions

Every difference between the application and a benchmark is classified as one of two kinds.

| | Group A — Parser defect | Group B — Business rule decision |
| --- | --- | --- |
| Meaning | The application misreads a document | The application reads correctly and applies a rule the benchmark disagrees with |
| Example | "East Java" extracted as the skill Java | Related major gets 0.6 education credit |
| Owner | Engineering | Product Owner |
| Fix | Parser change, in an approved sprint | Product Owner decision, recorded in a TDR, because it changes how candidates are scored |
| Effect on the benchmark | None. The expected result stays; the fix moves the app towards it | Either the rule changes, or the benchmark gets a new MAJOR version that adopts the rule |
| ID | `PD-NN` in the Dataset Report | Listed under Business Rule Decisions in the Dataset Report |

Rules:

- A Group B rule stays unchanged until the Product Owner decides otherwise. The current decision
  (17 November 2026) is to keep thresholds 70/45, related-major credit, and the behaviour when a
  vacancy has no minimum experience, until after the demo.
- A parser fix must not be presented as a scoring improvement. When a parser fix changes decisions
  because of a Group B rule, those changes are reported explicitly, never absorbed silently.
- The two groups interact. Correctly parsed CVs can expose a Group B rule that today's parser
  defects hide. Architecture v1.0.0 shows this for seven CVs (see its Dataset Report). Plan parser
  backlog items together with the related business rule discussion, and re-run the benchmark after
  each parser fix.
- When the classification of a finding is unclear, it is treated as Group B and raised with the
  Product Owner.
