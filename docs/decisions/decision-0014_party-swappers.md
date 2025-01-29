# Decision 14: Swapping parties

## Context

It is possible for an MP to change parties during his/her mandate period.


## Decision

MPs who leave a party in the mandate period have two rows in `party_affiliation.csv`; one for the party they belonged to at the time of election, until the date the left (-1 day), and one indicating their new party affiliation or non-affiliation for the unaffiliated period. CF decision-0005 re MPs with no-party affiliation.


## Consequences

We add rows to `party_affiliation.csv`. Data becomes more precise.
