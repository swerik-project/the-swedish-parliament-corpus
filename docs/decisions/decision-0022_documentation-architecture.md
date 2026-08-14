# Documentation architecture for SWERIK corpus repositories

## Context

The SWERIK project is distributed across several related repositories. Some repositories contain primary data, some contain metadata, some contain scripts or release coordination, and the umbrella repository points users to the wider corpus family. This makes documentation easy to duplicate and easy to let drift.

A data repository is a repository that contains data intended to be used as research data. The data may be primary corpus data or metadata. 

A data repository's README must explicitly state that it is a data repository and describe the data's scope, provenance, quality status, citation information, and reuse conditions.

We want each data repository to be understandable and reusable on its own, while keeping the Swedish Parliament Corpus repository useful as the first entry point for the project.

The decision is guided by the following documentation and data publication practices:

- GitHub recommends that a repository README explain what the project does, why it is useful, how users get started, where users can get help, and who maintains the project. It also notes that a README works together with a license, citation file, contribution guidelines, and code of conduct to set expectations for a project:
  <https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-readmes>.
- GitHub automatically surfaces `CONTRIBUTING.md` from `.github`, the repository root, or `docs`, and shows contribution links in pull requests, issues, the repository overview, and the repository sidebar:
  <https://docs.github.com/en/communities/setting-up-your-project-for-healthy-contributions/setting-guidelines-for-repository-contributors>.
- GitHub and the Citation File Format support `CITATION.cff` as a human- and machine-readable way to tell users how to cite a repository, including datasets:
  <https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-citation-files>
  and <https://citation-file-format.github.io/>.
- The FAIR principles emphasise persistent identifiers, rich metadata, searchable registration, standard access protocols, formal metadata languages, qualified links between datasets, clear licenses, provenance, and domain-relevant standards:
  <https://www.go-fair.org/fair-principles/>.
- DCAT is a W3C RDF vocabulary for describing datasets and data services in data catalogues. It supports discoverability, metadata aggregation, distributions, landing pages, licenses, versioning, checksums, and dataset series:
  <https://www.w3.org/TR/vocab-dcat-3/>.
- CSV on the Web provides a standard model for tabular data and metadata, which is useful for documenting CSV files in a machine-readable way:
  <https://www.w3.org/TR/tabular-data-model/>.

## Decision

Each SWERIK data repository must be documentation-wise standalone. A user who arrives directly at one repository should be able to understand what the data contains, whether it is suitable for their use, how to download it, how to cite it, how to inspect its quality, and how to contribute corrections without first reading another repository.

The Swedish Parliament Corpus repository is the project entry point and index. It should describe the corpus family, explain how the repositories relate to each other, link to the component repositories, show compatible versions, and point to project-level papers and resources. It should not duplicate component-specific documentation except for short summaries that are generated from, or clearly derived from, the component repositories.

Canonical human documentation for each repository should be stored in files that GitHub and users naturally discover:

- `README.md` in the repository root.
- `CONTRIBUTING.md` in the repository root.
- `CITATION.cff` in the repository root.
- `LICENSE` in the repository root.
- `quality/README.md` for quality-estimation documentation.
- `test/README.md` for integrity-test documentation.
- `docs/decisions/` for decisions.

Generated documentation may be published under `docs/` when needed for the project website, but generated files are outputs. They should not be the only manually maintained source of important documentation.

Quality documentation should be maintained through `quality/README.md`. The quality README should explain the available quality-estimation documentation, link to the individual QE documents, and describe how quality summaries, graphs, and release artefacts are produced or updated.

Integrity-test documentation should be maintained through `test/README.md`. The test README should explain what tests are run, how to run them, where the test files live, and how release or CI test summaries are produced or updated.

If the project website needs quality or test pages under `docs/`, those pages should be generated from `quality/README.md`, `test/README.md`, individual QE documents, test files, and release artefacts.

Each repository README should use the same basic structure, adjusted to the repository type:

- Explicit statement that the repository is a data repository, when applicable.
- What the repository contains.
- Temporal coverage and corpus scope.
- Provenance and source data.
- Compatibility with related repositories.
- Where the data files are located.
- How to download or install the data.
- How to use the data, including links to relevant software.
- Main file formats and schemas.
- Summary statistics that are generated during release when possible.
- Quality documentation and quality-estimation status.
- Integrity-test documentation and test status.
- Citation instructions.
- License and reuse conditions.
- Contribution instructions.
- Related repositories, papers, and project pages.

Machine-readable metadata should accompany human documentation:

- `CITATION.cff` is the canonical repository citation file.
- DCAT metadata should describe released datasets that should be discoverable in catalogues such as dataportal.se and data.europa.eu.
- CSV files that form part of the public data model should be documented with CSVW metadata.
- Metadata intended for SND, DORIS, Dataverse, or similar repositories should be derived from the same canonical project metadata where possible.

Documentation should follow these maintenance rules:

- Prefer one source of truth for each fact.
- Documentation generated from code, docstrings or other close-to-code sources should be preferred whenever possible.
- Link from overview pages to detailed pages instead of copying long sections.
- Each repository README should link to `quality/README.md` and `test/README.md` when those files exist, and should summarize rather than duplicate their contents.
- Keep contributor-facing workflows in `CONTRIBUTING.md`.
- Keep user-facing quick orientation in `README.md`.
- Keep quality and test details close to the code and data that produce them.
- Use relative links inside repositories when linking to files in the same repository.
- Validate links, citation metadata, release metadata, and generated summaries as part of release checks.
- Keep a machine-readable list of SWERIK data repositories in the umbrella repository and use automated tests to check that data repositories follow these documentation rules.

## Consequences

Users can understand and cite each dataset even if they arrive at a component repository from GitHub, Dataverse, SND, dataportal.se, data.europa.eu, a paper, or a search engine.

The umbrella repository becomes easier to maintain because it can act as a generated or lightly maintained index rather than a second copy of every component repository's documentation.

Repository maintainers have clearer rules for where to put new documentation. README files stay focused on orientation, contribution workflows live in `CONTRIBUTING.md`, quality and test details live with the relevant release machinery, and machine-readable metadata files support discovery and reuse.

Release automation becomes more important. Counts, versions, compatibility tables, quality summaries, test summaries, DCAT metadata, CSVW metadata, and Dataverse/SND metadata should be generated or validated so that documentation does not become stale.
