# Remove Status from Decisions Template

## Context

There has been some difficulty remembering to change the "status" part of the decision to approved before merging an approved decision.

## Decision

Remove the status section from the decision template. New decision documents should start with `## Context`, followed by `## Decision` and `## Consequences`.

Decisions that are not approved will simply not be merged to dev. Any decision documents found in the dev branch are considered to be approved and current unless amended or overturned in a later decision.

## Consequences

Decision making process workflow is smoother.
