---
type: llm
weight: 1
---

The response flags the error message "Error: data should be a data frame!!"
and suggests a rewrite in the "must" form naming what was received, e.g.
"`data` must be a data frame, not a character vector.", ideally with
`cli::cli_abort()`. Fail if the error message is not discussed.
