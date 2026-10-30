# Evidence for r-news rules

Collected 2026-10-05. Three sources:

1. **Corpus audit** of `NEWS.md` from the `main` branch of ggplot2, dplyr,
   tidyr, purrr, readr, stringr, forcats, tibble (tidyverse) and scales, rlang,
   vctrs, cli (r-lib), the same 12 packages as the roxygen-style audit. Only
   the development section (if present) and the 8 most recent releases of each
   were measured: 107 sections, 1,048 top-level bullets. Reproduce with
   `tools/r-news-audit/audit_news.py` in the plugin repository (see its header).
2. **Posit skills** (`posit-dev/skills`, local marketplace checkout).
3. **Published guidance**: tidyverse style guide, *R Packages*, pkgdown docs,
   CRAN policy.

## Posit skills

Only three mention NEWS, and only one gives rules.

- `r-lib/r-package-development`, section `NEWS.md`, five bullets: every
  user-facing change gets a bullet; none for small documentation changes or
  internal refactorings; describe the change to the end user briefly; put the
  function name early; reference issues/PRs as `(#123).` before the final
  period; order alphabetically by function name, with bullets that name no
  function first. All five are in `r-news` (rules 1-3, 8, 13, 17). It says
  nothing on headings, tense, wrapping, credit, breaking changes or releases;
  `r-news` adds those from the corpus and the style guide.
- `r-lib/cran-extrachecks`: create the file with `usethis::use_news_md()`;
  confirm it "documents changes for this version". No wording rules.
- `open-source/create-release-checklist`: reads the first NEWS section and
  suggests **Major** if it mentions "breaking" (any case), **Patch** if only
  "bug fixes"/"fixes", otherwise **Minor**. So the literal words *Breaking
  changes* and *Bug fixes* in a heading or bullet carry meaning to tooling
  (rule 18).
- `open-source/release-post`: turns NEWS bullets into blog posts. It wants
  bullets that name the function and link the issue, so the reader can find
  context (rules 8, 13).

## Corpus measurements

Percentages are of bullets unless noted.

  | Measure                                                   | Overall                          | Range across packages                                |
  | --------------------------------------------------------- | -------------------------------- | ---------------------------------------------------- |
  | Release headings `# pkg X.Y.Z`                            | 107/107 sections                 | all                                                  |
  | Heading contains a date                                   | 0/107                            | all 0                                                |
  | Development heading exactly `# pkg (development version)` | 11 of 12 packages                | one package was at a release heading                 |
  | Section has `##` subheadings                              | 27% of sections                  | 0% (readr, rlang, cli) – 88% (tibble)                |
  | Bullet marker `*` / `-`                                   | 97% / 3%                         | `-` only in tibble                                   |
  | Blank line between bullets                                | 76%                              | 36% (ggplot2) – 100%; ≥94% in 9 of 12                |
  | Ends with `.`                                             | 86%                              | 73% (ggplot2) – 100%                                 |
  | Has a trailing `(#n)`/`(@u, #n)`                          | 78%                              | —                                                    |
  | …of which period after the parenthesis `(#n).`            | 66% of all bullets               | —                                                    |
  | …no period at all                                         | 12%                              | —                                                    |
  | …period before the parenthesis `. (#n)`                   | 1%                               | —                                                    |
  | Mentions an issue/PR number                               | 81%                              | 36% (readr) – 92% (tidyr)                            |
  | Credits an `@user`                                        | 40%                              | 0% (vctrs), 9% (dplyr) – 71% (ggplot2)               |
  | Names a function `` `f()` `` anywhere                     | 74%                              | —                                                    |
  | …in the first 60 characters                               | 66% (89% of those that name one) | —                                                    |
  | Contains "now"                                            | 41%                              | 0% (tibble) – 60% (cli)                              |
  | Leads with past tense (Fixed, Added, Removed…)            | 9%                               | 0–22% (vctrs, ggplot2, rlang, purrr highest)         |
  | Leads with imperative (Fix, Add, Remove…)                 | 2%                               | 0–27% (tibble, whose NEWS is generated from commits) |
  | Leads with "New"                                          | 10%                              | —                                                    |
  | Contains "we"                                             | 2%                               | —                                                    |
  | Wrapped over more than one line                           | 63%                              | —                                                    |
  | Any line longer than 80 characters                        | 17%                              | 0% (cli) – 73% (readr)                               |
  | Single-line bullet longer than 80                         | 13%                              | —                                                    |
  | Average length                                            | 21 words                         | —                                                    |
  | Mentions "deprecated" in the first 200 characters         | 6%                               | —                                                    |
  | …and names the replacement (“in favour of”, etc.)         | 21 of 64                         | —                                                    |
  | "Previously …" explanation                                | 2%                               | —                                                    |
  | Starts with "BREAKING"                                    | 2 bullets (0.2%)                 | —                                                    |

Subheading names, all packages, count of sections: New features 12; Breaking
changes 7; Minor improvements and bug fixes (and five spelling variants) 14;
Bug fixes 5; Improvements 5; Continuous integration 4 and Uncategorized 4
(tibble only; commit-generated); Lifecycle changes 3 (dplyr, tidyr); API
changes 2; the rest are topic names (Rectangling, Transformations, Grids…).

