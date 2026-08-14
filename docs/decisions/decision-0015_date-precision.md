# Date precision for party affiliations

## Context

Some dates related to party affiliation are only as precise as the year. In practice, this makes it difficult to test for historical accuracy in the party affiliation data.

## Decision


Add precision value column with the suffix `_precision` to any column with dates. Values for a `*_precision` column are `year`, `month`, or `day`.

examples:

- add to `party_affiliation.csv`
	+ start_precision
	+ end_precision


For testing and comparison, dates with precision should be interpreted as intervals.

- `YYYY` with `year` precision covers `YYYY-01-01` through `YYYY-12-31`.
- `YYYY-MM` with `month` precision covers the first through last day of that month.
- `YYYY-MM-DD` with `day` precision covers that exact day.

A precision-aware comparison passes when an exact reference date falls inside the stored interval, or when two imprecise date intervals overlap. Tests should not treat imprecise dates as exact January 1 or month-start values except as interval boundaries.

Increasing precision after (manual) checks of dates is stored in `party_affiliation.csv` as well as relevant files under `test/data/`, and regular tests are implemented to ensure manually corrected data is not overwritten.

## Consequences

It becomes possible to test party affiliations with an appropriate level of precision.
