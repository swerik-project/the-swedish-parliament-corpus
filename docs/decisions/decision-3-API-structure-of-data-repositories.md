# API structure of data repositories

## Status
Decided

## Context
We need to have a unifide API to access and work with quality estimation for each individual repository. An example is that we want to have the data to estimate the OCR quality (i.e. the test data) in the repository so when the repository is updated the estimation can be conducted. 

This also includes that we need to store the estimated results in the corpus in a nice formats for the umbrella repository to easily access and use estimated quality.

See [#329](https://github.com/welfare-state-analytics/riksdagen-corpus/issues/329) for discussions.

## Decision
We store the data, test, and quality estimation in the following way.

### Data
/data/... -> the data is stored here

### Data integrity tests
/test/... -> data integrity tests of the specific data
/test/data/... -> data used by data integrity tests

### Quality estimation
/quality/... -> scripts used for quality estimation
/quality/data/... -> data used for quality estimation
/quality/estimates/... -> estimates by version stored for easy access
/quality/docs/... -> quality dimension descriptions

## Consequences
This will make clear where different data sources go.
