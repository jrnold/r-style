---
name: code-review
tags: [r-code-style, review]
max_turns: 10
allowed_tools: [Read, Glob, Grep, Skill]
---

Please review this function I'm adding to my R package (it has already been
run through air and lintr). Report the issues you'd raise in code review.

```r
#' @export
fit.models <- function(verbose = FALSE, data, use_fast = TRUE, ...) {
  # loop over the years
  for (yr in c(2018, 2019)) {
    if (verbose & nrow(data) > 0) message("fitting ", yr)
  }
  # set x to the data
  x <- data
  if (!is.data.frame(x)) stop("Error: data should be a data frame!!")
  if (use_fast) {
    model_2018 <- lm(y ~ x1, x[x$year == 2018, ])
    model_2019 <- lm(y ~ x1, x[x$year == 2019, ])
  }
  if (nrow(x) == 1) {
    return(coef(model_2018))
  }
  return(list(model_2018, model_2019))
}
```
