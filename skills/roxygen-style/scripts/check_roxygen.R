#!/usr/bin/env Rscript
# Heuristic roxygen style checker for the roxygen-style skill.
#
# Usage: Rscript check_roxygen.R PKG_DIR [--rules 1,2,4,10] [--spelling us|gb]
#
# Prints `file:line: rule N: message`. Checks rules 1, 2, 3, 4, 10, 13, 18
# from SKILL.md. Heuristic: review each hit before acting.
#
# Rule 18 target spelling: `--spelling us|gb`, else DESCRIPTION `Language:`
# (en-GB -> gb), else us.
#
# Needs roxygen2, which parses the blocks, so multi-line tags, `@rdname`
# groups, and the documented object come from roxygen itself.

small_words <- c(
  "a",
  "an",
  "the",
  "of",
  "and",
  "or",
  "to",
  "in",
  "for",
  "with",
  "by",
  "on",
  "as",
  "at",
  "from",
  "via",
  "vs"
)
# Second words that suggest the first word is a verb ("Creates a ...").
verbish_next <- c(
  "a",
  "an",
  "the",
  "one",
  "each",
  "all",
  "whether",
  "if",
  "its",
  "any",
  "new",
  "multiple",
  "two"
)

# Rule 18: British pattern, American pattern, American form, British form.
# Suffix groups keep identifiers like `scale_colour_hue` and "ColorBrewer"
# from matching (they lack a word boundary at the right place).
ise_stems <- paste0(
  "organi|recogni|initiali|normali|customi|summari|standardi|minimi|maximi|",
  "optimi|visuali|seriali|capitali|prioriti|categori|characteri|finali|",
  "utili|speciali|generali|parameteri|vectori|randomi|synchroni|apologi|",
  "emphasi|memori|authori|digiti|tokeni|locali|reali"
)
ise_end <- "(e|es|ed|ing|ation|ations|er|ers)"
spelling_rules <- list(
  c(
    "colour(s|ed|ing|ful|less|ation)?",
    "color(s|ed|ing|ful|less|ation)?",
    "color",
    "colour"
  ),
  c("behaviour(s|al)?", "behavior(s|al)?", "behavior", "behaviour"),
  c(
    "favour(s|ed|ing|ite|ites)?",
    "favor(s|ed|ing|ite|ites)?",
    "favor",
    "favour"
  ),
  c(
    "(neighbour|honour|labour|flavour|humour|rumour)(s|ed|ing|hood)?",
    "(neighbor|honor|labor|flavor|humor|rumor)(s|ed|ing|hood)?",
    "-or",
    "-our"
  ),
  c(
    "(centre|metre|litre|fibre|theatre)(s|d)?",
    "(center|meter|liter|fiber|theater)(s|ed)?",
    "-er",
    "-re"
  ),
  c("grey(s|ed|ish|scale)?", "gray(s|ed|ish|scale)?", "gray", "grey"),
  c("analys(e|es|ed|ing)", "analyz(e|es|ed|ing)", "analyze", "analyse"),
  c(
    paste0("(", ise_stems, ")s", ise_end),
    paste0("(", ise_stems, ")z", ise_end),
    "-ize",
    "-ise"
  ),
  c(
    "(model|label|cancel|travel|signal)l(ed|ing|er|ers)",
    "(model|label|cancel|travel|signal)(ed|ing|er|ers)",
    "single l (modeling, labeled)",
    "double l (modelling, labelled)"
  ),
  c(
    "(catalogue|analogue)(s|d)?",
    "(catalog|analog)(s|ed)?",
    "catalog/analog",
    "catalogue/analogue"
  ),
  c(
    "(licence|defence|offence)(s)?",
    "(license|defense|offense)(s)?",
    "-se",
    "-ce"
  ),
  c("(whilst|amongst)", "(while|among)", "while/among", "whilst/amongst")
)
# Text that keeps its own spelling: backticked code, double-quoted text
# (titles of cited works), Rd code/link macros, and [fn()] / [topic] links.
exempt_rx <- paste0(
  '`[^`]*`|"[^"]*"|',
  "\\\\(code|link|pkg|var|env|file|href|url)(\\[[^]]*\\])?\\{[^}]*\\}|",
  "\\[[^]\\s]*\\]"
)
# Tags whose text is not prose.
not_prose <- c(
  "examples",
  "examplesIf",
  "example",
  "rdname",
  "family",
  "export",
  "importFrom",
  "import",
  "inheritParams",
  "inherit",
  "inheritDotParams",
  "inheritSection",
  "name",
  "aliases",
  "usage",
  "keywords",
  "concept",
  "docType",
  "include",
  "eval",
  "evalRd",
  "S3method",
  "method",
  "useDynLib",
  "encoding",
  "md",
  "noMd",
  "order"
)

