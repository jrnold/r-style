# r-style

A [Claude Code](https://claude.com/claude-code) plugin with style rules for R
packages. Its `roxygen-style` skill covers wording and style
rules for roxygen2 documentation in R packages: titles, `@param`, `@returns`,
prose, and structure. The rules come from an audit of 12 tidyverse and r-lib
packages and from maintainer review comments; see
[`skills/roxygen-style/references/evidence.md`](skills/roxygen-style/references/evidence.md).

It complements the `r-lib` skills: `r-package-development` covers workflow and
`cran-extrachecks` covers CRAN requirements. This plugin covers prose style.

## Skills

- `r-review`: one review of an R package change (a PR, branch, or diff)
  covering code, package structure, roxygen, and `NEWS.md`. It decides which
  of the skills below apply, then reviews inline or launches one reviewer
  agent per aspect (`r-code-reviewer`, `pkg-reviewer`, `roxygen-reviewer`,
  `news-reviewer`), and merges the findings into one report labeled with the
  tidyverse code-review severities and rule IDs such as `[news:18]`.
- `roxygen-style`: wording and style of roxygen2 documentation.
- `r-news`: what earns a `NEWS.md` bullet, heading structure, bullet wording,
  ordering, breaking changes, deprecations, and release checks, with the
  tidyverse style guide as the standard and an audit of 1,048 bullets from 12
  tidyverse and r-lib packages as supporting evidence.
- `r-code-style`: review rules for R code that `air`, `styler`, and `lintr`
  cannot check (naming, comments, pipes, function and argument design, dots,
  input checking, error messages, idioms, test names). Drawn from the
  [tidyverse style guide](https://style.tidyverse.org/) and
  [tidy design principles](https://design.tidyverse.org/).
- `r-pkg-structure`: review rules for how a package is put together:
  dependencies, tidy evaluation in package code, S3 class constructors, file
  layout, `.onLoad()` and options, and the tidyverse upkeep checklist. Drawn
  from *R Packages*, *Advanced R*, and the dplyr and rlang docs.

Each rule skill's `references/evidence.md` quotes the source for each rule;
[`SOURCES.md`](SOURCES.md) lists every source with the date it was last
checked.

The skills leave workflow and mechanics (devtools commands, testthat, cli
syntax, lifecycle, CRAN checks) to the Posit
[r-lib skills](https://github.com/posit-dev/skills) and point to them by
name, so install those too:

```
/plugin marketplace add posit-dev/skills
```

## Install

```
/plugin marketplace add jrnold/r-style-plugin
/plugin install r-style@r-style
```

## Checker

`skills/roxygen-style/scripts/check_roxygen.R` flags mechanical violations
(title case, third-person titles, `@param` capitalization and full stops,
missing `@returns`, `\code{\link{}}`, mixed spelling varieties):

```bash
Rscript skills/roxygen-style/scripts/check_roxygen.R path/to/pkg
```

It parses blocks with roxygen2, but its rule checks are heuristic, so review
each hit before you change anything. It needs R 4.4 or later and roxygen2.
Its tests use testthat:

```bash
just test
```

## Evals

`evals/` holds a `claude plugin eval` suite:
two cases per rule skill (one review, one writing task), plus a second pair
for the `r-code-style` argument, input-checking, and idiom rules, two
`r-review` cases on a change that touches all four aspects (one inline, one
with the reviewer agents), and one negative case that checks no skill fires on a
Python task. Each case gives an R snippet, diff, or `NEWS.md` with seeded rule
violations. LLM graders check that the response catches them, and
`tool_used` graders check that the right skills and agents ran.

```bash
just eval                          # every case, with and without the plugin
just eval --tag r-news --runs 1    # one skill, one run per case
```

Each run is a full Claude session on your account, so the full suite (13 cases,
3 runs, 2 arms) costs a few dollars. Results go to `evals/results/`, which git
ignores.

## Keeping the rules current

The repository has a local skill, `check-upstream` (in `.claude/skills/`,
not shipped with the plugin), that compares the rules with their sources: it
lists upstream commits since each source's `Checked` date in `SOURCES.md`,
re-verifies every evidence quote, looks for new chapters and package changes,
and checks for overlap with the r-lib skills. It reports proposed changes and
edits only after approval. The mechanical part runs on its own:

```bash
just check-upstream skills/r-code-style/references/evidence.md \
  skills/r-pkg-structure/references/evidence.md
```

## License

MIT
