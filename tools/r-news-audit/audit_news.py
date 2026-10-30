"""Audit NEWS.md conventions across tidyverse/r-lib packages (evidence for r-news).

Usage: download NEWS.md for each package into the current directory as <pkg>.md, e.g.
  curl -sfL https://raw.githubusercontent.com/tidyverse/dplyr/main/NEWS.md -o dplyr.md
then: python3 audit_news.py   (edit PK and NREL below to change packages / releases measured).
Heuristic regexes; counts are approximate.
"""

import collections
import re
from pathlib import Path
from typing import Any

PK = [
    "ggplot2",
    "dplyr",
    "tidyr",
    "purrr",
    "readr",
    "stringr",
    "forcats",
    "tibble",
    "scales",
    "rlang",
    "vctrs",
    "cli",
]
NREL = 8


def sections(txt: str) -> list[tuple[str, str]]:
    """Split a NEWS.md file into (level-1 heading, body) pairs."""
    parts = re.split(r"(?m)^# (.*)$", txt)
    return [(parts[i], parts[i + 1]) for i in range(1, len(parts), 2)]


def bullets(body: str) -> list[dict[str, Any]]:
    """Parse the top-level bullets of a NEWS section, with their continuation lines."""
    out: list[dict[str, Any]] = []
    cur: dict[str, Any] | None = None
    blank = False
    for ln in body.split("\n"):
        if re.match(r"^[-*] ", ln):
            if cur is not None:
                out.append(cur)
            cur = {"lines": [ln], "blank_before": blank}
        elif ln.startswith("#"):
            if cur is not None:
                out.append(cur)
                cur = None
        elif ln.strip() == "":
            blank = True
            if cur is not None:
                cur["trail_blank"] = True
            continue
        elif cur is not None and (ln.startswith("  ") or ln.startswith("\t")):
            cur["lines"].append(ln)
        elif cur is not None:
            out.append(cur)
            cur = None
        blank = False if ln.strip() else blank
        if ln.strip() == "":
            pass
    if cur is not None:
        out.append(cur)
    for b in out:
        b["text"] = " ".join(ln.strip() for ln in b["lines"])
        b["first"] = b["lines"][0]
    return out


def pct(c: collections.Counter[str], b: int, k: str, d: int | None = None) -> int:
    """Return `c[k]` as a whole percentage of `d`, or of `b` when `d` is not given."""
    denom = b if d is None or d == 0 else d
    return round(100 * c[k] / denom) if denom else 0


