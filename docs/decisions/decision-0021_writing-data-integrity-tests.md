# How to write data integrity tests for corpus guarantees

## Context

Data integrity tests are part of the quality control process for SWERIK corpus repositories. Decision 0008 already says that data integrity tests should live in the repository where they are used, should be named after what they check, and should include documentation describing the test and testing process.

Although these checks may sometimes be discussed as "unit tests" in issues or pull requests, they are usually broader than ordinary code unit tests. 

Recent review work has shown that we also need clearer guidance on how these tests should be written. In particular, a corpus release can contain mistakes if a curation step changes one part of the data but a derived or dependent annotation is not updated afterwards. For example, editing `note` or `seg` elements without rerunning speaker detection can leave speaker mappings stale even when the XML is still valid.

The purpose of this decision is not to define every corpus guarantee that should be tested. Those guarantees depend on the repository, document type, and curation task. Instead, this decision defines the style and minimum expectations for writing data integrity tests so that they are understandable, defensive, and useful as release-blocking checks.

## Decision

SWERIK data integrity tests should be written as semantic, documented, CI-runnable checks of corpus guarantees. They should be easy to understand, easy to debug when they fail, and suitable for preventing known classes of mistakes from entering a release.

A data integrity test may scan a whole corpus or compare corpus data with a fixture, but it should still have a narrow, named guarantee and a small, readable implementation.

Data integrity test files and test functions should have semantic names that describe what is checked. For Python tests, use importable module names with underscores, such as `test_speaker_mapping_integrity.py`, `test_docdate_sequence.py`, or `test_xml_id_references.py`. Names based only on issue numbers, such as `test_issue_46.py`, should be avoided. Older generic wording such as `test-[what-is-checked].py` should be understood as a naming pattern, not as a recommendation to use hyphens in Python module names.

Before adding a new data integrity test, it should be checked whether a test for the same corpus guarantee already exists. If it does, the existing test should normally be extended instead of creating a duplicate test. If a new test is still added because the guarantee is distinct, the difference should be clear from the test name and documentation.

Each data integrity test file should include a docstring or header explaining:

* what general corpus guarantee the test checks
* why that guarantee matters
* what input data, gold-standard data, or reference data the test uses

Individual test functions should also have docstrings when their purpose is not obvious from the function name. The module docstring should describe the overall guarantee; function docstrings should describe only the more specific assertion made by that function, so documentation is less likely to drift when individual checks change.

Test failures should be readable and actionable. Assertion messages should explain what failed, how many failures were found when possible, and where detailed results can be inspected if the test writes result files.

Tests that scan many files or can produce more than a few failures should write structured diagnostic outputs to `test/results/`. These outputs should be suitable for review and follow-up curation work.

When a new data integrity test finds known current-data failures that are too large to fix in the same pull request, the test may use an explicit current-data threshold instead of failing immediately. This should only be done when the pull request or linked issue records the problem cases, a follow-up issue is open for fixing them, and later curation pull requests are expected to reduce the threshold.

A thresholded data integrity test is still a release-blocking hard gate. It blocks regressions beyond the accepted baseline and should normally be ratcheted down as known failures are fixed. The threshold should define the counted unit, such as rows, files, blocks, or unique ids, and the diagnostics, assertion message, and follow-up issue should use the same unit.

The `trainerlog` module should be used for logging progress, summaries, and diagnostic messages instead of ad hoc printing. Standard `unittest` output is sufficient only for small tests with one or a few clear assertions.

Data integrity tests must be included in the relevant CI workflow. A data integrity test is release-blocking when a failure should prevent a corpus revision or release from being accepted.

Pull requests for release-blocking data integrity tests should normally demonstrate that the test fails in CI by temporarily committing a minimal intentional data error and then reverting that commit before merge. Keeping both the failing-data commit and the revert commit in the PR branch gives reviewers an auditable red-then-green record.

The intentional data error must be minimal, clearly described in the pull request, and absent from the final corpus state. This red-then-green demonstration validates the test implementation before merge; it is not permission to leave test data broken or to change corpus data during quality control.

The central implementation template for new data integrity tests is [the data integrity test template](../templates/data-integrity-test-template.py) in the Swedish parliamentary corpus repository. Individual data repositories should use this template as a starting point and checklist, but should remove scaffolding that is not needed for the specific guarantee.

