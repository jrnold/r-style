---
type: llm
weight: 1
---

The response suggests replacing the hand-rolled `group` check
(`!is.character(group) || length(group) != 1`) with rlang's
`check_string()` (exported from rlang 1.2.0, or from the rlang standalone
`types-check` file). Suggesting only `cli::cli_abort()` or `stopifnot()`
does not pass.
