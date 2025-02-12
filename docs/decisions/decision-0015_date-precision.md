# Date precision for party existence and party affiliations

## Context

Some dates related to party existence and party affiliation are only as precise as the year. In practice, this makes it difficult to test for historical accuracy in the party affiliation data.

## Decision


Add precision value column with the suffix `_precision` to any column with dates. Values for a `*_precision` column are `year`, `month`, or `day`.

examples:

- add to `party.csv`
	+ inception_precision
	+ dissolution_precision

- add to `party_affiliation.csv`
	+ start_precision
	+ end_precision


Dates with only a year (4 digits) or YYYY-01-01 or YYYY-12-31 are automatically assigned year precision. 

Increasing precision after (manual) checks of dates are stored in `party.csv` / `party_affiliation.csv` as well as relevant files under `test/data/` and regular tests are implemented to ensure manually corrected data is not overwritten.

## Consequences

It becomes possible to test party affiliations with an appropriate level of precision.