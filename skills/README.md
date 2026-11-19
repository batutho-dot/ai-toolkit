# Skills

One folder per skill. Take the one you want; none depends on another.

| Skill | What it does | Starts | Files |
|---|---|---|---|
| [code-map](code-map/) | Draws a program's steps as a Mermaid diagram, with a table tying every box to `file:line` | By itself, on "show me the code" | `SKILL.md` |
| [create-verify](create-verify/) | Writes a repo's `verify` script to a fixed contract, so the agent reports PASS or FAIL from a real run | By itself, or on request | `SKILL.md` |
| [lint](lint/) | Runs a Markdown wiki's lint script, groups the findings, proposes fixes and applies only the approved ones | By itself, or `/lint` | `SKILL.md` |
| [librarian](librarian/) | Tidies a Markdown vault: orphans, likely duplicates, thin or unsourced pages, stale pages. Safe fixes alone, merges only after a yes | You type `/librarian` | `SKILL.md`, `librarian.py`, a sample vault |
| [lean-claude](lean-claude/) | Shrinks the always-loaded instruction files without losing a rule, with a rule map and test prompts as proof | You type `/lean-claude` | `SKILL.md`, `lean-size.py`, a sample project |

## Get one skill

A skill that is a single file (code-map, create-verify, lint): open its `SKILL.md` here and
press "Download raw file", or fetch it straight into your skills folder:

```bash
curl --create-dirs -o ~/.claude/skills/code-map/SKILL.md https://raw.githubusercontent.com/batutho-dot/ai-toolkit/main/skills/code-map/SKILL.md
```

A skill with a script (librarian, lean-claude) needs its whole folder. This downloads only
that folder, not the rest of the repo:

```bash
git clone --depth 1 --filter=blob:none --sparse https://github.com/batutho-dot/ai-toolkit
```

```bash
cd ai-toolkit && git sparse-checkout set skills/librarian && cp -r skills/librarian ~/.claude/skills/
```

For one project only, use `<project>/.claude/skills/` instead of `~/.claude/skills/`.
Restart Claude Code and type `/` to see the skill listed. The scripts need Python 3.9 or
newer and nothing else.

## Check them

```bash
python verify.py
```

Run from the repo root. It checks every skill's header, compiles the scripts and runs each
script on its sample, ending in `verify: PASS` or `verify: FAIL at <step>`.

How I make a skill, and which others I use and credit: [../docs/skills.md](../docs/skills.md).
