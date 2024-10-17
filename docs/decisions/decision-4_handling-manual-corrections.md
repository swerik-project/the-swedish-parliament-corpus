# Handling of manual curation

## Status

Decided

- Decision: accepted

## Context
As the SWERIK project grows, we will have an increased amount of data coming in from collaborators in different forms. This data will have different levels of quality. Some data might be simple programatical fixes (general low confidence in individual edits), student annotations, and expert/research annotated data.

We don't want higher quality manual curations to accidentaly be changed, as happended with some introductions when titles were added to the corpus. 

## Decision
The sugestion is to let manual annotations (by students and experts) fill two roles.

1. They should first be added as a test suite to the corpus, i.e. add a data integrity test that checks that these manual annotations has not been changed. Or - both the test suite and the data is changed at the same time if there is an error e.g. in students annotation.
2. They should be corrected in the data so the test suite pass.

## Consequences
Manually annotated data will not be overwritten by programatical changes.
