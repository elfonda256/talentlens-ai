# TalentLens AI — Demo Playbook

**For:** the TalentLens AI presentation to Allure Industries, 18 November 2026
**Audience:** HR Director, Head of Talent Acquisition, CIO, CEO
**Demo URL:** `https://talentlens-ai-azure.vercel.app`
**Live state (checked 18 Nov, 01:15 WIB):** 1 vacancy (Junior Architect), 5 company CVs,
3 Direkomendasikan, 2 Perlu ditinjau, 0 Tidak lolos. Scores 91,3 · 87,8 · 83,4 · 66,5 · 46,3.
All 5 AI summaries are already generated and saved, so they open instantly.

Speaking lines are written in English. Say them in Indonesian if the room speaks Indonesian; the
interface is already in Indonesian.

**Three lines to memorise**

- "The rules score. The AI explains. HR decides."
- "Same CV, same vacancy, same score, every time."
- "Every number on this screen can be traced back to a sentence in the CV."

---

## Candidate map

Names are hidden on screen. Use rank numbers when you speak.

| Rank | Score | Decision | Use it to show |
|---|---|---|---|
| #1 | 91,3 | Direkomendasikan, "Paling cocok" | The full explanation: score, AI summary, interview questions, breakdown |
| #2 | 87,8 | Direkomendasikan | Why 6,5 years of experience ranks below 3,9 years |
| #3 | 83,4 | Direkomendasikan | Missing Revit: recommended, with a gap flagged for the interview |
| #4 | 66,5 | Perlu ditinjau | Human-in-the-loop: education field and level do not match |
| #5 | 46,3 | Perlu ditinjau | Only if asked: 0,3 years of relevant experience, just above the reject line |

---

## 1. Before you start, and which page to open first

### The evening before or the morning of the demo

1. **Read all 5 AI summaries and their interview questions.** They are saved, so what you read is
   what the audience will see. Check that none contradicts the numbers on screen, and note which
   question on #1 targets an implied skill, so you can point to it.
2. **Take backup screenshots** (see section 9) and put them in one folder on the desktop.
3. **Record a 5-minute screen video** of the 5-minute version (section 10). It is your last resort.
4. **Rehearse the 10-minute version once, out loud, with a timer.**

### 30 minutes before

1. **Sign in to Vercel** in the demo browser (the account that owns the project). Every page is
   behind Vercel login. A share link exists, but it **expires 18 Nov at 12:24 WIB**; do not rely on it.
2. **Warm up the system.** Open the dashboard, the vacancy, and each of the 5 candidates once.
3. **Open tabs in this order**, so you can switch instead of loading during the talk:
   1. Dasbor rekrutmen (`/`)
   2. Pengumpulan CV (`/sources`)
   3. Vacancy page (Junior Architect)
   4. Candidate #1
   5. Candidate #2
   6. Candidate #4
4. Browser zoom 110–125% for the projector. Close other apps and notifications.
5. Confirm **"Tampilkan nama kandidat" is off**. These are real applicants.
6. Have the phone hotspot ready (section 9).

### First page to open

**Dasbor rekrutmen** (`/`). It shows the whole picture in one glance: one vacancy, five
candidates, three recommended, two to review. Start there, not on a candidate page.

---

## 2 and 3. Screen by screen: what to click and what to say

### Screen 1 — Dasbor rekrutmen

**Click:** nothing. Let them read the four numbers.

**Say:**
> "A recruiter's first pass through CVs takes minutes per CV, and it is the least valuable part of
> the job. TalentLens does that first pass in seconds and explains every decision. Here is one real
> vacancy from your team, Junior Architect, and the five CVs you gave us: three recommended for
> interview, two that need a human decision."

**Point to:** the four totals, then the colour bar on the job card (green recommended, amber review).

### Screen 2 — Pengumpulan CV (optional in the 5-minute version)

**Click:** **Pengumpulan CV** in the header.

