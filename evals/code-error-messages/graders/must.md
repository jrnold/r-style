---
type: llm
weight: 1
---

The rewrite of the `n` check uses the "must" form and names what was received,
e.g. "`n` must be a number, not a string." or
"{.arg n} must be a numeric vector, not {.obj_type_friendly {n}}.", via
`cli::cli_abort()`.
