---
type: llm
weight: 1
---

The response raises both: (1) `.onLoad()` sets `options(digits = 3)`, which overrides a global option the user may have set, and `verbose_summary` is not prefixed with the package name (e.g. `tidyfoo.verbose_summary`); (2) the welcome message belongs in `.onAttach()` with `packageStartupMessage()`, not `message()` in `.onLoad()`.
