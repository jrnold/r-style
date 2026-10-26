---
name: r-news
description: Rules for writing and reviewing NEWS.md in R packages - what earns a bullet, heading structure that pkgdown and R can parse, bullet wording and phrasing patterns from recent tidyverse NEWS, ordering, attribution, breaking changes, deprecations, and release polishing. Use when adding or editing a NEWS.md entry, preparing a release, reviewing a diff for a missing or poorly written NEWS bullet, or asked about R changelog conventions. Complements r-lib:r-package-development (workflow) and r-lib:lifecycle (deprecation).
---

# NEWS.md for R packages

No linter checks NEWS, so all of this is review work. Sources: the
[tidyverse style guide](https://style.tidyverse.org/news.html),
[R Packages](https://r-pkgs.org/other-markdown.html),
[pkgdown](https://pkgdown.r-lib.org/reference/build_news.html), and the
`r-lib:r-package-development` skill. The style guide is the standard: apply
it to new and edited bullets even when the existing file or other packages do
otherwise. Only an explicit, documented project rule (e.g. in CLAUDE.md)
overrides it. Don't rewrite old release sections to conform.

Rules state the ideal. An audit of 12 tidyverse and r-lib packages
(`references/evidence.md`) shows practice often falls short of it, so a package
that departs from a rule is not evidence the rule is wrong. The percentages
below show how far practice lags; use them to decide how hard to push in a
review, not whether the rule stands. Rules 1-3, 16-18, 22 matter most.

NEWS is for people who *use* the package. It is not a commit log; commit
messages are the developer-facing record.

## What gets a bullet

1. **Every user-facing change**: new or changed functions, arguments,
   defaults, output, messages users act on, bug fixes, deprecations, dropped
   support for an R or dependency version.
2. **No bullet** for internal refactors, test-only changes, CI, or small
   documentation fixes. A large documentation addition (new article, new
   examples users will look for) can have one.
3. **Add the bullet in the same change** that makes the behavior change, so
   review sees both together.

## Structure

4. **Newest release first.** In development the top heading is
   `# pkg (development version)`; a release heading is `# pkg 1.2.0`.
5. **Version headings are level 1** (`#`). pkgdown also accepts level 2, but
   use level 2 only for sections within a release. A version heading must
   match `pkg 1.2.0`, `Version 1.2.0`, or `Changes in 1.2.0`, or pkgdown
   cannot find the release. Don't put a date in the heading; pkgdown adds
   CRAN release dates itself. (0 of 107 audited headings has one.)
6. **Sections within a release are optional** and go in this order when
   used: `## Breaking changes`, `## New features`, `## Minor improvements and
   fixes`. Skip sections for a short release (73% of audited sections have
   none). Keep the literal word "breaking" in the heading: release tooling
   keys on it to suggest a major version. Use the project's existing names
   rather than inventing variants (the corpus has six spellings of the third).
7. **One bullet marker and one blank-line convention throughout the file.**
   `*` is the tidyverse's marker (97%), and `usethis::use_news_md()` writes
   it; most packages (9 of 12) separate bullets with a blank line.

## Wording

8. **Put the function name first or early** so readers can scan:
   `` `geom_segment()` gains a `linejoin` argument. ``
9. **Present tense, positive framing: say what now happens.**
   Good: `` `ggsave()` now uses full argument names to avoid partial match
   warnings. `` Poor: `` Fixed partial argument matches in `ggsave()`. ``
   This is the target even though only about 41% of audited bullets say
   "now" and some 9% still lead with "Fixed ...". Write new bullets this
   way even if the file's older bullets use another voice.
10. **Say what the user sees, not what the code did.** Name the symptom for
    a fix ("fails with 'object `i` not found' for `n = 0`; it now returns
    `character(0)`"), not the internal cause.
11. **Backtick functions (with parentheses), arguments, objects, and file
    names.** Package names are not code-formatted.
12. **One sentence for a simple fix or small change.** A complex feature may
    take several sentences and a fenced code example. If a bullet needs more
    than a short paragraph, the explanation belongs in a vignette; link it.
13. **Every bullet ends with a period.** Put references before it:
    `` ... (#123). `` or `` ... (@user, #123). `` Never after: not
    `` ... . (#123) ``.
14. **Credit external contributors with `@username`, and cite the issue or PR
    number** when there is one (81% of audited bullets do). Whether to credit
    the maintainers' own work varies by project (0% to 71% of bullets by
    package), so follow the project and don't flag it. References are linked
    automatically by GitHub and pkgdown when the repository is in DESCRIPTION.
15. **Consistent spelling variety** with the rest of the package prose (see
    `roxygen-style` rule 18). Avoid "we" (2% of audited bullets use it); name
    the package or the function as the subject.

Templates (from the tidyverse guide):

- New function: `` New `stat_qq_line()` makes it easy to add a simple line to
  a Q-Q plot. ``
- New argument: `` `geom_segment()` gains a `linejoin` argument. ``
- Behavior change: `` `reduce()` now throws an error if `.x` is empty and
  `.init` is not supplied. ``
- Argument change: `` In `separate()`, `col = -1` now refers to the far right
  position. Previously, and incorrectly, `col = -2` did. ``

## Ordering and wrapping

16. **During development, add new bullets at the top** of the development
    section, one bullet per change (a long bullet may stay on one line).
17. **Before release, tidy the section:** group into the sections above, put
    bullets that name no function first, then order the rest alphabetically
    by the first function mentioned, and wrap at 80 characters. This is the
    style guide's and Posit's stated order. Practice lags: 4 of 37 audited
    sections are fully sorted (adjacent pairs 67% in order), 83% of bullets
    have no line over 80. Do it when polishing the section being
    released.

## Breaking changes, deprecations, and removals

18. **A breaking change gets a bullet in `## Breaking changes`**, stating
    the **symptom** a user will see and the **fix** they need to make. Don't
    use a "BREAKING CHANGE:" prefix instead; the audited corpus has it in 2 of
    1,048 bullets, and the guide specifies a section.
19. **A deprecation says what to use instead** and names the function or
    argument: `` `old()` is deprecated in favor of `new()`. `` Only 21 of 64
    audited deprecation bullets name the replacement; that is a gap, and the
    reader is the one who pays for it. Use "soft-deprecated", "deprecated" and
    "defunct" to match the `lifecycle` stage.
20. **The release named in the NEWS bullet matches the `when` of
    `lifecycle::deprecate_*()`** and the version in DESCRIPTION after release,
    so a user can find the warning's version under a NEWS heading
    (`r-lib:lifecycle`).
21. **Never describe a removal that hasn't happened**, and never promise a
    future removal in the same release that announces the deprecation.

## Release checks

22. Before release: no `(development version)` heading left (replace it with
    the release version, e.g. with `usethis::use_version()`), the top version
    matches DESCRIPTION, every user-facing change since the last tag has a
    bullet, and nothing in the section is a draft, a TODO, or an internal
    note.
23. Smoke-test the file parses as releases:
    `Rscript -e 'tools:::.build_news_db_from_package_NEWS_md("NEWS.md")'`
    (internal function; it lists one row per release heading and ignores the
    development heading). After building the site, check pkgdown's News page.
24. CRAN doesn't require a NEWS file, but it links NEWS.md from the package
    page. Explanations of how you addressed a reviewer's comments belong in
    the submission form's comment field, not NEWS.

## Patterns from recent NEWS (supplementary)

Rules 1-24 are the style guide. These add concrete phrasing used in the newest
NEWS of the audited packages (the development section plus latest release,
197 bullets). They fit inside the guide and do not replace it; use them to
pick wording, not to override a rule above. Counts are small, so they are
conventions to prefer, not requirements.

25. **Lead by change type.** New function: ``New `f()` ...``. New argument:
    ``f() gains a `x` argument ...``. Behavior: ``f() now ...``,
    ``f() no longer ...``, ``f() is now ...``. Of the 197 bullets, 21 start
    "New `...`", 19 "`f()` now", 8 "`f()` no longer", 7 "`f()` gains".
26. **Pair "no longer" with a symptom for fixes.** ``f() no longer errors when
    the plot has multiple panels.`` keeps a fix in present tense and names what
    the user saw, which "Fixed an error ..." does not.
27. **Name the new argument value or default in parentheses** when it helps:
    ``f() gains a `quantile.type` parameter (default `7`) ...``, and say how to
    get the old behavior: ``set `quantile.type = 2` to match ...``.
28. **Add one clause of purpose**, after the change, when it isn't obvious:
    "to control axis drawing order", "allowing users to ...", "so you can ...",
    "for clarity", "in line with ...", "to match existing ...".
29. **Use `fn(arg)` shorthand** for an argument, aesthetic, or theme element
    that belongs to a function: `` `theme(strip.placement.x)` ``,
    `` `position_dodge2(group.row)` ``. Use `pkg::fn()` for functions from
    another package, and `fn_*()`-style wildcards for a family.
30. **Several functions, one change: join them.** ``f() and g() now ...``;
    ``f()/g() gain ...``. Don't repeat one bullet per function when the text
    would be identical.
31. **Package-wide changes use the package name as plain text**, not code:
    "dplyr is now fully compliant with the R C API (#7819).", "The base pipe is
    now used throughout the documentation (#7711)."
32. **Deprecations and removals carry the history.** For a list of removed
    functions, use ``f(). Deprecated in 1.0.0 (May 2020), use `pkg::g()`
    instead.`` For a single one, ``f() is deprecated in favor of g()`` or
    ``f() is soft-deprecated``. Use the lifecycle stage word that is true:
    *soft-deprecated*, *deprecated*, *defunct*, *superseded*
    (``label_dollar() has been superseded by label_currency()``).
33. **A minimum R version change is its own bullet**, states the new version,
    and gives the policy as the reason with a link: "R >=4.1.0 is now required,
    in line with the [tidyverse standard](...) of supporting the previous 5
    minor releases of R (#7711)."
34. **Inline examples start "For example," and use backticked code**; a longer
    one uses a fenced block (5 of 197). A multi-part behavior can carry an
    indented bullet sub-list after an introducing colon or "In particular:".
35. **For performance, give the cause:** "significantly faster and use much
    less memory due to a rewrite in C via vctrs (#7723)."
36. **Reference order is user, then issue**: ``(@user, #123)``, 49 against 17
    for the reverse in the recent bullets. Several issues:
    ``(#7723, #7725, #7727)``. An issue in another repository:
    ``(r-lib/vctrs#1935)``.
37. **Say when something is new to the docs, not the code:** "These have
    existed for some time but were not previously documented."
38. **Mark a bullet for extension authors** only when downstream code is
    affected, e.g. ggplot2's ``(internal)`` prefix. A change that affects no
    one outside the package gets no bullet (rule 2).

Seen in the newest NEWS but not adopted, because the guide says otherwise: no
final period or a period after the reference (17% of bullets end with no
period), "Fixed ..." / "Added ..." leads, and `(internal)` bullets for
test-only changes.

## Using this in a review

Report as `file:line: rule N: message`. Typical findings: a user-facing diff
with no bullet (1, 3); a bullet that describes implementation (10); past-tense
"Fixed ..." where the file uses "now ..." (9); a breaking change with no symptom
or fix (18); a deprecation whose version does not match NEWS (20). Don't
reformat old release sections to fit these rules; edit only the section being
worked on.
