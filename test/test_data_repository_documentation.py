import json
import os
import re
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
REGISTRY_PATH = REPO_ROOT / "metadata" / "config" / "data-repositories.json"
REQUIRE_DATA_REPOS = os.environ.get("SWERIK_REQUIRE_DATA_REPOSITORIES") == "1"

REQUIRED_FILES = [
    "README.md",
    "CONTRIBUTING.md",
    "CITATION.cff",
    "LICENSE",
    "quality/README.md",
    "test/README.md",
]

README_REQUIREMENTS = {
    "states that the repository is a data repository": [
        r"\bdata repository\b",
        r"\bresearch data\b",
    ],
    "describes the repository contents": [
        r"\bcontains?\b",
        r"\bdata\b",
    ],
    "describes research purpose": [
        r"\bresearch\b",
        r"\bpurpose\b|\buse cases?\b|\bused? for\b",
    ],
    "describes temporal coverage and scope": [
        r"\bcoverage\b|\bscope\b",
    ],
    "describes provenance or source data": [
        r"\bprovenance\b|\bsource data\b|\bsources?\b",
    ],
    "describes where data files are located": [
        r"\bdata files?\b|\bdata/\b|\bfiles? are located\b",
    ],
    "describes how to download or install the data": [
        r"\bdownload\b|\binstall\b|\brelease\b",
    ],
    "describes how to use the data": [
        r"\bhow to use\b|\busage\b|\buse the data\b|\buse\b",
    ],
    "describes formats or schemas": [
        r"\bformat\b|\bschema\b|\bxml\b|\bcsv\b|\bjson\b",
    ],
    "links to quality documentation or status": [
        r"\bquality\b",
    ],
    "links to integrity-test documentation or status": [
        r"\btest\b|\bintegrity\b",
    ],
    "gives citation instructions": [
        r"\bcitation\b|\bcite\b|\bciting\b",
    ],
    "states license and reuse conditions": [
        r"\blicen[cs]e\b",
        r"\breuse\b|\bre-use\b|\buse conditions\b",
    ],
    "gives contribution instructions": [
        r"\bcontribut",
    ],
}


class DataRepositoryDocumentationTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        with REGISTRY_PATH.open(encoding="utf-8") as file:
            cls.data_repositories = json.load(file)

    def test_registry_is_well_formed(self):
        self.assertIsInstance(self.data_repositories, list)
        self.assertGreater(len(self.data_repositories), 0)

        names = [repo.get("name") for repo in self.data_repositories]
        self.assertEqual(len(names), len(set(names)), "Repository names must be unique.")

        for repo in self.data_repositories:
            with self.subTest(repo=repo.get("name")):
                for key in ("name", "github_url", "local_path", "description"):
                    self.assertIn(key, repo)
                    self.assertIsInstance(repo[key], str)
                    self.assertTrue(repo[key].strip())
                self.assertTrue(repo["github_url"].startswith("https://github.com/swerik-project/"))

    def test_data_repositories_follow_documentation_decision(self):
        existing_repos = []
        missing_repos = []

        for repo in self.data_repositories:
            repo_path = (REPO_ROOT / repo["local_path"]).resolve()
            if repo_path.exists():
                existing_repos.append((repo, repo_path))
            else:
                missing_repos.append((repo["name"], repo_path))

        if REQUIRE_DATA_REPOS and missing_repos:
            missing = "\n".join(f"- {name}: {path}" for name, path in missing_repos)
            self.fail(f"Expected all data repositories to exist locally:\n{missing}")

        if not existing_repos:
            self.skipTest("No sibling data repositories found to audit.")

        for repo, repo_path in existing_repos:
            failures = []
            missing_files = [
                relative_path
                for relative_path in REQUIRED_FILES
                if not (repo_path / relative_path).is_file()
            ]
            if missing_files:
                failures.append("missing files: " + ", ".join(missing_files))

            readme_path = repo_path / "README.md"
            if readme_path.is_file():
                readme = readme_path.read_text(encoding="utf-8").lower()
                readme = re.sub(r"\s+", " ", readme)

                missing_readme_requirements = []
                for requirement, patterns in README_REQUIREMENTS.items():
                    if not all(re.search(pattern, readme) for pattern in patterns):
                        missing_readme_requirements.append(requirement)

                if missing_readme_requirements:
                    failures.append(
                        "README missing: " + "; ".join(missing_readme_requirements)
                    )

            with self.subTest(repo=repo["name"]):
                self.assertEqual([], failures)


if __name__ == "__main__":
    unittest.main()
