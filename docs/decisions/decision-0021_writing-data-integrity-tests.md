# How to write data integrity tests for corpus guarantees

## Relationship

This decision amends [Decision 0008](decision-0008_quality-dimensions.md) for data integrity tests. Data integrity test documentation belongs in the test file itself. Do not create or maintain separate data integrity test documentation in `test/docs/` or elsewhere. Existing external data integrity test documentation should be treated as legacy material until the useful content is moved into the relevant test file and the separate documentation is removed. This does not change the separate documentation conventions for quality estimations, issue drafts, or manual review artifacts.

Concrete coding-agent and contributor instructions and guidelines for applying this decision should live in the [Decision 0021 implementation guide](implementation-guides/decision-0021_writing-data-integrity-tests.md), so the formal decision can stay focused on the agreed policy.

## Context

Data integrity tests are part of the quality control process for SWERIK corpus repositories. Decision 0008 already says that data integrity tests should live in the repository where they are used, should be named after what they check, and should include documentation describing the test and testing process.


Recent review work has shown that we also need clearer guidance on how these tests should be written. In particular, a corpus release can contain mistakes if a curation step changes one part of the data but a derived or dependent annotation is not updated afterwards. For example, editing `note` or `seg` elements without rerunning speaker detection can leave speaker mappings stale even when the XML is still valid.

The purpose of this decision is not to define every corpus guarantee that should be tested. Those guarantees depend on the repository, document type, and curation task. Instead, this decision defines the style and minimum expectations for writing data integrity tests so that they are understandable, defensive, and useful as release-blocking checks.

## Decision

SWERIK data integrity tests should be written as semantic, documented, CI-runnable checks of corpus guarantees. They should be easy to understand, easy to debug when they fail, and suitable for preventing known classes of mistakes from entering a release.

When these goals conflict, contributors should prioritize them in this order:

1. Understandability and verifiability of the test code.
2. Understandability of error messages, logging, and output.
3. Performance.

Performance matters, especially for release-blocking corpus scans, but it should not be improved by making the tested guarantee harder to understand or verify unless there is a documented runtime problem.

A data integrity test may scan a whole corpus or compare corpus data with a fixture, but it should still have a narrow, named guarantee and a small, readable implementation.

For example, a speech corpus may have a "no dead man talking" guarantee: a speech dated after a person's recorded date of death should not be attributed to that person. The exact implementation depends on the available date and person metadata, but the guarantee is narrow, semantic, and easy to understand.

Each test function should check one corpus guarantee. Distinct guarantees should normally be separate test functions, even when they inspect the same files or reference data. It is acceptable for multiple tests to scan the same corpus separately when doing so makes each test smaller, more independent, and easier to review.

Data integrity test files and test functions should have semantic names that describe what is checked. For Python tests, use importable module names with underscores, such as `test_speaker_mapping_integrity.py`, `test_docdate_sequence.py`, or `test_xml_id_references.py`. Names based only on issue numbers, such as `test_issue_46.py`, should be avoided. Older generic wording such as `test-[what-is-checked].py` should be understood as a naming pattern, not as a recommendation to use hyphens in Python module names.

Before adding a new data integrity test, it should be checked whether a test for the same corpus guarantee already exists. If it does, the existing test should normally be extended instead of creating a duplicate test. If a new test is still added because the guarantee is distinct, the difference should be clear from the test name and in-test documentation.

Each data integrity test file should include a short docstring or header that identifies the family of checks in the file and any shared reference data. The authoritative documentation should live close to the individual test that uses it, in the same test file.

Individual test functions should normally have short docstrings with stable field headings, so a corpus guarantee catalog can be built without importing or running expensive tests. Each test function docstring must start with `Guarantee:`. Optional headings such as `Why this matters:`, `Data:` and `References:` may be added when they clarify the guarantee.

For example:

```python
def test_signature_who_values_are_unknown_or_known_person_ids(self):
    """Guarantee: every signature item has a valid ``@who`` value.

    Why this matters: invalid signature mappings make author-level analyses
    unreliable and can attribute motions to the wrong person or hide known
    signers from downstream users.

    Data: scans motion XML under ``data/`` and reads
    ``../riksdagen-persons/data/person.csv``.
    """
```

The docstring convention should remain plain text with field headings rather than YAML or frontmatter, so it stays readable in ordinary test files.

The module docstring should stay brief. Function-level documentation should describe the concrete assertion made by that function, so documentation is less likely to drift when individual checks change.

Test failures should be readable and actionable. Assertion messages should explain what failed, how many failures were found when possible, and that detailed rows were logged with `trainerlog`. If a test also writes a motivated result file, the assertion message should include its path.

