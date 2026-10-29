---
name: news-write
tags: [r-news, write]
max_turns: 10
allowed_tools: [Read, Glob, Grep, Skill]
---

I'm working on my R package "tidyfoo". I just made these changes:

1. Fixed a bug where `summarise_by()` errored with "object 'i' not found"
   when `n = 0`; it now returns an empty tibble. Reported by @jdoe in issue #142.
2. Added a new `.sort` argument to `count_by()` (default `FALSE`) that sorts
   the output by count. PR #150.
3. Refactored internal helper `vec_cache()` and moved tests around.

Here is the current NEWS.md. Give me the updated top section.

```markdown
# tidyfoo (development version)

* `pivot_foo()` now keeps attributes of the input (#130).

# tidyfoo 0.3.0

* Initial CRAN release.
```
