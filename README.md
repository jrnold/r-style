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
  covering code, roxygen, and `NEWS.md`. It decides which of the skills below
  apply, then reviews inline or launches one reviewer agent per aspect
  (`r-code-reviewer`, `roxygen-reviewer`, `news-reviewer`), and merges the
  findings into one ranked report with rule IDs such as `[news:18]`.
- `roxygen-style`: wording and style of roxygen2 documentation.
- `r-news`: what earns a `NEWS.md` bullet, heading structure, bullet wording,
  ordering, breaking changes, deprecations, and release checks, with the
  tidyverse style guide as the standard and an audit of 1,048 bullets from 12
  tidyverse and r-lib packages as supporting evidence.
- `r-code-style`: review rules for R code that `air`, `styler`, and `lintr`
  cannot check (naming, comments, pipes, function and argument design, error
  messages, test names). Drawn from the
  [tidyverse style guide](https://style.tidyverse.org/) and
  [tidy design principles](https://design.tidyverse.org/).

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
two cases per rule skill (one review, one writing task), two `r-review`
cases on a change that touches all three aspects (one inline, one with the
reviewer agents), and one negative case that checks no skill fires on a
Python task. Each case gives an R snippet, diff, or `NEWS.md` with seeded rule
violations. LLM graders check that the response catches them, and
`tool_used` graders check that the right skills and agents ran.

```bash
just eval                          # every case, with and without the plugin
just eval --tag r-news --runs 1    # one skill, one run per case
```

Each run is a full Claude session on your account, so the full suite (9 cases,
3 runs, 2 arms) costs a few dollars. Results go to `evals/results/`, which git
ignores.

## License

MIT
