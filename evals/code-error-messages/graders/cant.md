---
type: llm
weight: 1
---

The rewrite of the missing-column error leads with the "Can't" form, e.g.
"Can't find column {.field {col}} in `df`.", via `cli::cli_abort()`, and drops
the speculation that "the user made a typo". Extra `i` bullets are fine: one
that gives context (such as listing the available columns) or a hint phrased
as a question both pass. Fail only if the lead message doesn't use "Can't" or
the typo speculation remains.
