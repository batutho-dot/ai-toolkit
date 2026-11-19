# Rules, and what enforces them

Each rule came from something that went wrong, and each has a mechanism: a written rule holds only while the agent remembers it.

| Rule | Without it | Mechanism | Where |
|---|---|---|---|
| Never invent a value | A plausible unsourced figure ends up in a report | "I don't know" and "that is not in the source" are finished answers | [docs/verified-block.md](verified-block.md) |
| The agent shows what it checked | "It works" with no run behind it | Larger tasks end with Verified, Failed, Fixed, Unverified | [docs/verified-block.md](verified-block.md) |
| Enough model for the job, not more | A small model guesses at facts, or a large one burns budget on renames | Three worker agents on three model sizes, with a rule for what goes where | [docs/model-tiers.md](model-tiers.md), [agents/](../agents/) |
| The decision stays with a person | The agent silently picks a method that changes a result | Workers hand such choices back as options with trade-offs | [agents/](../agents/) |
| Confidential files stay out of reach | Private material reaches a helper agent or outside service | Workers never open the confidential folder; in my setup a script also refuses the hand-off | [agents/](../agents/) |
