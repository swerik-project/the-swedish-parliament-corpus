# Date precision for party existence and party affiliations

## Context

Some dates related to party existence and party affiliation are only as precise as the year. In practice, this makes it difficult to test for historical accuracy in the party affiliation data.

## Decision

Add columns to `party.csv`

- inception_precision: possible values y, m, d
- dissolution_precision: possible values y, m, d

Add columns to `party_affiliation.csv`

- start_precision: possible values y, m, d
- end_precision:possible values y, m, d


Dates with only a year (4 digits) or YYYY-01-01 or YYYY-12-31 are automatically assigned year precision. 

Increasing precision after (manual) checks of dates are stored in `party.csv` / `party_affiliation.csv` as well as relevant files under `test/data/` and regular tests are implemented to ensure manually corrected data is not overwritten.

## Consequences

It becomes possible to test party affiliations with an appropriate level of precision.