# Don't edit decision docs that have been decided upon

## Status

Decided

- Decision: accepted


## Context
I noticed in a previous decision (8), there were edits made to the decision 3 document. In this case the edit was sensible and small, but it shouldn't happen IMO -- this opens the door for post-hoc rewriting the rules, and lots of potential confusion.

## Decision
Don't merge any edits to decision documents that already exist in main -- ideally we formally block this in github. Changes to existing decisions should be proposed in a new decision.

## Consequences
Minor edits become tedious, but decision documents are more trustworthy.
