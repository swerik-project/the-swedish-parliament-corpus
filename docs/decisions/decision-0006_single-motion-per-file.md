# Single Motion per file (riksdagen-motions)


## Status

Decided

- Decision: accepted

## Context
In the motions source material there are two issues relating to clean curation of materials:

- motion documents can have trailing text from the previous motion and/or leading text from the following motion. This must be cleaned in order to (a) avoid duplicate text in the corpus, and (b) keep a clean metadata on an individual motion
- motion source files can also contain text that isn't part of the motion -- bihang, innehållsförteckning, förteckning, etc -- from the compendia of motions. This should be (re)moved as well


## Decision
Store only text and metadata about a single motion in its corresponding corpus file.

## Consequences
Cleaner corpus and facilitated data linking.
