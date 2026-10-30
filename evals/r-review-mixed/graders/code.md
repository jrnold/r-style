---
type: llm
weight: 1
---

The response raises at least two code issues in `count_by()`: the error
message should use the "must" form and name what was received (ideally with
`cli::cli_abort()`); the final `return()` is unnecessary; and/or a test file
for the new export is missing.
