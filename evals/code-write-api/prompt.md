---
name: code-write-api
tags: [r-code-style, write]
max_turns: 10
allowed_tools: [Read, Glob, Grep, Skill]
---

Write an exported function for my R package, `map_groups()`. It takes a data
frame, the name of a grouping column, and a function; applies the function to
each group's rows, passing along any extra arguments the user gives; and
returns a numeric vector with one value per group. Check its inputs. Give me
just the function with its roxygen block.
