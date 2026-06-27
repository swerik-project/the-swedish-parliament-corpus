# Link issues when a PR is opened, close them when the PR is merged

## Context

Issues are used to track work items and decisions, often broken down into actionable tasks (checklists, subtasks, or referenced TODOs). When the tasks in an issue are complete, the remaining work is typically reviewed and integrated through a pull request (PR).

Keeping issues open after implementation discussion has moved to a PR can create ambiguity about where review should happen. At the same time, closing issues as soon as a PR is opened can make the backlog look complete before the proposed change has been reviewed, passed checks, and merged.

To maintain a clean separation of responsibilities:

**Issues** describe and track *work to be done*.
**PRs** contain the proposed changes and serve as the place for review, discussion of implementation details, and final acceptance.

GitHub and GitLab both support the same general best-practice workflow (see references below): link the issue when the PR/MR is opened, and close the issue when the linked PR/MR is merged into the default branch. In GitHub, this can be automated with closing keywords such as `Fixes #123`, `Closes #123`, or `Resolves #123`.

## Decision

An issue should remain open until the work is merged, rejected, superseded, or explicitly deemed not planned.

When a PR is opened:

1. The issue must be linked from the PR.
2. If merging the PR will complete the issue, use a closing keyword in the PR description, for example `Fixes #123`, `Closes #123`, or `Resolves #123`.
3. If the PR only partially addresses the issue, use a non-closing reference such as `Refs #123`, and leave the issue open or split the remaining scope into follow-up issues.
4. Once the PR exists, ongoing implementation discussion, review feedback, and follow-up refinements should happen in the PR.
5. The issue or project item should be moved to an appropriate status such as `In review`, `PR opened`, or `On hold`, depending on the project board.

An issue should be closed when:

1. The linked PR has been merged into the default branch, or
2. The issue has been explicitly rejected, superseded, duplicated, or marked as not planned.

If new scope is discovered after an issue is closed, open a new issue, or re-open the original only if it truly represents unfinished work rather than new work.

## Consequences

**Pros**

  * Backlog stays accurate: open issues represent actual unfinished work.
  * Clear handoff: implementation discussion moves from “planning/tracking” (issue) to “review/merge” (PR).
  * Merge status remains the source of truth for whether the proposed change has actually landed.
  * Reduces duplicated coordination and status churn.
  * Supports GitHub's automatic issue-closing workflow.

**Cons**

  * Some issues remain open while the remaining work is review/merge rather than implementation; this should be handled with project status fields.
  * PR authors need to choose closing keywords carefully, especially when a PR only partially addresses an issue.

## References

* [GitHub Docs: Linking a pull request to an issue](https://docs.github.com/en/issues/tracking-your-work-with-issues/using-issues/linking-a-pull-request-to-an-issue)
* [GitHub Docs: About pull requests](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/about-pull-requests)
* [GitHub Docs: Best practices for Projects](https://docs.github.com/en/issues/planning-and-tracking-with-projects/learning-about-projects/best-practices-for-projects)
* [GitLab Docs: Managing issues](https://docs.gitlab.com/user/project/issues/managing_issues/)
