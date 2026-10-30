---
name: pkg-review
tags: [r-pkg-structure, review]
max_turns: 10
allowed_tools: [Read, Glob, Grep, Skill]
---

Please review the package-level parts of this PR to my R package tidyfoo
(`R CMD check` passes). Report the issues you'd raise in code review.

```diff
diff --git a/DESCRIPTION b/DESCRIPTION
--- a/DESCRIPTION
+++ b/DESCRIPTION
@@ -10,5 +10,8 @@ Imports:
     cli,
-    rlang (>= 1.1.0)
+    dplyr,
+    rlang (>= 1.1.0)
+Suggests:
+    ggplot2
diff --git a/R/zzz.R b/R/zzz.R
new file mode 100644
--- /dev/null
+++ b/R/zzz.R
@@ -0,0 +1,4 @@
+.onLoad <- function(libname, pkgname) {
+  options(digits = 3, verbose_summary = TRUE)
+  message("Welcome to tidyfoo!")
+}
diff --git a/R/functions.R b/R/functions.R
new file mode 100644
--- /dev/null
+++ b/R/functions.R
@@ -0,0 +1,25 @@
+#' @import dplyr
+NULL
+
+utils::globalVariables(c("grp", "value"))
+
+#' Mean of a column by group
+#'
+#' @param data A data frame with a `grp` column.
+#' @param col Name of the column to average, as a string.
+#' @returns A `means_tbl`.
+#' @export
+group_means <- function(data, col) {
+  out <- data |>
+    group_by(grp) |>
+    summarise(mean = mean(get(col)), n = n())
+  structure(out, class = c("means_tbl", class(out)))
+}
+
+#' Plot group means
+#'
+#' @param means A `means_tbl` from [group_means()].
+#' @returns A ggplot.
+#' @export
+plot_means <- function(means) {
+  ggplot2::ggplot(means, ggplot2::aes(grp, mean)) + ggplot2::geom_col()
+}
```
