#!/usr/bin/env python3
"""check_resume.py: measure how a resume reads to an ATS and to a tired recruiter.

Usage:
  python3 check_resume.py resume.pdf|resume.txt|resume.md [--jd job.txt] [--json]

Standard library only. PDF text extraction uses pypdf if it's installed
(pip install pypdf); otherwise pass a .txt or .md export of the resume.
Nothing leaves your machine.
"""
import argparse, json, re, statistics, sys
from collections import Counter
from pathlib import Path

BUZZ = """spearheaded orchestrated leveraged leverage synergy synergies results-driven dynamic
passionate detail-oriented cutting-edge innovative robust seamless seamlessly utilize utilized
utilizing facilitate facilitated championed pioneered fostered streamlined revolutionized
transformative visionary go-getter self-starter thought-leader best-in-class world-class
game-changer game-changing holistic impactful proactive proactively strategic strategically
meticulous meticulously adept adeptly showcasing showcased underscore underscoring pivotal
instrumental navigate navigated landscape realm tapestry testament delve elevate elevated
empower empowered unlock unlocked""".split()
PHRASES = ["proven track record", "results-oriented", "cross-functional collaboration",
           "fast-paced environment", "team player", "think outside the box", "hit the ground running",
           "wide range of", "a variety of", "responsible for", "duties included", "resulting in",
           "in order to", "ensuring", "driving", "with a focus on", "excellent communication"]
STOP = set("""a an the and or of to in on for with by at from as is are was were be been this that
these those it its into over under your you our we their they he she his her them i me my
will can may must should would could not no yes any all each per via experience years ideally strong comfortable nice have care youll work team role""".split())
METRIC = re.compile(r"(\d[\d,.]*\s?(%|x|k|m|bn|mn|million|billion|users|customers|ms|s|hrs?|hours|days|weeks|months|people|engineers|markets|countries|languages|screens|components|teams?)\b|[$£€₹]\s?\d|\d+\s?(→|->|to)\s?\d+)", re.I)
BULLET = re.compile(r"^\s*([•·\-\*–]|\d+[.)])\s+")

def read(path):
    p = Path(path)
    if p.suffix.lower() == ".pdf":
        try:
            from pypdf import PdfReader
        except ImportError:
            sys.exit("pypdf isn't installed: pip install pypdf, or pass a .txt export")
        r = PdfReader(str(p))
        meta = {k: str(v) for k, v in (r.metadata or {}).items()}
        return "\n".join(pg.extract_text() or "" for pg in r.pages), len(r.pages), meta
    return p.read_text(errors="ignore"), None, {}

def bullets(text):
    lines = [l.rstrip() for l in text.splitlines()]
    out = [BULLET.sub("", l).strip() for l in lines if BULLET.match(l)]
    if len(out) >= 3:
        return out
    # PDF exports often drop bullet glyphs and wrap long bullets over several lines.
    # Rebuild bullets: start at a capitalised line, keep joining until a line ends with a full stop.
    out, cur = [], ""
    for l in (x.strip() for x in lines):
        if not l or re.search(r"\b(19|20)\d{2}\b|\||@", l):
            cur = ""; continue
        if not cur and not re.match(r"^[A-Z][a-z]+\b", l):
            continue
        cur = (cur + " " + l).strip()
        if cur.endswith("."):
            if len(cur.split()) >= 6:
                out.append(cur)
            cur = ""
    return out

def words(t):
    return re.findall(r"[a-z][a-z+#.\-]*[a-z+#]|[a-z]", t.lower())

def jd_signals(jd, n=15):
    toks = [w for w in words(jd) if w not in STOP and len(w) > 2]
    bigr = [" ".join(p) for p in zip(toks, toks[1:])]
    c = Counter(toks) + Counter({b: v for b, v in Counter(bigr).items() if v >= 2})
    verbs = {"own", "lead", "support", "drive", "manage", "assist", "help"}
    return [w for w, v in c.most_common(n * 2) if v >= 2 and w not in verbs][:n]

