# Dehyphenation
## Status

Decided

- Decision: accepted

## Context
In most corpora there is dehyphenation at line and page breaks. This is simply due to the layout of the page. At the same time we should try to be minimize the textual representation error as much as possible. 

## Decision
Dehyphenation due to line- or page breaks should be combined and the word that is dehyphenated should belong to the page/line where the word starts.

## Consequences
It might make it slightly more difficult to estimate OCR error rates from the original ALTO files since some processing might be needed.
