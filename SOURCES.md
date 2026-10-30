# Sources

The upstream guidance the r-style rules are drawn from. Each skill's
`references/evidence.md` quotes these pages rule by rule; this file lists them
in one place so they can be re-checked. The `check-upstream` skill in
`.claude/skills/` reads the table below: it fetches each URL to re-verify
quotes, and lists commits to `Repo`/`Path` since the `Checked` date.

Keep one row per page. `Repo` and `Path` name the file the page is built
from; leave them as `-` when there is none. `Checked` is the date the row was
last compared against the rules.

  | Source                                    | URL                                                                                   | Repo                  | Path                                    | Used by                       | Checked    |
  | ----------------------------------------- | ------------------------------------------------------------------------------------- | --------------------- | --------------------------------------- | ----------------------------- | ---------- |
  | Style: syntax                             | https://style.tidyverse.org/syntax.html                                               | tidyverse/style       | syntax.qmd                              | r-code-style                  | 2026-10-29 |
  | Style: functions                          | https://style.tidyverse.org/functions.html                                            | tidyverse/style       | functions.qmd                           | r-code-style                  | 2026-10-29 |
  | Style: pipes                              | https://style.tidyverse.org/pipes.html                                                | tidyverse/style       | pipes.qmd                               | r-code-style                  | 2026-10-29 |
  | Style: ggplot2                            | https://style.tidyverse.org/ggplot2.html                                              | tidyverse/style       | ggplot2.qmd                             | r-code-style                  | 2026-10-29 |
  | Style: errors                             | https://style.tidyverse.org/errors.html                                               | tidyverse/style       | errors.qmd                              | r-code-style                  | 2026-10-29 |
  | Style: tests                              | https://style.tidyverse.org/tests.html                                                | tidyverse/style       | tests.qmd                               | r-code-style                  | 2026-10-29 |
  | Style: documentation                      | https://style.tidyverse.org/documentation.html                                        | tidyverse/style       | documentation.qmd                       | roxygen-style                 | 2026-10-04 |
  | Style: NEWS                               | https://style.tidyverse.org/news.html                                                 | tidyverse/style       | news.qmd                                | r-news                        | 2026-10-05 |
  | Design: important arguments first         | https://design.tidyverse.org/important-args-first.html                                | tidyverse/design      | important-args-first.qmd                | r-code-style                  | 2026-10-29 |
  | Design: required, no defaults             | https://design.tidyverse.org/required-no-defaults.html                                | tidyverse/design      | required-no-defaults.qmd                | r-code-style                  | 2026-10-29 |
  | Design: dots after required               | https://design.tidyverse.org/dots-after-required.html                                 | tidyverse/design      | dots-after-required.qmd                 | r-code-style                  | 2026-10-29 |
  | Design: short defaults                    | https://design.tidyverse.org/defaults-short-and-sweet.html                            | tidyverse/design      | defaults-short-and-sweet.qmd            | r-code-style                  | 2026-10-29 |
  | Design: magical defaults                  | https://design.tidyverse.org/def-magical.html                                         | tidyverse/design      | def-magical.qmd                         | r-code-style                  | 2026-10-29 |
  | Design: boolean strategies                | https://design.tidyverse.org/boolean-strategies.html                                  | tidyverse/design      | boolean-strategies.qmd                  | r-code-style                  | 2026-10-29 |
  | Design: enumerate options                 | https://design.tidyverse.org/enumerate-options.html                                   | tidyverse/design      | enumerate-options.qmd                   | r-code-style                  | 2026-10-29 |
  | Design: independent meaning               | https://design.tidyverse.org/independent-meaning.html                                 | tidyverse/design      | independent-meaning.qmd                 | r-code-style                  | 2026-10-29 |
  | Design: type stability                    | https://design.tidyverse.org/out-type-stability.html                                  | tidyverse/design      | out-type-stability.qmd                  | r-code-style                  | 2026-10-29 |
  | Design: invisible output                  | https://design.tidyverse.org/out-invisible.html                                       | tidyverse/design      | out-invisible.qmd                       | r-code-style                  | 2026-10-29 |
  | Design: side effects                      | https://design.tidyverse.org/side-effects.html                                        | tidyverse/design      | side-effects.qmd                        | r-code-style                  | 2026-10-29 |
  | Design: dot prefix                        | https://design.tidyverse.org/dots-prefix.html                                         | tidyverse/design      | dots-prefix.qmd                         | r-code-style                  | 2026-10-29 |
  | Design: inspect the dots                  | https://design.tidyverse.org/dots-inspect.html                                        | tidyverse/design      | dots-inspect.qmd                        | r-code-style                  | 2026-10-29 |
  | Design: function names                    | https://design.tidyverse.org/function-names.html                                      | tidyverse/design      | function-names.qmd                      | r-code-style                  | 2026-10-29 |
  | Design: consistent argument names (draft) | https://raw.githubusercontent.com/tidyverse/design/main/consistent-argument-names.qmd | tidyverse/design      | consistent-argument-names.qmd           | r-code-style                  | 2026-10-29 |
  | Code review: writing comments             | https://code-review.tidyverse.org/reviewer/comments.html                              | tidyverse/code-review | reviewer/comments.qmd                   | r-review                      | 2026-10-29 |
  | Code review: focused PRs                  | https://code-review.tidyverse.org/author/focused.html                                 | tidyverse/code-review | author/focused.qmd                      | r-review                      | 2026-10-29 |
  | R Packages: code                          | https://r-pkgs.org/code.html                                                          | hadley/r-pkgs         | code.Rmd                                | r-code-style, r-pkg-structure | 2026-10-29 |
  | R Packages: dependencies in practice      | https://r-pkgs.org/dependencies-in-practice.html                                      | hadley/r-pkgs         | dependencies-in-practice.Rmd            | r-pkg-structure               | 2026-10-29 |
  | R Packages: dependency mindset            | https://r-pkgs.org/dependencies-mindset-background.html                               | hadley/r-pkgs         | dependencies-mindset-background.Rmd     | r-code-style, r-pkg-structure | 2026-10-29 |
  | R Packages: lifecycle                     | https://r-pkgs.org/lifecycle.html                                                     | hadley/r-pkgs         | lifecycle.Rmd                           | r-code-style                  | 2026-10-29 |
  | Advanced R: S3                            | https://adv-r.hadley.nz/s3.html                                                       | hadley/adv-r          | S3.Rmd                                  | r-pkg-structure               | 2026-10-29 |
  | Advanced R: functionals                   | https://adv-r.hadley.nz/functionals.html                                              | hadley/adv-r          | Functionals.Rmd                         | r-code-style                  | 2026-10-29 |
  | Advanced R: control flow                  | https://adv-r.hadley.nz/control-flow.html                                             | hadley/adv-r          | Control-flow.Rmd                        | r-code-style                  | 2026-10-29 |
  | rlang: check_dots_empty()                 | https://rlang.r-lib.org/reference/check_dots_empty.html                               | r-lib/rlang           | R/dots-ellipsis.R                       | r-code-style                  | 2026-10-29 |
  | rlang: dots-ellipsis source               | https://raw.githubusercontent.com/r-lib/rlang/main/R/dots-ellipsis.R                  | r-lib/rlang           | R/dots-ellipsis.R                       | r-code-style                  | 2026-10-29 |
  | rlang: check_exclusive()                  | https://rlang.r-lib.org/reference/check_exclusive.html                                | r-lib/rlang           | R/arg.R                                 | r-code-style                  | 2026-10-29 |
  | rlang: arg source                         | https://raw.githubusercontent.com/r-lib/rlang/main/R/arg.R                            | r-lib/rlang           | R/arg.R                                 | r-code-style                  | 2026-10-29 |
  | rlang: data-mask programming              | https://rlang.r-lib.org/reference/topic-data-mask-programming.html                    | r-lib/rlang           | man/rmd/topic-data-mask-programming.Rmd | r-pkg-structure               | 2026-10-29 |
  | rlang: NEWS                               | https://raw.githubusercontent.com/r-lib/rlang/main/NEWS.md                            | r-lib/rlang           | NEWS.md                                 | r-code-style                  | 2026-10-29 |
  | rlang: standalone types-check             | https://raw.githubusercontent.com/r-lib/rlang/main/R/standalone-types-check.R         | r-lib/rlang           | R/standalone-types-check.R              | r-code-style                  | 2026-10-29 |
  | vctrs: recycling FAQ                      | https://vctrs.r-lib.org/reference/theory-faq-recycling.html                           | r-lib/vctrs           | man/faq/developer/theory-recycling.Rmd  | r-code-style                  | 2026-10-29 |
  | testthat: test_that()                     | https://testthat.r-lib.org/reference/test_that.html                                   | r-lib/testthat        | R/test-that.R                           | r-code-style                  | 2026-10-29 |
  | usethis: use_standalone()                 | https://usethis.r-lib.org/reference/use_standalone.html                               | r-lib/usethis         | R/use_standalone.R                      | r-code-style                  | 2026-10-29 |
  | usethis: upkeep checklist                 | https://raw.githubusercontent.com/r-lib/usethis/main/R/upkeep.R                       | r-lib/usethis         | R/upkeep.R                              | r-pkg-structure               | 2026-10-29 |
  | dplyr: using dplyr in packages            | https://dplyr.tidyverse.org/articles/in-packages.html                                 | tidyverse/dplyr       | vignettes/in-packages.Rmd               | r-pkg-structure               | 2026-10-29 |
  | dplyr: programming                        | https://dplyr.tidyverse.org/articles/programming.html                                 | tidyverse/dplyr       | vignettes/programming.Rmd               | r-pkg-structure               | 2026-10-29 |
  | Posit r-lib skills (overlap)              | -                                                                                     | posit-dev/skills      | r-lib                                   | all                           | 2026-10-29 |

The `roxygen-style` and `r-news` rows record only the style-guide chapters;
their corpus audits (12 tidyverse and r-lib packages) are described in each
skill's `references/evidence.md` and are re-run with `tools/r-news-audit/`
and `skills/roxygen-style/scripts/check_roxygen.R`, not by `check-upstream`.
