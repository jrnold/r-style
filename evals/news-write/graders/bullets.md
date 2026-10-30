---
type: llm
weight: 1
---

Judge only the bullets inside the updated NEWS.md section, not the
commentary around it (commentary may quote words like "Fixed" when explaining
choices; that is fine).

Pass if the section has a bullet for the `summarise_by()` fix and one for the
new `count_by()` argument, and each bullet names its function at or near the
start, describes the current behavior in present tense (e.g. "`summarise_by()`
no longer errors ..." or "... now returns ...", "`count_by()` gains a `.sort`
argument ..."), and does not begin with "Fixed" or "Added". Wording, order,
and blank lines between bullets don't matter.
