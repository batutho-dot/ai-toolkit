# librarian

Tidies a Markdown vault: orphans, likely duplicates, thin or unsourced pages, stale pages. Safe fixes alone, merges only after a yes.

- **Starts:** You type `/librarian`.
- **Files:** `SKILL.md`, `librarian.py`, a sample vault

## Get it

This skill has a script, so it needs its whole folder. This downloads only that folder, not
the rest of the repo:

```bash
git clone --depth 1 --filter=blob:none --sparse https://github.com/batutho-dot/ai-toolkit
```

```bash
cd ai-toolkit && git sparse-checkout set skills/librarian && cp -r skills/librarian ~/.claude/skills/
```

For one project only, use `<project>/.claude/skills/` instead of `~/.claude/skills/`.
Restart Claude Code and type `/` to see the skill listed.
The script needs Python 3.9 or newer and nothing else. Try it on `sample-vault/` first.

All skills, and how I make them: [../README.md](../README.md).