**Ordering.** Of 37 sections with six or more named functions, 4 were fully in
alphabetical order. Adjacent named-function pairs were in order 67% of the
time (50% would be chance), so most sections are loosely grouped by topic, not
sorted. Bullets naming no function came before the first named one in 26 of 55
sub-sections. That is a gap against the style guide, not a reason to relax it.

**Tense.** "Fixed …" appears in 7% of bullets, and in two ggplot2 releases it is
13 and 15 bullets. In every other package it is a handful per release. The
style guide's "now …" form is followed by under half; most bullets start with a
function name or a subject noun, which the guide also accepts.

**Who is credited.** In ggplot2 the maintainer's handle appears in 205
bullets (71% of bullets carry an `@user`); in dplyr, vctrs, readr and rlang
fewer than 15% of bullets do. There is no single norm for crediting
maintainers.

## Recent NEWS patterns (rules 25-38)

Sample: the development section plus the latest release of each package
(three sections where the development one was short): 197 bullets, mostly
dplyr 44, scales 34, ggplot2 31. Heuristic, small counts. Script:
`tools/r-news-audit/recent_patterns.py` in the plugin repository (run after
`audit_news.py` setup).

  | Pattern                                             | Count (of 197)             |
  | --------------------------------------------------- | -------------------------- |
  | Starts "New `...`"                                  | 21                         |
  | Starts "`f()` now"                                  | 19                         |
  | Starts "`f()` and ..." (grouped)                    | 13                         |
  | Starts "`f()` no longer"                            | 8 (14 contain "no longer") |
  | Starts "`f()` gains"                                | 7 (9 contain "gains")      |
  | Contains "now"                                      | 80 (40%)                   |
  | Contains "instead"                                  | 23                         |
  | "Deprecated in X (Mon YYYY), use ... instead"       | 11                         |
  | Stage words: soft-deprecated / defunct / superseded | 5 / 2 / 2                  |
  | R version requirement                               | 12                         |
  | `pkg::fn`                                           | 16                         |
  | `(@user, #n)` / `(#n, @user)`                       | 49 / 17                    |
  | Single `(#n)`                                       | 66                         |
  | Cross-repo `(r-lib/vctrs#n)`                        | 2                          |
  | Contains a fenced code block                        | 5                          |
  | Contains an inline sub-list                         | 7                          |
  | "For example" / "e.g."                              | 6                          |
  | Purpose clause (allowing, so you can, to control…)  | 6                          |
  | "Fixed a ..."                                       | 7                          |
  | `(internal)` prefix                                 | 2 (ggplot2 only)           |
  | Ends with no period                                 | 34 (17%)                   |

Ones in the table that contradict the style guide (no period, "Fixed" leads,
`(internal)`) are listed in the skill as seen but not adopted.

## Published guidance (quoted)

- Style guide: bullets "briefly describe the change so users of the packages
  can understand what's changed"; references go "in parentheses before the
  final period"; good `` `ggsave()` now uses full argument names to avoid
  partial match warnings (@wch, #2355). `` vs poor `` ... warnings. (@wch,
  #2355) ``; good `` `ggsave()` now uses ... `` vs poor ``Fixed partial
  argument matches in `ggsave()` (#2355).``; function names near the front;
  wrap at 80; level-1 heading per release with package name and version;
  level-2 headings *Breaking changes*, *New features*, *Minor improvements and
  fixes*; alphabetical within a section by first function; breaking changes
  describe "symptoms and required fixes".
- *R Packages* (NEWS chapter): top heading per version, newest first,
  `# somepackage (development version)`; cite `(#101, @username)`; NEWS is
  linked from CRAN and shown as the Changelog on pkgdown.
- pkgdown: version headings must match `pkg 1.3.0`, `v1.3.0`, `Version 1.3.0`,
  `Changes in 1.3.0` (case-insensitive); level 1 or 2; release dates come from
  CRAN, not the heading; issue and `@user` links need a GitHub URL in
  DESCRIPTION.
- CRAN policy: no NEWS requirement; resubmission explanations go in the
  submission form comment. Updates "must have an increased version".
- Verified locally: `tools:::.build_news_db_from_package_NEWS_md()` lists one
  row per release heading and skips the `(development version)` heading.

## How the audit was used

The rules state the style guide's ideal; the audit shows how often practice
meets it. Low compliance is **not** a reason to drop or soften a rule (the
roxygen-style audit treated low-compliance text as legacy, not as a competing
convention). Measured practice changed the rules only where it exposed a claim
that was factually wrong or gave a reason to prioritise:

- Rule 14: removed "maintainers typically omit their own handle", which the
  corpus contradicts (0%-71% by package). The rule now credits external
  contributors and leaves maintainer credit to the project.
- Rules 17, 9, 19: kept as the style guide states them; each records how far
  practice lags. Practice never overrides the guide.
- Rule 18: the section heading stays the form to use; a prefix is not an
  alternative.
- Rules 6, 7: gained the observed norms (literal word "breaking"; `*` marker;
  blank lines) so a reviewer can match an existing file.
- Priority: rules 1-3, 16-18, 22 are the ones with the clearest cost to users.
