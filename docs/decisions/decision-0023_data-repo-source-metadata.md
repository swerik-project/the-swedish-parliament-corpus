# Data repo source metadata

## Context

SWERIK data repositories need machine-readable metadata for several purposes:
catalogue harvesting, citation, publication, search indexing, research data
repositories, generated documentation, and release checks. The immediate need is
to publish DCAT-AP-SE metadata for dataportal.se and data.europa.eu, but the
same repository facts are also relevant for SND/DORIS, Dataverse, Schema.org
JSON-LD, README summaries, release pages, and other discovery or publication
workflows.

At the same time, the word "metadata" is already used in the corpus context for
metadata that belongs to the research data itself. Examples include person
metadata, party affiliations, document dates, identifiers, signatories,
chambers, sessions, XML attributes, CSV tables, and CSVW descriptions of public
tables. Users may analyze this metadata as part of their research.

We therefore need a clear distinction between:

- research data metadata, which is part of the corpus data model and is used by
  researchers;
- data repo source metadata, which describes a repository or released dataset as
  a publishable source for discovery, citation, catalogue harvesting, and
  archival workflows to alight with FAIR principles.

Keeping these concepts separate avoids confusing user-facing corpus metadata
with project/release metadata used by infrastructure.

## Decision

SWERIK distinguishes research data metadata from data repo source metadata.

Research data metadata is metadata that forms part of the data users analyze or
use to interpret the corpus. It may live in `metadata/`, `data/`, CSV files, XML
files, schemas, CSVW files, or other corpus-specific locations depending on the
repository. This decision does not change how research metadata is stored.

Data repo source metadata is metadata that describes a data repository or
released dataset as a source to be discovered, cited, harvested, published, and
archived. It includes facts such as title, description, publisher, contact
point, license, version, release date, landing page, repository URL, download
URLs, file formats, temporal coverage, languages, keywords, citation
information, quality documentation, test documentation, and related resources.

Each SWERIK data repository should store its canonical data repo source metadata
under:

```text
config/source-metadata/[repo-name].yml
```

For example:

```text
config/source-metadata/riksdagen-records.yml
config/source-metadata/riksdagen-persons.yml
config/source-metadata/riksdagen-motions.yml
```

The file name should match the repository name. This makes the file unambiguous
when metadata is copied, aggregated, validated, or used by the umbrella
repository.

The source metadata file should be the human-maintained source of truth for
repository-level publication metadata. Catalogue-specific and publication-
specific files should be generated from, or validated against, this source where
practical. Possible generated or validated outputs include:

- DCAT-AP-SE RDF/XML for dataportal.se harvesting;
- DCAT Turtle for human review and debugging;
- Schema.org JSON-LD for search engines;
- Dataverse metadata;
- SND/DORIS metadata;
- README and release-page metadata summaries;
- repository catalogues in the Swedish Parliament Corpus umbrella repository;
- other future catalogue, archive, or discovery formats.

Generated publication artifacts may be written to `docs/` when they are intended
to be served by GitHub Pages or another documentation site. For DCAT, the
recommended generated layout is:

```text
docs/dcat/[repo-name].rdf
docs/dcat/[repo-name].ttl
```

The RDF/XML file is the harvestable machine-facing artifact. The Turtle file is
for human review and debugging. Both should be treated as generated publication
artifacts unless a repository explicitly documents another maintenance model.

The `metadata/` directory should not be used for data repo source metadata when
that would conflict with research data metadata. Repositories may continue to use
`metadata/` for corpus-internal or research-facing metadata.

Source metadata files should use stable, absolute URLs and identifiers when they
describe public resources. For catalogue outputs, generated metadata should
avoid blank nodes for core resources such as catalogues, datasets,
distributions, publishers, and contacts.

## Consequences

The same repository facts can be reused across several publication workflows
instead of being copied into separate hand-maintained DCAT, Dataverse, SND,
README, and web-page files.

Users and maintainers get a clearer boundary between metadata that is part of
the research data and metadata that describes the repository as a source.
Researchers can continue to look for corpus-internal metadata in the data model,
while infrastructure code can look for publication metadata in
`config/source-metadata/`.

DCAT work for dataportal.se can start from
`config/source-metadata/riksdagen-records.yml` and generate
`docs/dcat/riksdagen-records.rdf` and `docs/dcat/riksdagen-records.ttl`. The
same pattern can later be reused for `riksdagen-persons`, `riksdagen-motions`,
and other SWERIK data repositories.

Release automation becomes responsible for keeping generated metadata current.
Tests should check that source metadata is valid, generated outputs are not
stale, required catalogue fields are present, public URLs are absolute, and
generated RDF avoids unsupported blank nodes.

Adding this source metadata layer introduces one more maintained file per data
repository, but it reduces drift across catalogues, citation files, release
pages, and documentation.
