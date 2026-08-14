# Don't edit decision docs that have been decided upon

## Context
I noticed in a previous decision (8), there were edits made to the decision 3 document. In this case the edit was sensible and small, but it shouldn't happen IMO -- this opens the door for post-hoc rewriting the rules, and lots of potential confusion.

## Decision
Don't merge substantive edits to decision documents that already exist in `dev` -- ideally we formally block this in GitHub. Narrow mechanical maintenance, such as adding relationship metadata, is allowed. When a task amends, changes, or supersedes an existing decision, that same task should add the relationship metadata to the affected decision documents. Substantive changes to existing decisions should be proposed in a new decision.

## Consequences
Minor edits become tedious, but decision documents are more trustworthy.
