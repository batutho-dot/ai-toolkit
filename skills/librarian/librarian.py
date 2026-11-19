#!/usr/bin/env python3
"""librarian.py: the fact-finding half of the librarian skill. Read-only; it changes nothing.

    python3 librarian.py --vault <folder>              # report on a Markdown vault
    python3 librarian.py --vault <folder> --stale 60   # stale after 60 days instead of 28
    python3 librarian.py --vault <folder> --ignore-busy

Works on any folder of Markdown pages with [[wiki links]] or [text](relative.md) links,
such as an Obsidian vault. Pages are read from <vault>/wiki/ when it exists, else from the
whole vault. Prints a Markdown report; every finding is a lead to judge, not a verdict:

  S1  orphans: no other page links to it (worst first when it also links nowhere)
  S2  likely duplicates: very similar titles
  S3  thin pages (under --thin words of body text) and pages with no link and no citation
  S4  stale: pages with `status: active` in their frontmatter, untouched for --stale days
  L1  log lines that name a page that does not exist (when <vault>/wiki/log.md exists)
  Busy  files with uncommitted changes in git: another session may be working on them

Folders skipped: .git, .obsidian, .trash, raw, _archive, and any given with --exclude.
"""
import argparse
import datetime
import difflib
import os
import re
import subprocess
import sys

SKIP = {".git", ".obsidian", ".trash", "raw", "_archive", "node_modules"}
WIKILINK = re.compile(r"\[\[([^\]|#]+)(?:#[^\]|]*)?(?:\|[^\]]*)?\]\]")
MDLINK = re.compile(r"\]\(([^)#\s]+\.md)(?:#[^)]*)?\)")
CITATION = re.compile(r"\(([A-Z][A-Za-z'\-]+(?: et al\.)?(?: and [A-Z][A-Za-z'\-]+)?),? (\d{4}|n\.d\.)")
URL = re.compile(r"https?://")


def read(path):
    with open(path, encoding="utf-8", errors="replace") as f:
        return f.read()


def split_frontmatter(text):
    if text.startswith("---"):
        end = text.find("\n---", 3)
        if end != -1:
            return text[3:end], text[end + 4:]
    return "", text


def pages_under(root, exclude):
    out = {}
    for d, dirs, files in os.walk(root):
        dirs[:] = [x for x in dirs if x not in SKIP and x not in exclude]
        for f in files:
            if f.lower().endswith(".md"):
                p = os.path.join(d, f)
                out[os.path.relpath(p, root).replace("\\", "/")] = p
    return out


def git(root, *args):
    try:
        r = subprocess.run(["git", "-C", root, *args], capture_output=True, text=True,
                           encoding="utf-8", errors="replace")
        return r.stdout if r.returncode == 0 else ""
    except OSError:
        return ""


def busy_files(vault, base):
    busy = set()
    top = git(vault, "rev-parse", "--show-toplevel").strip()
    if not top:
        return busy  # not a git repository: nothing can be called busy
    out = git(vault, "-c", "core.quotepath=off", "status", "--porcelain", "--untracked-files=all")
    for line in out.splitlines():
        p = line[3:].strip().strip('"')
        if " -> " in p:
            p = p.split(" -> ", 1)[1]
        full = os.path.normpath(os.path.join(top, p))
        busy.add(os.path.relpath(full, base).replace("\\", "/"))
    return busy


def last_changed(vault, path):
    out = git(vault, "log", "-1", "--format=%ad", "--date=short", "--", path).strip()
    if out:
        return datetime.date.fromisoformat(out)
    return datetime.date.fromtimestamp(os.path.getmtime(path))


