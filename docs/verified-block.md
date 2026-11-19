# The Verified block

Every larger task ends with these four lines. Nothing is marked done without a check to point to.

```
Verified:   what was checked and how (test run, build, page opened, source opened, link resolved)
Failed:     what did not pass, with the output
Fixed:      what was changed in response
Unverified: what could not be checked, and why
```

The last line matters most: it says what the agent did not look at. The check that counts is the one a reviewer would make on the real output: open the page, run the script, click the link, read the source.

- "I don't know" and "that is not in the source" are finished answers. A plausible value with no source is not.
- A helper agent's report goes under Unverified until the main session opens the source.
- Practice data is labelled as practice and never quoted as a result.
- Assumptions and the range tested are stated.

Example (invented):

```
Verified:   Script ran on a clean folder and wrote 37 rows; the two totals match the
            source table (opened, page 4).
Failed:     One country code had no price data for 2010 to 2012.
Fixed:      Those years are dropped for that country and the README says so.
Unverified: The source's own revision date. The page did not show one.
```