**Say:**
> "Today CVs come in by manual upload, which is what we use in this demo. This page shows where the
> product goes next: career site, email inbox, shared folders, LinkedIn, Jobstreet, Kalibrr and Indeed.
> Each one is marked as a future production integration. They will connect through official partner
> access, never by scraping, and every source feeds the same screening engine and the same rules."

**Point to:** the architecture row: Sumber lamaran → Lapisan integrasi (future) → Mesin penyaringan
TalentLens (already running). Then the four principles at the bottom.

**Do not say** that any of these sources is connected. None is.

### Screen 3 — Vacancy page, criteria

**Click:** **Dasbor** → the **Junior Architect** card → expand **Kriteria penilaian**.

**Say:**
> "Before screening anyone, the system read the job description and turned it into criteria:
> two years minimum, an architecture or interior design degree, eight required skills and two
> nice-to-haves. HR can check these before trusting the ranking. If the job description is wrong,
> you see it here first."

### Screen 4 — Vacancy page, ranking

**Click:** scroll to **Peringkat kandidat**. Leave the filter on all candidates.

**Say:**
> "This is the ranking. The large number is the AI score out of 100. Number one has the badge
> 'Paling cocok'. Names are hidden by default, so the first pass is blind. Each row already says the
> one thing HR should know, for example how many required skills were found and the relevant years."

**Point to:** the score ring of #1, the badge, the "Keterampilan wajib" and "Pengalaman" facts, the
recommendation badge on the right.

### Screen 5 — Candidate #1 (the main screen)

**Click:** row **#1**.

Walk down the page in this order:

1. **Score and decision (top card).**
   > "91,3 out of 100, recommended, best match. The bar shows what made up that score."
2. **Ringkasan AI untuk hiring manager.**
   > "This is what a hiring manager reads instead of the CV: a verdict, strengths, gaps, and the
   > reason for the recommendation. The AI writes these words from facts the system already
   > calculated. It never changes the score, and the candidate's name and contact details are never
   > sent to it."
3. **Pertanyaan wawancara.**
   > "And these are interview questions written for this candidate's own gaps, not a generic list,
   > such as the skills the CV only implies."
4. **The three panels: Rekomendasi tindak lanjut, Keyakinan AI, Potensi risiko.**
   > "Next steps for HR, how confident the system is and why, and what to watch for."
5. **Dari mana skor ini berasal.**
   > "This is the part that matters most for trust. Five components, each with its weight and its
   > points. They add up exactly to 91,3. Nothing is hidden."
6. **Kecocokan dengan syarat lowongan.**
   > "Each required skill shows whether it is written in the CV, only implied, or not found.
   > 'Tersirat' means the work described shows the skill even though the CV doesn't name it. It gets
   > partial credit and is flagged for HR to confirm in the interview."
7. **Bukti dari CV** (top of the section only).
   > "And here is the exact sentence from the CV behind each match."

### Screen 6 — Candidate #2 (the planned "aha" moment)

**Click:** back → row **#2**.

**Say:**
> "You may ask: why does someone with 6,5 years rank below someone with 3,9 years? Experience counts
> until the requirement is clearly met, then extra years add little. Both pass the two-year minimum,
> so their experience points are almost the same. Number one wins on skills written explicitly in the
> CV, and on how closely the CV matches the job. Every point is visible here."

**Point to:** **Dari mana skor ini berasal**, compare the *Pengalaman* and *Kesesuaian isi CV* rows
with what you showed for #1. Then **Potensi risiko**: the system notes that experience is far above
the requirement, so salary and role expectations should be checked.

### Screen 7 — Candidate #4 (human in the loop)

**Click:** back → row **#4**.

**Say:**
> "This candidate has solid drafting experience, but the education doesn't match the requirement.
> The system doesn't reject them. It sends them to HR as 'Perlu ditinjau' and says exactly what to
> decide: can we accept the education gap? That decision belongs to a person."

**Point to:** **Rekomendasi tindak lanjut** (the "Putuskan apakah ini dapat ditoleransi" steps).

