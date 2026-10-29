---
name: roxygen-review
tags: [roxygen-style, review]
max_turns: 10
allowed_tools: [Read, Glob, Grep, Skill]
---

Review the roxygen documentation in this file from my R package for style
problems. List each problem with the line it is on and a suggested rewrite.
Don't rewrite the code.

```r
#' Calculates The Weighted Mean Of A Vector.
#'
#' This function computes a weighted mean. We use \code{\link{weighted.mean}}
#' under the hood, and the colour of the output is not unimportant.
#'
#' @param x numeric vector of values
#' @param w weights, defaults to NULL
#' @param na.rm should missing values be removed
#' @export
wmean <- function(x, w = NULL, na.rm = FALSE) {
  if (is.null(w)) w <- rep(1, length(x))
  weighted.mean(x, w, na.rm = na.rm)
}
```
