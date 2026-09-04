# How to write data integrity tests for corpus guarantees

Here details are included on how to implement decision 21. This guidelines and instructions are for both coding agents and new persons that want help with how to write these type of unit tests.

For narrow guarantees, a readable loop inside the test method can be clearer than a large collection framework. Multiple simple scans are preferable to a shared collection framework when the shared framework makes the tests less independent. Helper functions should be nested close to the code that uses them: inside the test method when used by one test, on the test class when shared by multiple test methods in that class, and at module level only when shared across classes or when they express common domain logic used throughout the suite. Variables and constants should follow the same scoping rule. Current-data thresholds that reviewers are expected to ratchet down are a good example of central variables: define them as named module-level constants in a small baseline block, not as a shared dictionary for independent guarantees. Abstraction for abstraction's sake should be avoided, because it reduces readability and increases code surface area. Reviewers should be able to identify the code that checks the guarantee without following unrelated helper layers.


### Coding-agent implementation recipe

When a coding agent adds or modifies a data integrity test, it should normally:

1. Check existing tests and their docstrings for the same guarantee.
2. Extend an existing test only when the guarantee is the same; create a separate test function when the guarantee is distinct.
3. Start from the central template, then delete unused scaffolding.
4. Use `pyriksdagen` for corpus iteration, TEI parsing, metadata, and corpus helpers when the library has suitable functionality.
5. Parse XML/TEI with `pyriksdagen.io.parse_tei`, `lxml`, not with regular expressions or raw tag scans.
6. Use `polars` for CSV/TSV fixtures, joins, filtering, sorting, and diagnostics unless a different library clearly simplifies the implementation.
7. Log summaries and observed errors with `trainerlog`; use a `tqdm` progress bar for long corpus scans; add structured diagnostics to `test/results/` only when a separate file is motivated by review or follow-up curation needs, and keep written diagnostics scoped to one test or guarantee.
8. Keep scans sequential unless the pull request documents measured CI/runtime evidence for a more complex implementation.
9. Add actionable assertion messages that report counts, say that details were logged, and include diagnostic file paths only when the test writes a motivated result file.
10. Wire release-blocking tests into the relevant CI workflow.
11. Run the pre-review grep checklist and either remove or justify remaining matches.

### Implementation checklist

When adding or modifying a data integrity test, contributors should check that:

