---
type: llm
weight: 1
---

Inputs are validated with rlang standalone helpers (`check_data_frame()`,
`check_string()`, `check_function()`, ...) or with `cli::cli_abort()`
messages in the "must" form (e.g. "{.arg .by} must be a single string, not
...") rather than bare `stop()` or `stopifnot()`. The function does not call
`library()` or `require()`.
