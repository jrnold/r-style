---
name: r-pkg-structure
description: Review rules for how an R package is put together - dependencies (Imports, Suggests, `::` versus `@importFrom`), tidy evaluation in package code (`{{ }}`, `.data`, no-visible-binding NOTEs), S3 class constructors, `R/` file organization, `.onLoad()` and options, and the tidyverse upkeep checklist. Use when reviewing or writing package infrastructure, changing DESCRIPTION or NAMESPACE, adding a dependency, using dplyr or ggplot2 inside a package, defining an S3 class, or modernizing a package. Complements r-code-style (code inside functions), r-lib:r-package-development (workflow), r-lib:testing-r-packages, and r-lib:cran-extrachecks.
---

# R package structure: dependencies, tidy eval, classes, load hooks

Rules for how a package is assembled, which `R CMD check` doesn't judge. The
source for each rule is in [references/evidence.md](references/evidence.md).
For code inside functions see `r-style:r-code-style`; for commands and test
mechanics see `r-lib:r-package-development` and `r-lib:testing-r-packages`.

## Dependencies

1. **Weigh a new dependency by its cost, not by the count.** Base and
   recommended packages are nearly free; a package already pulled in by an
   existing dependency adds nothing; one that is slow or hard to install
   costs users. Ask whether the new code needs it.
2. **Call other packages with `pkg::fun()` by default.** Import into the
   namespace (`@importFrom pkg fun`) only operators (`%||%`), functions used
   so often that `::` hurts readability, or functions called in a tight loop.
3. **Check a `Suggests` package before using it.** When the function can't
   work without it, use `rlang::check_installed("pkg", reason = "to ...")`;
   when there is a fallback, branch on `rlang::is_installed("pkg")` or
   `requireNamespace("pkg", quietly = TRUE)`. `library()` in `R/` is
   `r-code-style` rule 41.

## Tidy evaluation in package code

4. **Forward a user's column argument with `{{ }}`**
   (`summarise(data, mean = mean({{ var }}))`).
5. **Columns the package names itself use `.data$col` in data masking and
   `"col"` in tidy selection**, with `@importFrom rlang .data`. Bare column
   names give the "no visible binding for global variable" NOTE.
6. **A column name held in a string uses `.data[[var]]`**.
7. **`utils::globalVariables()` is a last resort** for names that `.data`
   can't express, such as functions in a DSL (`join_by(closest())`). Don't
   use it to silence NOTEs about ordinary columns.

## S3 classes

8. **Every S3 class has a constructor, `new_myclass()`**, that builds the
   structure; don't scatter `structure(..., class = "myclass")` through the
   code. Add `validate_myclass()` when values need checking beyond their
   type, and a helper `myclass()` when users create objects. For vector-like
   classes, use the constructors and helpers in vctrs.

## Files

9. **Name `R/` files for the functions they hold.** Avoid both extremes: one
   file for everything (`functions.R`) and one file per small function.

## Load hooks and options

10. **`.onLoad()` does only the setup the package needs**, such as default
    options. Prefix option names with the package name (`mypkg.verbose`), and
    don't overwrite an option the user has already set.
11. **Startup messages go in `.onAttach()` with `packageStartupMessage()`**,
    not in `.onLoad()`.

## Upkeep

12. **When a change touches `DESCRIPTION`, CI, or package-wide setup, check
    it against the tidyverse upkeep checklist** (`usethis::use_tidy_upkeep_issue()`).
    Raise missing items as optional, not blocking:
    - roxygen Markdown (`usethis::use_roxygen_md()`);
    - air formatting (`usethis::use_air()`);
    - cli errors (`r-code-style` rules 24-29) and lifecycle deprecations
      (`r-lib:lifecycle`) instead of home-grown ones;
    - rlang type checkers instead of hand-rolled ones (`r-code-style` rule
      38; the checklist still names the standalone file, which predates
      rlang 1.2.0);
    - a minimum R version of `oldrel-4`, set with
      `usethis::use_package("R", "Depends", ...)`;
    - files in `R/` and `tests/testthat/` end in `.R`, not `.r`;
    - testthat 3rd edition (`r-lib:testing-r-packages`), the base pipe and
      `\(x)` (`r-lib:r-package-development`), and `use_tidy_description()`
      (`r-lib:cran-extrachecks`).

## Using this in a review

Report findings as `file:line: rule N: message`, most important first. Rules
1-3 and 8 are design decisions: raise them for new dependencies and new
classes, and don't demand churn in code the change doesn't touch. Rule 12 is
always optional.
