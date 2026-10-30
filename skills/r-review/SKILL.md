---
name: r-review
description: Review a change to an R package as a whole - code, roxygen documentation, and NEWS.md - in one report, inline or with one reviewer agent per aspect. Use when asked to review an R package PR, branch, diff, or commit, or to check a change is ready to merge or release. Coordinates r-code-style (code), roxygen-style (documentation prose), and r-news (NEWS.md); for a question about only one of those, use that skill directly.
---

# Review an R package change

One review of a change, drawing on three rule sets:

  | Aspect  | Skill                   | Agent                      | Rule prefix |
  | ------- | ----------------------- | -------------------------- | ----------- |
  | Code    | `r-style:r-code-style`  | `r-style:r-code-reviewer`  | `code:`     |
  | Roxygen | `r-style:roxygen-style` | `r-style:roxygen-reviewer` | `roxygen:`  |
  | NEWS    | `r-style:r-news`        | `r-style:news-reviewer`    | `news:`     |

The skills hold the rules; this skill decides which apply, runs them, and
merges the results. It reports and does not edit, unless the user asks for
fixes.

## 1. Get the change

- A branch: `git diff "$(git merge-base HEAD origin/HEAD)"...HEAD`, falling
  back to `main` or `master` when `origin/HEAD` is unset.
- A PR: `gh pr diff <number>`.
- Files or a pasted diff: use what the user gave.

Find the package root (the directory with `DESCRIPTION`) and note its
`Package:` name and `Version:`. Read the whole of each changed function, not
only the hunk, when the hunk alone can't show the problem.

## 2. Scope the aspects

  | The change touches                                  | Aspects            |
  | --------------------------------------------------- | ------------------ |
  | Code in `R/`                                        | code               |
  | `#'` lines, or adds or changes an exported function | roxygen            |
  | Anything a user can see, or `NEWS.md` itself        | NEWS               |
  | `tests/`                                            | code (rules 31-32) |
  | Only CI, `.Rbuildignore`, or internal refactors     | code only; no NEWS |

NEWS is in scope whenever behavior changes, even when `NEWS.md` is not in the
diff: a missing bullet is the most common NEWS finding.

## 3. Choose inline or agents

- **Inline** when one aspect is in scope, or the diff is under about 300
  changed lines. Call the Skill tool once for each in-scope skill (for
  example `r-style:r-news`) before you review, then review against it
  yourself. Don't review from memory or from the rule numbers quoted here;
  this skill names only a few of each skill's rules.
- **Agents** when two or more aspects are in scope and the diff is larger, or
  the user asks for it. Launch the in-scope reviewer agents in one message so
  they run in parallel. Give each the diff command or text, the package root,
  and the list of changed files. Each loads its own skill and reports only on
  its aspect.

Inline costs less; agents keep each rule set in a fresh context, so findings
on one aspect don't crowd out another on a large change. When unsure, go
inline.

## 4. Check across aspects

Do these yourself in either mode, because they need the whole change:

- **New export:** has roxygen with `@returns` (`roxygen:10`), a NEWS bullet
  (`news:1`), and a test file (`code:31`).
- **Changed behavior, argument, or default:** has a NEWS bullet (`news:1`);
  a breaking one is in `## Breaking changes` with the symptom and fix
  (`news:18`).
- **Deprecation:** uses `lifecycle` (`code:23`), the NEWS bullet names the
  replacement (`news:19`), and the version in `deprecate_*()` matches the
  NEWS heading it will ship under (`news:20`).
- **Removed export or argument:** flag it (`code:23`).

## 5. Merge and report

1. Drop duplicates. When two aspects report the same line and problem, keep
   the one with the more specific rule.
2. Rank: bugs and breaking API changes, then missing docs, NEWS bullets, or
   tests, then design (`code:14`-`23`), then wording and style.
3. Write each finding as `file:line: [prefix:N] message`, for example
   `R/fit.R:12: [code:25] Error says "should"; use "must" and name the type received.`
   The prefix matters: each skill numbers its rules from 1.
4. Open with a one-line verdict: ready to merge, or what blocks it. Then
   group the findings under **Must fix**, **Should fix**, and **Consider**.

Follow the skills' review limits: don't churn correct code or prose over
taste, and raise API rules (`code:14`-`23`) only for new or changed exports.
