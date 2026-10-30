---
type: llm
weight: 1
---

The function forwards `group` and `value` with the embrace operator `{{ }}`, and refers to columns it creates itself (such as the mean) with `.data$name` (with `@importFrom rlang .data`) or as strings in tidy selection. It does not use `utils::globalVariables()` for column names.
