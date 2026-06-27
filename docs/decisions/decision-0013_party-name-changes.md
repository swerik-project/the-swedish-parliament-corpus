# Decision 13: Handling Party Name Changes

## Context

Some MP's party affiliations are over a time period when the party changed names or became a different party. Given that we implement a swerik ID for parties -- 1 ID per named party -- we need to decide how to handle these names in the `party_affiliation.csv` data.


## Decision

Represent party name changes and party dissolutions in `party_affiliation.csv`. When a party dissolves or changes name during a mandate period, add a row for affected MPs with the new party label and party ID.

- party affiliation at the time of election ends on the date (-1 day) of dissolution/name change 
- new / renamed party affiliation starts on the date of dissolution/name change 


## Consequences

We add rows to `party_affiliation.csv`. Data becomes more precise.
