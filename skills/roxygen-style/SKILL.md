---
name: roxygen-style
description: Wording and style rules for roxygen2 documentation in R packages, derived from an audit of 12 tidyverse/r-lib packages and maintainer review comments. Use when writing, editing, reviewing, or auditing roxygen comments (titles, @param, @returns, @description, @family, examples prose), when asked about R documentation conventions or language style, or before submitting doc changes in an R package. Complements r-lib:r-package-development (workflow) and r-lib:cran-extrachecks (CRAN requirements); this skill covers prose style.
---

# Roxygen documentation style

Rules for *how documentation reads*. For workflow (document(), pkgdown index)
see `r-lib:r-package-development`; for CRAN requirements (DESCRIPTION Title,
`\dontrun`, URLs) see `r-lib:cran-extrachecks`. Where tidyverse practice and
CRAN disagree, CRAN wins (rule 10).

Percentages are measured compliance across ggplot2, dplyr, tidyr, purrr, readr,
stringr, forcats, tibble, scales, rlang, vctrs, cli (2026). Sources and quotes:
`references/evidence.md`.

## Titles

1. **Sentence case, no trailing period.** (98% / 99%.) Exception: the
   DESCRIPTION `Title:` field is Title Case (CRAN).
2. **Imperative verb or noun phrase; never third-person.**
   "Create a new ggplot", "Select a subset of columns",
   "Transformed Cartesian coordinate system". Not "Creates …".
   Predicates may start "Is"/"Does" ("Is object a formula?").
3. **≤ 65 characters**, no markup beyond backticked code.

## `@param`

4. **A sentence: capital first letter, ends with a full stop** — even short
   fragments: `@param x A numeric vector.` (89% / 86%.)
5. **Lead with the type or the condition.** Common openers:
   "A/An …" (`A data frame.`, `A string.`), "If `TRUE`, …", "Whether to …",
   "One of …", "Optional …", "Number of …". Arguments using tidy evaluation
   start with the tag, e.g. ``<[`tidy-select`][dplyr_tidy_select]> Columns to …``.
6. **State the default when the signature doesn't make it obvious** (e.g. it is
   `NULL`, computed, or an option). Preferred forms:
   - ``If `TRUE` (the default), …``
   - `` `"fastest"`, the default, keeps … `` (inside an options list)
   - ``If `NULL`, the default, …``
7. **Enumerate allowed values as a bulleted list** introduced by a colon; each
   bullet is a sentence with the value in backticks first.
8. **Don't duplicate text** across functions — use `@inheritParams`. Do not
   restate inherited params with trivial rewording.
9. **Deprecated args:** start with `` `r lifecycle::badge("deprecated")` `` then
   say what to use instead: "Please use `cols` instead."

## `@returns`

10. **Every exported topic documents its return value** (CRAN requirement;
    tidyverse packages often omit it — don't copy that). Side-effect functions:
    "Called for its side effect; returns `x` invisibly." or
    "No return value, called for side effects."
11. **Prefer `@returns`** for new docs; don't churn existing `@return`.
12. **Start with "A/An …", describe type and size relative to inputs, end with
    a period.** Patterns:
    - "A vector the same size as `x`."
    - "An object of the same type as `.data`." then bullets on rows/columns.
    - For multi-function pages, one bullet per function:
      "- `foo()` returns a character vector."

## Prose

13. **Functions as `[fn()]`** (auto-link) or `` `fn()` ``; never
    `\code{\link{}}`. Backtick arguments, values (`TRUE`, `NULL`, `NA`, `...`),
    literal code, and class names. Never capitalise function or package names,
    even at sentence start.
14. **Say what the function does first**, then exceptions. Document edge cases
    (empty input, missing rows, `NA`) and side effects (messages, warnings,
    files written).
15. **One term per concept.** Don't use a word that already names something in
    the package for something else (e.g. "select" for rows in dplyr).
16. **Plain, positive wording.** "is completely opaque", not "is not
    transparent at all". Address the reader as "you" when needed; avoid "we".
17. **Don't churn correct prose.** Copy-edits are for typos, clear grammatical
    errors, or clear gains in clarity — not comma placement or since/because.
    Keep doc-only changes focused and separate from code changes.
18. **Use American spelling, consistently**, across all prose: roxygen,
    vignettes, README, NEWS — "color", "behavior", "summarize", "center",
    "analyze", "-ize" endings. Never mix varieties in text. (Tidyverse does mix
    them — ggplot2 has colour 93 / color 42 — so don't copy that.)
    - **Only exception:** a project that explicitly declares British English
      (`Language: en-GB` in DESCRIPTION, or its CLAUDE.md says so). Then use
      British consistently instead. Existing British text in the docs is not a
      declaration — it is text to convert.
    - **Declare it** in DESCRIPTION as `Language: en-US`;
      `spelling::spell_check_package()` checks against that dictionary.
    - **Exempt:** code in backticks, function and argument names
      (`scale_colour_*()` and `scale_color_*()` aliases stay as they are), proper
      nouns and titles of cited works ("ColorBrewer", a book title), and quoted
      text. When prose refers to an exempt name, the name keeps its spelling but
      the surrounding words follow the package variety.
    - Converting existing text to the chosen variety is a legitimate doc fix
      (an exception to rule 17), but do it as a separate, spelling-only change.

## Structure

19. Second intro paragraph is the description. Use explicit `@description`
    only for multiple paragraphs or lists. Use `# Heading` markdown sections
    for long topics instead of many `@details`.
20. Link related topics with `@family` (for a group) or `@seealso` (for a few
    specific pointers). Both are sentences.
21. Bracketed intervals like `[0, 1]` must be in backticks, or markdown makes
    them links.
22. Wrap roxygen at 80 characters; re-run `devtools::document()` after edits.

## Checking

Run the checker (in this skill's `scripts/` directory) against a package to
flag mechanical violations (rules 1, 2, 3, 4, 10, 13, 18):

```bash
Rscript <skill-dir>/scripts/check_roxygen.R path/to/pkg
```

It needs roxygen2 and prints `file:line: rule N: message`. It is heuristic —
read each hit before changing anything, and report findings before editing
when the user asked for an audit. Rule 18 flags British spellings (or American
ones, if DESCRIPTION has `Language: en-GB`; override with `--spelling us|gb`).
It checks roxygen only — also grep vignettes and README by hand. Rules 5–9, 12, 14–17, 19–20 need human judgement.
