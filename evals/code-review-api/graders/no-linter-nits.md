---
type: llm
weight: 1
---

The response does not raise pure formatting nits that air, styler, or lintr
already handle: indentation or spacing, line length, `<-` versus `=`, or
snake_case versus camelCase casing. These are NOT formatting nits and are
fine to raise: dots in function names, putting `return()`/`stop()`/`message()`
on their own braced line, `&` versus `&&`, unnecessary `return()`, and
comment content. Pass if none of the listed formatting nits appear.
