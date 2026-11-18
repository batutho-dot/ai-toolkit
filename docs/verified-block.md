# The Verified block

Every larger task ends with these four lines. Nothing is marked done that the agent cannot
point to.

```
Verified:   what was checked and how (test run, build, page opened, source opened, link resolved)
Failed:     what did not pass, with the output
Fixed:      what was changed in response
Unverified: what could not be checked, and why
```

## Why it has this shape

An agent that says "done, it works" gives me nothing to check. The block forces four
separate statements, and the last one matters most: it is where the agent has to say what
it did not look at.

The check that counts is the one a careful reviewer would make on the real output: open the
rendered page, run the script, click the link, read the source. Saying it works is not a
check.

## Rules that go with it

- **"I don't know" is a finished answer.** So is "that is not in the source". A plausible
  value with no source is not.
- **A helper agent's report is a lead.** It goes under Unverified until the main session
  has opened the source itself.
- **Practice data is labelled as practice** every time it appears, and is never quoted as a
  result.
- **Assumptions and the range tested are stated,** instead of one number presented as
  settled.

## Example

```
Verified:   Script ran on a clean folder and wrote 37 rows; the two totals match the
            source table (opened, page 4).
Failed:     One country code had no price data for 2010 to 2012.
Fixed:      Those years are dropped for that country and the README says so.
Unverified: The source's own revision date. The page did not show one.
```

The example is invented for illustration.
