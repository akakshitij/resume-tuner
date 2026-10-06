# resume-tuner

**Tune your real resume to one job, without inventing anything, and without it reading as AI-written.**

By **Kshitij Khandelwal**, product designer · [akakshitij.com](https://akakshitij.com)

---

## Why it exists

Two things get a resume binned before anyone reads it properly:

1. **The ATS can't match it.** You did the work, but you called it something else.
2. **It reads as AI-written.** Ten bullets the same length, "spearheaded", "leveraged", "…resulting
   in improved…". Recruiters spot it in seconds.

Ask a chatbot to "tailor my resume" and it rewrites the whole page, and quietly adds things you
never said. In testing, a plain Claude rewrite decided a company was a payments business because
the job ad was. resume-tuner makes **2–3 changes that matter**, keeps every word traceable to your
real resume, and marks what's missing as `[NEED: …]` or **GAP** instead of filling it in.

## What it does

1. **Echoes your profile** back first, so it never tunes a stale resume.
2. **Reads the job for signals**: required skills, seniority verbs ("own" vs "support"), and the
   words it repeats. Repetition is what the job actually cares about.
3. **Sorts each signal**: present, buried (you have it, under another name), or missing (a gap,
   never faked).
4. **Makes 2–3 changes**, before → after: a keyword surfaced verbatim, one bullet rewritten to lead
   with the #1 requirement, a reorder or a summary fix.
5. **Pushes for real numbers.** Aims for 70% of bullets with one, by asking you specific questions.
   Never estimates.
6. **Makes it read human**, with a checker that measures the tells.
7. **Checks ATS format**, and optionally scores fit (0–1) and drafts a 200-character note to the
   hiring manager.

## The checker

`scripts/check_resume.py` turns "does this look AI?" into numbers. Standard library only; reads PDFs
if `pypdf` is installed. Nothing leaves your machine.

```bash
python3 scripts/check_resume.py resume.pdf --jd job.txt
```

It reports: bullets with a number, how uniform bullet lengths are, repeated opening verbs,
buzzwords, stock phrases, "…, resulting in" chains, em dashes, first person, sentences copied from
the job, job keywords missing verbatim, page count, and generator names in the PDF metadata.

## Install

```bash
git clone https://github.com/akakshitij/resume-tuner ~/.claude/skills/resume-tuner
```

Start a new Claude Code session. On claude.ai, zip the folder and upload it under Settings →
Capabilities → Skills.

## Use

```
Tailor my resume for this job: resume.pdf + <paste the job posting>
Does my CV look AI-generated?
Why am I not getting interviews? Here's my resume and three jobs I applied to.
```

See [`examples/sample-tuning.md`](examples/sample-tuning.md) for a full run.

## The one rule

**Reframe, never fabricate.** A resume change that invents experience gets you an interview you'll
fail.

## Credits

The tuning flow (profile echo, top-5 signals, present/buried/missing, 2–3 changes, the fit-score
weights and the 200-character note) is adapted from **Abhijay Vuyyuru**'s Job Hunt OS and "5 steps
to land at least 1 interview" (Substack, 2026). The AI-tells list, the checker and the honesty
rules are mine.

## License

MIT © 2026 Kshitij Khandelwal
