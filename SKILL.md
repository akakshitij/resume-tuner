---
name: resume-tuner
description: >-
  Tunes a real resume to one job description without inventing anything: pulls the job's top
  signals, sorts them into present, buried or missing, makes the 2–3 changes that matter most,
  flags honest gaps, and removes the tells that get a resume binned as AI-written. Use when
  someone says "tailor my resume", "tune my CV for this job", "does my resume look AI-generated",
  "ATS check", "why am I not getting interviews", "rewrite my bullets", "make my resume sound
  human", or pastes a resume and a job posting together, even if they only ask "is this good?".
  Not for writing a resume from nothing (it needs a real one to start from).
metadata:
  author: Kshitij Khandelwal
  homepage: https://akakshitij.com
  version: 1.0.0
  license: MIT
---

# resume-tuner

Two things get a resume rejected before anyone reads it properly: **an ATS can't match it to the
job**, and **a recruiter thinks AI wrote it**. This skill fixes both, using only what's true.

**The one rule: reframe, never fabricate.** Every word in the tuned resume traces to the person's
own resume or something they told you in this conversation. A change that invents experience gets
an interview they'll fail. Missing facts are written as `[NEED: …]` and asked for, never filled in.

## 1. Echo the profile first

From the resume, write back in five lines: target titles, level, hard skills, the 2–3 strongest
results (with their real numbers, or "none have numbers yet" and the best raw material), past
companies and education. Ask "Anything out of date or
missing?" and wait. Old resumes miss current roles; tuning a stale one wastes the run.

## 2. Read the job for signals

Run the checker if you can execute code:

```bash
python3 scripts/check_resume.py <resume.pdf|.txt|.md> --jd <job.txt>
```

Then read the posting yourself and pull the **top 5 signals**: required skills and tools, the
seniority verbs ("own", "lead", "support" each mean a different level), and **repeated words**.
Repetition is the posting telling you what it actually cares about.

Sort every signal into one bucket:

| Bucket | Meaning | What to do |
|---|---|---|
| **Present** | In the resume, in the job's words | Leave it, maybe move it up |
| **Buried** | They have it, but call it something else or it's low on the page | Rename it **verbatim** to the job's term, move it up, **only if it's the same thing** |
| **Missing** | Genuinely not there | **GAP**: never add it. Say it to them; it goes in the cover letter or outreach |

## 3. Make 2–3 changes, no more

Most impact first. Each change is one of these three, shown as before → after:

1. **Surface a keyword.** "The posting says 'user research' three times; you call it 'UX
   discovery'. Rename it in your skills and your top bullet." Verbatim matters for ATS matching.
   **Check the fact first:** rename only when it's genuinely the same thing. If 'model QA' wasn't
   on an LLM, it isn't 'LLM evals': ask, and if not, it's a GAP.
2. **Rewrite one bullet** so it leads with the job's #1 requirement, keeping the real numbers.
   Formula: **action verb + what they did + quantified result**.
3. **Reorder**: the most relevant role or bullet moves above the fold.
4. **Fix the summary** (counts as a change): one true line (what they do, for whom, one
   distinguishing fact), or cut it.

Three changes a person makes beat twelve they skim. If more is wrong, say so and offer a second
pass. The human-read fixes in step 5 are separate from these 2–3: they're about how every line
reads, not what it says.

## 4. Push for real numbers

Aim for **at least 70% of bullets carrying a number**. Numbers come from the person, never from
you:

- For each bullet without one, ask a specific question: "Roughly how many users went through the
  new onboarding? Did activation move, and by how much?"
- Accept **ranges and scope** when there's no outcome number: markets, platforms, screens, team
  size, weeks, users. "Across 3 markets and 2 platforms" is a real number.
- Never estimate, round up, or turn "improved" into a percentage. A number they can't defend in an
  interview is worse than none. Put `[NEED: number]` and move on.
- **If the resume has no numbers at all**, don't rewrite every bullet full of `[NEED]` slots. Make
  the 2–3 changes, list the number questions, and offer the full rewrite once they've answered.

## 5. Make it read human

Recruiters bin resumes that sound generated. Run the checks in `references/ai-tells.md`. The usual
culprits: buzzwords (spearheaded, leveraged, orchestrated, results-driven), every bullet the same
length and shape, chains of "…, resulting in", em dashes, a summary that could describe anyone, and
whole sentences lifted from the job posting. Fix from the facts; swapping one buzzword for its
synonym creates a new tell.

## 6. Check the format

ATS rules in `references/ats-format.md`: single column, no tables, icons or images, standard
headings, reverse chronological, PDF, one page under 10 years of experience, and a PDF whose
metadata doesn't name an AI tool. Given a .txt, .md or .docx instead of a PDF, check headings and
order, and say the page count and metadata need a re-check on the exported PDF.

## 7. Score the fit, honestly

Only if they ask whether to apply, or for several jobs at once: score 0–1 with the weights in
`references/fit-score.md` (title and level 35%, skills 35%, domain 15%, logistics 15%), give
**why they match** and **what a recruiter will question**, and say "skip" under 0.55.

## Output

```
Profile: <5 lines> (confirmed)
Signals: <top 5> · Present: … · Buried: … · Missing (GAP): …
Change 1: <before> → <after> (why)
Change 2: …
Change 3: …
Numbers to ask for: <bullet> → <question>
Human-read fixes: <what the checker or the tells list caught, and the fix>
Format: <pass or the specific fix>
Gaps to use in the letter or outreach: <one line each>
Next: <their next action>
```

Optional: a LinkedIn connection note for the hiring manager or recruiter, under 200 characters:
one real hook + one proof point + one small ask. Every personal line must trace to something
public and checked; with no real hook, open with the role. Fake familiarity reads worse than none.
See `references/outreach-note.md`.

## Red flags

| Thought | Reality |
|---|---|
| "They probably did something like this" | Not unless they say so. Ask, or mark it GAP |
| "I'll put 30% in, it's plausible" | An invented number is a lie they'll be asked about. `[NEED: number]` |
| "Paste the job's requirements in as bullets" | Mirror the keywords, never the sentences. Copied lines read as fake |
| "Twelve improvements will impress them" | Two or three that get made. Offer a second pass |
| "Replace 'leveraged' with 'utilised'" | That's a synonym, not a fix. Rewrite the line from the fact |

## Files

- `scripts/check_resume.py`: measures numbers per bullet, length uniformity, buzzwords, stock
  phrases, em dashes, keywords missing from the job, copied sentences, page count and PDF metadata
- `references/ai-tells.md`: what makes a resume read as AI-written, and the fix for each
- `references/ats-format.md`: format rules that get a resume parsed
- `references/fit-score.md`: the 0–1 fit score and when to skip
- `references/outreach-note.md`: the 200-character note
- `examples/sample-tuning.md`: a full run on a fictional resume
