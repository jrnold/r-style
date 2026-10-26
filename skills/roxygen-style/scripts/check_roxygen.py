#!/usr/bin/env python3
"""Heuristic roxygen style checker for the roxygen-style skill.

Usage: check_roxygen.py PKG_DIR [--rules 1,2,4,10]

Prints `file:line: rule N: message`. Checks rules 1, 2, 3, 4, 10, 13, 18
from SKILL.md. Heuristic: review each hit before acting.

Rule 18 target spelling: `--spelling us|gb`, else DESCRIPTION `Language:`
(en-GB -> gb), else us.
"""

import argparse
import collections
import glob
import os
import re
import sys

SMALL = {
    "a",
    "an",
    "the",
    "of",
    "and",
    "or",
    "to",
    "in",
    "for",
    "with",
    "by",
    "on",
    "as",
    "at",
    "from",
    "via",
    "vs",
}
# Second words that suggest the first word is a verb ("Creates a ...").
VERBISH_NEXT = {
    "a",
    "an",
    "the",
    "one",
    "each",
    "all",
    "whether",
    "if",
    "its",
    "any",
    "new",
    "multiple",
    "two",
}
TAG = re.compile(r"^@(\w+)\s*(.*)$")
FUN = re.compile(r"^`?([\w.]+)`?\s*(<-|=)\s*function\b")

# Rule 18: (British regex, American regex, American form, British form).
# Suffix groups keep identifiers like `scale_colour_hue` and "ColorBrewer"
# from matching (they lack a word boundary at the right place).
_ISE = (
    "organi|recogni|initiali|normali|customi|summari|standardi|minimi|maximi|"
    "optimi|visuali|seriali|capitali|prioriti|categori|characteri|finali|"
    "utili|speciali|generali|parameteri|vectori|randomi|synchroni|apologi|"
    "emphasi|memori|authori|digiti|tokeni|locali|reali"
)
_END = r"(e|es|ed|ing|ation|ations|er|ers)"
SPELLING = [
    (r"colour(s|ed|ing|ful|less|ation)?", r"color(s|ed|ing|ful|less|ation)?", "color", "colour"),
    (r"behaviour(s|al)?", r"behavior(s|al)?", "behavior", "behaviour"),
    (r"favour(s|ed|ing|ite|ites)?", r"favor(s|ed|ing|ite|ites)?", "favor", "favour"),
    (
        r"(neighbour|honour|labour|flavour|humour|rumour)(s|ed|ing|hood)?",
        r"(neighbor|honor|labor|flavor|humor|rumor)(s|ed|ing|hood)?",
        "-or",
        "-our",
    ),
    (
        r"(centre|metre|litre|fibre|theatre)(s|d)?",
        r"(center|meter|liter|fiber|theater)(s|ed)?",
        "-er",
        "-re",
    ),
    (r"grey(s|ed|ish|scale)?", r"gray(s|ed|ish|scale)?", "gray", "grey"),
    (r"analys(e|es|ed|ing)", r"analyz(e|es|ed|ing)", "analyze", "analyse"),
    (r"(" + _ISE + r")s" + _END, r"(" + _ISE + r")z" + _END, "-ize", "-ise"),
    (
        r"(model|label|cancel|travel|signal)l(ed|ing|er|ers)",
        r"(model|label|cancel|travel|signal)(ed|ing|er|ers)",
        "single l (modeling, labeled)",
        "double l (modelling, labelled)",
    ),
    (
        r"(catalogue|analogue)(s|d)?",
        r"(catalog|analog)(s|ed)?",
        "catalog/analog",
        "catalogue/analogue",
    ),
    (r"(licence|defence|offence)(s)?", r"(license|defense|offense)(s)?", "-se", "-ce"),
    (r"(whilst|amongst)", r"(while|among)", "while/among", "whilst/amongst"),
]
# Text that keeps its own spelling: backticked code, double-quoted text
# (titles of cited works), Rd code/link macros, and [fn()] / [topic] links.
_EXEMPT = re.compile(
    r'`[^`]*`|"[^"]*"|' r"\\(code|link|pkg|var|env|file|href|url)(\[[^]]*\])?\{[^}]*\}|\[[^]\s]*\]"
)
# Tags whose text is not prose.
_NOT_PROSE = {
    "examples",
    "examplesIf",
    "example",
    "rdname",
    "family",
    "export",
    "importFrom",
    "import",
    "inheritParams",
    "inherit",
    "inheritDotParams",
    "inheritSection",
    "name",
    "aliases",
    "usage",
    "keywords",
    "concept",
    "docType",
    "include",
    "eval",
    "evalRd",
    "S3method",
    "method",
    "useDynLib",
    "encoding",
    "md",
    "noMd",
    "order",
}


