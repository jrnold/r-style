---
type: llm
weight: 1
---

The function builds its result type-stably with `vapply(..., numeric(1))`,
`purrr::map_dbl()`, or a preallocated `numeric()` vector, not with
`sapply()` or `unlist(lapply())`. Any index loop uses `seq_along()` or
`seq_len()`, never `1:n` or `1:length(x)`.
