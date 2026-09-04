# Person data scope

## Context

The `riksdagen-persons` repository stores data about people, roles, and supporting authorities needed to work with the Swedish parliamentary corpus. The data is used to identify speakers, signatories, ministers, speakers of the Riksdag, governments, chairs, party affiliations, parties, mandate periods, parliamentary sessions, source references, and similar entities that appear in or are needed to interpret parliamentary records and related corpus documents.

Broader attributes (e.g. profession etc) may be useful for external research questions, but they are not within the scope of MPs engagement with the Riksdag in the same sense as names, mandate periods, party labels, parliamentary roles, or identifiers that allow users to map corpus persons to external authority data.

Because the persons data is part of the corpus API, adding broad biographical or social-media attributes increases maintenance cost, creates extra quality-control obligations, GDPR issues, and makes it less clear which information SWERIK treats as source-grounded parliamentary data.

## Decision

The `riksdagen-persons` data model should store only data that is directly relevant for representing, interpreting, mapping, validating, or documenting provenance for the parliamentary corpus.

The data does not need to be printed in the parliamentary proceedings themselves. It may come from parliamentary records, related corpus documents, official parliamentary sources, biographical source works, manually curated correction files, or stable external authority systems when the information is needed for corpus interpretation, disambiguation, validation, or provenance.

In practice, a field or table belongs in `riksdagen-persons` when it satisfies at least one of these criteria:

1. It is attested in parliamentary records or related corpus documents and is needed to represent those documents.
2. It is needed to map document text to a person, role, party, government, chamber, session, source, or other supporting authority in the corpus, for example names, location specifiers, party labels, mandate periods, ministerial roles, or speaker/chair roles.
3. It is needed for corpus data-integrity tests or quality estimation, for example dates used to validate that a person could hold a mandate, role, chair, or party affiliation.
4. It documents source provenance for corpus data, for example which source supports a person, role, date, affiliation, or manually curated correction.
5. It is a stable SWERIK identifier or stable external authority identifier that lets users join SWERIK persons or supporting authorities to richer external datasets.

Supporting authority tables are in scope when they are needed to interpret person data. This includes tables for parties, party labels and abbreviations, governments, chairs, parliamentary years, source references, and similar corpus-facing authorities. These tables may describe non-person entities, but they belong in this repository when they are necessary to interpret or validate person roles and affiliations in the corpus.

Attributes that are not needed for the corpus itself should not be stored as first-class person data. Instead, SWERIK should expose stable external identifiers so users can retrieve additional biographical, social, or contemporary information from external sources when their research question requires it.

Mutable, platform-specific, or broad enrichment attributes, such as social-media handles, portrait URLs, professions, education, family relations, or general biographical facts, should normally remain outside the core data model unless they are needed for corpus mapping, disambiguation, validation, or provenance. Existing tables in this category should be treated as legacy or transitional data until a separate decision either justifies keeping them, moves them to a more appropriate external-identifier/provenance model, or deprecates them.

### External identifiers

`external_identifiers.csv` is the preferred place for stable crosswalks to external authority systems. Its purpose is to support mapping, not to replicate arbitrary external data inside SWERIK.

External identifiers should be stable enough to support joins over time and should point users to richer sources such as Wikidata, Riksdagen identifiers, or other maintained authority datasets. Mutable or platform-specific attributes should normally remain outside the corpus even if they can be represented as identifiers elsewhere.

## Consequences

### Benefits

- Keeps `riksdagen-persons` focused on parliamentary-document interpretation rather than general biography.
- Reduces maintenance and quality-control obligations for attributes that are not source-grounded in the corpus.
- Makes the corpus API easier to explain to users and future contributors.
- Encourages external joins for research-specific enrichments instead of expanding the core data model.

### Costs

- Some downstream users may need to fetch non-corpus attributes from external sources instead of reading them directly from SWERIK.
- The boundary may need case-by-case interpretation for attributes that are not literally printed in records but are required for disambiguation, validation, or source provenance.
