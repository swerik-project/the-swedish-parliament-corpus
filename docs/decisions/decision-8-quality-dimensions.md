# Title
## Status
proposed

## Context
An important part of the continous integration of the swerik corpora is the quality control step, consisting of automated tests and the estimation of quality dimensions of interest.

The estimation of quality is commonly done using sampling strategies and are then automatically estimated during quality control. Currently the description of the quality estimation is found in a google doc. We want the quality estimation to be stored together with the actual corpora to document how the estimation is done.

The test files for automated tests are already included as separate tests. 

Quality dimension estimation is commonly done by counting or by estimation based on a sample. There is a need to understand what is estimated and why it is estimated/motivation behind the quality estimation. Hence we need to describe how the each quality dimension more thoroughly.

## Decision
All separate quality dimensions sheet should be included in the actual repository where they are used/analyzed for each quality dimension we estimate in that corpus. See the quality dimension template.

Each test should be stored as `test-[what-is-checked-automatically].py/r`. Each test should include a header in comment describing the test and why it has been included. See the data-integrity-test template.

## Consequences
This makes it easier to follow and understand the quality dimension, unit testing and to automatically parse the descriptions of the tests and how it is computed for each individual corpus. It also makes the corpus quality control process an integrated part of each individual corpus that then will work independently. 

