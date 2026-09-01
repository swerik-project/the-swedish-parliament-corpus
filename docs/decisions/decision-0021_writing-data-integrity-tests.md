# Writing data integrity tests for corpus guarantees

## Context

Data integrity tests are part of the quality control process for SWERIK corpus repositories. Decision 0008 already says that data integrity tests should live in the repository where they are used, should be named after what they check, and should include documentation describing the test and testing process.

Recent review work has shown that we also need clearer guidance on how these tests should be written. In particular, a corpus release can contain mistakes if a curation step changes one part of the data but a derived or dependent annotation is not updated afterwards. For example, editing `note` or `seg` elements without rerunning speaker detection can leave speaker mappings stale even when the XML is still valid.

The purpose of this decision is not to define every corpus guarantee that should be tested. Those guarantees depend on the repository, document type, and curation task. Instead, this decision defines the style and minimum expectations for writing data integrity tests so that they are understandable, defensive, and useful as release-blocking checks.

## Decision

SWERIK data integrity tests should be written as semantic, documented, CI-runnable checks of corpus guarantees. They should be easy to understand, easy to debug when they fail, and suitable for preventing known classes of mistakes from entering a release.

Data integrity test files and test functions should have semantic names that describe what is checked. Names such as `test_speaker_mapping_integrity.py`, `test_docdate_sequence.py`, or `test_xml_id_references.py` are preferred. Names based only on issue numbers, such as `test_issue_46.py`, should be avoided.

Before adding a new data integrity test, contributors should check whether a test for the same corpus guarantee already exists. If it does, the existing test should normally be extended instead of creating a duplicate test. If a new test is still added because the guarantee is distinct, the difference should be clear from the test name and documentation.

Each data integrity test file should include a docstring or header explaining:

* what corpus guarantee the test checks
* why that guarantee matters
* what input data, gold-standard data, or reference data the test uses
* where fuller documentation lives, when a separate test description exists

Individual test functions should also have short docstrings when their purpose is not obvious from the function name.

Test failures should be readable and actionable. Assertion messages should explain what failed, how many failures were found when possible, and where detailed results can be inspected if the test writes result files.

Tests that scan many files or can produce more than a few failures should write structured diagnostic outputs to `test/results/`. These outputs should be suitable for review and follow-up curation work.

The `trainerlog` module should be used for logging progress, summaries, and diagnostic messages instead of ad hoc printing. Standard `unittest` output is sufficient only for small tests with one or a few clear assertions.

Data integrity tests must be included in the relevant CI workflow. A data integrity test is release-blocking when a failure should prevent a corpus revision or release from being accepted. 

Pull requests for release-blocking data integrity tests should normally demonstrate that the test fails in CI by temporarily committing a minimal intentional data error and then reverting that commit before merge. Keeping both the failing-data commit and the revert commit in the PR branch gives reviewers an auditable red-then-green record.

The central implementation template for new data integrity tests is [the data integrity test template](../templates/data-integrity-test-template.py) in the umbrella repository. Corpus repositories should use this template directly as the starting point for new data integrity tests. 

### Implementation checklist

When adding or modifying a data integrity test, contributors should check that:

