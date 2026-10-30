---
type: llm
weight: 1
---

The response raises at least four of: (1) `group` and `group_index` are
mutually exclusive and `group_index` silently wins; (2) `remove_na` should be
`na.rm`; (3) `rep(weights, length.out = nrow(data))` silently recycles any
length, when only length 1 or `nrow(data)` should be allowed; (4) `1:n`
breaks when there are no groups; (5) `sapply()` should be `vapply()` or
`purrr::map_dbl()`; (6) `library(dplyr)` must not appear in package code.
