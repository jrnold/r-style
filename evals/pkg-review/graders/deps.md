---
type: llm
weight: 1
---

The response raises both: (1) `#' @import dplyr` imports the whole namespace; call `dplyr::` functions or use `@importFrom` for the few used heavily; (2) `plot_means()` uses ggplot2, which is only in `Suggests`, without first checking it is installed (`rlang::check_installed("ggplot2")` or `requireNamespace()`).
