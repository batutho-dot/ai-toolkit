#!/usr/bin/env python3
"""lean-size.py: measure the instruction files Claude loads, for the /lean-claude skill.

    python3 lean-size.py                    # table for the current project
    python3 lean-size.py --project <dir>    # another project
    python3 lean-size.py --hook             # one warning line, only when a file grew >15 %
    python3 lean-size.py --set-baseline     # record today's sizes after a lean run

Files: ~/.claude/CLAUDE.md, <project>/CLAUDE.md, every <project>/.claude/rules/*.md (marked
"scoped" when its frontmatter has `paths:`, so it loads only in those folders) and the
project's memory index MEMORY.md. Tokens are estimated at 4 characters each, an estimate,
not a count. The baseline is per machine, in ~/.claude/lean-baseline.json, because the
global file and the memory folder live outside git. Set LEAN_BASELINE to keep it elsewhere.
The warning threshold is 15 % growth; change GROWTH to taste.
"""
import argparse
import datetime
import glob
import json
import os
import re
import subprocess
import sys

HOME = os.path.expanduser("~")
BASELINE = os.environ.get("LEAN_BASELINE") or os.path.join(HOME, ".claude", "lean-baseline.json")
GROWTH = 0.15


def files(project):
    project = os.path.abspath(project)
    out = [("global", os.path.join(HOME, ".claude", "CLAUDE.md"), True),
           ("project", os.path.join(project, "CLAUDE.md"), True)]
    for p in sorted(glob.glob(os.path.join(project, ".claude", "rules", "*.md"))):
        head = open(p, encoding="utf-8", errors="replace").read(400)
        scoped = head.startswith("---") and re.search(r"^paths:", head, re.M) is not None
        out.append(("rules/" + os.path.basename(p), p, not scoped))
    slug = re.sub(r"[^A-Za-z0-9]", "-", project)
    out.append(("memory", os.path.join(HOME, ".claude", "projects", slug, "memory", "MEMORY.md"), True))
    return [(k, p, always) for k, p, always in out if os.path.exists(p)]


def load_baseline():
    try:
        return json.load(open(BASELINE, encoding="utf-8"))
    except (OSError, ValueError):
        return {}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--project", default=None,
                    help="project root; default: the git root above the current folder")
    ap.add_argument("--hook", action="store_true")
    ap.add_argument("--set-baseline", action="store_true")
    a = ap.parse_args()
    sys.stdout.reconfigure(encoding="utf-8")
    if a.project is None:
        # a run from any subfolder must still measure the project, not the folder
        r = subprocess.run(["git", "rev-parse", "--show-toplevel"], capture_output=True, text=True)
        a.project = r.stdout.strip() if r.returncode == 0 and r.stdout.strip() else os.getcwd()
    if not os.path.exists(os.path.join(a.project, "CLAUDE.md")):
        print(f"lean-size: no CLAUDE.md in {a.project}; pass --project <root>", file=sys.stderr)
        if not a.hook:
            sys.exit(2)

    rows = [(k, p, always, len(open(p, encoding="utf-8", errors="replace").read()))
            for k, p, always in files(a.project)]
    key = os.path.abspath(a.project)
    base = load_baseline()
    mine = base.get(key, {})

    if a.set_baseline:
        base[key] = {k: n for k, _, _, n in rows}
        base[key]["_date"] = str(datetime.date.today())
        json.dump(base, open(BASELINE, "w", encoding="utf-8"), indent=1)
        print(f"Baseline set for {key}: " + ", ".join(f"{k} {n}" for k, _, _, n in rows))
        return

    if a.hook:
        grown = [f"{k} {mine[k]} to {n} chars (+{(n - mine[k]) / mine[k]:.0%})"
                 for k, _, always, n in rows if always and mine.get(k) and n > mine[k] * (1 + GROWTH)]
        if grown:
            print(f"  Lean: instruction files grew past the {mine.get('_date')} baseline: "
                  + "; ".join(grown) + ". Offer /lean-claude.")
        return

    total = sum(n for _, _, always, n in rows if always)
    print(f"| File | Loads | Chars | ~Tokens | Baseline {mine.get('_date', 'none')} |")
    print("|---|---|---|---|---|")
    for k, p, always, n in rows:
        b = mine.get(k)
        bs = f"{b} ({(n - b) / b:+.0%})" if b else "none"
        print(f"| {k} | {'always' if always else 'scoped'} | {n} | {n // 4} | {bs} |")
    print(f"\nAlways loaded: {total} chars, about {total // 4} tokens (estimate, 4 chars per token).")


if __name__ == "__main__":
    main()
