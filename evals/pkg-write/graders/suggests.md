---
type: llm
weight: 1
---

Before using ggplot2, the function checks it is installed with `rlang::check_installed("ggplot2", ...)` (or `requireNamespace()` with an informative error). ggplot2 functions are called as `ggplot2::...` rather than imported with `@import ggplot2`, and ggplot2 stays in Suggests.
