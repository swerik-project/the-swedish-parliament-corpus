# Data repositories

`metadata/config/data-repositories.json` is the machine-readable list of SWERIK
repositories that contain data intended to be used as research data.

The list is maintained in the umbrella repository's metadata/configuration area
so project-level checks can audit whether each data repository follows the
documentation architecture decision in
`docs/decisions/decision-0022_documentation-architecture.md`.

Each entry contains:

- `name`: repository name.
- `github_url`: canonical GitHub repository URL.
- `local_path`: expected sibling path when the SWERIK repositories are checked
  out next to the umbrella repository.
- `description`: short description for humans and generated summaries.

When a new SWERIK research data repository is added, add it to this file and
make sure the repository README states that it is a data repository and covers
scope, research purpose, provenance, quality status, citation, reuse, and
contribution information.
