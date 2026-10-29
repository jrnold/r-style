---
name: roxygen-write
tags: [roxygen-style, write]
max_turns: 10
allowed_tools: [Read, Glob, Grep, Skill]
---

Write roxygen2 documentation for this exported function from my R package.
Reply with just the roxygen block and the function.

```r
normalise_names <- function(x, sep = "_", case = c("snake", "lower")) {
  case <- match.arg(case)
  out <- gsub("[^[:alnum:]]+", sep, x)
  if (case == "snake") out <- tolower(out)
  out
}
```
