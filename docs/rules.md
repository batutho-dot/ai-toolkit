# Rules, and what enforces them

Each rule came from something that went wrong, and each has a mechanism, because a rule
that is only written down holds only as long as the agent remembers it.

| Rule | What goes wrong without it | Mechanism | Where |
|---|---|---|---|
| Never invent a value | A plausible figure with no source ends up in a report | The agent is told that "I don't know" and "that is not in the source" are finished answers; a reply reports what it could not check | [docs/verified-block.md](verified-block.md) |
| The agent shows what it checked | "It works" with no run behind it | Every larger task ends with a four-line block: Verified, Failed, Fixed, Unverified | [docs/verified-block.md](verified-block.md) |
| Enough model for the job, not more | A small model guesses at facts, or a large model burns budget on renaming files | Three worker agents on three model sizes, with a written rule for what goes where | [docs/model-tiers.md](model-tiers.md), [agents/](../agents/) |
| The decision stays with a person | The agent picks a method that changes a result and nobody notices | Workers hand such choices back as options with trade-offs | [agents/](../agents/) |
| Confidential files stay out of reach | Private material is sent to a helper agent or an outside service | Workers are told never to open the confidential folder; in my own setup a script also refuses the hand-off | [agents/](../agents/) |
