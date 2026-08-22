# Data repo source metadata

## Context

SWERIK data repositories need machine-readable metadata for the repositories 
for several purposes:
catalogue harvesting, citation, publication, search indexing, research data
repositories, generated documentation, and release checks. The immediate need is
to publish DCAT-AP-SE metadata for dataportal.se and data.europa.eu, but the
same repository facts are also relevant for SND/DORIS, Dataverse, Schema.org
JSON-LD, README summaries, release pages, and other discovery or publication
workflows.

We therefore need a clear distinction between:

- research data, which is part of the corpus data model and is used by
  researchers;
- repository information, which describes a repository or released dataset as
  a publishable source for discovery, citation, catalogue harvesting, and
  archival workflows to align with FAIR principles.

Keeping these concepts separate avoids confusing user-facing corpus data
with project/release information used by infrastructure.

## Decision

Repository information is metadata that describes a repository or
released dataset as a source to be discovered, cited, harvested, published, and
archived. It includes facts such as title, description, publisher, contact
point, license, version, release date, landing page, repository URL, download
URLs, file formats, temporal coverage, languages, keywords, citation
information, quality documentation, test documentation, and related resources.

Each SWERIK data repository should store its canonical repository information under:

```text
docs/[repo-name]-info.yml
```

For example (in the `riksdagen-records` repo):

```text
docs/riksdagen-records-info.yml
```

The file name should match the repository name. This makes the file unambiguous
when metadata on the repo is copied, aggregated, validated, or used by the umbrella
repository.

The repository info file should use a common set of top-level slots. For
`riksdagen-records`, the initial file should contain a core set of slots that
can be expanded incrementally:

```yaml
metadata_type: repository_information
metadata_version: 1

repository:
  name: riksdagen-records
  url: https://github.com/swerik-project/riksdagen-records
  issue_tracker_url: https://github.com/swerik-project/riksdagen-records/issues

dataset:
  identifier: riksdagen-records
  title:
    en: "The Swedish Parliament Corpus: Riksdagen Records"
    sv: "Sveriges riksdagskorpus: Riksdagsprotokoll"
  description:
    en: ""
    sv: ""
  languages:
    - sv
  keywords:
    en: []
    sv: []
  type: dataset

publisher:
  name:
    en: Uppsala University
    sv: Uppsala universitet
  identifier: ""
  url: https://www.uu.se/

contact:
  name: ""
  url: ""

documentation:
  readme_url: https://github.com/swerik-project/riksdagen-records#readme

citation:
  cff_url: https://github.com/swerik-project/riksdagen-records/blob/main/CITATION.cff

relations:
  related_repositories:
    - https://github.com/swerik-project/riksdagen-persons
```

The exact values will be completed incrementally as needs is identified, but the top-level slots should
remain stable so tooling can validate and transform the file across
repositories. Empty strings and empty lists are acceptable while the first
metadata files are being drafted, but release automation should eventually fail
for required public-catalogue fields that are still empty.

The info file should be the human-maintained source of truth for
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

Repository info files should use stable, absolute URLs and identifiers when they
describe public resources. For catalogue outputs, generated metadata should
avoid blank nodes for core resources such as catalogues, datasets,
distributions, publishers, and contacts.

## Consequences

The same repository facts can be reused across several publication workflows
instead of being copied into separate hand-maintained DCAT, Dataverse, SND,
README, and web-page files.

Users and maintainers get a clearer boundary between repo info that is part of
the data and metadata that describes the repository as a source.
Researchers can continue to look for corpus-internal metadata in the data model,
while infrastructure code can look for publication metadata in
`docs`.

DCAT work for dataportal.se can start from
`docs/riksdagen-records-info.yml` and generate
`docs/dcat/riksdagen-records.rdf` and `docs/dcat/riksdagen-records.ttl`. The
same pattern can later be reused for `riksdagen-persons`, `riksdagen-motions`,
and other SWERIK data repositories.

Release automation becomes responsible for keeping generated repo information current.
Tests should check that source metadata is valid, generated outputs are not
stale, required catalogue fields are present, public URLs are absolute, and
generated RDF avoids unsupported blank nodes.

Adding this repository information layer introduces one more maintained file per data
repository, but it reduces drift across catalogues, citation files, release
pages, and documentation.
