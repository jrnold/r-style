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

`skills/roxygen-style/scripts/check_roxygen.py` flags mechanical violations
(title case, third-person titles, `@param` capitalization and full stops,
missing `@returns`, `\code{\link{}}`, mixed spelling varieties):

```bash
python3 skills/roxygen-style/scripts/check_roxygen.py path/to/pkg
```

It is heuristic, so review each hit before you change anything. It needs only
the Python 3 standard library.

## License

MIT
