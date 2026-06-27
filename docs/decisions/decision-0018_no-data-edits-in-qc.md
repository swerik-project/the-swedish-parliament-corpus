# Do not edit data in the quality control process

## Context

The Swedish Parliamentary Corpus is curated iteratively: changes are introduced as revision proposals, then evaluated (automated integrity tests and manual/statistical checks of sampled edits) before being accepted into the next released state.  

This workflow rely on a **revision proposals** step (where data/metadata changes are made and reviewed), and  **Quality control** (which *evaluates* proposals and decides accept/reject, but does not itself change the dataset).

If QC were allowed to directly edit data or metadata, the QC step would no longer be an independent evaluation of a proposal. It would also weaken traceability, since edits could be introduced outside the normal revision/PR pathway that documents rationale, review, and provenance. 

## Decision

During the quality control (QC) process:

1. **No edits may be made to corpus data**
2. **All data/metadata changes must be introduced via pull requests**
3. QC outputs may include **reports, annotations, and identified issues**, but any resulting data changes must be implemented as follow-up PRs.

## Consequences

**Pros**

  * Stronger independence of QC: QC remains an evaluation/verification step rather than a curation step. 
  * Clear provenance and reproducibility: every change is tied to a PR/revision with review history. Protects the iterative accept/reject model where quality is assessed on proposed edits. 

**Cons**

  * Small fixes discovered during QC become more tedious (must be logged and fixed via PR).
  * QC may surface “obvious” errors that cannot be immediately fixed; it requires an extra iteration.
