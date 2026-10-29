---
type: llm
weight: 1
---

The prose in the roxygen block uses American spelling ("normalize",
"behavior", etc.). The function name `normalise_names` may keep its spelling
because it is code. Fail if any free prose (not code in backticks) uses a
British "-ise"/"-our" spelling.