target_spelling <- function(pkg, override = NULL) {
  if (!is.null(override)) {
    return(override)
  }
  desc <- file.path(pkg, "DESCRIPTION")
  lang <- if (file.exists(desc)) {
    read.dcf(desc, fields = "Language")[1, 1]
  } else {
    NA
  }
  if (!is.na(lang) && startsWith(tolower(lang), "en-gb")) "gb" else "us"
}

# Words in a prose line that use the other spelling variety, with the
# form to use instead.
spelling_hits <- function(text, target) {
  text <- gsub(exempt_rx, " ", text, perl = TRUE)
  hits <- list()
  for (rule in spelling_rules) {
    rx <- if (target == "us") rule[[1]] else rule[[2]]
    want <- if (target == "us") rule[[3]] else rule[[4]]
    m <- gregexpr(
      paste0("\\b", rx, "\\b"),
      text,
      perl = TRUE,
      ignore.case = TRUE
    )
    for (word in regmatches(text, m)[[1]]) {
      hits[[length(hits) + 1]] <- c(word, want)
    }
  }
  hits
}

squish <- function(x) trimws(gsub("\\s+", " ", x))

# Name of the function a block documents, or NULL.
function_name <- function(call) {
  is_assign <- is.call(call) &&
    length(call) == 3 &&
    as.character(call[[1]]) %in% c("<-", "=")
  if (
    is_assign &&
      is.call(call[[3]]) &&
      identical(call[[3]][[1]], as.name("function"))
  ) {
    as.character(call[[2]])
  }
}

check_title <- function(title, hit) {
  t <- squish(title$raw)
  ln <- title$line
  if (endsWith(t, ".") && !endsWith(t, "...")) {
    hit(ln, 1, sprintf("title ends with a period: '%s'", t))
  }
  stripped <- gsub("`[^`]*`", "CODE", t)
  words <- regmatches(
    stripped,
    gregexpr("[A-Za-z][\\w'-]*", stripped, perl = TRUE)
  )[[1]]
  later <- words[-1]
  later <- later[!tolower(later) %in% small_words & later != "CODE"]
  caps <- grepl("^[A-Z]", later) & later != toupper(later)
  if (length(later) >= 2 && caps[[1]] && mean(caps) >= 0.6) {
    hit(ln, 1, sprintf("title looks Title Case (use sentence case): '%s'", t))
  }
  if (length(words) >= 2) {
    w1 <- tolower(words[[2]])
    third_person <- grepl("^[A-Z][a-z]{2,}[^su]s$", words[[1]])
    if (third_person && w1 %in% c(verbish_next, "code")) {
      hit(
        ln,
        2,
        sprintf(
          "title starts with third-person verb '%s' (use imperative): '%s'",
          words[[1]],
          t
        )
      )
    }
  }
  if (nchar(t) > 65) {
    hit(ln, 3, sprintf("title is %d chars (> 65)", nchar(t)))
  }
}

check_param <- function(tag, hit) {
  raw <- trimws(tag$raw)
  m <- regmatches(
    raw,
    regexec("(?s)^([\\w.,`\\s]+?)\\s+(.*)$", raw, perl = TRUE)
  )
  m <- m[[1]]
  if (length(m) == 0) {
    return(invisible())
  }
  name <- trimws(m[[2]])
  d <- squish(m[[3]])
  if (d == "") {
    return(invisible())
  }
  capital <- grepl("^([A-Z`<\\[*\\-\\\\]|\\d)", d, perl = TRUE) ||
    startsWith(d, "e.g.") ||
    startsWith(d, "i.e.")
  if (!capital) {
    hit(
      tag$line,
      4,
      sprintf(
        "@param %s: should start with a capital: '%s'",
        name,
        substr(d, 1, 60)
      )
    )
  }
  if (!grepl("[.!?:]\\)?`?$|^`r lifecycle", d, perl = TRUE)) {
    tail <- substr(d, max(1, nchar(d) - 49), nchar(d))
    hit(
      tag$line,
      4,
      sprintf("@param %s: should end with a full stop: ...'%s'", name, tail)
    )
  }
}

# Rules 13 and 18 look at each line of a tag's text.
check_lines <- function(tag, spelling, hit) {
  lines <- strsplit(tag$raw, "\n", fixed = TRUE)[[1]]
  for (i in seq_along(lines)) {
    text <- lines[[i]]
    ln <- tag$line + i - 1
    if (grepl("\\code{\\link", text, fixed = TRUE)) {
      hit(ln, 13, "use [fn()] instead of \\code{\\link{}}")
    }
    if (tag$tag %in% not_prose) {
      next
    }
    if (tag$tag == "param" && i == 1) {
      text <- sub("^[\\w.,`]+\\s*", "", text, perl = TRUE)
    }
    variety <- if (spelling == "us") "American" else "British"
    for (h in spelling_hits(text, spelling)) {
      msg <- sprintf(
        "'%s': use %s spelling (%s), or backtick it if it names code",
        h[[1]],
        variety,
        h[[2]]
      )
      hit(ln, 18, msg)
    }
  }
}

