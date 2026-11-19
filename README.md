# ai-toolkit

How I work with AI as a teammate: it earns more responsibility as it proves itself. Three worker agents, five skills to take one at a time, and the rules behind them. General versions, cleaned of anything private.

## Use it

A skill: open its folder in [skills/](skills/) for the one command to get it.

Worker agents: copy `agents/` into `.claude/agents/` (or `~/.claude/agents/` for every project) and start Claude Code. Each file names a folder the worker must never open. Change it.

| Folder | What | Start with |
|---|---|---|
| [skills/](skills/) | `code-map`, `create-verify`, `lean-claude`, `librarian`, `lint` | [skills/](skills/) |
| [agents/](agents/) | Three workers on three model sizes: light, standard, heavy | [docs/model-tiers.md](docs/model-tiers.md) |
| [docs/](docs/) | The thinking behind it | below |

## How it works

- **Trust is earned per step.** A step climbs a level only after a check that fails on a planted bad case, 10 runs in a row with no correction from me, and a way to undo it. [docs/trust-ladder.md](docs/trust-ladder.md)
- **The agent shows what it checked:** Verified, Failed, Fixed, Unverified. [docs/verified-block.md](docs/verified-block.md)
- **Every rule has a mechanism.** [docs/rules.md](docs/rules.md)
- **Skills start from a failure I watched** and get three test cases. [skills/](skills/) also lists the ones I use from others.

## Credit and licence

I write these with Claude Code. The trust ladder is Lauren Tan's idea. The notes system follows Andrej Karpathy's LLM Wiki pattern, laid out as in `nashsu/llm_wiki`. I also use and adapt skills by Lauren Tan ([pstack](https://github.com/michael-denyer/pstack-claude)), Matt Pocock ([mattpocock/skills](https://github.com/mattpocock/skills)) and Anthropic (`anthropics/skills`). Those are theirs, not copied here.

`create-verify`'s feature map step is adapted from pstack's `create-verification-skill` (MIT licence, copyright 2026 Lauren Tan and 2026 Michael Denyer, whose Claude Code port I use). `code-map` borrows zoom levels from Simon Brown's C4 model.

MIT, see [LICENSE](LICENSE).
