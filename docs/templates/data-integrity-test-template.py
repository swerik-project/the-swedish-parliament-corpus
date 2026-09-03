"""
Template for SWERIK data integrity tests.

Copy this file into a corpus repository as ``test/test_<guarantee>.py`` and
rename the example names before use. Use importable Python module names with
underscores, not hyphens.

Keep data integrity test documentation in this file. The module docstring can
briefly describe the family of checks and shared reference data. Each test
function should document its own guarantee, motivation, input data, accepted
threshold, and logging or diagnostic output when applicable. Do not create a
separate Markdown documentation file for the test.

If another guarantee is added to this file, add another self-contained test
function with its own threshold. Scanning the same corpus again is fine when it
keeps tests independent and easy to follow. Add structured diagnostic files only
when they are specifically useful for review or follow-up curation work.
"""

import unittest
import polars as pl
from pyriksdagen.io import parse_tei
from pyriksdagen.utils import corpus_iterator
from trainerlog import get_logger
from tqdm import tqdm


LOGGER = get_logger(name="example-reference-id-integrity")

REFERENCE_PATH = "test/data/example-reference.csv"

MAX_NULL_REFERENCE_IDS = 0
MAX_MISSING_REFERENCE_ROWS = 0


class TestExampleGuaranteeIntegrity(unittest.TestCase):
    """Release-blocking checks for the example corpus guarantee."""

    def test_example_reference_fixture_has_no_null_reference_ids(self):
        """Guarantee: the example reference fixture has no null reference ids.

        Why this matters: the reference fixture contains manually curated
        identifiers used by later corpus checks. The test reads
        ``test/data/example-reference.csv`` with Polars and lets unexpected null
        values fail clearly rather than dropping or replacing them. The accepted
        threshold is zero null values. Summary diagnostics are logged with
        ``trainerlog``.
        """
        reference = pl.read_csv(REFERENCE_PATH, infer_schema_length=10000)
        null_reference_ids = reference.filter(pl.col("reference_id").is_null())

        if null_reference_ids.height > 0:
            LOGGER.error(
                "file=%s | issue=null reference_id value(s) in fixture | count=%s",
                REFERENCE_PATH,
                null_reference_ids.height,
            )

        self.assertEqual(
            null_reference_ids.height,
            MAX_NULL_REFERENCE_IDS,
            f"{REFERENCE_PATH} has {null_reference_ids.height} null reference_id value(s)",
        )

    def test_example_reference_ids_are_present_in_xml(self):
        """Guarantee: every XML document has a row in the example reference fixture.

        Why this matters: the reference fixture contains manually curated
        information that must cover each accepted corpus file. The test reads
        ``test/data/example-reference.csv`` with Polars and scans XML files under
        ``data/`` with ``pyriksdagen``. The accepted threshold is zero missing
        reference rows. Individual errors are logged with ``trainerlog``. A
        structured result file can be added later if logger output is not enough
        for review or follow-up curation work.
        """
        reference = pl.read_csv(REFERENCE_PATH, infer_schema_length=10000)
        known_reference_ids = set(reference.get_column("reference_id").to_list())
        missing_reference_rows = 0
        paths = sorted(corpus_iterator("records", corpus_root="data"))
        LOGGER.info("Checking example guarantee for %s records", len(paths))

        for path in tqdm(paths, desc="example guarantee"):
            root = parse_tei(path, get_ns=False)
            xml_id = root.get("{http://www.w3.org/XML/1998/namespace}id")
            if xml_id not in known_reference_ids:
                missing_reference_rows += 1
                LOGGER.error(
                    "file=%s | xml_id=%s | issue=missing reference fixture row",
                    path,
                    xml_id,
                )

        self.assertLessEqual(
            missing_reference_rows,
            MAX_MISSING_REFERENCE_ROWS,
            (
                f"{missing_reference_rows} missing reference row(s), exceeding "
                f"baseline {MAX_MISSING_REFERENCE_ROWS}; diagnostics logged "
                "with trainerlog"
            ),
        )


if __name__ == "__main__":
    unittest.main()
