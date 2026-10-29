---
name: code-error-messages
tags: [r-code-style, write]
max_turns: 10
allowed_tools: [Read, Glob, Grep, Skill]
---

Rewrite the error messages in this R package function so they follow
tidyverse style. Use cli.

```r
get_col <- function(df, col, n) {
  if (!is.numeric(n)) stop("n is wrong")
  if (!col %in% names(df)) {
    stop(paste0("Could not find column '", col, "'. Maybe the user made a typo?"))
  }
  head(df[[col]], n)
}
```
