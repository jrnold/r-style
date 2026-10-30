---
type: llm
weight: 1
---

The response raises at least two of: (1) `utils::globalVariables()` is used to silence NOTEs about the columns `grp` and `value`; use `.data$grp` (with `@importFrom rlang .data`) instead; (2) `mean(get(col))` should be `mean(.data[[col]])`; (3) `aes(grp, mean)` uses bare column names in package code; use `.data$grp` and `.data$mean`.
