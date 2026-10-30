"""Check the r-style rules against their upstream sources.

Reads the table in SOURCES.md and reports two things:

1. Commits to each source's Repo/Path since its Checked date (via `gh api`).
2. Quotes in evidence files that no longer appear in any fetched source.

Run from the repository root:

    uv run python tools/check-upstream/check_upstream.py \
        skills/r-code-style/references/evidence.md \
        skills/r-pkg-structure/references/evidence.md

Pass --no-fetch to skip the quote check, or --no-commits to skip `gh`.
"""

import argparse
import json
import re
import subprocess
import urllib.request
from html import unescape
from pathlib import Path

SOURCES = Path("SOURCES.md")


BLOCK_TAGS = re.compile(r"</?(?:p|li|div|h[1-6]|br|tr|td|th|pre|dd|dt)\b[^>]*>", re.IGNORECASE)


def html_to_text(html: str) -> str:
    """Reduce an HTML page to its visible text.

    Inline tags such as <code> are dropped without a space, so "<code>x</code>,"
    reads "x,"; block tags become a space so paragraphs don't run together.
    """
    html = re.sub(r"<(script|style)\b.*?</\1>", " ", html, flags=re.DOTALL | re.IGNORECASE)
    html = BLOCK_TAGS.sub(" ", html)
    return unescape(re.sub(r"<[^>]+>", "", html))


def parse_sources(path: Path = SOURCES) -> list[dict[str, str]]:
    """Return the rows of the sources table as dicts keyed by header."""
    rows = [
        [c.strip() for c in line.strip().strip("|").split("|")]
        for line in path.read_text().splitlines()
        if line.lstrip().startswith("|")
    ]
    header, body = rows[0], [r for r in rows[2:] if len(r) == len(rows[0])]
    return [dict(zip(header, r, strict=True)) for r in body]


def normalize(text: str) -> str:
    """Fold quotes, markup, and whitespace so prose compares across formats."""
    text = text.translate(str.maketrans({"‘": "'", "’": "'", "“": '"', "”": '"'}))
    text = text.replace("…", "...")
    text = re.sub(r"[`*\\]", "", text)
    text = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", text)
    return re.sub(r"\s+", " ", text).strip().lower()


def fetch_text(url: str) -> str:
    """Download a page and return its text; HTML is reduced to visible text."""
    if not url.startswith("https://"):
        raise ValueError(f"refusing non-https URL: {url}")
    with urllib.request.urlopen(url, timeout=30) as resp:  # noqa: S310 (https checked above)
        body = str(resp.read().decode("utf-8", errors="replace"))
    if "<html" in body[:2000].lower():
        return html_to_text(body)
    if url.endswith(".R"):
        # Comment blocks in R source: drop the leading "#" or "#'" on each line.
        return re.sub(r"(?m)^\s*#'? ?", "", body)
    return body


def quote_cells(evidence: Path) -> list[tuple[str, str]]:
    """Return (rule, cell) for the last column of each evidence table row."""
    out = []
    for line in evidence.read_text().splitlines():
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if line.lstrip().startswith("|") and len(cells) >= 2 and re.match(r"\d+", cells[0]):
            out.append((cells[0], cells[-1]))
    return out


def missing_quotes(cell: str, corpus: str) -> list[str]:
    """Return quotes in a cell that are not in the corpus.

    Quotes are spans between straight double quotes. A quote may itself hold
    quoted words, so when a span isn't found, it is retried joined with the
    next one or two spans. Text around `...` is matched piece by piece.
    """

    def found(quote: str) -> bool:
        pieces = [normalize(p) for p in quote.split("...")]
        return all(p.strip(" .") in corpus for p in pieces if len(p) > 8)

    segs = cell.split('"')
    missing: list[str] = []
    i = 1
    while i < len(segs):
        for k in (0, 2, 4):
            if found('"'.join(segs[i : i + k + 1])):
                i += k + 2
                break
        else:
            if len(segs[i]) > 15:
                missing.append(segs[i])
            i += 2
    return missing


def commits_since(repo: str, path: str, since: str) -> list[str]:
    """List commits to repo/path after the date, newest first."""
    endpoint = f"repos/{repo}/commits?path={path}&since={since}T00:00:00Z&per_page=20"
    result = subprocess.run(  # noqa: S603 (fixed argv, no shell)
        ["gh", "api", endpoint],  # noqa: S607 (gh is resolved on PATH)
        capture_output=True,
        text=True,
        check=True,
    )
    return [
        f"{c['commit']['author']['date'][:10]} {c['sha'][:7]} "
        f"{c['commit']['message'].splitlines()[0]}"
        for c in json.loads(result.stdout)
    ]


def main() -> None:
    """Print a Markdown report of upstream changes and stale quotes."""
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("evidence", nargs="*", type=Path, help="evidence.md files to check")
    ap.add_argument("--no-fetch", action="store_true", help="skip fetching pages")
    ap.add_argument("--no-commits", action="store_true", help="skip the gh commit check")
    args = ap.parse_args()
    sources = parse_sources()

    if not args.no_commits:
        print("## Upstream commits since last check\n")
        for row in sources:
            if row["Repo"] == "-":
                continue
            path = "" if row["Path"] == "-" else row["Path"]
            commits = commits_since(row["Repo"], path, row["Checked"])
            if commits:
                print(f"### {row['Source']} ({row['Repo']}/{path}, checked {row['Checked']})\n")
                print("\n".join(f"- {c}" for c in commits), end="\n\n")

    if not args.no_fetch and args.evidence:
        print("## Quotes not found in any source\n")
        texts = []
        for row in sources:
            if row["URL"] == "-":
                continue
            try:
                texts.append(fetch_text(row["URL"]))
            except OSError as err:
                print(f"- could not fetch {row['URL']}: {err}")
        corpus = normalize("\n".join(texts))
        for evidence in args.evidence:
            for rule, cell in quote_cells(evidence):
                for quote in missing_quotes(cell, corpus):
                    print(f"- {evidence} rule {rule}: {quote[:100]}")
        print()


if __name__ == "__main__":
    main()
