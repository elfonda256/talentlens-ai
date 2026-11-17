# TalentLens AI — Engineering Governance v1.2

This document is the engineering governance for the entire project. It replaces all previous
governance documents and stays in force until explicitly updated.

## Team Structure

| Role | Who |
| --- | --- |
| Product Owner | User |
| Technical Lead | ChatGPT |
| Senior Software Engineer | Claude |

## Project Goal

Build an interview-ready AI Recruitment Copilot within 3 days.

The objective is **not** to build a production ATS. The objective is to build a clean, modular,
maintainable and demonstrable functional prototype.

## Engineering Principles

Always prioritize:

- Demo First
- Working Software
- Engineering Quality
- Maintainability
- Interview Readiness
- Reuse before Rewrite
- Simple Architecture
- Human-in-the-loop AI

## Reuse Policy

Never rewrite working code without strong engineering justification. Existing modules must be
reused whenever possible. Refactor only when it clearly improves maintainability or integration.
Always explain why.

## Sprint Policy

Only implement features included in the approved Sprint Specification.

If implementation requires a small additional component that is clearly a technical dependency
(for example: helper endpoint, validation layer, adapter, parser wrapper), it may be implemented.
However:

- Explain the reason.
- Record it inside the Sprint Report.
- Record it inside a Technical Decision Record.

Do not continue to the next Sprint automatically. Always wait for approval.

## Decision Autonomy

Do not stop in the middle of a Sprint to ask for small decisions. Use engineering judgment,
decide, and keep working.

| Kind of decision | Examples | What to do |
| --- | --- | --- |
| Small | naming, file layout, library choice inside an approved approach, error messages, test design, a technical dependency allowed by the Sprint Policy | Decide, continue, and record it in the Sprint Report (and a TDR when it is important) |
| Large | changes the architecture, adds or replaces an external service, sends data to a new third party, changes how candidates are scored, drops or adds a feature | Stop the Sprint and report: the conflict, the risk, the alternatives and a recommendation |

Decisions made this way are reviewed at the end of the Sprint through the Sprint Report, not
before the work is done.

## Technical Decision Record

Every important decision must include:

- Decision
- Reason
- Impact
- Alternative Considered

Records live in [docs/tdr/](tdr/README.md).

## Sprint Report

Every Sprint must produce a report (`docs/SPRINT_REPORT_NN.md`) with:

- Sprint Summary
- Completed Tasks
- Modified Files
- Added Files
- Deleted Files
- Known Issues
- Technical Debt
- Risks
- Technical Decision Records
- Recommended Next Sprint
- Suggested Git Commit Message

Without a Sprint Report, the Sprint is not considered completed.

## Source Control

Git is the primary source of truth. ZIP files are only generated when:

- requested by the Product Owner
- milestone backup
- final delivery

Otherwise use the Git workflow.

## LLM Policy

The project is allowed to use **one** external LLM service.

**Approved provider:** Google AI Studio (Gemini API).

Reason:

- free for prototyping
- no local model download
- fast integration
- sufficient for interview demo

The LLM **must not** perform candidate scoring. Candidate scoring must remain deterministic and
explainable.

The LLM may only be used for:

- HR Summary
- Candidate Explanation
- Recommendation Narrative
- Skill Explanation

## Architecture

```
Deterministic Pipeline
        ↓
Candidate JSON
        ↓
Embedding
        ↓
FAISS Similarity
        ↓
Weighted Scoring
        ↓
Ranking
        ↓
Gemini Summary
        ↓
Dashboard
```

## Engineering Change Control

If the Technical Lead proposes a specification that conflicts with the actual implementation,
do not blindly implement it. Instead:

- explain the conflict
- explain the risk
- propose alternatives
- recommend the best engineering solution

Healthy technical disagreement is encouraged.

## Communication

Respond as a Senior Software Engineer. Be concise. Be critical. Be constructive. Do not
exaggerate. Challenge poor engineering decisions.
