# Quality control for new data

## Context

The SWERIK project is maintaining corpora as iterative data object/states. For ordinary corrections to existing data, the current quality control process can sample edits from the difference between the proposed revision and the current corpus state. The sampled edits are then checked manually before the revision is accepted.

This edit-sampling procedure is not always meaningful when adding new data. A new parliamentary year, new document type, new batch of pages, or new source collection may not have a useful previous state to compare against. In these cases, the relevant question is not whether sampled edits are correct, but whether the newly ingested data is good enough to enter the corpus and support future quality estimation and curation.

At the same time, new data can introduce systematic errors through OCR, segmentation, classification, source linking, metadata extraction, or speaker/signatory mapping. Fully manual checking is not feasible, but new data should not be released without a clear acceptance process.

## Decision

When adding genuinely new corpus data where ordinary edit sampling is not meaningful, SWERIK should use unit-based quality control before release.

This decision applies to newly added corpus material, such as new parliamentary years, new batches of pages or documents, new document types, or new source collections similarly to a version 0.1 of a new corpus. It does not apply to corrections of existing data. Corrections should use the ordinary edit-sampling procedure unless another decision specifies a different procedure for clustered or ambiguous edits.

The default evaluation unit for records and OCR-derived material is the page. The page is preferred because it can be checked against a source image or PDF page. If page is not meaningful for a born-digital document or another document type, the smallest source-comparable unit should be used instead, such as a document or section. The evaluation unit must be declared before sampling.

Before manual review, new data must pass automated data-integrity tests. The relevant tests depend on the corpus and document type, but should include hard checks for:

- valid XML and schema conformance
- no duplicate files, IDs, or broken ID references
- required corpus API structure
- required metadata fields or columns
- source links to scans, PDFs, or other source material
- non-empty body text where source text exists
- no impossible person/date relations where metadata is linked
- no unexpected changes to existing released data

After the automated checks pass, a random sample of 20 units should be drawn from the new batch and manually checked against the original source. A sampled page or unit passes if:

- it links to the correct source page, PDF page, scan, or equivalent source unit
- the expected source text is present in the corpus file
- no substantial source text is missing
- the text is in broadly correct reading order
- the markup is sufficient to support later quality estimation and curation

Small deviations in page boundaries are acceptable if no text is missing and the source link is correct. This is especially important when page boundaries are inferred approximately from HTML or other born-digital sources while the PDF or scan defines the physical page split.

The new batch should be accepted if all 20 sampled units pass the basic inclusion check. If one or two sampled units contain only minor non-blocking problems, the batch may still be accepted if the problems are documented as an issue and clearly not systematic. A sampled unit should fail if it has a wrong source link, missing substantial text, an empty body where source text exists, or another error that prevents meaningful future quality estimation.

Acceptance sampling is not a replacement for quality estimation. For each substantial new data batch, the relevant gold standard should be expanded with examples from the new data when needed, and relevant quality estimates should be run or updated before release. However, it is ok to open an issue to fix the new gold standard at a later stage.

Quality imperfections that do not block inclusion should be documented as future curation issues. Examples include OCR errors, imperfect segmentation, unmapped speakers or signatories, approximate page breaks, uncertain but traceable metadata, and formatting variation in a period or source type.

Every new-data pull request should include a short quality-control note with:

- what data was added and from which source
- the sampling unit and manual sample result
- which automated integrity tests were run
- known non-blocking issues opened or linked for future curation

Adding new data in a backwards-compatible way should normally be treated as a minor version change. Adding new data in a way that changes the corpus API should be treated as a major version change. 

## Consequences

This creates a clear path for accepting new corpus material even when edit-level sampling is not meaningful. It keeps the existing release logic of automated tests, manual quality control, and versioned releases, but changes the sampling object from edits to source-comparable units.

The process makes it easier to add new parliamentary years and new document types without pretending that additions are ordinary corrections. It also makes new-data quality more transparent by requiring source links, sample results, quality-estimation updates, and issue tracking for known imperfections.

The process adds some work to new-data releases. Each substantial new batch needs declared sampling units, manual source comparison, and documentation of the result. Some borderline cases will also require judgement about whether an issue is blocking or should be logged for future curation.

This decision does not settle how to review clustered edits to existing data. That case should be handled in a separate decision.
