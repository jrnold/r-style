# Evidence for roxygen-style rules

Collected 2026-10-04. Two sources:

1. **Corpus audit** — roxygen blocks parsed from shallow clones of ggplot2,
   dplyr, tidyr, purrr, readr, stringr, forcats, tibble (tidyverse) and scales,
   rlang, vctrs, cli (r-lib): 3,402 blocks, 730 titles, 2,087 `@param`, 311
   `@return(s)`. Blocks with `@noRd` / `@keywords internal` excluded.
2. **Maintainer corrections** — issues, PRs, review comments.

## Corpus measurements

| Measure | Overall | Range across packages |
|---|---|---|
| Title ends with `.` | 1% | 0–6% |
| Title in Title Case | 2% | 0–5% |
| Title first word third-person (-s) | 4% | 0–11% |
| Title > 65 chars | 2% | 0–14% |
| `@param` starts capital/backtick | 89% | 65% (scales), 72% (ggplot2) – 100% |
| `@param` ends with `.` | 86% | 59% (scales) – 97% |
| `@param` starts "A/An" | 21% | 2–53% |
| `@param` mentions a default | 20% | 8–32% |
| `@return(s)` ends with `.` | 94% | 56–100% |
| `@return(s)` starts "A/An" | 50% | 14–80% |
| `@returns` share of return tags | 10% | 0–33% |
| Exported topics with `@return(s)` | ~18% median | 5% (tidyr) – 67% (stringr) |
| Uses `[fn()]` links | 15% of blocks | — |
| Uses `\code{\link{}}` | 0% | — |
| Uses "you" / "we" | 8% / 1% | — |

Default phrasing counts: "The default" 106, "By default," 90, "(default)" 71,
"Defaults to" 58, ", the default," 54, "(the default)" 52.

Spelling (prose, backticked code removed): ggplot2 colour 93 / color 42,
center 15 / centre 1; scales colour 74 / color 10; cli color 115 / colour 0;
dplyr behaviour 22 / behavior 8, summarise 55 / summarize 0. No consistent
house style.

Low-compliance packages (scales, older ggplot2 files) are legacy text, not a
competing convention: ggplot2#2416 was merged solely to add capitals and full
stops.

## Maintainer statements

- Titles sentence case, no full stop; tag text is a sentence with capital and
  full stop — Hadley, https://github.com/tidyverse/style/pull/24#discussion_r120644224,
  https://github.com/tidyverse/style/pull/24#discussion_r120644122
- "you should never use title case in anything even adjacent to the
  tidyverse" — Hadley, https://github.com/tidyverse/style/pull/166
- Capitals + full stops + backticks sweep merged: "This is lovely" —
  https://github.com/tidyverse/ggplot2/pull/2416
- Default added to param description, merged — https://github.com/tidyverse/purrr/pull/1135
- `@inheritParams` to avoid duplication; mention `@family`; explicit
  `@description` only for multi-paragraph/list — Hadley, style#24 inline review
- `@returns` loosely preferred, "mostly interchangeable" — DavisVaughan,
  https://github.com/r-lib/vctrs/pull/1779 (verified)
- `select` → `select()`; "Mention what happens if the row doesn't exist?";
  terminology consistency — Hadley, https://github.com/tidyverse/dplyr/pull/3689
- "Select seems particularly bad to use here since that is about columns";
  "mention that it outputs a message" — DavisVaughan,
  https://github.com/tidyverse/dplyr/pull/6352
- "write 'is completely opaque'" — clauswilke,
  https://github.com/tidyverse/ggplot2/pull/3788
- "Fewer commas throughout please … this advice should hold for all
  copy-editing changes, i.e. things that are not typos, clear grammatical
  errors, or that do not clearly improve upon the clarity of the doc" —
  lionel-, https://github.com/r-lib/rlang/pull/542#discussion_r192459683 (verified)
- "Working with multiple spellings was a mistake that we don't want to
  replicate elsewhere" — Hadley, https://github.com/tidyverse/ggplot2/issues/4554
  (verified; about function aliases, not prose)
- `[0, 1]` in `@param` became a link — https://github.com/tidyverse/ggplot2/pull/2166
- Singular phrasing for function groups is clearer — jennybc,
  https://github.com/tidyverse/stringr/pull/530

## CRAN (overrides tidyverse practice)

- Every `.Rd` needs `\value`, even side-effect functions ("No return value,
  called for side effects"); data topics exempt — CRAN Cookbook,
  https://contributor.r-project.org/cran-cookbook/docs_issues.html
- WRE §2 has no prose-style rules; DESCRIPTION rules live in WRE §1.1.1 and
  `r-lib:cran-extrachecks`.
