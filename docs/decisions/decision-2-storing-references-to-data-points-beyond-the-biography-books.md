# Storing references to data points beyond the Biography Books

## Status

Proposed


## Context

To data, we have relied on the Bio Books as an authoritative source of information. However, it has been pointed out that some of the information is imprecise / incorrect. While we have kept track of MPs' page references in the bio books, we have not indicated the scope of these page references over particular data points in any way.

So while we don't necessarily want to go through the bio books once again, person by person to add scope over each data point, we _do_ want to implement a means of tracking references to other data sources that may conflict with or further specify info from the bio books.

An ideal strategy would allow addition of such information to the corpus, with a reference scoped to the individual data point and a means to indicate which datum/reference we consider to be the most accurate or up to date.


## Decision

Given that we already have a `test/data/` directory in each of the data repositories where we keep manually-curated data for integrity tests, the suggestion is that updated data points and references be kept here in CSV format. The CSV files are then used:

- (a) to update information in Wikidata as necessary
- (b) to test that the information does not change after querying from Wikidata

For example, this question arose from the fact that there is more precise information about MP mandates in person registers, so we would have a file `data/test/mandate.csv` with the following columns:


| person_id |       date | date_type | source               | page | endorse |
| ---       | ---        | ---       | ---                  | ---  | ---     |
| i-abc123  | 2022-10-04 | start     | register_bibtex_code | 13   | True    |
| i-xyz987  | 2022-10-01 | end       | register_bibtex_code | 15   | False   |
| i-xyz987  | 2022-10-03 | end       | anotherref_bib_code  | 123  | True    |


Each row refers to a single data point (start or end date of mandate in this case, but the principle should apply to other cases as well) with a reference to the source of the information. The final column is a means to encode precedence of information for a single data point without removing rows from other sources -- in the case of person i-xyz987, we found info in the registers, another source with info we understand to be even more precise, hence the register info is not endorsed.


## Consequences

We are able to add / update info with more precision under scoped references.
