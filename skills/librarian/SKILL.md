---
name: librarian
description: Tidy a Markdown knowledge base (an Obsidian vault or an LLM-maintained wiki). Runs a read-only report that finds slop (orphans, likely duplicates, thin or unsourced pages, stale active pages, log lines naming missing pages), fixes the mechanical things itself, and merges or archives only after a breakdown and the user's yes.
disable-model-invocation: true
allowed-tools: Bash, Read, Edit, Write, Grep, Glob
---

# Librarian

Keeps the compiled layer of a knowledge base clean, so its owner never has to wonder whether
it is filling with slop or whether a change the agent reported really happened. Good as a
step of a weekly review, or on `/librarian`.

The facts come from a read-only script; the judgement and the edits are this skill's.

**What it assumes.** A folder of Markdown pages that link with `[[wiki links]]` or
`[text](relative.md)`. When `<vault>/wiki/` exists, only that folder is read (the LLM Wiki
layout: `raw/` sources, `wiki/` compiled pages, `wiki/log.md` a dated change log). Otherwise
the whole vault is read. `.git`, `.obsidian`, `.trash`, `raw` and `_archive` are always
skipped. If the vault has a lint script of its own (see the `lint` skill), it runs too.

## Steps

1. **Measure.** From the vault root:

   ```bash
   python3 <skill folder>/librarian.py --vault .
   <lint command> --report                  # only if the vault has a lint script
   ```

   `librarian.py` options: `--stale N` (days before a `status: active` page counts as
   stale, default 28), `--thin N` (body words below which a page is thin, default 80),
   `--exclude <folder>` (repeatable), `--hubs <file name>` (pages never called orphans or
   unsourced; default `index.md`, `log.md`, `overview.md`), `--ignore-busy`. Codes: S1
   orphans, S2 likely duplicates, S3 thin or unsourced, S4 stale, L1 log lines naming a
   missing page, Busy. A lint script often exits non-zero whenever errors exist; that is
   its normal report. Note its error count: step 7 compares against it. Done when both
   reports are in hand with their counts.

2. **Leave busy files alone.** Every file under **Busy** (uncommitted in git) may belong to
   a session or a person still working. It gets no edit this run and is listed as
   "skipped: in use" in the report.

3. **Judge every finding.** Open each flagged page before calling it anything; a script
   count is a lead. Sort each finding into exactly one bucket:

   | Bucket | What goes in it |
   |---|---|
   | **Safe fix** | mechanical, reversible, one obvious answer (list below) |
   | **Merge** | two pages carry the same topic; one survives and takes the other's unique content |
   | **Archive** | nothing worth keeping that a live page does not already hold |
   | **Landed gap** | a promise that did not reach the files: a log line naming a page that is not there, a decision not marked decided where it was asked |
   | **Keep** | flagged but fine (a hub page with no inbound link by design, a deliberate stub). Say why in one line |
   | **Script wrong** | the script misread the page (a link it failed to parse, a false match). Report it as a script problem with the line that shows it; the page is not edited |

   Done when every finding sits in one bucket with a reason.

4. **Apply the safe fixes, then report them.** Only these count as safe:
   - regenerate the index with the vault's own command, if it has one;
   - repoint a broken link when exactly one live page is its target (a rename visible in
     `git log --follow`, or a single matching file name);
   - link an orphan from the one page its own frontmatter names as its parent (for example
     `project:`), as a bullet in that page's links section;
   - fill a log gap for a change you can point to in git (date, verb, the page);
   - add a missing index entry.

   Anything not on this list is not a safe fix.

5. **Break it down, then ask.** For every Merge, Archive and Landed gap that needs more than
   a safe fix, show a breakdown before touching a file, one block per item:

   ```
   ITEM <n>  Archive  wiki/<folder>/<page>.md
   Why:      <code and numbers, e.g. S1 orphan, links nowhere, last commit 40 days ago>
   Goes to:  wiki/_archive/<folder>/<page>.md
   Links:    <n> inbound to repoint (list them); <n> outbound lost
   Kept:     <what unique content moves where, or: nothing unique, covered by [[page]]>
   Undo:     git mv it back
   ```

   A Merge block also names the surviving page, the paragraphs or claims that move into it,
   and every link repointed to it. Then ask, up to four items at a time, with three options
   per item: do it, keep it, decide later. Apply only the items approved.

6. **Merge and archive by these rules.**
   - Merge first, archive the rest. Merged content keeps its citations and deep links; a
     line the owner marked as checked moves word for word, never rewritten.
   - Archive: `git mv` into `_archive/<same subfolder>/`, then set `status: deprecated`,
     add `archived: YYYY-MM-DD` and `archived_reason:` (one line). Before the move, repoint
     or remove every inbound link, as the breakdown listed.
   - Never delete a file. Never touch `raw/`, a confidential folder, or the owner's
     personal notes (a diary, an about-me folder).
   - Contradictions are recorded with a line naming both sides, never settled by picking one.

7. **Close the run.**
   - Regenerate the index and run the lint again, if the vault has them: the error count is
     not above step 1's baseline.
   - `librarian.py --ignore-busy` again (this run's own edits are uncommitted, so without
     the flag they would be skipped): the counts moved as the applied items say.
   - One **Lint** bullet in the change log under today's date: what changed, with counts per
     code (for example "S1 2 to 1, 1 archived").
   - Report: safe fixes applied, items approved and done, items kept, items waiting, busy
     files skipped, and what was checked and how.

## Limits

- The script never opens a folder it is told to skip; keep confidential material in one.
- Practice or scratch pages are never merged into reference pages.
- A finding the script gets wrong is reported as a script problem, never fixed by editing the
  page to silence it.

## Try it

```bash
python3 librarian.py --vault sample-vault --ignore-busy --stale 0
```

`sample-vault/` holds six invented pages that trigger every check once or twice.
