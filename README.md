# ai-toolkit

How I set up AI coding agents so that their work can be checked.

I am an environmental engineer, not a software engineer by training. I use
[Claude Code](https://claude.com/claude-code) every day.
In life cycle assessment and energy modelling, an unsourced number quietly becomes a
result, so most of what is here exists to stop that: rules the agent reads, small helper
agents sized for the job, and a fixed way of reporting what was checked.

This repo holds the general parts of that setup, cleaned of anything private. It grows one
piece at a time.

## Why these exist

Each rule came from something that went wrong, and each has a mechanism, because a rule
that is only written down holds only as long as the agent remembers it.

| Rule | What goes wrong without it | Mechanism | Where |
|---|---|---|---|
| Never invent a value | A plausible figure with no source ends up in a report | The agent is told that "I don't know" and "that is not in the source" are finished answers; a reply reports what it could not check | [docs/verified-block.md](docs/verified-block.md) |
| The agent shows what it checked | "It works" with no run behind it | Every larger task ends with a four-line block: Verified, Failed, Fixed, Unverified | [docs/verified-block.md](docs/verified-block.md) |
| Enough model for the job, not more | A small model guesses at facts, or a large model burns budget on renaming files | Three worker agents on three model sizes, with a written rule for what goes where | [docs/model-tiers.md](docs/model-tiers.md), [agents/](agents/) |
| The decision stays with a person | The agent picks a method that changes a result and nobody notices | Workers hand such choices back as options with trade-offs | [agents/](agents/) |
| Confidential files stay out of reach | Private material is sent to a helper agent or an outside service | Workers are told never to open the confidential folder; in my own setup a script also refuses the hand-off | [agents/](agents/) |

## The trust ladder

How much I let an agent do is decided per step, not per model. A step climbs one level
only when a check exists that fails on a planted bad case, the step ran 10 times in a row
with no correction from me, and it can be undone. Most of my steps sit at level 1 or 2
today. The full picture, including who builds, who validates, why the check exists before
the build and how I stress test: [docs/trust-ladder.md](docs/trust-ladder.md).

## Skills

A skill is a Markdown file that tells the agent how to do one kind of task. Mine start
from a failure I watched, get three test cases (trigger, core steps, boundary) and are
judged by a different model from the one that ran them. How I make them and the full list
with credits: [docs/skills.md](docs/skills.md).

| Group | Skills |
|---|---|
| My own | `create-verify`, `code-map`, `lint`, `librarian`, `lean-claude` |
| Adapted from [pstack](https://github.com/michael-denyer/pstack-claude) by Lauren Tan | `blast-radius`, `explain-change`, `ketchup`, `sharpen`, `decision-log`, `reflect`, `correct` |
| From [mattpocock/skills](https://github.com/mattpocock/skills) by Matt Pocock | `teach`, `research`, `retro` |

## What is here

```
agents/
  worker-light.md      one small, checkable job; smallest model
  worker-standard.md   multi-step work with a clear goal; mid-size model
  worker-heavy.md      hard, self-contained problems; largest model
docs/
  trust-ladder.md      how much I let an agent do, and what moves a step up or down
  skills.md            the skills I use and how I make my own
  model-tiers.md       which work goes to which worker, and when to go one up
  verified-block.md    the report every larger task ends with
```

Two hooks that enforce these rules (no credentials in commits, no long turn without a
Verified block) live in their own repo: [claude-guardrail-hooks](https://github.com/batutho-dot/claude-guardrail-hooks).

## Use one

The worker agents are plain Markdown files. Copy the `agents/` folder into `.claude/agents/`
in a project (or `~/.claude/agents/` for every project), then start Claude Code. The agents
appear under those names. Change `confidential/` in each file to the folder you want kept
out of reach.

## Credit

I write these together with Claude Code. The trust ladder is Lauren Tan's idea. The notes
system follows Andrej Karpathy's LLM Wiki pattern, in the layout of the `nashsu/llm_wiki` project. In my private setup I also use
and adapt skills by Lauren Tan (`pstack`), Matt Pocock (`mattpocock/skills`) and Anthropic
(`anthropics/skills`); those are theirs and are not copied here.

No licence file yet. Until one is added, please ask before reusing.
