# Evidence for r-pkg-structure rules

Checked 2026-10-29 against the live pages below, converted to Markdown and
searched for each rule's wording. Quotes are verbatim, trimmed with `...`.
Re-check with the repository's `check-upstream` skill.

Overlap with the Posit r-lib skills was checked the same day by searching
their `SKILL.md` and `references/` files. They cover `use_testthat(3)` and
`Config/testthat/edition` (`testing-r-packages`) and `use_tidy_description()`
(`cran-extrachecks`), so rule 12 points to them. None of rules 1-11 appear
there.

## Dependencies

  | Rule | Source                                                                                       | Quote                                                                                                                                                                                                                                                                                                                                                                          |
  | ---- | -------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
  | 1    | R Packages, [dependencies: mindset](https://r-pkgs.org/dependencies-mindset-background.html) | "One problem with simply minimizing the absolute number of dependencies is that it treats all dependencies as equivalent" / "Already fulfilled dependencies. If your package depends on dplyr then taking a dependency on tibble does not change the dependency footprint"                                                                                                     |
  | 2    | R Packages, [dependencies in practice](https://r-pkgs.org/dependencies-in-practice.html)     | "we recommend that you default to *not* importing anything from aaapkg into your namespace" / exceptions: "An operator", "A function that you use *a lot*", "A function that you call in a tight loop"                                                                                                                                                                         |
  | 3    | R Packages, [dependencies in practice](https://r-pkgs.org/dependencies-in-practice.html)     | "check for the availability of a suggested package with `requireNamespace("aaapkg", quietly = TRUE)`. There are two basic scenarios: the dependency is absolutely required or your package offers some sort of fallback behaviour." / "The rlang package has some useful functions for checking package availability: `rlang::check_installed()` and `rlang::is_installed()`." |

## Tidy evaluation

  | Rule | Source                                                                                             | Quote                                                                                                                                                                                                |
  | ---- | -------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
  | 4    | rlang, [data-mask programming](https://rlang.r-lib.org/reference/topic-data-mask-programming.html) | "The embrace operator `{{` is a forwarding syntax for single arguments."                                                                                                                             |
  | 5    | dplyr, [using dplyr in packages](https://dplyr.tidyverse.org/articles/in-packages.html)            | "For data masking, import `.data` from rlang and then use `.data$var` instead of `var`." / "For tidy selection, use `"var"` instead of `var`."                                                       |
  | 6    | dplyr, [programming](https://dplyr.tidyverse.org/articles/programming.html)                        | "When you have an env-variable that is a character vector, you need to index into the `.data` pronoun with `[[`"                                                                                     |
  | 7    | dplyr, [using dplyr in packages](https://dplyr.tidyverse.org/articles/in-packages.html)            | "To silence this, place `utils::globalVariables("closest")` in a source file in your package (but outside of any function)." The example is the `closest()` helper inside `join_by()`, not a column. |

## S3 classes

  | Rule | Source                                            | Quote                                                                                                                                                                                                                                                                                                                                                                           |
  | ---- | ------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
  | 8    | Advanced R, [S3](https://adv-r.hadley.nz/s3.html) | "A low-level **constructor**, `new_myclass()` ... A **validator**, `validate_myclass()` ... A user-friendly **helper**, `myclass()`" / "You don't need a validator for very simple classes, and you can skip the helper if the class is for internal use only, but you should always provide a constructor." / "you can learn more from the documentation of the vctrs package" |

## Files

  | Rule | Source                                           | Quote                                                                                                                                                                                 |
  | ---- | ------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
  | 9    | R Packages, [code](https://r-pkgs.org/code.html) | "The file name should be meaningful and convey which functions are defined within." / "don't put all functions into one file and don't put each function into its own separate file." |

## Load hooks and options

  | Rule | Source                                           | Quote                                                                                                                                                                                                                                        |
  | ---- | ------------------------------------------------ | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
  | 10   | R Packages, [code](https://r-pkgs.org/code.html) | "To set custom options for your package with `options()`. To avoid conflicts with other packages, ensure that you prefix option names with the name of your package. Also be careful not to override options that the user has already set." |
  | 11   | R Packages, [code](https://r-pkgs.org/code.html) | "Startup messages are one place where you should use `.onAttach()` instead of `.onLoad()`. To display startup messages, always use `packageStartupMessage()`"                                                                                |

## Upkeep

  | Rule | Source                                                                                                    | Quote                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  |
  | ---- | --------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
  | 12   | usethis, [`R/upkeep.R`](https://github.com/r-lib/usethis/blob/main/R/upkeep.R), `tidy_upkeep_checklist()` | Items used: "`usethis::use_roxygen_md()`", "Use lifecycle instead of artisanal deprecation messages", "Use cli errors", "`usethis::use_standalone("r-lib/rlang", "types-check")` instead of home grown argument checkers", "Change files ending in `.r` to `.R`", "`usethis::use_air()`", "Switch to the base pipe", "`usethis::use_package("R", "Depends", "{tidy_minimum_r_version()}")`" (which reads `r-oldrel/4` from the R-hub versions API), "`usethis::use_tidy_description()`", "`usethis::use_testthat(3)`". |

Items not used: those specific to Posit (copyright holder, ROR, email
domains), GitHub and pkgdown site setup, logos, and the code of conduct.
These are project administration, not package structure.
