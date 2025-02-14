# Remove Status from Decisions Template

## Context

There has been some difficulty remembering to change the "status" part of the decision to approved before merging an approved decision.

## Decision

Change the template from:

```
## Status
What is the status, such as proposed, accepted, rejected, deprecated, superseded, etc.?

## Context
What is the issue that we're seeing that is motivating this decision or change?

## Decision
What is the change that we're proposing and/or doing?

## Consequences
What becomes easier or more difficult to do because of this change?
```

to:
```
## Context
What is the issue that we're seeing that is motivating this decision or change?

## Decision
What is the change that we're proposing and/or doing?

## Consequences
What becomes easier or more difficult to do because of this change?
```

Decisions that are not approved will simply not be merged to main. Any decision documents found in the main branch are considered to be approved and current unless amended or overturned in a later decision.

## Consequences

Decision making process workflow is smoother.