check_roxygen <- function(
  pkg,
  rules = c(1, 2, 3, 4, 10, 13, 18),
  spelling = NULL
) {
  spelling <- target_spelling(pkg, spelling)
  files <- sort(list.files(
    file.path(pkg, "R"),
    pattern = "\\.[Rr]$",
    full.names = TRUE
  ))
  if (length(files) == 0) {
    stop(sprintf("No R/*.R files under %s.", pkg), call. = FALSE)
  }

  out <- data.frame(
    file = character(),
    line = integer(),
    rule = integer(),
    msg = character()
  )
  topics <- list()

  for (f in files) {
    hit <- function(ln, rule, msg) {
      if (rule %in% rules) {
        out[nrow(out) + 1, ] <<- list(f, ln, rule, msg)
      }
    }
    blocks <- tryCatch(
      roxygen2::parse_file(f, env = NULL),
      error = function(e) {
        message(sprintf(
          "%s: skipped, roxygen2 can't parse it: %s",
          f,
          conditionMessage(e)
        ))
        list()
      }
    )
    for (block in blocks) {
      tags <- block$tags
      tag_names <- vapply(tags, `[[`, "", "tag")
      if ("noRd" %in% tag_names) {
        next
      }
      # A bare `@export` block (S3 method, re-export) creates no help topic.
      if (!any(c("title", "rdname", "describeIn", "name") %in% tag_names)) {
        next
      }
      value <- function(name) {
        if (name %in% tag_names) trimws(tags[[match(name, tag_names)]]$raw)
      }
      start <- min(vapply(tags, `[[`, 0, "line"))
      topic <- value("rdname") %||%
        value("name") %||%
        function_name(block$call) %||%
        paste0(f, ":", start)

      t <- topics[[topic]] %||%
        list(export = NULL, returns = FALSE, data = FALSE)
      if ("export" %in% tag_names && is.null(t$export)) {
        t$export <- list(file = f, line = start)
      }
      if (any(c("returns", "return", "inherit") %in% tag_names)) {
        t$returns <- TRUE
      }
      if (
        "format" %in%
          tag_names ||
          isTRUE(value("docType") %in% c("data", "package")) ||
          is.character(block$call)
      ) {
        t$data <- TRUE
      }
      topics[[topic]] <- t

      if ("title" %in% tag_names) {
        check_title(tags[[match("title", tag_names)]], hit)
      }
      for (tag in tags) {
        if (tag$tag == "param") {
          check_param(tag, hit)
        }
        check_lines(tag, spelling, hit)
      }
    }
  }

  for (name in names(topics)) {
    t <- topics[[name]]
    if (!is.null(t$export) && !t$returns && !t$data && 10 %in% rules) {
      out[nrow(out) + 1, ] <- list(
        t$export$file,
        t$export$line,
        10,
        sprintf("exported topic '%s' has no @returns", name)
      )
    }
  }

  out <- out[order(out$file, out$line), ]
  sprintf("%s:%d: rule %d: %s", out$file, out$line, out$rule, out$msg)
}

main <- function(args) {
  usage <- paste(
    "Usage: Rscript check_roxygen.R PKG_DIR",
    "[--rules 1,2,4,10] [--spelling us|gb]"
  )
  opt <- function(name) {
    i <- match(name, args)
    if (!is.na(i)) args[[i + 1]]
  }
  pkg <- args[
    !startsWith(args, "--") & !args %in% c(opt("--rules"), opt("--spelling"))
  ]
  if (length(pkg) != 1) {
    stop(usage, call. = FALSE)
  }
  rules <- as.integer(strsplit(opt("--rules") %||% "1,2,3,4,10,13,18", ",")[[
    1
  ]])
  spelling <- opt("--spelling")
  if (!is.null(spelling) && !spelling %in% c("us", "gb")) {
    stop("`--spelling` must be \"us\" or \"gb\".", call. = FALSE)
  }

  hits <- check_roxygen(pkg, rules, spelling)
  writeLines(hits)
  counts <- table(as.integer(sub(".*: rule (\\d+):.*", "\\1", hits)))
  summary <- paste0("rule ", names(counts), ": ", counts, collapse = ", ")
  message("\n", length(hits), " findings: ", summary)
}

if (sys.nframe() == 0L) {
  main(commandArgs(trailingOnly = TRUE))
}