### Screen 8 — Close (on the dashboard)

**Click:** **Dasbor**.

**Say:**
> "To sum up: the first pass that took a recruiter hours now takes seconds. Every candidate is judged
> by the same rules. Every score can be traced to a sentence in the CV. The AI writes the
> explanation, and HR makes the decision. Next steps toward production are validating more job
> families, hosting in Indonesia with a data-protection policy, user roles and an audit trail, and
> connecting the sources you saw on the collection page."

---

## 4 and 5. Expected questions and best answers

Rule for every answer: **one or two sentences, then show it on screen, then stop.** If a weakness
comes up, admit it in one sentence, name the next step, and go back to the screen.

### HR Director and Head of Talent Acquisition

**Q1. "Our ATS already filters keywords. What's different?"**
Keyword filters miss people who describe the same skill differently. TalentLens matches meaning, it
recognises skills implied by the work described, and every match shows the CV sentence it came from.
*Show:* #1 → Kecocokan dengan syarat lowongan → a "Tersirat" skill.

**Q2. "Why is #1 (3,9 years) above #2 (6,5 years)?"**
See Screen 6. Experience counts until the requirement is clearly met; the difference is skills
written explicitly and how well the CV fits the job.
*Show:* Dari mana skor ini berasal on #1 and #2.

**Q3. "Can it discriminate by gender, age, religion, or university?"**
The score uses four things only: skills, relevant experience, education field, and how well the CV
fits the job. Name, photo, age, gender, religion and address never enter the score, and names are
hidden on screen by default.
*Show:* the hidden names on the ranking.

**Q4. "Who makes the final decision?"**
HR, always. The system recommends and explains; it never rejects anyone on its own.
*Show:* the footer line on every page.

**Q5. "What about a good candidate with a badly written CV?"**
Three safety nets: implied skills still get partial credit, sections the system cannot read are not
counted as zero, and borderline candidates go to "Perlu ditinjau" instead of rejection.
*Show:* #1 → Pembacaan dokumen.

**Q6. "Can you show us uploading a CV?"**
Yes, it accepts PDF, Word and scanned CVs and screens in seconds. Today I'm using the five CVs your
team provided so the results stay comparable. Show the **Unggah CV** button; upload only if they
insist (see section 7).

**Q7. "Which formats? What about scanned CVs?"**
PDF, DOCX and TXT. Scanned PDFs are read with text recognition, and the screen tells HR what kind of
document it was and how much of each section was read.
*Show:* Pembacaan dokumen.

**Q8. "How accurate is it?"**
Don't give a percentage. "We test it against a fixed benchmark: 20 architecture CVs across 5
vacancies, with the expected results written before the system ran. Every change must reproduce that
benchmark before it ships, and 178 automated tests run on every change. On your five CVs, the order
matches what an experienced recruiter would expect."
*Honest limit:* the benchmark covers architecture roles only so far.

**Q9. "Can the AI summary make things up?"**
The AI only puts into words facts the system already calculated. It cannot change a score, it is
told to mark implied skills as needing confirmation, and if the AI service fails a standard summary
is shown instead.
*Show:* the caption under Ringkasan AI.

**Q10. "What does 'Tersirat' mean?"**
The CV doesn't name the skill, but the work described shows it. It gets partial credit and is
flagged for HR to confirm in the interview.

**Q11. "Why is AI confidence 'Sedang' for everyone?"**
Confidence reflects how completely the CV was read and how far the score is from a decision line.
Each of these five has at least one skill that is only implied, so the system says "medium" instead
of overclaiming. The ranking doesn't change.

**Q12. "Can it detect a fake CV?"**
No screener truly can. What it does is show which sentence supports each claim, separate written
skills from implied ones, and give interview questions that test those claims.

**Q13. "Does it work for finance, sales or IT roles?"**
The engine reads any vacancy and any CV. We validate one job family at a time with a fixed benchmark;
architecture is done and the others are planned. Never claim other roles are validated.

