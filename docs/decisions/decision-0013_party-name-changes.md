# decision 13: Handling party name changes

## Context

Some MP's party affiliations are over a time period when the party changed names or became a different party. Given that we implement a swerik ID for parties -- 1 ID per named party -- we need to decide how to handle these names in the `party_affiliation.csv` data.


## Decision

Store dates of name changes/dissolution of parties in `party.csv`. When a party dissolves / changes name during a mandate period, add a row for affected MPs with the new party.

- party affiliation at the time of election ends on the date (-1 day) of dissolution/name change 
- new / renamed party affiliation starts on the date of dissolution/name change 


## Consequences

We add rows to `party_affiliation.csv`. Data becomes more precise.
