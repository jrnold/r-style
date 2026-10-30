---
type: llm
weight: 1
---

The response flags that the PR adds `ggplot2` to `Imports` in `DESCRIPTION`
although nothing in the diff uses it, and suggests removing it or justifying
the dependency. Pass whether or not it cites a `pkg:` rule.