def target_spelling(pkg, override):
    if override:
        return override
    try:
        with open(os.path.join(pkg, "DESCRIPTION"), encoding="utf-8") as fh:
            m = re.search(r"^Language:\s*(\S+)", fh.read(), re.M)
    except OSError:
        m = None
    return "gb" if m and m.group(1).lower().startswith("en-gb") else "us"


def spelling_hits(text, target):
    """Yield (word, suggestion) for wrong-variety words in a prose line."""
    text = _EXEMPT.sub(" ", text)
    for gb_rx, us_rx, us_form, gb_form in SPELLING:
        rx, want = (gb_rx, us_form) if target == "us" else (us_rx, gb_form)
        for m in re.finditer(r"\b" + rx + r"\b", text, re.I):
            yield m.group(0), want


def blocks(path):
    """Yield (start_line, lines, next_code_line) for each roxygen block."""
    cur, start = [], None
    with open(path, encoding="utf-8", errors="replace") as fh:
        for i, line in enumerate(fh, 1):
            m = re.match(r"^\s*#'\s?(.*)$", line.rstrip("\n"))
            if m:
                if not cur:
                    start = i
                cur.append(m.group(1))
                continue
            # Plain comments (e.g. `# nolint end`) between block and object.
            if cur and re.match(r"^\s*#", line):
                continue
            if cur:
                yield start, cur, line.strip()
                cur = []
    if cur:
        yield start, cur, ""


def parse(start, lines):
    intro, tags, cur = [], [], None
    for off, l in enumerate(lines):
        m = TAG.match(l)
        if m:
            cur = [m.group(1), m.group(2), start + off]
            tags.append(cur)
        elif cur is None:
            intro.append((start + off, l))
        else:
            cur[1] += "\n" + l
    paras, buf = [], []
    for ln, l in intro + [(None, "")]:
        if l.strip():
            buf.append((ln, l))
        elif buf:
            paras.append((buf[0][0], " ".join(x.strip() for _, x in buf)))
            buf = []
    return paras, [(t, x.strip(), ln) for t, x, ln in tags]


