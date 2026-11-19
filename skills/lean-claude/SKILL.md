---
name: lean-claude
description: Make the always-loaded instruction files (global and project CLAUDE.md, .claude/rules, the memory index) leaner without losing a rule. Moves task-specific rules to where they load only when needed, then trims; proves every rule still has a home with a rule map and test prompts.
disable-model-invocation: true
allowed-tools: Bash, Read, Edit, Write, Grep, Glob, Agent, AskUserQuestion
---

# Lean CLAUDE

Every always-loaded line costs tokens and attention on every turn. This skill shrinks that
cost while keeping each rule reachable. Run it once a month, when `lean-size.py --hook`
prints a **Lean:** warning at session start, or on `/lean-claude`.

The **rule map** is the spine of a run: one line per rule, before and after. A run is done
only when every line of the map points to a real file and line.

## Steps

1. **Measure and back up.** From the project root (the script also finds the git root
   itself, and exits 2 when there is no `CLAUDE.md` there):

   ```bash
   python3 ~/.claude/skills/lean-claude/lean-size.py --project "<project root>"
   ```

   Copy every file in its table, as it is, into `~/.claude/lean-runs/YYYY-MM-DD/before/`.
   Done when the backups exist and the table names the global file, the project file, the
   rules files and the memory index.

2. **Build the rule map.** Write `~/.claude/lean-runs/YYYY-MM-DD/rule-map.md`: one row per
   rule, ID (`G-` global, `P-` project, `R-` rules file, `M-` memory, numbered), file:line
   range, the rule in under 15 words, a bucket, and an empty **After** column. A rule is any
   sentence that changes what the agent does; context and explanation ride with their rule.
   Done when every non-blank line of every file sits inside some row's range.

   | Bucket | Test | Action |
   |---|---|---|
   | **Keep** | needed in most sessions of the projects that load it | stays; trim wording |
   | **Move** | only one kind of task needs it (decks, one tool, one domain, voice, code review) | into an existing skill or a `paths:`-scoped rules file, leaving a one-line pointer whose leading word is the task's trigger. A new skill only with one parked in the same block: the skill listing has a size limit, and past it skills drop out and stop triggering |
   | **Hook** | a hook enforces it **on every machine that loads the file** | cut to the one pointer line the hook needs. A global file shared by two machines needs the hook on both |
   | **Duplicate** | the same meaning in two files | a rule that applies in every project stays in the global file and the project copy goes; a rule for one project stays in that project's file |
   | **Conflict** | two files say different things (a number, a level, a yes and a no) | never resolved by the skill: the block shows both lines and the user says which is true |
   | **Stale** | names a hook, skill, path or tool not present on this machine | ask; it may exist on another machine. Never cut silently |
   | **No-op** | the model does it by default | cut the whole sentence |

3. **Apply the safe trims alone.** Only two kinds:
   - an **exact duplicate**: the same sentence, word for word after whitespace, in two
     files; the copy the Duplicate rule says goes, goes;
   - a **wording trim** inside a Keep rule that leaves every number, name, file path and
     condition in place.
   Note each in the map. Anything else, including a duplicate in different words, is step 4.

4. **Break down the rest, then ask.** Order the blocks by saving, largest first; group rules
   that move to the same place into one block; drop single items under 100 characters
   unless they are Conflict or Stale. One block per item:

   ```
   <ID>  <Bucket>  <file>:<lines> "<first words of the rule>"
   Why:      <the test it meets, with numbers: lines, chars, ~tokens every turn>
   Goes to:  <new home>; pointer left: "<pointer line>"   (or: cut, because ...)
   Refs:     <every file that names the moved path, from grep, and how each is updated>
   Undo:     restore from ~/.claude/lean-runs/YYYY-MM-DD/before/
   ```

   Then ask, up to four blocks at a time: do it, keep it, decide later. Apply only what is
   approved. A move into a folder the user keeps for themselves is their call: the block
   says so.

5. **Hold these lines.**
   - Safety rules (never invent a value, confidential data stays local, ask before a
     decision that is the user's, the end-of-task report) stay in the always-loaded files in
     full meaning. Wording trims only, never Hook or Move.
   - If the global file has a master copy elsewhere (a synced folder, a dotfiles repo), edit
     the master and copy it over, and note that other machines need the same copy.
   - After a move, `grep` the old path across the project and `~/.claude` and update every
     reference the block listed.
   - Memory: merge duplicate memories into one file, fix the index line, delete only the
     duplicate memory file, after opening both.

6. **Verify.**
   - Fill the **After** column: every rule ID maps to the file:line where it now lives, or
     "cut: no-op" / "cut: duplicate of <ID>" / "cut: hook <name>". Open each target and
     confirm the line is there. Zero rows without an After entry.
   - Test prompts: give a fresh subagent on a capable model only the new files' paths and
     five to eight scenarios built from the moved and cut rules (for example "make a slide
     deck for the review", "commit this CSV of client prices", "what is the carbon footprint
     of material X"). It answers, per scenario, which rule applies and where it found it.
     Pass: every answer finds the right rule at its new home. A miss sharpens the pointer
     wording and reruns that scenario.
   - Run `lean-size.py --project "<project root>"` again, then the same with
     `--set-baseline`, so the start-of-session warning measures from here.

7. **Report.** A short results note: before and after sizes per file (chars, estimated
   tokens), rules moved, cut, kept, waiting, conflicts and stale flags with the user's
   answers, and the test-prompt results, with what was checked and how.

## Files in the skill folder

- `lean-size.py`: the measure. `--hook` prints one warning line at 15 percent growth (wire
  it into a SessionStart hook), `--set-baseline` records sizes per machine in
  `~/.claude/lean-baseline.json` (or the file in `LEAN_BASELINE`).
- `sample/`: an invented home folder and project to try it on:

  ```bash
  HOME=sample/home USERPROFILE=sample/home LEAN_BASELINE=sample/baseline.json \
    python3 lean-size.py --project sample/project
  ```
