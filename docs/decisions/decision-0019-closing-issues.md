# Close issues when tasks are done, and a PR has been opened

## Context

Issues are used to track work items and decisions, often broken down into actionable tasks (checklists, subtasks, or referenced TODOs). When the tasks in an issue are complete, the remaining work is typically reviewed and integrated through a pull request (PR).

Keeping issues open after all tasks are done creates ambiguity about whether more work is expected in the issue itself, duplicates coordination effort (status updates in both issue and PR), and makes it harder to interpret the project’s backlog and throughput.

To maintain a clean separation of responsibilities:

**Issues** describe and track *work to be done*.
**PRs** contain the proposed changes and serve as the place for review, discussion of implementation details, and final acceptance.

## Decision

An issue should be **closed** when:

1. **All tasks in the issue are completed**, and
2. **A pull request has been opened** that implements (or will implement) the work described.

Additional rules:

* The issue must be linked from the PR (e.g., using “Fixes #123” / “Closes #123” or an explicit reference).
* Ongoing discussion, review feedback, and follow-up refinements should happen in the PR once it exists.
* If a new scope is discovered after closing an issue, open a **new issue** (or re-open the original only if it truly represents unfinished work rather than new work).

## Consequences

**Pros**

  * Backlog stays accurate: open issues represent actual unfinished work.
  * Clear handoff: work moves from “planning/tracking” (issue) to “review/merge” (PR).
  * Reduces duplicated coordination and status churn.

**Cons**

  * Some work may still be pending (review/merge) even though the issue is closed; this shifts responsibility for tracking remaining steps to the PR.
