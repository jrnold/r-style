import importlib.util
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
_spec = importlib.util.spec_from_file_location(
    "check_upstream", ROOT / "tools" / "check-upstream" / "check_upstream.py"
)
assert _spec is not None
assert _spec.loader is not None
cu = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(cu)

CORPUS = cu.normalize(
    "If the cause of the problem is clear (e.g. an incorrect type or size), use “must”. "
    "Reserve pipes for a sequence of steps applied to one primary object. "
    'Use requireNamespace("aaapkg", quietly = TRUE) to check.'
)


def test_sources_table_parses() -> None:
    rows = cu.parse_sources(ROOT / "SOURCES.md")
    assert rows
    assert set(rows[0]) == {"Source", "URL", "Repo", "Path", "Used by", "Checked"}
    for row in rows:
        assert re.fullmatch(r"\d{4}-\d{2}-\d{2}", row["Checked"]), row["Source"]
        assert row["URL"] == "-" or row["URL"].startswith("https://"), row["Source"]


def test_found_quote_is_not_reported() -> None:
    cell = '"Reserve pipes for a sequence of steps applied to one primary object."'
    assert cu.missing_quotes(cell, CORPUS) == []


def test_invented_quote_is_reported() -> None:
    cell = '"Always name functions with a gerund." / "Reserve pipes for a sequence of steps"'
    assert cu.missing_quotes(cell, CORPUS) == ["Always name functions with a gerund."]


def test_nested_and_curly_quotes_match() -> None:
    assert cu.missing_quotes('"use “must”" and more', CORPUS) == []
    assert cu.missing_quotes('"Use requireNamespace("aaapkg", quietly = TRUE)"', CORPUS) == []


def test_ellipsis_matches_pieces() -> None:
    cell = '"If the cause of the problem is clear ... use “must”"'
    assert cu.missing_quotes(cell, CORPUS) == []


def test_inline_tags_add_no_space() -> None:
    text = cu.html_to_text("<p>names (e.g. <code>model_2018</code>, <code>x</code>)</p><p>Next</p>")
    assert cu.normalize(text) == "names (e.g. model_2018, x) next"


def test_evidence_files_have_quotes_for_every_rule() -> None:
    for name in ("r-code-style", "r-pkg-structure"):
        cells = cu.quote_cells(ROOT / "skills" / name / "references" / "evidence.md")
        assert cells, name