* existing tests and test documentation have been checked for overlap, e.g. by introducing an error supposed to be caught by the new test and see if it is already captured by an existing test
* schema, primary-key, and foreign-key checks are delegated to CSVW metadata tests when possible
* new tests check a distinct semantic corpus guarantee rather than duplicating existing structural validation
* the file name describes the corpus guarantee being checked
* the module has a docstring explaining the guarantee, motivation, input data, and documentation link when applicable
* documentation links in module docstrings point to existing, current repository documentation or umbrella decisions
* test functions have semantic names
* test uses functionality from the `pyriksdagen` Python library if available
* new tabular CSV tests use `polars` unless there is a good reason not to
* libraries outside the central template's standard imports are added only when they remove real complexity, and the reason for each additional library is documented in the module docstring or near the import
* if a test imports `polars`, tabular reading, null filtering, date parsing, joins, selections, sorting, and CSV output are normally handled with `polars` expressions rather than row-wise Python code
* missing diagnostic values are represented as `None` or `polars` nulls, not as empty strings or other string sentinels
* dates remain typed as dates or datetimes until the final output boundary; repeated `strftime`/`strptime` calls inside corpus scan loops are avoided when `polars` or `pyriksdagen` can parse or format centrally
* diagnostic tables have a stable nullable schema, or normalize optional columns before sorting/writing, so the test works when there are zero failures or only some error categories are present
* test functions have docstrings when their purpose is not obvious from the name
* unnecessary object-oriented boilerplate is avoided; prefer module-level helper functions and a single data-collection function unless the test framework genuinely requires shared test state
* `unittest.TestCase` classes, when used for CI discovery, have semantic names and contain only the test assertions; corpus scanning and diagnostics should stay in module-level functions
* helper functions do real domain work or remove meaningful repetition; helpers that only wrap one obvious library call are avoided
* data structures match the guarantee being checked; use sets for unordered membership, lists or tuples only when order matters, and avoid canonicalization helpers unless the comparison genuinely needs them
* failures include actionable assertion messages
* large failure sets are written to `test/results/`
* tests that collect several related error categories prefer one diagnostics table with an `error_type` column over multiple per-error CSV files
* diagnostic tables are usually built with `polars` and sorted by stable review keys such as `file`, `error_type`, and relevant location columns before being written
* magic constants and repeated formatting inside scan loops are avoided; use named thresholds such as `MAX_SPAN_DAYS = 7` and format output values in one place when possible
* `trainerlog` is used for progress and diagnostics; progress bars and ad hoc printing are avoided in release-blocking CI tests unless there is a documented reason
* known exceptions, baselines, and transition allowances are explicit, narrow, and documented close to the assertion that uses them unless they are shared by several tests
* temporary or compatibility tests document what transition they protect and when the test, exception, or baseline can be removed or ratcheted down
* tests are included in CI/Github Actions
* the PR demonstrates, when practical, that the test fails in CI for a minimal intentional data error and passes again after that error is reverted

### Pre-review grep checklist

Before requesting review, contributors should run a quick search for common implementation smells:

```bash
rg 'import csv|csv\.DictReader|print\(|tqdm|strftime|strptime|FunctionTestCase|def load_tests|TestStringMethods' test
rg '= ""|: ""|return ""|get\([^,]+, ""\)' test
```

Matches are not automatically wrong. They should, however, be removed or justified before review. In particular, `csv.DictReader`, repeated date string conversion, generic test class names, custom `load_tests` glue, empty-string sentinels, progress bars, and ad hoc printing are common signs that a data integrity test should be simplified or moved toward `pyriksdagen`, `polars`, `trainerlog`, and the shared template.

## Consequences

**Pros**

* Data integrity tests become easier to understand, review, and maintain.
* Failing tests provide clearer information about what broke and where to start debugging.
* Tests are less likely to exist only as unused scripts, because release-blocking guarantees must be wired into CI.
* Corpus guarantees are expressed in a way that is understandable to both developers and data curators.

**Cons**

* Writing new tests takes more care, since naming, documentation, logging, and failure output need to be considered.
* Some existing tests may need gradual cleanup to match this style.
* CI workflows may need updates when a diagnostic test becomes a release-blocking guarantee.

## References

* [Decision 0008: How do document quality dimensions and data integrity tests](decision-0008_quality-dimensions.md)
* [Decision 0004: Handling manual corrections](decision-0004_handling-manual-corrections.md)
* [Issue 134: Decide on how to write data integrity tests in the corpus](https://github.com/swerik-project/the-swedish-parliament-corpus/issues/134)
* [riksdagen-records issue 46: Write defensive unit tests](https://github.com/swerik-project/riksdagen-records/issues/46)
