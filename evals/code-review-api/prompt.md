---
name: code-review-api
tags: [r-code-style, review]
max_turns: 10
allowed_tools: [Read, Glob, Grep, Skill]
---

Please review these functions I'm adding to my R package (they have already
been run through air and lintr). Report the issues you'd raise in code review.

```r
#' @export
summarise_groups <- function(data, fn, group = NULL, group_index = NULL,
                             weights = 1, remove_na = FALSE, ...) {
  library(dplyr)
  if (!is.null(group_index)) {
    group <- names(data)[[group_index]]
  }
  if (!is.character(group) || length(group) != 1) {
    stop("`group` must be a single string.")
  }
  weights <- rep(weights, length.out = nrow(data))
  keys <- unique(data[[group]])
  n <- length(keys)
  out <- vector("list", n)
  for (i in 1:n) {
    in_group <- data[[group]] == keys[[i]]
    out[[i]] <- fn(data[in_group, ], weights[in_group], ...)
  }
  if (remove_na) {
    out <- lapply(out, function(x) x[!is.na(x)])
  }
  structure(sapply(out, mean), class = "group_summary")
}

#' @export
print.group_summary <- function(x, digits = 3, ...) {
  cat(format(unclass(x), digits = digits), sep = "\n")
  invisible(x)
}
```
