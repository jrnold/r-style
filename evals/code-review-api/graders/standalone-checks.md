---
type: llm
weight: 1
---

The response suggests replacing the hand-rolled `group` check
(`!is.character(group) || length(group) != 1`) with an rlang standalone
helper such as `check_string()` (from
`usethis::use_standalone("r-lib/rlang", "types-check")`). Suggesting only
`cli::cli_abort()` or `stopifnot()` does not pass.
