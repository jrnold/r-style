---
name: r-code-style
description: Judgment-based review rules for R package code from the tidyverse style guide and tidy design principles, covering what air, styler, and lintr cannot check - naming, comments, pipes, function and argument design, error messages, and test naming. Use when reviewing or writing R code, doing a code review of an R diff, designing function signatures, or writing error messages in an R package. Complements r-lib:cli (error mechanics), r-lib:lifecycle (deprecation), r-lib:testing-r-packages (test mechanics), roxygen-style (documentation prose), and r-news (NEWS.md).
---

# R code review: what linters can't check

Rules for reviewing R code *after* `air`/`styler` and `lintr` have run. Do not
report whitespace, line length, `<-` versus `=`, or name casing; the tools own
those. Sources: [tidyverse style guide](https://style.tidyverse.org/) and
[tidy design principles](https://design.tidyverse.org/). Where the project
sets its own line length or conventions, the project wins.

For documentation prose see `roxygen-style`; for `cli` error mechanics see
`r-lib:cli`; for deprecation staging see `r-lib:lifecycle`.

## Names and structure

1. **Functions are verbs, variables are nouns.** Concise but meaningful.
2. **No dots in new function or class names** outside S3 methods.
3. **Don't shadow** base, stats, or ggplot2 functions with variables.
4. **Don't encode data in names** (`model_2018`, `model_2019`). Use a list or
   data frame.
5. **No assignment inside calls**, except to capture a side effect.
6. **`return()` only for early exits.** `return()`, `stop()`, `next`, and
   `break` get their own braced line, never inline.
7. **`&&`/`||` in conditions**, not `&`/`|`.
8. **Prefer early returns or a helper over deep nesting.** A function that is
   hard to keep readable in 80 columns usually needs a redesign, not a
   longer line limit.

## Comments

9. **Explain why**, not what or how: a decision, a surprising finding, a
   source. A comment that restates the code should be deleted, or the code
   renamed so it isn't needed.
10. **Long explanations belong in a vignette or Rmd**, not a comment block.

## Pipes

11. **Pipe a sequence of steps on one primary object.** Don't pipe across
    several objects.
12. **Break a long chain** into a named intermediate when the name helps the
    reader. Don't name steps that need no name.
13. **Data manipulation happens before `ggplot()`**, not inside its `data`
    argument.

## Function design

14. **The primary input comes first** (the thing being transformed), so the
    function pipes naturally.
15. **Required arguments have no default; optional ones do.** Then the
    signature reads without the docs.
16. **`...` goes after required arguments, before optional ones**, so optional
    arguments must be named in full.
17. **Defaults are short and not magical.** The function must behave the same
    whether a default is passed explicitly or omitted. Use `NULL` and resolve
    inside; avoid `missing()` and defaults that call unexported helpers.
18. **Prefer an enum over a boolean** when the argument picks a strategy, even
    with two choices (`match.arg()` / `rlang::arg_match()`).
19. **Argument meaning is independent.** Flag arguments whose meaning depends
    on another argument's value.
20. **Type-stable return.** The output type depends on input types, never on
    input values.
21. **Side-effect functions return their first argument invisibly**, so they
    pipe.
22. **Don't mix computation with side effects** in one function. When global
    state must change, restore it with `on.exit()` or `withr`.
23. **Never remove an exported function or argument outright.** Deprecate and
    forward (`r-lib:lifecycle`).

## Error messages

Use `cli` (`r-lib:cli`). The wording rules:

24. **Lead with a short problem statement:** sentence case, ends with a period.
25. **"must" when you know what was expected**, naming what was received:
    `` `n` must be a numeric vector, not a character vector. ``
    **"Can't" when you can't say what was expected:**
    `` Can't find column `b` in `.data`. ``
26. **Put detail in bullets:** `✖` for problems, `ℹ` for context. Short,
    singular sentences. Argument names in backticks; say "Column `x`" to
    disambiguate.
27. **Hints go last** as `ℹ` bullets ending in a question mark
    (``Did you mean `Species == "setosa"`?``), and only when the cause and fix
    are clear and common.
28. **Don't blame an argument or speculate** about a cause you haven't
    verified.
29. **List at most five problems**, then say how many more there are.

## NEWS.md

30. **See the `r-news` skill.** Flag a user-facing change that has no bullet.

## Tests

31. **Test file mirrors the `R/` file** (`R/foofy.R` -> `tests/testthat/test-foofy.R`)
    unless the project documents another layout. Use `usethis::use_test()`.
32. **Test names state the behavior** being checked, because the name appears
    in failure output. Test mechanics: `r-lib:testing-r-packages`.

## Using this in a review

Report findings as `file:line: rule N: message`, most important first. Cite
the rule number so the author can look it up. Don't churn code that passes
these rules over taste, and keep style-only fixes in a separate change from
behavior changes. Rules 14-23 are API decisions: raise them for new or changed
exports, and don't demand a breaking change to an existing one.
