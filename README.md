# roxygen-style

A [Claude Code](https://claude.com/claude-code) plugin with wording and style
rules for roxygen2 documentation in R packages: titles, `@param`, `@returns`,
prose, and structure. The rules come from an audit of 12 tidyverse and r-lib
packages and from maintainer review comments; see
[`skills/roxygen-style/references/evidence.md`](skills/roxygen-style/references/evidence.md).

It complements the `r-lib` skills: `r-package-development` covers workflow and
`cran-extrachecks` covers CRAN requirements. This plugin covers prose style.

## Install

```
/plugin marketplace add jrnold/roxygen-style
/plugin install roxygen-style@roxygen-style
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
