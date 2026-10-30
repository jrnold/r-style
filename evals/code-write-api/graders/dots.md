---
type: llm
weight: 1
---

The function forwards `...` to the user's function, and its own named
arguments are dot-prefixed (e.g. `.data`, `.by` or `.group`, `.f`) so they
can't collide with the user's extra arguments. Pass also if the arguments are
not dot-prefixed but `...` is placed and handled so collisions are
impossible and the response explains this.
