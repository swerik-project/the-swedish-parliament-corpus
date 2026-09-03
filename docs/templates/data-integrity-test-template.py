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


from pathlib import Path
import unittest

import polars as pl
from pyriksdagen.io import parse_tei
from pyriksdagen.utils import corpus_iterator
from trainerlog import get_logger
from tqdm import tqdm


LOGGER = get_logger(name="example-reference-id-integrity")

REFERENCE_PATH = Path("test/data/example-reference.csv")

MAX_MISSING_REFERENCE_ROWS = 0


def format_error(row: dict[str, object]) -> str:
    """Format one diagnostic row for log and assertion output."""
    return " | ".join(f"{key}={value}" for key, value in row.items())


def log_errors(errors: list[dict[str, object]]) -> str:
    """Log diagnostic rows and return concise text for the assertion message."""
    if len(errors) == 0:
        return "no diagnostics"

    for row in errors:
        LOGGER.error(format_error(row))
    return "diagnostics logged with trainerlog"


class TestExampleGuaranteeIntegrity(unittest.TestCase):
    """Release-blocking checks for the example corpus guarantee."""

    def test_example_reference_ids_are_present_in_xml(self):
        """Guarantee: every XML document has a row in the example reference fixture.

        Why this matters: the reference fixture contains manually curated
        information that must cover each accepted corpus file. The test reads
        ``test/data/example-reference.csv`` with Polars and scans XML files under
        ``data/`` with ``pyriksdagen``. Unexpected null ``reference_id`` values
        in the fixture should fail clearly rather than being dropped or replaced.
        The accepted threshold is zero errors. Individual errors are logged with
        ``trainerlog``. A structured result file can be added later if logger
        output is not enough for review or follow-up curation work.
        """
        reference = pl.read_csv(REFERENCE_PATH, infer_schema_length=10000)
        null_reference_ids = reference.filter(pl.col("reference_id").is_null())
        self.assertEqual(
            null_reference_ids.height,
            0,
            f"{REFERENCE_PATH} has {null_reference_ids.height} null reference_id value(s)",
        )

        known_reference_ids = set(reference.get_column("reference_id").to_list())
        errors = []
        paths = sorted(corpus_iterator("records", corpus_root="data"))
        LOGGER.info("Checking example guarantee for %s records", len(paths))

        for path in tqdm(paths, desc="example guarantee"):
            root = parse_tei(path, get_ns=False)
            xml_id = root.get(f"{{http://www.w3.org/XML/1998/namespace}}id")
            if xml_id not in known_reference_ids:
                errors.append(
                    {
                        "file": path,
                        "xml_id": xml_id,
                        "issue": "XML document has no row in the reference fixture",
                        "expected": "reference fixture row",
                    }
                )

        details = log_errors(errors)
        self.assertLessEqual(
            len(errors),
            MAX_MISSING_REFERENCE_ROWS,
            (
                f"{len(errors)} missing reference row(s), exceeding baseline "
                f"{MAX_MISSING_REFERENCE_ROWS}; {details}"
            ),
        )


if __name__ == "__main__":
    unittest.main()
