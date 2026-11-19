# Model tiers: which work goes to which worker

The main session reads the request, writes a brief, checks what comes back and answers. A worker of the right size does the work. Power for the job comes first. Saving tokens only chooses between two tiers that would both do it properly; if the lower might miss, go one up.

| Tier | Worker | Use for | Never for |
|---|---|---|---|
| Light | `worker-light` (smallest model) | One-step mechanical work, answer in the input: file sweeps, listings, renames, link checks, formatting, conversion | Facts, multi-step tool use |
| Standard | `worker-standard` (mid-size model) | Building and writing, facts in the input: a script from a spec, a summary of supplied notes, a routine review draft, a bug with a known cause | Anything resting on knowledge the input lacks |
| Heavy | `worker-heavy` (largest model) | Judgement and anything resting on knowledge: architecture, a hard bug with no known cause, method questions, any figure, citation or claim | Work a lower tier does properly |

Stays in the main session: tasks of a few steps (a worker starts cold), a step whose result decides the next, work needing the conversation so far, anything touching confidential files.

## Hand-off rules

1. A brief has the outcome, the conditions that make it done, and a request for the report in [the Verified shape](verified-block.md).
2. A thin or wrong result is rerun one tier up, not patched by hand.
3. A worker's report is a lead. Anything about a source, figure or citation is checked first.
4. Several workers at once need a reason: large, independent parts.
5. Say which tier ran and why, in one line.
