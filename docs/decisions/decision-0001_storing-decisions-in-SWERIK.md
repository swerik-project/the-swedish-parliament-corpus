# Storing decisions in SWERIK

## Context

We want to store project-wide decisions in a `docs/decisions` folder of this (umbrella) repository.

Similarly we store repository-specific decisions in a `docs/decisions` folder in individual repositories.

Individual repositories should only create `docs/decisions` when they have repository-specific decisions to store. Empty decision folders are not required.

The template is in large part taken from [here](https://github.com/joelparkerhenderson/architecture-decision-record/tree/main/locales/en/templates/decision-record-template-by-michael-nygard). By following this format we can use [adr-tools](https://github.com/npryce/adr-tools) for managing the decision files.


## Decision
We use [this template](decision-template.md) for decisions.



## Consequences
By having a clear decision on how we store decisions, we can process and follow the decisions made in the project.
