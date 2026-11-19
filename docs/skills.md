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

Written by me together with Claude Code. Listed, not published.

| Skill | What it does |
|---|---|
| `create-verify` | Writes the verify script for a repo: real run on a fixed input, compared to a known-good output, proven on a planted break |
| `code-map` | Draws a program's steps as a diagram, each box tied to file and line, so I see the shape of code before its lines |
| `lint` | Runs the checker over my notes (links, page shape, sources), proposes fixes and applies only the ones I approve |
| `librarian` | Tidies the notes and checks that changes the agent reported really landed |
| `lean-claude` | Shrinks the always-loaded instruction files without losing a rule, proven with a rule map and test prompts |

`create-verify` borrows its feature map step from pstack (below).

## Adapted from pstack, by Lauren Tan

[pstack](https://github.com/michael-denyer/pstack-claude) is Lauren Tan's set of skills and
principles (MIT). I use the Claude Code version linked here. These are my adaptations, cut
down and fitted to my rules. They are hers in idea.

| My skill | From | What I changed |
|---|---|---|
| `blast-radius` | `blast-radius` | Runs between the explanation of a change and its build |
| `explain-change` | `in-your-own-words` | Writes a plain note before the build and stops for my yes |
| `ketchup` | `ketchup` | Catches me up on a long session and lists the decisions waiting on me |
| `sharpen` | `sharpen` | Any outside check it adds must be traceable to a source |
| `decision-log` | `show-me-your-work` | One row per decision with reason and evidence, for long runs |
| `reflect` | `reflect` | Cut down to run in the main session |
| `correct` | `correct` | Turns repeated corrections into structure or a check before a written rule |

## From Matt Pocock

[mattpocock/skills](https://github.com/mattpocock/skills) (MIT). Used close to the
original, with a short section of my own rules added at the end of each.

| Skill | What I use it for |
|---|---|
| `teach` | Learning a topic over several sessions |
| `research` | Docs and API facts from primary sources |
| `retro` | A look back at a coding session, ending in proposed changes to the setup |

## Others

`verify-this` is adapted from Cursor's team kit (MIT). I also use skills from Anthropic's
[anthropics/skills](https://github.com/anthropics/skills). None of the third-party files
are copied into this repo.
