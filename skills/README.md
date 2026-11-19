# Skills: what I use and how I make my own

A skill is a Markdown file that tells the agent how to do one kind of task: when to start,
which steps in which order, where to stop. Claude Code loads the short description of every
skill and opens the full file only when a task matches.

## How I make a skill

I do not write a skill because it sounds useful. A skill starts from something that went
wrong.

1. **Watch the failure.** I read what the agent actually did (its tool calls), and find the
   place where it guessed, skipped a step or stopped too early. One failure, one skill.
2. **Try structure first.** If a script, a hook or a different folder layout can make the
   mistake impossible, I do that instead. A skill is a soft rule: the agent can forget it.
3. **Write the description as the trigger.** The description decides whether the skill ever
   runs, so it names the words I really use and the cases it is not for.
4. **Keep the body to steps.** Numbered, in order, each with what it produces. A "Never"
   list for the lines it must not cross, and an explicit stop where the decision is mine.
5. **Write three test cases** before the skill counts as done:
   - **Trigger:** does it start when it should?
   - **Core steps:** does it do them in order and stop where it must?
   - **Boundary:** does it refuse the case it must not handle?
6. **Run the cases blind.** Fresh throwaway copy, the prompt pasted with no hints, and a
   judge that is a different model from the one that ran the case. Each check is pass or
   fail with the line of the transcript that shows it.
7. **Count the use.** A script counts how often each skill was called. In my first 22 days
   on one machine, 29 of 37 active skills were never called once. Most skill failures are
   trigger failures, so an unused skill gets a better description or is parked.
8. **Change it only through its tests.** An edit to a skill is done when its three cases
   pass again.

Not every skill has its test file yet, and some first runs were judged by the same model
that ran them. Those results are marked as not independent.

## My own skills

Written by me together with Claude Code. Open one to see how to get it.

| Skill | What it does |
|---|---|
| [`create-verify`](create-verify/) | Writes the verify script for a repo: real run on a fixed input, compared to a known-good output, proven on a planted break |
| [`code-map`](code-map/) | Draws a program's steps as a diagram, each box tied to file and line, so I see the shape of code before its lines |
| [`lint`](lint/) | Runs the checker over my notes (links, page shape, sources), proposes fixes and applies only the ones I approve |
| [`librarian`](librarian/) | Tidies the notes and checks that changes the agent reported really landed |
| [`lean-claude`](lean-claude/) | Shrinks the always-loaded instruction files without losing a rule, proven with a rule map and test prompts |

`create-verify` borrows its feature map step from pstack (below).

## Skills from others, and when I use them

Two people's work is part of my daily workflow, and I want that visible. The counts are
real: calls in 298 Claude Code sessions on one machine, 8 October to 19 November 2026,
counted by a script over the session logs. A count of 0 means installed and never called
by name in that period.

### From pstack, by Lauren Tan

[pstack](https://github.com/michael-denyer/pstack-claude) is Lauren Tan's set of skills and
principles (MIT). I use Michael Denyer's Claude Code version, linked here. Mine are
adaptations: cut down and fitted to my rules. The ideas are hers.

| My skill | Her skill | When I use it | Calls |
|---|---|---|---|
| `explain-change` | `in-your-own-words` | Before any change to code I answer for. The agent writes a plain note, then stops for my yes | 33, in 30 sessions |
| `ketchup` | `ketchup` | When I come back to a long session and need what changed and which decisions wait on me | 17 |
| `blast-radius` | `blast-radius` | After the explanation, before the build: what could this break outside the diff | 3 |
| `create-verify` (one step) | `create-verification-skill` | Setting up a repo's verify script. The feature map step is hers, the rest is mine | 9 |
| `sharpen` | `sharpen` | To make a task deeper before starting it | 0 |
| `decision-log` | `show-me-your-work` | One row per decision on long runs | 0 |
| `reflect`, `correct` | `reflect`, `correct` | Turning repeated corrections into a check or a rule. Their routine runs inside my weekly review, not by name | 0 |

### From Matt Pocock

[mattpocock/skills](https://github.com/mattpocock/skills) (MIT). I use these close to the
original, with a short section of my own rules added at the end of some.

| Skill | When I use it | Calls |
|---|---|---|
| `handoff` | When a session's context gets long. A hook tells the agent to write the hand-over document before the context is compacted, so nothing is lost | 75, in 58 sessions |
| `grilling` | Before a plan or decision locks: the agent interviews me until the open questions are found | 22, in 15 sessions |
| `improve-codebase-architecture` | When a codebase needs restructuring, not just a fix | 9 |
| `codebase-design` | Designing a module's interface before writing it | 5 |
| `writing-for-agents` | Whenever I write or edit a skill or an instructions file | 4 |
| `teach` | Learning a topic over several sessions | 1 |
| `research`, `retro`, `diagnosing-bugs`, `domain-modeling`, `wait-what` | Installed for docs research, session retrospectives, hard bugs, a shared glossary and "say that again, plainly" | 0 |

What the counts say: `handoff`, `explain-change` and `grilling` carry most of my sessions,
and all three come from these two people. Half of what I installed I never called. Those
get a better trigger or get parked.

### Others

`verify-this` is adapted from Cursor's team kit (MIT). I also use skills from Anthropic's
[anthropics/skills](https://github.com/anthropics/skills). None of the third-party files
are copied into this repo.

## Check them

```bash
python verify.py
```

Run from the repo root. It checks every skill's header, compiles the scripts and runs each
script on its sample, ending in `verify: PASS` or `verify: FAIL at <step>`.