**Q14. "Are the interview questions generic?"**
No. Open #1 and #2: the questions differ because they come from each candidate's own gaps.

**Q15. "Indonesian and English CVs?"**
Yes. The matching model is multilingual; your five CVs are in English and the interface is in
Indonesian.

**Q16. "Why is #5 not rejected?"**
Its score of 46,3 sits just above the rejection line, so the system hands it to a person rather than
rejecting it. The thresholds are business rules HR can tighten later. Don't volunteer this one.

### About CV collection (new page)

**Q17. "Is it connected to LinkedIn or Jobstreet now?"**
No. Those are marked as the next production phase. Today CVs come in by upload. The page shows how
they will connect and what each connection needs.

**Q18. "Why not just scrape LinkedIn or Jobstreet?"**
Scraping breaks those platforms' terms of use and creates a personal-data risk under UU PDP. We
connect only through the official partner or API access each platform provides.

**Q19. "How long would integrations take?"**
Don't promise dates. "Email inbox and shared folders are the fastest, because they only need access
from your IT team. Job portals depend on each platform approving partner access."

### CIO

**Q20. "Where is candidate data stored? Are we UU PDP compliant?"**
For this proof of concept the app runs on managed cloud services behind login, with files on a
private storage volume. For production we would host in an Indonesian region or on your own servers,
with a retention and deletion policy and candidate consent. The application is containerised, so it
can move. If asked directly: the demo backend runs in a US region.

**Q21. "Is our data sent to Google?"**
Scoring runs entirely on our own server with our own language model; no CV leaves it for scoring.
Only the summary step calls Gemini, and it receives facts without name, email or phone number.

**Q22. "Is it secure?"**
Every page is behind authentication. The backend requires a secret key that stays on the server and
never reaches the browser, API documentation pages are disabled in production, and requests from
unknown sites are rejected. User roles and audit logging are production items.

**Q23. "What if the AI service goes down?"**
Scoring doesn't depend on it. Only the written summary switches to a standard version, and the system
tries a second AI model before that.

**Q24. "Can it integrate with our ATS or HRIS?"**
Everything you see runs through an API (vacancy, upload, screening, ranking), so integration is a
connector, not a rebuild. It is outside the proof of concept.

**Q25. "What's the stack? Who maintains it?"**
Next.js frontend; Python and FastAPI backend in Docker; a multilingual language model running locally
for matching; plain rules for scoring; Gemini for summaries. Maintained in Git with documented
decisions, 178 automated tests and a benchmark every change must pass.

**Q26. "Can results be reproduced for an audit?"**
Yes. The same CV and vacancy always give the same score, and each score breaks down into parts that
add up exactly. Say this with confidence.

**Q27. "What does it cost to run?"**
Scoring runs on a small server with no per-CV AI fee. The only usage-based cost is the AI summary,
created once per candidate and then saved. Exact cost depends on volume; don't quote numbers.

### CEO

**Q28. "What's the business value?"**
First-pass reading goes from minutes per CV to seconds per batch, every candidate is judged by the
same rules, and hiring managers get a reasoned summary and interview questions instead of a pile of
PDFs. Ask them: "How many CVs does one opening receive?" Don't invent ROI percentages.

**Q29. "Will this replace recruiters?"**
No. It removes the reading, not the judgement. Recruiters spend their time on the shortlist and the
interview.

**Q30. "What if it rejects a great candidate?"**
It never rejects anyone automatically. Every decision is a recommendation with a written reason,
borderline cases go to review, and HR can open any candidate.

**Q31. "What does it take to go to production?"**
Four steps: validate more job families, including against your past hiring decisions; host in
Indonesia with a data-protection policy; add user roles and an audit trail; connect the CV sources and
your ATS. Don't commit to dates on stage.

**Q32. "Why build this instead of buying an ATS with AI?"**
Every score is explained down to the sentence, scoring runs on infrastructure you control, and it
works in Indonesian on your vacancies. Most packaged tools give a match score without the reasoning.

---

## 6. Features to emphasise

