---
type: llm
weight: 1
---

The response says that `summarise_groups()`'s named arguments (`data`, `fn`,
and the others) should be dot-prefixed (`.data`, `.f` or `.fn`, ...) because
`...` is forwarded to `fn`, so a user's extra argument could collide with or
partially match them. Fail if dot-prefixing is not suggested.
