# lean-claude

Shrinks the always-loaded instruction files without losing a rule, with a rule map and test prompts as proof.

- **Starts:** You type `/lean-claude`.
- **Files:** `SKILL.md`, `lean-size.py`, a sample project

## Get it

This skill has a script, so it needs its whole folder. This downloads only that folder, not
the rest of the repo:

```bash
git clone --depth 1 --filter=blob:none --sparse https://github.com/batutho-dot/ai-toolkit
```

```bash
cd ai-toolkit && git sparse-checkout set skills/lean-claude && cp -r skills/lean-claude ~/.claude/skills/
```

For one project only, use `<project>/.claude/skills/` instead of `~/.claude/skills/`.
Restart Claude Code and type `/` to see the skill listed.
The script needs Python 3.9 or newer and nothing else. Try it on `sample/` first.

All skills, and how I make them: [../README.md](../README.md).