Tests should start by logging observed errors with the `trainerlog` logger and reporting the failure clearly in the assertion message. A separate CSV or TSV diagnostic file should be added later only when logger output is not enough for a concrete review or follow-up curation use case.

When a new data integrity test finds known current-data failures that are too large to fix in the same pull request, the test may use an explicit current-data threshold instead of failing immediately. This should only be done when the pull request or linked issue records the problem cases, a follow-up issue is open for fixing them, and later curation pull requests are expected to reduce the threshold.

A thresholded data integrity test is still a release-blocking hard gate. It blocks regressions beyond the accepted baseline and should normally be ratcheted down as known failures are fixed. The threshold should define the counted unit, such as rows, files, blocks, or unique ids, and the logger output, assertion message, optional diagnostics, and follow-up issue should use the same unit.

The `trainerlog` module should be used for start/end summaries and diagnostic messages instead of ad hoc printing. Long corpus scans should use progress bars from known project dependencies such as tqdm. Standard `unittest` output is sufficient only for small tests with one or a few clear assertions.

Data integrity tests must be included in the relevant CI workflow.

The one writing the test should make the test fail locally by testing to change the data so the test turns red to prove that the test works as expected.

Concrete examples of corpus-guarantee tests include the `records docdate test` in `riksdagen-records/test/docdates.py` and the `persons mandates test` in `riksdagen-persons/test/mandates.py`. These are examples of this decision and can be used as a starting point for new tests.

The preferred implementation is the smallest structured test that states the corpus guarantee directly: iterate over the relevant corpus files with `pyriksdagen`, parse the relevant structured data, collect only the observations needed for that test's assertion, and assert the accepted baseline. Extra layers such as custom caches, chunkers, worker pools, broad canonicalization pipelines, combined error taxonomies, shared baseline dictionaries for independent guarantees, or multi-stage diagnostics should be avoided as much as possible, and only be added when they solve a concrete, documented problem.

Several implementation choices follow from this preferred shape:

* Prefer counters over diagnostic dataframes when the assertion only needs counts.
* Log failures at the point where they are found, instead of collecting generic error rows and formatting them later.
* Repeat simple reference loading in separate tests when that keeps each guarantee independent.
* Avoid shared `error_type` taxonomies for independent guarantees.
* Use the natural counted unit for the guarantee, such as duplicate signer blocks counting blocks rather than diagnostic rows.
* Helper functions are fine only for real domain logic, such as extracting a signature location, not for hiding a short scan or assertion.
* Helper functions and variables should be scoped as close as possible to the tests that use them.
* Variables should pay rent: they should significantly reduce repetition, name a meaningful domain value, or represent a value that should be changed centrally in the test.

When a test only needs a count, use a simple integer counter and log each failure where it is detected. Do not build a diagnostic dataframe, shared error taxonomy, or generic row formatter unless the test actually needs tabular output for a motivated review workflow.

Repeating small reference-data reads or corpus scans across test functions is acceptable when it keeps each guarantee self-contained. The preferred shape is close to the assertion: load the reference data needed by that guarantee, scan the relevant corpus files, log observed failures, and assert the guarantee's natural counted unit.

Data integrity tests should be written with human reviewers in mind, i.e. they should be kept short and easy to follow.

Data integrity tests should run sequentially and deterministically. Do not parallelize corpus scans in tests with threads, processes, async workers, or environment-controlled worker pools unless the pull request documents a measured CI/runtime problem and explains why the sequential implementation is insufficient. Note that you only get one core for CI.

## Consequences

**Pros**

* Data integrity tests become easier to understand, review, and maintain.
* Failing tests provide clearer information about what broke and where to start debugging.
* Tests are less likely to exist only as unused scripts, because release-blocking guarantees must be wired into CI.
* Corpus guarantees are expressed in a way that is understandable to both developers and data curators.

**Cons**

* Writing new tests takes more care, since naming, documentation, logging, and failure output need to be considered.
* Some existing tests may need gradual cleanup to match this style.

## References

* [Decision 0008: How do document quality dimensions and data integrity tests](decision-0008_quality-dimensions.md)
* [Decision 0004: Handling manual corrections](decision-0004_handling-manual-corrections.md)
* [Issue 134: Decide on how to write data integrity tests in the corpus](https://github.com/swerik-project/the-swedish-parliament-corpus/issues/134)
* [riksdagen-records issue 46: Write defensive unit tests](https://github.com/swerik-project/riksdagen-records/issues/46)
* [riksdagen-motions PR 109: motion signature integrity test review](https://github.com/swerik-project/riksdagen-motions/pull/109)