def strip_code(s):
    return re.sub(r"`[^`]*`", "CODE", s)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("pkg")
    ap.add_argument("--rules", default="1,2,3,4,10,13,18")
    ap.add_argument("--spelling", choices=["us", "gb"])
    a = ap.parse_args()
    spelling = target_spelling(a.pkg, a.spelling)
    want = {int(x) for x in a.rules.split(",")}
    files = sorted(glob.glob(os.path.join(a.pkg, "R", "*.R")))
    if not files:
        sys.exit(f"no R/*.R files under {a.pkg}")

    out = []
    topics = collections.defaultdict(lambda: {"export": None, "returns": False, "data": False})

    def hit(f, ln, rule, msg):
        if rule in want:
            out.append(f"{os.path.relpath(f)}:{ln}: rule {rule}: {msg}")

    for f in files:
        for start, lines, nxt in blocks(f):
            paras, tags = parse(start, lines)
            tn = {t for t, _, _ in tags}
            tv = {t: x for t, x, _ in tags}
            if "noRd" in tn:
                continue
            fun = FUN.match(nxt)
            topic = (
                tv.get("rdname")
                or tv.get("name")
                or (fun.group(1) if fun else None)
                or f"{f}:{start}"
            )
            # A bare `@export` block (S3 method, re-export) creates no help topic.
            makes_topic = bool(paras) or tn & {"title", "rdname", "describeIn", "name"}
            if not makes_topic:
                continue
            T = topics[topic]
            if "export" in tn and T["export"] is None:
                T["export"] = (f, start)
            if "returns" in tn or "return" in tn or "inherit" in tn:
                T["returns"] = True
            if "format" in tn or tv.get("docType") in ("data", "package") or nxt.startswith('"'):
                T["data"] = True

            # Title
            title = None
            if "title" in tn:
                title = (
                    next(ln for t, _, ln in tags if t == "title"),
                    " ".join(tv["title"].split()),
                )
            elif paras:
                title = paras[0]
            if title:
                ln, t = title
                if t.endswith(".") and not t.endswith("..."):
                    hit(f, ln, 1, f"title ends with a period: {t!r}")
                words = re.findall(r"[A-Za-z][\w'-]*", strip_code(t))
                later = [w for w in words[1:] if w.lower() not in SMALL and w != "CODE"]
                caps = [w[0].isupper() and not w.isupper() for w in later]
                if len(later) >= 2 and caps[0] and sum(caps) / len(caps) >= 0.6:
                    hit(f, ln, 1, f"title looks Title Case (use sentence case): {t!r}")
                if len(words) >= 2:
                    w0, w1 = words[0], words[1].lower()
                    if re.fullmatch(r"[A-Z][a-z]{2,}[^su]s", w0) and (
                        w1 in VERBISH_NEXT or w1 == "code"
                    ):
                        hit(
                            f,
                            ln,
                            2,
                            f"title starts with third-person verb {w0!r} (use imperative): {t!r}",
                        )
                if len(t) > 65:
                    hit(f, ln, 3, f"title is {len(t)} chars (> 65)")

            # Params
            for tag, x, ln in tags:
                if tag != "param":
                    continue
                m = re.match(r"([\w.,`\s]+?)\s+(.*)", x, re.S)
                if not m:
                    continue
                name, d = m.group(1).strip(), " ".join(m.group(2).split())
                if not d:
                    continue
                if not re.match(r"[A-Z`<\[*\-\\]|\d", d) and not d.startswith(("e.g.", "i.e.")):
                    hit(f, ln, 4, f"@param {name}: should start with a capital: {d[:60]!r}")
                if not re.search(r"[.!?:]\)?`?$|^`r lifecycle", d):
                    hit(f, ln, 4, f"@param {name}: should end with a full stop: ...{d[-50:]!r}")

            # Old-style links, and spelling in prose lines.
            cur_tag = None
            for off, l in enumerate(lines):
                if re.search(r"\\code\{\\link", l):
                    hit(f, start + off, 13, "use [fn()] instead of \\code{\\link{}}")
                m = TAG.match(l)
                if m:
                    cur_tag = m.group(1)
                    l = m.group(2)
                if cur_tag in _NOT_PROSE:
                    continue
                if cur_tag == "param":
                    l = re.sub(r"^[\w.,`]+\s*", "", l) if m else l
                for word, fix in spelling_hits(l, spelling):
                    variety = "American" if spelling == "us" else "British"
                    hit(
                        f,
                        start + off,
                        18,
                        f"{word!r}: use {variety} spelling ({fix}), or backtick it if it names code",
                    )

    for name, T in topics.items():
        if T["export"] and not T["returns"] and not T["data"]:
            f, ln = T["export"]
            hit(f, ln, 10, f"exported topic {name!r} has no @returns")

    print("\n".join(sorted(out, key=lambda s: (s.split(":")[0], int(s.split(":")[1])))))
    counts = collections.Counter(re.search(r"rule (\d+)", s).group(1) for s in out)
    print(
        f"\n{len(out)} findings: "
        + ", ".join(f"rule {k}: {v}" for k, v in sorted(counts.items(), key=lambda kv: int(kv[0]))),
        file=sys.stderr,
    )


if __name__ == "__main__":
    main()