* existing tests and their docstrings have been checked for overlap, e.g. by introducing a minimal error that the new test should catch and seeing whether an existing test already catches it
* schema, primary-key, and foreign-key checks are delegated to CSVW metadata tests when possible
* new tests check a distinct semantic corpus guarantee rather than duplicating existing structural validation
* each test function checks one corpus guarantee
* distinct corpus guarantees are kept in separate test functions, even when they scan the same files
* the module has a brief docstring explaining the broad family of checks and any shared input data, but is not so specific that it must be rewritten whenever a new individual guarantee is added
* test-function docstrings start with `Guarantee:`
* optional test-function docstring headings such as `Why this matters:`, `Data:` and `References:` are used when they clarify the guarantee
* data integrity test documentation is kept in the test file itself; do not create separate Markdown documentation under `test/docs/` for new data integrity tests
* test functions have semantic names
* the implementation starts from the simplest readable structured scan of the data, and only keeps template sections that the guarantee actually needs
* repeated simple corpus scans are accepted when they keep individual tests independent and easy to follow
* the test uses functionality from the `pyriksdagen` Python library if available
* structured corpus formats are parsed with the project-standard parser; XML/TEI should be parsed with `pyriksdagen.io.parse_tei`, `lxml`, or another explicit XML parser (if `lxml` is not sufficient), not with regular expressions, string splitting, or raw text scans of tags and attributes
* XML traversal should prefer direct element traversal or XPath on the parsed tree; streaming parsers such as `lxml.iterparse` are used only when ordinary parsing is not practical for the corpus files being tested
* regular expressions may be used on extracted text content, but not to parse XML tags, attributes, nesting, or element boundaries.
* performance concerns do not justify bypassing XML parsing; use `pyriksdagen` iterators, `lxml.iterparse`, XPath or element traversal, narrower file selection, or CI partitioning instead
* tests are not parallelized by default; threads, processes, async workers, worker-count environment variables, and chunking for parallel execution need an explicit runtime justification in the pull request
* static data integrity tests do not invoke shell commands or depend on the repository being a Git checkout; avoid `subprocess`, `os.system`, `git grep`, `grep`, `rg`, `find`, and similar commands inside tests
* new CSV/TSV fixture and diagnostic tests use `polars` for reading and writing tabular data unless there is a good reason not to
* imports are grouped and written plainly so the test dependencies are easy to read and documented if needed
* tabular reading, null checks, date parsing, joins, selections, and sorting are normally handled with `polars` expressions rather than row-wise Python code; CSV output should also use `polars` when a test writes an optional diagnostic file
* missing diagnostic values are represented as `None` or `polars` nulls, not as empty strings or other string sentinels. Similarly, when `polars` is used to create a dataframe, `None` or `polars` nulls should be used.
* missing values from source data remain missing values throughout the test; do not use options such as `null_values=[""]` to override source parsing, do not drop nulls by default, and do not turn nulls into empty strings just to simplify formatting or sorting
* dates remain typed as dates or datetimes until the final output boundary; repeated `strftime`/`strptime` calls inside corpus scan loops are avoided when `polars` or `pyriksdagen` can parse or format centrally
* test functions have docstrings when their purpose is not obvious from the name
* unnecessary object-oriented boilerplate is avoided; prefer straightforward test methods and small helper functions only when they remove meaningful repetition
* `unittest.TestCase` classes, when used for CI discovery, have semantic names and should be assertion-focused; direct scan loops are acceptable and often preferred for simple one-pass checks
* `subTest`, shared collectors, shared caches, and shared threshold dictionaries are not used to combine independent guarantees into one test
* helper functions do real domain work or remove meaningful repetition; helpers that only wrap one obvious library call, split one attribute, copy a dictionary, or hide a short element traversal are avoided
* helper functions are scoped as close as possible to the tests that use them: inside one test method when used by one test, on the test class when shared by multiple methods in that class, and at module level only when shared across classes or across the suite
* variables and constants are scoped as close as possible to the tests that use them
* variables and constants pay rent by significantly reducing repetition, naming a meaningful domain value, or representing a value that should be changed centrally in the test
* current-data thresholds that should be ratcheted down are a good example of central variables and may be module-level named constants
* tests normally should not write data; if a test writes a motivated diagnostic file, it should not write outside `test/results`
* data structures match the guarantee being checked; use sets for unordered membership, lists or tuples only when order matters, and avoid canonicalization helpers unless the comparison genuinely needs them
* failures include actionable assertion messages
* tests start by logging observed errors with `trainerlog` and keep assertion messages readable and actionable
* structured diagnostics in `test/results/` are added only when a separate file is motivated by review or follow-up curation needs
* magic constants and repeated formatting inside scan loops are avoided; use named thresholds such as `MAX_SPAN_DAYS = 7` and format output values in one place when possible
* `trainerlog` is used for summaries and diagnostics, progress bars from known project dependencies such as `tqdm` are used for long scans, and ad hoc printing is avoided in release-blocking CI tests
* known exceptions, baselines, and transition allowances are explicit, narrow, and documented close to the assertion that uses them
* current-data thresholds define the counted unit, such as rows, files, blocks, or unique ids; logger output, assertions, optional diagnostics, and follow-up issues should use the same unit
* temporary or compatibility tests (e.g. when waiting for functionality to go into pyriksdagen) document what transition they protect and when the test, exception, or baseline can be removed or ratcheted down
* tests are included in the existing relevant CI/Github Actions workflow unless a separate workflow has a distinct schedule, trigger, or dependency reason; the same release-blocking test should not be duplicated across workflows
* the PR demonstrates, when practical, that the test fails in CI for a minimal intentional data error and passes again after that error is reverted

### Pre-review grep checklist

Before requesting review, contributors should run a quick search for common implementation smells:

```bash
rg 'import csv|print\(|strftime|strptime|FunctionTestCase|def load_tests|TestStringMethods' test
rg 'subprocess|Popen|os\.system|git grep|grep |rg |find |read_bytes|read_text' test
rg 're\.compile|re\.search|re\.finditer|xml:id=|who=|<[^>]+>|subTest|ERROR_BASELINES' test
rg '= ""|: ""|return ""|get\([^,]+, ""\)|null_values|drop_nulls|fill_null|fill_nan' test
rg 'ThreadPoolExecutor|ProcessPoolExecutor|multiprocessing|asyncio|WORKERS|unicodedata|casefold|normalize|TODO|pass$' test
```

Matches are not automatically wrong. They should, however, be removed or justified before review. In particular, repeated date string conversion, generic test class names, custom `load_tests` glue, shared `subTest` blocks for independent guarantees, shared baseline dictionaries, common diagnostics for several guarantees, empty-string sentinels, null override/drop/fill shortcuts, ad hoc printing, shell commands, Git-dependent scans, raw XML file reads, parallel execution scaffolding, broad Unicode normalization, placeholder tests, and regular expressions that inspect XML markup are common signs that a data integrity test should be simplified or moved toward direct `pyriksdagen`, `polars`, `trainerlog`, and parsed-XML code. The `re` module is not banned; regular expressions are acceptable for already-extracted text content when they do not replace structured parsing.

The grep checklist is a contributor review step outside the tests. It does not override the rule that static data integrity tests themselves should not invoke shell commands or depend on the repository being a Git checkout.