In this order of importance:

1. **Explainable scoring.** Five components that add up exactly to the score, and the CV sentence
   behind each match. This is the differentiator.
2. **Deterministic and auditable.** Same input, same score. The AI never scores.
3. **AI with guardrails.** Gemini writes the hiring manager summary and interview questions from
   computed facts; personal data is masked; a standard summary appears if the AI is unavailable.
4. **Ready for HR's next step.** Candidate-specific interview questions, next steps, risks.
5. **Human in the loop.** Borderline cases go to "Perlu ditinjau" with a decision to make.
6. **Blind by default.** Names hidden.
7. **A credible roadmap.** The Pengumpulan CV page: one engine, many future sources, official
   access only.
8. **Engineering discipline** (CIO only). Golden benchmark, 178 tests, documented decisions.

---

## 7. Do NOT demonstrate

| Do not | Why | If they ask |
|---|---|---|
| Press **Susun ulang** on a summary | It calls the AI live, can take 15–60 s, and produces new wording you haven't read | "It rewrites the summary; the saved one is what HR reviews." |
| Turn on **Tampilkan nama kandidat** | These are real applicants' names on a projector | "Names are available to HR, hidden by default for blind screening." |
| Upload a new CV or click **Tambah lowongan** | Changes the numbers you rehearsed, and a first summary for a new CV takes 7–18 s | Show the button; upload only if they insist, using a CV they hand you |
| Click **Saring ulang** | Not needed; it re-runs screening on the server and adds waiting time | "It reproduces identical scores; we checked after the last update." |
| Claim any source on **Pengumpulan CV** is connected | None is | "That's the next production phase." |
| Scroll to the bottom of **Bukti dari CV** | Some lower evidence pairings look odd | Stay on the first items |
| Open Railway, Vercel, GitHub, logs or API URLs | Off-message, and exposes infrastructure | Offer a technical follow-up session |
| Show candidate #5 unprompted | Weakest case to explain in a short demo | See Q16 |
| Give accuracy percentages, ROI figures or dates | You can't back them up on stage | Use the Q8, Q28 and Q31 framing |

---

## 8. Backup plan: Gemini temporarily fails

**What you'll see:** nothing alarming. The five demo candidates' summaries are already saved and
open instantly without calling Gemini. For a newly uploaded CV, the app tries two Gemini models with
retries; if both fail, a standard summary in the same layout appears after up to about a minute.
There is no error message on screen.

**What to do:**

1. **Stay on the five saved candidates.** Their AI summaries cannot fail.
2. **Never press Susun ulang.** That is the only way to trigger a live call on a saved candidate.
3. If you uploaded a new CV and the summary is slow, keep talking over the skeleton for a few
   seconds, then move on: open the score breakdown, which never depends on Gemini.
4. **If someone notices the wording is plainer, say:**
   > "The AI service is temporarily busy, so the system used its standard summary. Notice that the
   > score, ranking and evidence are unchanged. Scoring never depends on the AI. That's by design."
5. Turn it into a strength: it demonstrates Q23.

---

## 9. Backup plan: slow internet

**Prepare tonight:**

- **Screenshots** in one desktop folder, named in demo order:
  `01-dasbor`, `02-pengumpulan-cv`, `03-kriteria`, `04-peringkat`, `05-kandidat-1-skor-ringkasan`,
  `06-kandidat-1-pertanyaan-panel`, `07-kandidat-1-rincian-skor`, `08-kandidat-1-kecocokan`,
  `09-kandidat-2-rincian-skor`, `10-kandidat-4-rekomendasi`. Keep names hidden in every shot.
- **A 5-minute screen recording** of section 10.
- **Phone hotspot** charged and tested with the demo laptop.

**On the day, escalate step by step:**

1. **Pages loading slowly (3–10 s):** use the tabs you opened 30 minutes before; switch tabs instead
   of clicking links. Fill the pause with the next talking point.
2. **The venue Wi-Fi is unreliable:** switch to the phone hotspot. The pages are light; a 4G
   connection is enough.
