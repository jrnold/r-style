"""Sample recent NEWS bullets and count wording patterns (evidence for r-news).

Run it in the directory that holds <pkg>.md files, as for audit_news.py.
"""

import collections
import random
import re
from pathlib import Path

from audit_news import PK, bullets, sections

allb = []  # (pkg, heading, text)
for p in PK:
    secs = sections(Path(f"{p}.md").read_text())
    dev = bool(re.search("development version", secs[0][0], re.IGNORECASE))
    take = secs[:2] if dev else secs[:1]
    # also include previous release when dev section is short
    if dev and len(bullets(secs[0][1])) < 8:
        take = secs[:3]
    for h, body in take:
        allb.extend((p, h, b["text"][2:].strip()) for b in bullets(body))
print("recent bullets", len(allb), collections.Counter(p for p, _, _ in allb))


def norm(t: str) -> str:
    """Replace backticked code with a placeholder so openers group together."""
    return re.sub(r"`[^`]*`", "FN", t)


op = collections.Counter()
op2 = collections.Counter()
for _, _, t in allb:
    w = norm(t).split()
    op[" ".join(w[:2])] += 1
print("\nOPENERS (2 words):", op.most_common(25))
# verbs following a leading `fn()`
v = collections.Counter()
for _, _, t in allb:
    m = re.match(
        r"^(?:In )?`[^`]+`(?: and `[^`]+`)*(?:, `[^`]+`)*(?:,? and `[^`]+`)? (\w+(?: \w+)?)", t
    )
    if m:
        v[m.group(1).lower()] += 1
print("\nVERB after leading fn:", v.most_common(30))
# phrases
ph = [
    "now",
    "no longer",
    "gains",
    "is now",
    "are now",
    "can now",
    "now works",
    "now supports",
    "now errors",
    "now warns",
    "now returns",
    "now throws",
    "now respects",
    "now accepts",
    "now uses",
    "is deprecated",
    "are deprecated",
    "soft-deprecated",
    "defunct",
    "lifecycle",
    "regression",
    "previously",
    "instead",
    "new argument",
    "new `",
    "fixed a",
    "fixes",
    "fix ",
    "thanks",
    "see `",
    "see ?",
    "vignette(",
    "improved",
    "improves",
    "better",
    "more informative",
    "informative",
    "helpful",
    "error message",
    "messages",
    "warns",
    "warning",
    "consistently",
    "correctly",
    "no longer",
    "unexpected",
    "spurious",
    "incorrectly",
    "#",
    "(@",
    "(#",
]
tot = len(allb)
print("\nPHRASES of", tot)
for x in ph:
    n = sum(1 for _, _, t in allb if x in t.lower())
    print(f"  {x!r}: {n} ({100 * n // tot}%)")
# reference formats
REF = r"(?:@[\w-]+|#\d+|[\w-]+/[\w-]+#\d+)"
fm = collections.Counter()
for _, _, t in allb:
    m = re.search(
        rf"\(({REF}(?:(?:, | and | ){REF})*)\)\.?\s*$",
        t,
    )
    if m:
        toks = re.findall(r"@[\w-]+|#\d+|[\w-]+/[\w-]+#\d+", m.group(1))
        kind = "".join("U" if x.startswith("@") else ("X" if "/" in x else "I") for x in toks)
        sep = "comma" if ", " in m.group(1) else ("and" if " and " in m.group(1) else "space")
        fm[(kind, sep)] += 1
print("\nREF FORMATS (U=@user I=#issue X=owner/repo#n):", fm.most_common(15))
# link styles
ls = collections.Counter()
for _, _, t in allb:
    if re.search(r"\[`[^`]+`\]\(", t):
        ls["[`fn()`](url)"] += 1
    if re.search(r"\[[^\]`]+\]\(http", t):
        ls["[text](http)"] += 1
    if re.search(r"\bhttps?://", t):
        ls["bare url"] += 1
    if re.search(r"`vignette\(|\bvignette\(", t):
        ls["vignette()"] += 1
    if re.search(r"`\?\w+`|\?\w+", t):
        ls["?topic"] += 1
    if re.search(r"\w+::\w+", t):
        ls["pkg::fn"] += 1
    if "```" in t:
        ls["code fence"] += 1
    if re.search(r"`NULL`|`TRUE`|`FALSE`|`NA`", t):
        ls["literal value in backticks"] += 1
    if re.search(r"\*[A-Za-z][^*]*\*", t):
        ls["*italic*"] += 1
    if re.search(r"\bR (>=|\d)", t):
        ls["R version"] += 1
    if re.search(r"edition|breaking", t, re.IGNORECASE):
        ls["edition/breaking word"] += 1
print("LINK/FORMAT:", dict(ls))
# internal/dev-facing language
for k in [
    "internal",
    "refactor",
    "developers",
    "extension",
    "package authors",
    "downstream",
    "CRAN",
    "performance",
    "faster",
    "memory",
    "typo",
    "documentation",
]:
    n = sum(1 for _, _, t in allb if k.lower() in t.lower())
    print(" ", k, n)
random.seed(7)
print("\nSAMPLES")
for p, _, t in random.sample(allb, 45):
    print(f"[{p}]", t[:230])
