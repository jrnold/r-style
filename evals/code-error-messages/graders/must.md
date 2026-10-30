---
type: llm
weight: 1
---

The rewrite of the `n` check produces a "must" message that names what was
received, either written with `cli::cli_abort()`, e.g.
"{.arg n} must be a numeric vector, not {.obj_type_friendly {n}}.", or by
replacing the check with an rlang type checker such as
`rlang::check_number_whole(n)` or `check_number_decimal(n)`, which produces
"`n` must be a whole number, not ...".
