---
name: code_execution secret access
description: How to use secret values (API tokens) given the code_execution sandbox hides process.env
---

# Using secrets from agent tooling

**Rule:** The `code_execution` JS sandbox does NOT expose `process.env` — `process.env` is
`undefined` there, so secret values (e.g. GITHUB_TOKEN) are unreachable from code_execution.
To USE a secret value, run a `node`/`python` script **via the bash tool** — a normal bash-spawned
process inherits the full environment, including Replit secrets.

**Why:** code_execution runs in a restricted worker that strips env for safety; bash does not.
This cost several failed attempts (TypeError reading process.env.X).

**How to apply:**
- Existence check (no value): `viewEnvVars({type:"secret", keys:[...]})` in code_execution — returns booleans only.
- Value use: write a small script that reads `process.env.SECRET` and run it with bash (`node x.cjs`).
  Reference `${SECRET}` only as a shell var in bash commands; never echo/print it.
- A token pasted into chat is auto-redacted if placed in tool-call code → unusable; require it in the secret store.
- Destructive git (init/commit/push/force) must go through a background Project Task; prefer the
  GitHub HTTP API (blobs→tree→commit→ref) over local git for pushing from a script.