3. **No connection at all:** open the screenshot folder full screen and present the same script.
   Say once: "The connection is unstable, so I'll walk you through the same screens from captures."
4. **Very little time left:** play the 5-minute recording and keep the time for questions.

Never wait in silence for a page. Keep talking, or move to the next screenshot.

---

## 10. The 5-minute version

For an executive slot. One message: *explainable AI screening that keeps HR in control.*

| Time | Screen | Do | Say (core line) |
|---|---|---|---|
| 0:00–0:40 | Dasbor | — | Problem and result: 5 real CVs, 3 recommended, 2 for review |
| 0:40–1:30 | Vacancy → Peringkat kandidat | Scroll to the ranking | Scores out of 100, "Paling cocok", names hidden |
| 1:30–3:30 | Candidate #1 | Score → Ringkasan AI → Pertanyaan wawancara → Dari mana skor ini berasal | "The AI explains, the rules score; the five parts add up to 91,3" |
| 3:30–4:15 | Pengumpulan CV | Header link | "Upload today; career site, email and job portals next, through official access only" |
| 4:15–5:00 | Dasbor | — | Close with the three lines, and production next steps |

Skip: criteria, candidates #2 and #4, panels detail. Questions go after.

---

## 11. The 10-minute version

The recommended default.

| Time | Screen | Do | Say |
|---|---|---|---|
| 0:00–1:00 | Dasbor | — | Screen 1 |
| 1:00–1:45 | Pengumpulan CV | Header link | Screen 2, short |
| 1:45–2:45 | Vacancy | Expand Kriteria penilaian | Screen 3 |
| 2:45–3:30 | Vacancy | Peringkat kandidat | Screen 4 |
| 3:30–6:30 | Candidate #1 | Walk all seven blocks | Screen 5 |
| 6:30–7:45 | Candidate #2 | Dari mana skor ini berasal, Potensi risiko | Screen 6, the "aha" |
| 7:45–8:45 | Candidate #4 | Rekomendasi tindak lanjut | Screen 7 |
| 8:45–10:00 | Dasbor | — | Screen 8, close |

---

## 12. The 15-minute version

For a mixed HR and IT audience that wants depth. Includes planned question time.

| Time | Screen | Do | Say |
|---|---|---|---|
| 0:00–1:15 | Dasbor | — | Screen 1, plus the problem in their terms: "How many CVs does one opening get?" |
| 1:15–3:00 | Pengumpulan CV | Walk the diagram, the source groups and the principles | Screen 2 in full: one engine, many sources, official access, PII protected, source recorded |
| 3:00–4:00 | Vacancy | Expand Kriteria penilaian | Screen 3 |
| 4:00–4:45 | Vacancy | Peringkat kandidat | Screen 4 |
| 4:45–8:00 | Candidate #1 | All seven blocks, plus **Pembacaan dokumen** (document type and how much was read) | Screen 5, and Q5 on badly written CVs |
| 8:00–9:15 | Candidate #2 | Breakdown and risks | Screen 6 |
| 9:15–10:15 | Candidate #4 | Next steps | Screen 7 |
| 10:15–11:30 | Dasbor (no new screen) | — | How it is validated: fixed benchmark of 20 CVs with expected results written first; 178 automated tests; scoring code unchanged since the benchmark; AI never scores (Q8, Q26) |
| 11:30–12:00 | Dasbor | — | Close and production next steps (Q31) |
| 12:00–15:00 | — | Questions | Use section 4. Answer short, show on screen, stop |

---

## Quick reference card

- First page: **Dasbor**. Main screen: **Candidate #1**. "Aha": **#2 vs #1**. Human in the loop: **#4**.
- Never: Susun ulang, show names, upload, Saring ulang, claim integrations are live.
- Gemini trouble: stay on the five saved candidates; scoring never depends on AI.
- Network trouble: tabs → hotspot → screenshots → recording.
- Close: "The rules score. The AI explains. HR decides."
