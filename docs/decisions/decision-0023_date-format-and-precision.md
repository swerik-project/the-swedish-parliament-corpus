# Date format and precision

## Context

Decision 0015 introduced precision columns for party existence and party affiliation dates.

Issue https://github.com/welfare-state-analytics/riksdagen-corpus/issues/205 notes that the project had settled on ISO-style dates, but that this design choice was not documented. 

This decision amends decision 0015. Where this decision conflicts with decision 0015, this decision takes precedence.

## Decision

All date-like values in SWERIK corpus metadata should use the extended ISO 8601 profile described by W3C NOTE-datetime: https://www.w3.org/TR/NOTE-datetime.

Allowed date granularities are:

- `YYYY` for year precision, e.g. `1867`
- `YYYY-MM` for month precision, e.g. `1867-05`
- `YYYY-MM-DD` for day precision, e.g. `1867-05-14`

Datetime values should only be used when time is semantically part of the source data. When used, they should follow the same profile, e.g. `YYYY-MM-DDThh:mmTZD`, `YYYY-MM-DDThh:mm:ssTZD`, or a more precise timestamp with fractional seconds.

## Consequences

Date format is documented as a corpus-wide design choice rather than only a party-affiliation rule.

Downstream users can distinguish exact dates from reduced-precision dates without guessing whether placeholder month or day values are meaningful.

Existing data that uses `YYYY-01-01` or `YYYY-12-31` as reduced-precision placeholders may need migration rules, precision columns, or tests before it can be treated as conforming to this decision.