def main():
    ap = argparse.ArgumentParser(description="Read-only tidy report for a Markdown vault.")
    ap.add_argument("--vault", default=".")
    ap.add_argument("--stale", type=int, default=28, help="days before an active page is stale")
    ap.add_argument("--thin", type=int, default=80, help="body words below which a page is thin")
    ap.add_argument("--exclude", action="append", default=[], help="folder name to skip")
    ap.add_argument("--hubs", action="append", default=["index.md", "log.md", "overview.md"],
                    help="file names never reported as orphans or unsourced")
    ap.add_argument("--ignore-busy", action="store_true")
    a = ap.parse_args()
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")

    vault = os.path.abspath(a.vault)
    if not os.path.isdir(vault):
        print(f"librarian: no folder {vault}", file=sys.stderr)
        return 2
    base = os.path.join(vault, "wiki") if os.path.isdir(os.path.join(vault, "wiki")) else vault
    pages = pages_under(base, set(a.exclude))
    stems = {}
    for rel in pages:
        stems.setdefault(os.path.splitext(os.path.basename(rel))[0].lower(), []).append(rel)
    busy = set() if a.ignore_busy else busy_files(vault, base)

    inbound = {rel: set() for rel in pages}
    outbound, meta, body_words, sourced = {}, {}, {}, {}
    for rel, path in pages.items():
        fm, body = split_frontmatter(read(path))
        meta[rel] = fm
        body_words[rel] = len(re.findall(r"\w+", body))
        targets = set()
        for m in WIKILINK.finditer(body + "\n" + fm):
            name = m.group(1).strip().split("/")[-1].lower()
            name = name[:-3] if name.endswith(".md") else name
            targets.update(stems.get(name, []))
        for m in MDLINK.finditer(body):
            t = os.path.normpath(os.path.join(os.path.dirname(rel), m.group(1))).replace("\\", "/")
            if t in pages:
                targets.add(t)
        targets.discard(rel)
        outbound[rel] = targets
        for t in targets:
            inbound[t].add(rel)
        sourced[rel] = bool(targets or CITATION.search(body) or URL.search(body))

    def skip(rel):
        return rel in busy or os.path.basename(rel) in a.hubs

    s1 = sorted((rel for rel in pages if not inbound[rel] and not skip(rel)),
                key=lambda r: (len(outbound[r]) > 0, r))
    titles = sorted(stems)
    s2 = []
    for i, x in enumerate(titles):
        for y in titles[i + 1:]:
            if difflib.SequenceMatcher(None, x, y).ratio() >= 0.85:
                s2.append((stems[x][0], stems[y][0]))
    s3_thin = sorted(r for r in pages if body_words[r] < a.thin and not skip(r))
    s3_unsourced = sorted(r for r in pages if not sourced[r] and not skip(r))
    today = datetime.date.today()
    s4 = []
    for rel, path in pages.items():
        if re.search(r"^status:\s*active\s*$", meta[rel], re.M) and not skip(rel):
            age = (today - last_changed(vault, path)).days
            if age >= a.stale:
                s4.append((rel, age))
    l1 = []
    log = os.path.join(base, "log.md")
    if os.path.exists(log):
        for n, line in enumerate(read(log).splitlines(), 1):
            for m in WIKILINK.finditer(line):
                name = m.group(1).strip().split("/")[-1].lower()
                if name.endswith(".md"):
                    name = name[:-3]
                if name not in stems:
                    l1.append((n, m.group(1).strip()))

    print(f"# Librarian report {today}\n")
    print(f"Vault: `{vault}`. Pages read: {len(pages)} under `{os.path.relpath(base, vault)}`. "
          f"Busy (skipped): {len(busy & set(pages))}.\n")
    print("| Code | Check | Count |\n|---|---|---|")
    for code, name, n in (("S1", "orphans", len(s1)), ("S2", "likely duplicates", len(s2)),
                          ("S3", "thin pages", len(s3_thin)),
                          ("S3", "no link and no citation", len(s3_unsourced)),
                          ("S4", f"active, untouched {a.stale}+ days", len(s4)),
                          ("L1", "log lines naming a missing page", len(l1))):
        print(f"| {code} | {name} | {n} |")
    print("\n## S1 orphans")
    for r in s1:
        print(f"- {r}" + ("" if outbound[r] else " (also links nowhere)"))
    print("\n## S2 likely duplicates")
    for x, y in s2:
        print(f"- {x} <> {y}")
    print("\n## S3 thin pages")
    for r in s3_thin:
        print(f"- {r} ({body_words[r]} words)")
    print("\n## S3 no link and no citation")
    for r in s3_unsourced:
        print(f"- {r}")
    print("\n## S4 stale")
    for r, age in sorted(s4):
        print(f"- {r} ({age} days)")
    print("\n## L1 log lines naming a missing page")
    for n, name in l1:
        print(f"- log.md:{n} [[{name}]]")
    print("\n## Busy")
    for r in sorted(busy & set(pages)):
        print(f"- {r}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
