# ai-toolkit

How I work with AI as a teammate: it earns more responsibility as it proves itself.

**What you get:** three worker agents, five skills you can take one at a time, and the
rules behind them. General versions, cleaned of anything private.

## Use it

A skill: open its folder in [skills/](skills/). Its page has the one command to get it.

The worker agents: copy `agents/` into `.claude/agents/` in a project (or `~/.claude/agents/`
for every project) and start Claude Code. Each file names a folder the worker must never
open; change it to yours.

## What is here

| Folder | What | Start with |
|---|---|---|
| [skills/](skills/) | `code-map`, `create-verify`, `lean-claude`, `librarian`, `lint` | [skills/](skills/) |
| [agents/](agents/) | Three workers on three model sizes: light, standard, heavy | [docs/model-tiers.md](docs/model-tiers.md) |
| [docs/](docs/) | The thinking behind it | below |

## How it works

- **Trust is earned per step.** A step climbs one level only when a check exists that fails
  on a planted bad case, it ran 10 times in a row with no correction from me, and it can be
  undone. Most of my steps sit at level 1 or 2 today. Chart, plan and stress tests:
  [docs/trust-ladder.md](docs/trust-ladder.md).
- **The agent shows what it checked.** Every larger task ends with four lines: Verified,
  Failed, Fixed, Unverified. [docs/verified-block.md](docs/verified-block.md).
- **Every rule has a mechanism,** because a rule that is only written down holds only as
  long as the agent remembers it. [docs/rules.md](docs/rules.md).
- **Skills start from a failure I watched** and get three test cases. How I make them, and
  which skills by Lauren Tan and Matt Pocock I use, when, and how often:
  [skills/](skills/).

## Credit and licence

I write these together with Claude Code. The trust ladder is Lauren Tan's idea. The notes
system follows Andrej Karpathy's LLM Wiki pattern, in the layout of the `nashsu/llm_wiki`
project. I also use and adapt skills by Lauren Tan
([pstack](https://github.com/michael-denyer/pstack-claude)), Matt Pocock
([mattpocock/skills](https://github.com/mattpocock/skills)) and Anthropic
(`anthropics/skills`); those are theirs and are not copied here.

The feature map step in `create-verify` is adapted from pstack's `create-verification-skill`
(MIT licence, copyright 2026 Lauren Tan and 2026 Michael Denyer, whose Claude Code port I
use). `code-map` borrows the idea of zoom levels from Simon Brown's C4 model.

MIT, see [LICENSE](LICENSE).
