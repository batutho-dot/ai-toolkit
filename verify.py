#!/usr/bin/env python3
"""verify.py: check the skills in skills/ end to end. Prints PASS or FAIL from real runs.

    python verify.py    # checks need no external software

Steps: every SKILL.md has frontmatter whose name matches its folder and a description;
every Python script compiles; each script runs on its sample
input and its output is compared with what the sample is built to produce; no text file
holds an em dash. Writes nothing inside the repository.
"""
import glob
import os
import re
import shutil
import subprocess
import sys
import tempfile

ROOT = os.path.dirname(os.path.abspath(__file__))
SKILLS = os.path.join(ROOT, "skills")
PY = sys.executable
EMDASH = chr(0x2014)


class Fail(Exception):
    pass


def run(cmd, env=None, cwd=SKILLS):
    r = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8",
                       errors="replace", env=env, cwd=cwd)
    return r.returncode, r.stdout + r.stderr


def step_frontmatter():
    skills = sorted(glob.glob(os.path.join(SKILLS, "*", "SKILL.md")))
    if not skills:
        raise Fail("no SKILL.md found")
    for p in skills:
        text = open(p, encoding="utf-8").read()
        m = re.match(r"---\n(.*?)\n---\n", text, re.S)
        if not m:
            raise Fail(f"{p}: no frontmatter")
        name = re.search(r"^name:\s*(\S+)", m.group(1), re.M)
        if not name or name.group(1) != os.path.basename(os.path.dirname(p)):
            raise Fail(f"{p}: name does not match folder")
        if not re.search(r"^description:\s*\S", m.group(1), re.M):
            raise Fail(f"{p}: no description")
    return f"{len(skills)} skills"


def step_compile():
    files = glob.glob(os.path.join(ROOT, "**", "*.py"), recursive=True)
    for f in files:
        code, out = run([PY, "-m", "py_compile", f])
        if code:
            raise Fail(out.strip())
    # py_compile writes __pycache__; remove it so the tree stays as it was
    for d in glob.glob(os.path.join(ROOT, "**", "__pycache__"), recursive=True):
        shutil.rmtree(d, ignore_errors=True)
    return f"{len(files)} files"


def step_librarian():
    code, out = run([PY, "librarian/librarian.py", "--vault", "librarian/sample-vault",
                     "--ignore-busy", "--stale", "0"])
    if code:
        raise Fail(out.strip())
    want = {"| S1 | orphans | 2 |", "| S2 | likely duplicates | 1 |", "| S3 | thin pages | 2 |",
            "| S3 | no link and no citation | 2 |", "| S4 | active, untouched 0+ days | 2 |",
            "| L1 | log lines naming a missing page | 1 |", "- log.md:3 [[solar-thermal]]",
            "- concepts/heat-pump.md <> concepts/heat-pumps.md"}
    missing = [w for w in want if w not in out]
    if missing:
        raise Fail("missing lines: " + "; ".join(missing))
    return "sample vault counts match"


def step_lean():
    tmp = tempfile.mkdtemp()
    try:
        home = os.path.join(SKILLS, "lean-claude", "sample", "home")
        env = dict(os.environ, HOME=home, USERPROFILE=home,
                   LEAN_BASELINE=os.path.join(tmp, "baseline.json"))
        proj = os.path.join("lean-claude", "sample", "project")
        code, out = run([PY, "lean-claude/lean-size.py", "--project", proj], env=env)
        if code or "| rules/docs-only.md | scoped |" not in out or "| global | always |" not in out:
            raise Fail("table wrong: " + out.strip())
        code, out = run([PY, "lean-claude/lean-size.py", "--project", proj, "--set-baseline"], env=env)
        if code or "Baseline set" not in out:
            raise Fail("baseline: " + out.strip())
        code, out = run([PY, "lean-claude/lean-size.py", "--project", proj, "--hook"], env=env)
        if code or out.strip():
            raise Fail("hook warned with no growth: " + out.strip())
        # grow a copy of the project past 15 percent and expect one warning line
        grown = os.path.join(tmp, "project")
        shutil.copytree(os.path.join(SKILLS, proj), grown)
        env2 = dict(env, LEAN_BASELINE=os.path.join(tmp, "baseline2.json"))
        run([PY, "lean-claude/lean-size.py", "--project", grown, "--set-baseline"], env=env2)
        with open(os.path.join(grown, "CLAUDE.md"), "a", encoding="utf-8") as f:
            f.write("- an added rule long enough to grow this small file past fifteen percent.\n")
        code, out = run([PY, "lean-claude/lean-size.py", "--project", grown, "--hook"], env=env2)
        if "Lean:" not in out or "project" not in out:
            raise Fail("hook did not warn on growth: " + out.strip())
        code, out = run([PY, "lean-claude/lean-size.py", "--project", os.path.join(tmp, "none")], env=env)
        if code != 2:
            raise Fail(f"no CLAUDE.md should exit 2, got {code}")
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    return "table, baseline, hook quiet, hook warns, exit 2"


def step_emdash():
    hits = []
    for p in glob.glob(os.path.join(ROOT, "**", "*"), recursive=True):
        if ".git" in p.split(os.sep) or not os.path.isfile(p):
            continue
        try:
            text = open(p, encoding="utf-8").read()
        except (UnicodeDecodeError, OSError):
            continue
        for n, line in enumerate(text.splitlines(), 1):
            if EMDASH in line:
                hits.append(f"{os.path.relpath(p, ROOT)}:{n}")
    if hits:
        raise Fail("em dash at " + ", ".join(hits))
    return "none"


def main():
    print(f"verify-repo: {ROOT}")
    steps = [("frontmatter", step_frontmatter), ("compile", step_compile),
             ("librarian", step_librarian), ("lean-size", step_lean),
             ("em dashes", step_emdash)]
    for name, fn in steps:
        try:
            print(f"{name}: {fn()}")
        except Fail as e:
            reason = " | ".join(x.strip() for x in str(e).splitlines() if x.strip())
            print(f"verify: FAIL at {name}: {reason}")  # one line, always last
            return 1
    print("verify: PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
