---
name: create-verify
description: Write, or repair, the verify script for a code repository, so the agent checks its own changes there and reports PASS or FAIL from a real run instead of from belief. Use when a repository has no verify script, when the user asks to "set up verify", "make it checkable" or "add a verification step", or when an existing verify script no longer catches a break.
---

# Create a verify script

Every code repository gets one `verify` entry point, so the agent checks its own work and
the person is not the checker. A hook can then stop a reply when code changed after the last
`verify: PASS`. This skill writes the script
that answers it.

## The contract (a hook can rely on it)

- One file at the repository root: `verify.py` (preferred; it runs on Windows, macOS and
  Linux alike), `verify.sh` or `verify.ps1`.
- It prints `verify-repo: <absolute repository root>` first, then one line per step, and
  last exactly `verify: PASS` or `verify: FAIL at <step>: <reason>`.
- Exit code 0 on PASS, 1 on FAIL. It stops at the first failing step.
- It changes nothing in the repository: scratch output goes to a temporary folder.
- It is fast enough to run after every change. A slow, full check (a benchmark run) is a
  separate step behind a flag such as `--full`, named in the script's help.

## Steps

1. **Read before writing.** Find how the project is really checked: its test runner
   (pytest, npm test, cargo test), linter or type checker, build, and how the program is
   started. Read the README, the CI file, `package.json` or `pyproject.toml`, and how recent
   sessions ran it. Do not invent a check the project does not have; a step that cannot run
   here is left out and named in the report.
2. **Write a feature map** (adapted from pstack's `create-verification-skill`, MIT
   licence; see the repository README). A folder `verify-features/` at the root: a
   `README.md` index and one short file per feature, starting with the three to five that matter most, found from
   the commands, entry points, notebooks or docs. Each file says what the feature does for
   its user, how to reach it, how `verify` drives it (the command and a small fixed input),
   the observable end state that proves it worked, and its gotchas. No placeholders: a
   section with nothing found says so. Step 3's real run is chosen from this map, and a
   check that drives only one entry point of a feature that has several is incomplete. A
   journey that fails for a missing precondition gets the reason in its gotchas; it is never
   weakened to pass. When a change adds or alters a feature, its file changes in the same
   commit.
3. **Pick the steps**, cheapest first: syntax or compile check of the changed language, the
   linter, the tests, then one real run of the program on a small fixed input with its
   output compared to a known-good copy. The real run is what makes it verification, not
   just tests. If there is no known-good output yet, say so and propose one; do not
   fabricate it.
4. **Write the script** to the contract. Known, accepted failures (for example tests that
   fail only on one operating system) go in a named list the script reads, with a reason
   each, and the script fails if any other test fails or a listed one starts passing.
5. **Prove it catches a break.** In a scratch copy (a temporary clone or worktree, never the
   working tree), break one thing on purpose (a failing assertion, a syntax error) and check
   that `verify` says FAIL at the right step. Then run it on the real tree and check PASS.
   Paste both result lines.
6. **Report** in plain words: what each step checks, what it cannot catch, how long it
   takes, and the two result lines. For code the user is accountable for at work, explain
   the plan first and wait for their yes before the script is added.

## Never

- Weaken a check so verify passes. If the real tree fails, report FAIL and why.
- Print PASS from anything but the steps having run.
- Send confidential code to a subagent while doing this.

## Example

This collection's own `verify.py`, at the repository root, follows the contract: it
compiles every script, checks the shell script parses, runs each script on its sample input
and compares the result with what is expected.
