---
type: llm
weight: 1
---

The response raises at least three of these function-design issues:
(1) `data` (the primary input) should be the first argument / required
arguments should come before optional ones; (2) `...` should come after
required arguments and before optional ones; (3) `use_fast` is a boolean that
picks a strategy and should be an enum (e.g. `method = c("fast", ...)`);
(4) the return type depends on input values (`nrow(x) == 1` returns
coefficients, otherwise a list) and is not type-stable.
