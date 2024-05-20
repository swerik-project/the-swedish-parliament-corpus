# Storing decisions in SWERIK

## Status

Proposed

## Context

We want to store project-wide decisions in a doc/decisions folder of this (umbrella) repository.

Similarly we store repository-specific decisions in a doc/decisions folder in individual repositories.

The template is in large part taken from [here](https://github.com/joelparkerhenderson/architecture-decision-record/tree/main/locales/en/templates/decision-record-template-by-michael-nygard). By following this format we can use [adr-tools](https://github.com/npryce/adr-tools) for managing the decision files.


## Decision:
We use the following template for decisions.

### Title
#### Status
What is the status, such as proposed, accepted, rejected, deprecated, superseded, etc.?

#### Context
What is the issue that we're seeing that is motivating this decision or change?

#### Decision
What is the change that we're proposing and/or doing?

#### Consequences
What becomes easier or more difficult to do because of this change?


## Consequences
By having a clear decision on how we store decisions, we can process and follow the decisions made in the project.
