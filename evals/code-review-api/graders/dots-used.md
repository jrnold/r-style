---
type: llm
weight: 1
---

The response says the `top_groups()` generic should call
`rlang::check_dots_used()` before `UseMethod()`, so a misspelled method
argument such as `top_groups(x, m = 3)` errors instead of being silently
ignored. Fail if it suggests adding the check only inside the method, or
doesn't raise unchecked dots in `top_groups()` at all. Not adding a check
to `print.group_summary()` is fine.