def main() -> None:
    """Print the NEWS.md convention counts for each package in `PK`."""
    R = collections.defaultdict(collections.Counter)
    for p in PK:
        txt = Path(f"{p}.md").read_text()
        secs = sections(txt)
        c = R[p]
        c["n_sections_total"] = len(secs)
        c["dev_first"] = int(bool(re.search(r"development version", secs[0][0], re.IGNORECASE)))
        c["dev_heading_exact"] = int(bool(re.match(rf"^{p} \(development version\)$", secs[0][0])))
        rec = secs[: NREL + (1 if c["dev_first"] else 0)]
        for h, body in rec:
            c["sections"] += 1
            c["heading_pkg_ver"] += bool(re.match(rf"^{re.escape(p)} (\d|\(dev)", h))
            c["heading_has_date"] += bool(re.search(r"\d{4}-\d\d-\d\d|\(\d{4}", h))
            subs = re.findall(r"(?m)^## (.*)$", body)
            if subs:
                c["sections_with_subheads"] += 1
            for s in subs:
                c["sub:" + s.strip().lower()] += 1
            bl = bullets(body)
            for b in bl:
                t = b["text"]
                first = b["first"]
                c["bullets"] += 1
                c["marker_dash"] += first.startswith("- ")
                c["marker_star"] += first.startswith("* ")
                c["ends_period"] += bool(re.search(r"\.\s*$|```\s*$", t)) or bool(
                    re.search(r"\.\)\s*$", t)
                )
                c["ends_period_strict"] += bool(re.search(r"\.\s*$", t))
                # attribution
                m = re.search(r"\(((?:@[\w-]+|#\d+)(?:[, ]+(?:@[\w-]+|#\d+|and))*)\)(\.?)\s*$", t)
                if m:
                    c["attrib"] += 1
                    c["attrib_before_period" if m.group(2) == "." else "attrib_no_period"] += 1
                m2 = re.search(r"\.\s*\(((?:@[\w-]+|#\d+)(?:[, ]+(?:@[\w-]+|#\d+))*)\)\s*$", t)
                if m2:
                    c["attrib_after_period"] += 1
                if re.search(r"#\d+", t):
                    c["has_issue"] += 1
                if re.search(r"@[\w-]+", t):
                    c["has_user"] += 1
                # function early (backticked name within first 60 chars)
                if re.search(r"`[^`]*\(\)`", t[:60]):
                    c["fn_early"] += 1
                if re.search(r"`[^`]*\(\)`", t):
                    c["has_fn"] += 1
                w = re.sub(r"[`*_]", "", t[2:]).split()
                fw = w[0].lower() if w else ""
                if re.match(
                    r"^(fixed|added|removed|changed|updated|improved|deprecated|renamed|replaced|dropped|made|now|fix|add|remove|change|update|improve|new)$",
                    fw,
                ):
                    c["fw:" + fw] += 1
                if re.search(r"\bnow\b", t[:200], re.IGNORECASE):
                    c["has_now"] += 1
                if re.search(
                    r"^(\S+\s+)?(Fixed|Added|Removed|Changed|Updated|Improved|Deprecated|Renamed|Replaced|Dropped|Made)\b",
                    t[2:],
                ):
                    c["past_lead"] += 1
                if re.search(
                    r"^(Fix|Add|Remove|Change|Update|Improve|Deprecate|Rename|Replace|Drop|Make)\b",
                    t[2:],
                ):
                    c["imperative_lead"] += 1
                if re.search(r"^(New|\S+\(\)` (now|gains|is|has|no longer))", t[2:]):
                    c["new_or_now"] += 1
                if re.search(r"breaking", t[:80], re.IGNORECASE):
                    c["breaking_in_bullet"] += 1
                L = max(len(ln) for ln in b["lines"])
                c["bullet_maxline_gt80"] += L > 80
                c["multiline"] += len(b["lines"]) > 1
                c["single_line_long"] += len(b["lines"]) == 1 and len(first) > 80
                c["bullet_lines"] += len(b["lines"])
                c["words"] += len(w)
                if b["blank_before"]:
                    c["blank_before"] += 1
                if "lifecycle" in t.lower() or "deprecated" in t.lower():
                    c["deprecation_bullets"] += 1
                if re.search(r"deprecated (in favou?r of|and replaced|in)", t):
                    c["depr_says_instead"] += 1
                if "Previously" in t or "previously" in t:
                    c["previously"] += 1
                if re.search(r"\bwe\b", t, re.IGNORECASE):
                    c["we"] += 1
            # ordering: alphabetical by first fn within each subsection (or whole section if none)
            parts = re.split(r"(?m)^## .*$", body)
            for part in parts:
                bl2 = bullets(part)
                names = []
                for b in bl2:
                    m = re.search(r"`([A-Za-z0-9_.:]+)\(\)`", b["text"][:80])
                    names.append(m.group(1).lower() if m else None)
                if sum(1 for n in names if n is not None) >= 4:
                    c["order_checked"] += 1
                    seq = [n for n in names if n is not None]
                    c["order_sorted"] += seq == sorted(seq)
                    # non-fn first?
                    first_fn = next((i for i, n in enumerate(names) if n is not None), None)
                    last_nonfn = max((i for i, n in enumerate(names) if n is None), default=-1)
                    c["nonfn_first_checked"] += 1
                    c["nonfn_first_ok"] += (last_nonfn < first_fn) if first_fn is not None else True
    print(
        "package,sections,bullets,dash%,end.%,attrib,beforePeriod,afterPeriod,fn_early%,past%,imper%,now%,subheads%,>80%,blank%"
    )
    for p in PK:
        c = R[p]
        b = c["bullets"]
        print(
            p,
            c["sections"],
            b,
            pct(c, b, "marker_dash"),
            pct(c, b, "ends_period_strict"),
            c["attrib"],
            c["attrib_before_period"],
            c["attrib_after_period"],
            pct(c, b, "fn_early"),
            pct(c, b, "past_lead"),
            pct(c, b, "imperative_lead"),
            pct(c, b, "has_now"),
            pct(c, b, "sections_with_subheads", c["sections"]),
            pct(c, b, "bullet_maxline_gt80"),
            pct(c, b, "blank_before"),
            sep=",",
        )
    T = collections.Counter()
    for p in PK:
        T.update(R[p])
    b = T["bullets"]
    print("\nTOTAL bullets", b, "sections", T["sections"])
    for k in [
        "marker_dash",
        "marker_star",
        "ends_period_strict",
        "ends_period",
        "attrib",
        "attrib_before_period",
        "attrib_no_period",
        "attrib_after_period",
        "has_issue",
        "has_user",
        "has_fn",
        "fn_early",
        "past_lead",
        "imperative_lead",
        "has_now",
        "new_or_now",
        "multiline",
        "single_line_long",
        "bullet_maxline_gt80",
        "blank_before",
        "breaking_in_bullet",
        "deprecation_bullets",
        "depr_says_instead",
        "previously",
        "we",
    ]:
        print(f"{k}: {T[k]} ({100 * T[k] / b:.1f}%)")
    print("avg words", T["words"] / b, "avg lines", T["bullet_lines"] / b)
    print(
        "heading pkg ver",
        T["heading_pkg_ver"],
        "/",
        T["sections"],
        "dated",
        T["heading_has_date"],
        "dev first",
        T["dev_first"],
        "/12 exact",
        T["dev_heading_exact"],
    )
    print("subhead sections", T["sections_with_subheads"], "/", T["sections"])
    print(
        "order sorted",
        T["order_sorted"],
        "/",
        T["order_checked"],
        " nonfn-first",
        T["nonfn_first_ok"],
        "/",
        T["nonfn_first_checked"],
    )
    subs = collections.Counter({k[4:]: v for k, v in T.items() if k.startswith("sub:")})
    print(subs.most_common(25))
    print({k: v for k, v in T.items() if k.startswith("fw:")})
    for p in PK:
        s = [(k[4:], v) for k, v in R[p].items() if k.startswith("sub:")]
        print(p, sorted(s, key=lambda x: -x[1])[:5])


if __name__ == "__main__":
    main()