def ngrams(t, n=8):
    w = words(t)
    return {" ".join(w[i:i+n]) for i in range(len(w) - n + 1)}

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("resume"); ap.add_argument("--jd"); ap.add_argument("--json", action="store_true")
    a = ap.parse_args()
    text, pages, meta = read(a.resume)
    low = text.lower()
    bl = bullets(text)
    lens = [len(b.split()) for b in bl]
    first = Counter(b.split()[0].lower() for b in bl if b.split())
    res = {
        "pages": pages,
        "pdf_producer_creator": {k: v for k, v in meta.items() if k in ("/Producer", "/Creator")},
        "bullets": len(bl),
        "metric_ratio": round(sum(bool(METRIC.search(b)) for b in bl) / len(bl), 2) if bl else None,
        "bullet_length_mean": round(statistics.mean(lens), 1) if lens else None,
        "bullet_length_spread": round(statistics.pstdev(lens) / statistics.mean(lens), 2) if len(lens) > 1 else None,
        "repeated_openers": {w: c for w, c in first.items() if c >= 3},
        "buzzwords": {w: c for w, c in Counter(w for w in words(text) if w in BUZZ).items()},
        "stock_phrases": {p: low.count(p) for p in PHRASES if low.count(p)},
        "em_dashes": text.count("—"),
        "first_person": len(re.findall(r"\b(I|me|my)\b", text)),
        "resulting_in_shape": len(re.findall(r"(?i),\s*(resulting in|leading to|driving)\b", text)),
    }
    if a.jd:
        jd = Path(a.jd).read_text(errors="ignore")
        sig = jd_signals(jd)
        res["jd_signals"] = sig
        res["jd_signals_missing_verbatim"] = [s for s in sig if s not in low]
        res["jd_sentences_copied"] = len(ngrams(text) & ngrams(jd))
    flags = []
    if pages and pages > 1: flags.append(f"{pages} pages: one page unless 10+ years")
    if any(re.search(r"(?i)gpt|openai|claude|anthropic|reportlab|skia|headless", v) for v in res["pdf_producer_creator"].values()):
        flags.append("PDF metadata names a generator: strip /Producer and /Creator")
    if res["metric_ratio"] is not None and res["metric_ratio"] < 0.7:
        flags.append(f"{res['metric_ratio']:.0%} of bullets carry a number (target 70%, real numbers only)")
    if res["bullet_length_spread"] is not None and res["bullet_length_spread"] < 0.2 and len(lens) >= 6:
        flags.append("bullets are suspiciously uniform in length (spread < 0.2): an AI tell")
    if res["repeated_openers"]: flags.append(f"same opening verb 3+ times: {res['repeated_openers']}")
    if sum(res["buzzwords"].values()) >= 3: flags.append(f"buzzwords: {res['buzzwords']}")
    if res["stock_phrases"]: flags.append(f"stock phrases: {res['stock_phrases']}")
    if res["em_dashes"] >= 2: flags.append(f"{res['em_dashes']} em dashes: an AI tell on resumes")
    if res["first_person"]: flags.append(f"{res['first_person']} first-person words (I/me/my) in a resume")
    if res["resulting_in_shape"] >= 3: flags.append(f"'..., resulting in' shape used {res['resulting_in_shape']}x: vary it")
    if a.jd and res["jd_sentences_copied"]: flags.append(f"{res['jd_sentences_copied']} 8-word runs copied from the JD: mirror keywords, never sentences")
    if pages is not None: flags.append("PDF: bullet counts and lengths are rebuilt from wrapped lines, so treat them as approximate; a .txt export is exact")
    if pages is None: flags.append("not a PDF: page count and metadata not checked; export to PDF and re-run")
    res["flags"] = flags
    if a.json:
        print(json.dumps(res, indent=2, ensure_ascii=False)); return
    for k, v in res.items():
        if k != "flags": print(f"{k:28} {v}")
    print("\nFLAGS" if flags else "\nFLAGS  none")
    for f in flags: print(" -", f)

if __name__ == "__main__":
    main()
