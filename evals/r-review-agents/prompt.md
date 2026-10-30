---
name: r-review-agents
tags: [r-review, review, agents]
max_turns: 20
allowed_tools: [Read, Glob, Grep, Skill, Agent]
---

Please review this PR to my R package tidyfoo before I merge it, using the
separate reviewer agents. The package
is at version 0.4.0.9000. Here is the full diff:

```diff
diff --git a/R/count.R b/R/count.R
new file mode 100644
--- /dev/null
+++ b/R/count.R
@@ -0,0 +1,14 @@
+#' Counts Rows By Group.
+#'
+#' @param data a data frame
+#' @param by columns to count by
+#' @export
+count_by <- function(data, by) {
+  if (!is.data.frame(data)) {
+    stop("data should be a data frame")
+  }
+  out <- table(data[by])
+  return(as.data.frame(out))
+}
diff --git a/R/summarise.R b/R/summarise.R
--- a/R/summarise.R
+++ b/R/summarise.R
@@ -20,7 +20,7 @@ summarise_by <- function(data, by, na.rm = FALSE) {
-summarise_by <- function(data, by, na.rm = FALSE) {
+summarise_by <- function(data, by, na.rm = TRUE) {
```

The top of NEWS.md, which this PR doesn't change:

```markdown
# tidyfoo (development version)

* `pivot_foo()` now keeps attributes of the input (#130).
```
