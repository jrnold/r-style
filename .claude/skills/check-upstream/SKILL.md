---
name: check-upstream
description: Check this plugin's rules against their upstream sources (tidyverse style guide, tidy design principles, R Packages, Advanced R, rlang, vctrs, usethis, dplyr, the tidyverse code-review guide) and against the Posit r-lib skills, and report rules to add, change, or drop. Use when asked to "check for upstream changes", "update the rules", "are the sources still current?", "refresh the evidence", or before a plugin release. Reports first; edits only after the user approves.
---

# Check upstream sources

The rules in `skills/*/SKILL.md` are only as current as the pages they quote.
`SOURCES.md` lists every page with the date it was last checked, and each
skill's `references/evidence.md` quotes the source for each rule. This skill
finds what changed upstream since then and proposes edits.

Two principles hold throughout:

- **Quote only what you fetched.** Never write a rule or an evidence quote
  from memory. Every quote must come from a page fetched in this session,
  and `just check-upstream` must find it. If a rule has no source, mark it †
  (a house rule) rather than inventing one.
- **Don't duplicate r-lib.** If a Posit r-lib skill now covers a rule, the
  rule becomes a pointer to that skill.

## 1. Run the checker

```bash
just check-upstream skills/r-code-style/references/evidence.md \
  skills/r-pkg-structure/references/evidence.md
```

It prints commits to each source's `Repo`/`Path` since its `Checked` date,
and any evidence quote that no longer appears in the fetched pages. Needs
`gh` signed in.

## 2. Read each change

For every commit listed, read the diff for that file:

```bash
gh api repos/<repo>/commits/<sha> --jq '.files[] | select(.filename == "<path>") | .patch'
```

Classify it:

- **Cosmetic** (typos, links, build): no rule change.
- **Changed guidance** behind a rule: find the rule in the evidence tables
  and propose new wording.
- **New guidance** in a source we already use: propose a rule only if a
  reviewer could act on it and no linter (air, lintr) already enforces it.

For each stale quote, fetch the page, find the current wording, and decide
whether the rule still follows from it.

## 3. Look for new sources

- New chapters: compare the `.qmd`/`.Rmd` files in `tidyverse/style`,
  `tidyverse/design`, `tidyverse/code-review`, and `hadley/r-pkgs` (`gh api
  "repos/<repo>/git/trees/HEAD?recursive=1" --jq '.tree[].path'`) with the
  `Path` column. Draft chapters in the repo but not on the site count, but
  say they are drafts.
- Package changes: read the NEWS of rlang, vctrs, usethis, testthat, and
  dplyr since the `Checked` date for new exports, deprecations, or renamed
  functions that a rule names (rule 38 changed this way when rlang 1.2.0
  exported `check_string()`).
- The upkeep checklist in `r-lib/usethis` `R/upkeep.R`: new year sections
  feed `r-pkg-structure` rule 12.

## 4. Check overlap with the r-lib skills

List commits to `posit-dev/skills` under `r-lib/` since the `Checked` date.
Then search the r-lib skills (`SKILL.md` and `references/`) for each rule's
key function or topic. A rule that r-lib now states becomes a one-line
pointer (as `r-code-style` rule 31 points to `r-lib:r-package-development`).
Incidental use in an example doesn't count as coverage.

## 5. Report and stop

Report one table, most important first:

  | Rule | What changed upstream | Proposal |
  | ---- | --------------------- | -------- |

Proposals are one of: reword, new rule, drop, make a pointer to r-lib, or
mark †. Include the fetched quote for each. Then stop and wait for approval.

## 6. After approval

1. Edit the rules. Append new rules at the end of a skill so cited rule IDs
   (`code:23`, `pkg:5`) keep their meaning.
2. Update the evidence rows with the new quotes and links.
3. Set `Checked` to today for every row you reviewed, changed or not, and
   add rows for new sources.
4. Run `just check-upstream ...` (no missing quotes), `just test`, and
   `just lint`.
5. Run the eval cases for any skill whose rules changed
   (`just eval --tag <skill> --runs 1`), and update graders that test a
   changed rule.
6. Bump `version` in `.claude-plugin/plugin.json` and `pyproject.toml`.