The preferred implementation is the smallest structured test that states the corpus guarantee directly: iterate over the relevant corpus files with `pyriksdagen`, parse the relevant structured data, collect the observations that violate the guarantee, and assert the accepted baseline. Extra layers such as custom caches, chunkers, worker pools, broad canonicalization pipelines, or multi-stage diagnostics should be avoided as much as possible, and only be added when they solve a concrete, documented problem.

For narrow guarantees, a readable loop inside one or two test methods can be clearer than a large collection framework. For expensive full-corpus scans, tests that share a scan across several assertions, or tests that produce large review outputs, use module-level collection functions so the corpus is scanned once and diagnostics are written consistently. In both cases, reviewers should be able to identify the code that checks the guarantee without following unrelated helper layers.

Data integrity tests should be written with human reviewers in mind, i.e. they should be kept short and easy to follow.

Data integrity tests should run sequentially and deterministically. Do not parallelize corpus scans in tests with threads, processes, async workers, or environment-controlled worker pools unless the pull request documents a measured CI/runtime problem and explains why the sequential implementation is insufficient. 

### Coding-agent implementation recipe

When a coding agent adds or modifies a data integrity test, it should normally:

1. Check existing tests and `test/docs/` for the same guarantee.
2. Extend an existing test when the guarantee is the same; create a new test only when the guarantee is distinct.
3. Start from the central template, then delete unused scaffolding.
4. Use `pyriksdagen` for corpus iteration, TEI parsing, metadata, and corpus helpers when the library has suitable functionality.
5. Parse XML/TEI with `pyriksdagen.io.parse_tei`, `lxml`, XPath, or direct element traversal, not with regular expressions or raw tag scans.
6. Use `polars` for CSV/TSV fixtures, joins, filtering, sorting, and diagnostics unless a different library clearly simplifies the implementation.
7. Write diagnostics only to `test/results/`, and keep diagnostics structured and stably sorted.
8. Keep scans sequential unless the pull request documents measured CI/runtime evidence for a more complex implementation.
9. Add actionable assertion messages that report counts and diagnostic file paths when applicable.
10. Wire release-blocking tests into the relevant CI workflow.
11. Run the pre-review grep checklist and either remove or justify remaining matches.

### Implementation checklist

When adding or modifying a data integrity test, contributors should check that:

