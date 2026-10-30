---
name: pkg-write
tags: [r-pkg-structure, write]
max_turns: 10
allowed_tools: [Read, Glob, Grep, Skill]
---

Add an exported function `plot_group_means(data, group, value)` to my R
package. Users pass bare column names, like dplyr. It should compute the mean
of `value` for each `group` with dplyr (in Imports) and draw a bar chart with
ggplot2 (in Suggests). Give me the function with its roxygen block, and any
changes to DESCRIPTION or NAMESPACE tags it needs.
