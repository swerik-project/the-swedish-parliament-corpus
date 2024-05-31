# API structure of data repositories

## Status
proposed

## Context
We need to have a unifide API to access and work with quality estimation for each individual repository. An example is that we want to have the data to estimate the OCR quality (i.e. the test data) in the repository so when the repository is updated the estimation can be conducted. 

This also includes that we need to store the estimated results in the corpus in a nice formats for the umbrella repository to easily access and use estimated quality.

The suggested API (see [#329](https://github.com/welfare-state-analytics/riksdagen-corpus/issues/329) for discussions ):

### Data
/data/... -> the data is stored here

### Data integrity tests
/test/... -> data integrity tests of the specific data
/test/data/... -> data used by data integrity tests

### Quality estimation
/quality_estimation/... -> scripts used for quality estimation
/quality_estimation/data/... -> data used for quality estimation
/quality_estimation/estimates/... -> estimates by version stored for easy access

## Decision
-

## Consequences
What becomes easier or more difficult to do because of this change?