* existing tests and test documentation have been checked for overlap, e.g. by introducing a minimal error that the new test should catch and seeing whether an existing test already catches it
* schema, primary-key, and foreign-key checks are delegated to CSVW metadata tests when possible
* new tests check a distinct semantic corpus guarantee rather than duplicating existing structural validation
* Python test file names use importable underscore names such as `test_<semantic_guarantee>.py`
* the file name describes the corpus guarantee being checked
* the module has a docstring explaining the guarantee, motivation, input data, and documentation links when applicable
* documentation links in module docstrings point to existing repo-local test documentation and relevant umbrella decisions when applicable
* test functions have semantic names
* the implementation starts from the simplest readable structured scan of the data, and only keeps template sections that the guarantee actually needs
* the test uses functionality from the `pyriksdagen` Python library if available
* structured corpus formats are parsed with the project-standard parser; XML/TEI should be parsed with `pyriksdagen.io.parse_tei`, `lxml`, or another explicit XML parser, not with regular expressions, string splitting, or raw text scans of tags and attributes
* XML traversal should prefer direct element traversal or XPath on the parsed tree; streaming parsers such as `lxml.iterparse` are used only when ordinary parsing is not practical for the corpus files being tested
* regular expressions may be used on extracted text content, but not to parse XML tags, attributes, nesting, or element boundaries.
* performance concerns do not justify bypassing XML parsing; use `pyriksdagen` iterators, `lxml.iterparse`, XPath or element traversal, narrower file selection, cached diagnostics, or CI partitioning instead
* tests are not parallelized by default; threads, processes, async workers, worker-count environment variables, and chunking for parallel execution need an explicit runtime justification in the pull request
* static data integrity tests do not invoke shell commands or depend on the repository being a Git checkout; avoid `subprocess`, `os.system`, `git grep`, `grep`, `rg`, `find`, and similar commands inside tests
* new CSV/TSV fixture and diagnostic tests use `polars` for reading and writing tabular data unless there is a good reason not to
* libraries outside the central template's standard imports are added only when they remove real complexity, and the reason for each additional library is documented in the module docstring or near the import
* tabular reading, null filtering, date parsing, joins, selections, sorting, and CSV output are normally handled with `polars` expressions rather than row-wise Python code
* missing diagnostic values are represented as `None` or `polars` nulls, not as empty strings or other string sentinels. Similarly, when `polars` is used to create a dataframe, `None` or `polars` nulls should be used.
* missing values from source data remain missing values throughout the test; do not turn nulls into empty strings just to simplify formatting or sorting
* dates remain typed as dates or datetimes until the final output boundary; repeated `strftime`/`strptime` calls inside corpus scan loops are avoided when `polars` or `pyriksdagen` can parse or format centrally
* diagnostic tables have a stable nullable schema, or normalize optional columns before sorting/writing, so the test works when there are zero failures or only some error categories are present
* test functions have docstrings when their purpose is not obvious from the name
* unnecessary object-oriented boilerplate is avoided; prefer module-level helper functions and a single data-collection function
* `unittest.TestCase` classes, when used for CI discovery, have semantic names and should be assertion-focused; direct scan loops are acceptable for simple one-pass checks, while shared corpus scanning and diagnostic writing should stay in module-level functions
* helper functions do real domain work or remove meaningful repetition; helpers that only wrap one obvious library call, split one attribute, copy a dictionary, or hide a short element traversal are avoided
* test should never edit/write data outside test/results
* data structures match the guarantee being checked; use sets for unordered membership, lists or tuples only when order matters, and avoid canonicalization helpers unless the comparison genuinely needs them
* text normalization is narrow, comparison-specific, and documented close to the code that uses it; Swedish letters and accents are preserved unless the tested guarantee explicitly needs accent-insensitive matching
* failures include actionable assertion messages
* large actionable failure sets are written to `test/results/`, while small failure sets stay in readable assertion messages
* tests that collect several related error categories prefer one diagnostics table with an `error_type` column over multiple per-error CSV files
* diagnostic tables are usually built with `polars` and sorted by stable review keys such as `file`, `error_type`, and relevant location columns before being written
* magic constants and repeated formatting inside scan loops are avoided; use named thresholds such as `MAX_SPAN_DAYS = 7` and format output values in one place when possible
* `trainerlog` is used for progress and diagnostics; progress bars and ad hoc printing are avoided in release-blocking CI tests
* known exceptions, baselines, and transition allowances are explicit, narrow, and documented close to the assertion that uses them unless they are shared by several tests
* current-data thresholds define the counted unit, such as rows, files, blocks, or unique ids; diagnostics, assertions, and follow-up issues should use the same unit
* temporary or compatibility tests (e.g. when waiting for functionality to go into pyriksdagen) document what transition they protect and when the test, exception, or baseline can be removed or ratcheted down
* tests are included in the existing relevant CI/Github Actions workflow unless a separate workflow has a distinct schedule, trigger, or dependency reason; the same release-blocking test should not be duplicated across workflows
* the PR demonstrates, when practical, that the test fails in CI for a minimal intentional data error and passes again after that error is reverted

### Pre-review grep checklist

Before requesting review, contributors should run a quick search for common implementation smells:

```bash
rg 'import csv|print\(|tqdm|strftime|strptime|FunctionTestCase|def load_tests|TestStringMethods' test
rg 'subprocess|Popen|os\.system|git grep|grep |rg |find |read_bytes|read_text' test
rg 're\.compile|re\.search|re\.finditer|xml:id=|who=|<[^>]+>' test
rg '= ""|: ""|return ""|get\([^,]+, ""\)' test
rg 'ThreadPoolExecutor|ProcessPoolExecutor|multiprocessing|asyncio|WORKERS|unicodedata|casefold|normalize|TODO|pass$' test
```

Matches are not automatically wrong. They should, however, be removed or justified before review. In particular, repeated date string conversion, generic test class names, custom `load_tests` glue, empty-string sentinels, progress bars, ad hoc printing, shell commands, Git-dependent scans, raw XML file reads, parallel execution scaffolding, broad Unicode normalization, placeholder tests, and regular expressions that inspect XML markup are common signs that a data integrity test should be simplified or moved toward direct `pyriksdagen`, `polars`, `trainerlog`, and parsed-XML code. The `re` module is not banned; regular expressions are acceptable for already-extracted text content when they do not replace structured parsing.

The grep checklist is a contributor review step outside the tests. It does not override the rule that static data integrity tests themselves should not invoke shell commands or depend on the repository being a Git checkout.

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
* [riksdagen-motions PR 109: motion signature integrity test review](https://github.com/swerik-project/riksdagen-motions/pull/109)
