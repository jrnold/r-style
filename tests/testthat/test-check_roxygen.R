script <- test_path("../../skills/roxygen-style/scripts/check_roxygen.R")
source(script, local = TRUE)

pkg <- test_path("fixtures/pkg")
hits <- check_roxygen(pkg)

hits_for <- function(rule) {
  grep(paste0(": rule ", rule, ": "), hits, value = TRUE)
}

test_that("flags a title with a period, Title Case, and a third-person verb", {
  expect_match(
    hits_for(1),
    "bad.R:1: rule 1: title ends with a period",
    all = FALSE
  )
  expect_match(hits_for(1), "title looks Title Case", all = FALSE)
  expect_match(hits_for(2), "bad.R:1: .*third-person verb 'Creates'")
})

test_that("flags a title longer than 65 characters", {
  expect_match(hits_for(3), "bad.R:12: rule 3: title is 74 chars")
})

test_that("flags @param text that isn't a sentence", {
  expect_length(grep("@param x: should start with a capital", hits_for(4)), 1)
  expect_length(grep("@param w: should end with a full stop", hits_for(4)), 1)
})

test_that("flags exported topics with no @returns, not data or S3 methods", {
  expect_length(hits_for(10), 2)
  expect_match(
    hits_for(10),
    "bad.R:1: rule 10: exported topic 'wmean'",
    all = FALSE
  )
  # A quoted operator name is a function, not a dataset.
  expect_match(
    hits_for(10),
    "bad.R:19: rule 10: exported topic '-.myplot'",
    all = FALSE
  )
})

test_that("flags \\code{\\link{}}", {
  expect_match(hits_for(13), "bad.R:3: rule 13:")
})

test_that("flags British spelling in prose but not in code, quotes, or links", {
  expect_length(hits_for(18), 1)
  expect_match(hits_for(18), "bad.R:3: rule 18: 'colour'")
})

test_that("good.R has no findings", {
  expect_false(any(grepl("good.R", hits, fixed = TRUE)))
})

test_that("`rules` selects which rules to report", {
  expect_setequal(
    sub(".*: rule (\\d+):.*", "\\1", check_roxygen(pkg, rules = c(2, 13))),
    c("2", "13")
  )
})

test_that("Language: en-GB flips rule 18, and `spelling` overrides it", {
  gb <- test_path("fixtures/pkg-gb")
  expect_match(
    check_roxygen(gb, rules = 18),
    "gb.R:3: rule 18: 'color': use British spelling"
  )
  expect_match(
    check_roxygen(gb, rules = 18, spelling = "us"),
    "'Normalise'",
    all = FALSE
  )
})

test_that("the command line prints findings and a summary", {
  out <- system2(
    "Rscript",
    c(script, pkg, "--rules", "13"),
    stdout = TRUE,
    stderr = TRUE
  )
  expect_match(out, "bad.R:3: rule 13:", all = FALSE)
  expect_match(out, "1 findings: rule 13: 1", all = FALSE)
})

test_that("the command line rejects a bad --spelling", {
  out <- suppressWarnings(system2(
    "Rscript",
    c(script, pkg, "--spelling", "au"),
    stdout = TRUE,
    stderr = TRUE
  ))
  expect_match(out, "must be \"us\" or \"gb\"", all = FALSE)
})
