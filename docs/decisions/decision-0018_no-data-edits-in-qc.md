# Do not edit data in the quality control process

## Context

The Swedish Parliament Corpus is curated iteratively: changes are introduced as revision proposals, then evaluated (automated integrity tests and manual/statistical checks of sampled edits) before being accepted into the next released state.

This workflow relies on a **revision proposals** step (where data/metadata changes are made and reviewed), and **quality control** (which *evaluates* proposals and decides accept/reject, but does not itself change the dataset).

If QC were allowed to directly edit data or metadata, the QC step would no longer be an independent evaluation of a proposal. It would also weaken traceability, since edits could be introduced outside the normal revision/PR pathway that documents rationale, review, and provenance. 

Before manual quality control begins, errors may be fixed in the same PR as part of preparing the revision proposal. Once the QC sample has been drawn, however, the proposal should be treated as fixed. This preserves the logic of decision 0017, where PRs involving data edits are evaluated through a sampled edit check.

## Decision

During quality control (QC):

1. No edits may be made to corpus data or corpus metadata.
2. Data and metadata changes must be introduced through revision PRs.
3. QC may update QC artifacts, including review notes, sampled-edit assessments, reports, quality estimates, test results, plots, and issue lists.
4. Errors found during QC must be fixed in a follow-up PR, or by restarting the current revision PR before QC is rerun.
5. If corpus data or metadata changes after the QC sample has been drawn, the QC result is invalid and the sample/check must be rerun.

## Consequences

**Pros**

  * Stronger independence of QC: QC remains an evaluation/verification step rather than a curation step. 
  * Clear provenance and reproducibility: every change is tied to a PR/revision with review history. Protects the iterative accept/reject model where quality is assessed on proposed edits. 
  * The sampled edit check in decision 0017 remains meaningful because the checked proposal is the same proposal that is accepted or rejected.

**Cons**

  * Small fixes discovered during QC become more tedious (must be logged and fixed via PR).
  * QC may surface “obvious” errors that cannot be immediately fixed; it requires an extra iteration.
  * If data changes after QC has started, manual checks may need to be repeated.
