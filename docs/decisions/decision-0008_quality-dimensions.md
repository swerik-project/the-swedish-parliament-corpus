# How do document quality dimensions and data integrity tests
## Status

Decided

- Decision: approved

## Context
An important part of the continuous integration of the SWERIK corpora is the quality control step, consisting of automated tests and the estimation of quality dimensions of interest.

The estimation of quality is commonly done using sampling strategies and are then automatically estimated during quality control. Currently the description of the quality estimation is found in a google doc. We want the quality estimation to be stored together with the actual corpora to document how the estimation is done.

The test files for automated tests are already included as separate tests. 

Quality dimension estimation is commonly done by counting or by estimation based on a sample. There is a need to understand what is estimated and why it is estimated/motivation behind the quality estimation. Hence we need to describe how the each quality dimension more thoroughly.

## Decision

All quality estimations and data-integrity tests should be included in the actual repository where they are used/analyzed. Each quality dimension estimation should be stored as `qe-[what-dimension-is-estimated].py/r` and should include a short docstring / header describing the the estimation as well as a reference to or "inclusion" of the markdown file that contains more detailed descriptions of what is estimated and the estimation process. See the quality dimension template.

Similarly each data-integrity test should be stored as `test-[what-is-checked-automatically].py/r` and should include a short docstring / header describing the test as well as a reference to or "inclusion" of the markdown file that contains more detailed descriptions of what is tested and the testing process. See the data-integrity-test template.

Python functions contained in the quality estimation and data-integrity test files described with docstrings that "include" the relevant .md files provide the basis to end-user API documentation. API documentation is then generated with the pdoc module and becomes available under `swerik-project.github.io/<reponame>/quality-estimation` or `swerik-project.gihub.io/<reponame>/data-integrity`

## Consequences
This makes it easier to follow and understand the quality dimension, unit testing and to automatically parse the descriptions of the tests and how it is computed for each individual corpus. It also makes the corpus quality control process an integrated part of each individual corpus that then will work independently. 

