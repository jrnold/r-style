---
name: news-review
tags: [r-news, review]
max_turns: 10
allowed_tools: [Read, Glob, Grep, Skill]
---

Review the development section of this NEWS.md before I release tidyfoo 1.0.0.
List the problems; don't rewrite the whole file.

```markdown
## tidyfoo (development version) - 2026-10-01

* BREAKING CHANGE: `read_foo()` returns a tibble.
* Fixed a bug in `write_foo()`. (#88)
* `old_fun()` is deprecated.
* We refactored the internal parser for speed
- `tidy_foo()` gains a `quiet` argument (@contrib, #91).
```
