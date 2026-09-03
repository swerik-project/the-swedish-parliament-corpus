"""
Template for SWERIK data integrity tests.

Copy this file into a corpus repository as test/test_<guarantee>.py and rename
the example names before use. Use importable Python module names with
underscores, not hyphens. The module docstring in the copied test should explain:

* what corpus guarantee the test checks
* why that guarantee matters
* what input, gold-standard, or reference data the test uses

See Decision 21 on writing unit tests for convensions.
"""
from pathlib import Path
import unittest

import polars as pl
from pyriksdagen.io import parse_tei
from pyriksdagen.utils import corpus_iterator, get_doc_dates, infer_metadata
from trainerlog import get_logger


LOGGER = get_logger(name="example-guarantee-integrity")

RESULTS_PATH = Path("test/results/example-guarantee-integrity.csv")
REFERENCE_PATH = Path("test/data/example-reference.csv")

# Replace this with the current-data baseline when the guarantee has known
# legacy failures. A thresholded test is still release-blocking: it blocks
# regressions beyond the accepted baseline. Define the counted unit clearly in
# the test docs and tighten the threshold in later curation PRs.
MAX_EXAMPLE_ERRORS = 0

# Defining the test error output schema
DIAGNOSTIC_SCHEMA = {
    "file": pl.Utf8,
    "error_type": pl.Utf8,
    "issue": pl.Utf8,
    "xml_id": pl.Utf8,
    "observed": pl.Utf8,
    "expected": pl.Utf8,
    "parliament_year": pl.Utf8,
}
SORT_COLUMNS = ["file", "error_type", "xml_id"]

# Module-level cache populated by example_errors(). unittest may run several
# assertions in one process; caching avoids repeating the same corpus scan.
# None means diagnostics have not been collected yet.
_EXAMPLE_ERRORS = None


def load_reference_data():
    """Load tabular reference data with Polars and preserve null values."""
    if not REFERENCE_PATH.exists():
        raise FileNotFoundError(
            f"Missing {REFERENCE_PATH}; add the fixture or update REFERENCE_PATH"
        )

    return (
        pl.read_csv(REFERENCE_PATH, try_parse_dates=True, infer_schema_length=10000)
        .filter(pl.col("reference_id").is_not_null())
    )


def collect_example_errors():
    """Collect one row per guarantee violation."""
    reference = load_reference_data()
    known_reference_ids = set(
        reference.select(pl.col("reference_id").cast(pl.Utf8))
        .get_column("reference_id")
        .to_list()
    )

    paths = list(corpus_iterator("records", corpus_root="data"))
    LOGGER.info("Checking example guarantee for %s records", len(paths))

    rows = []
    for path in paths:
        metadata = infer_metadata(path)
        parliament_year = metadata.get("sitting")
        root, _ = parse_tei(path)
        docdate_mismatch, docdates = get_doc_dates(root)

        if docdate_mismatch:
            rows.append(
                {
                    "file": path,
                    "error_type": "docdate_attribute_text_mismatch",
                    "issue": "docDate @when value differs from element text",
                    "observed": "; ".join(sorted(docdates)),
                    "expected": None,
                    "parliament_year": (
                        str(parliament_year) if parliament_year is not None else None
                    ),
                }
            )

        protocol_id = metadata.get("protocol")
        if protocol_id not in known_reference_ids:
            rows.append(
                {
                    "file": path,
                    "error_type": "missing_reference_row",
                    "issue": "protocol has no row in the reference fixture",
                    "observed": protocol_id,
                    "expected": "reference fixture row",
                    "parliament_year": (
                        str(parliament_year) if parliament_year is not None else None
                    ),
                }
            )

    return rows


def example_errors():
    """Return cached diagnostics as a stable Polars DataFrame."""
    global _EXAMPLE_ERRORS

    # Run the expensive corpus scan only once; later calls reuse the cached diagnostics.
    if _EXAMPLE_ERRORS is None:
        df = pl.DataFrame(collect_example_errors(), schema=DIAGNOSTIC_SCHEMA)
        df = df.sort([column for column in SORT_COLUMNS if column in df.columns])

        if len(df) > 0:
            RESULTS_PATH.parent.mkdir(parents=True, exist_ok=True)
            df.write_csv(RESULTS_PATH)

        _EXAMPLE_ERRORS = df

    return _EXAMPLE_ERRORS


class TestExampleGuaranteeIntegrity(unittest.TestCase):
    """Release-blocking checks for the example corpus guarantee."""

    def test_example_guarantee_has_no_unexpected_errors(self):
        """The example guarantee should not exceed the accepted baseline."""
        df = example_errors()
        self.assertLessEqual(
            len(df),
            MAX_EXAMPLE_ERRORS,
            (
                f"{len(df)} example guarantee error(s), exceeding baseline "
                f"{MAX_EXAMPLE_ERRORS}; see {RESULTS_PATH}"
            ),
        )


if __name__ == "__main__":
    unittest.main()
