# Model tiers: which work goes to which worker

The main session reads the request, sizes it, writes a brief, checks what comes back and
answers. The doing goes to a worker of the right size.

## The priority is fixed

Enough power for the job comes first. Saving tokens comes second. Saving is only a choice
between two tiers that would both do the job properly. If the tier below might not get it
right the first time, go one up.

## The tiers

| Tier | Worker | Use for | Never for |
|---|---|---|---|
| Light | `worker-light` (smallest model) | One-step mechanical work where the answer is in the input: file sweeps, listings, renames, link checks, formatting, conversion | Facts, multi-step tool use |
| Standard | `worker-standard` (mid-size model) | Building and writing where the facts are in the input: a script from a spec, a summary of supplied notes, a routine review draft, a bug with a known cause | Anything resting on knowledge the input does not hold |
| Heavy | `worker-heavy` (largest model) | Judgement and anything resting on knowledge: architecture, a hard bug with no known cause, method questions, any figure, citation or claim | Work a lower tier does properly |

In short: the smallest model never touches a fact, and the mid-size model only gets work
whose facts are in what it was given.

## What stays in the main session

- A task of a few steps. A worker starts cold, so handing it over costs more than doing it.
- A step whose result decides the next step.
- Work that needs the conversation so far.
- Anything touching confidential files. Those are never sent to a worker.

## Rules around a hand-off

1. **A brief has three parts:** the outcome, the conditions that make it done, and a request
   for the report in [the Verified shape](verified-block.md).
2. **A thin or wrong result is rerun one tier up,** not patched by hand.
3. **What a worker reports is a lead, not a result.** Anything it says about a source, a
   figure or a citation is checked before it is passed on.
4. **Several workers at once need a reason:** only for parts that are large and do not
   depend on each other.
5. **Say which tier ran and why,** in one line, so the choice can be questioned.
