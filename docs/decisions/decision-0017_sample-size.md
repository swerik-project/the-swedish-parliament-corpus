# Sample size for Pull Requests

## Context
Previously we used a sample size of 50 to estimate quality of proposed changes to the corpus. Due to some mathematical wizardry, we estimate that we can reduce the sample size while still guaranteeing continued improvement to the corpus.

## Decision
On Pull Requests involving edits to data: 

 - author of PR draws a random sample of 20 edits to evaluate
 - author checks sample first before proposing PR with sample
 - 15 of 20 need to be correct edits in order to continue to a merge
 - author opens pr, posts sample, and assigns reviewer
 - reviewer checks sample & posts count of correct vs incorrect
 - if sample is good, author of PR merges PR
 
### reviewers

No one should review their own work. Reviewers should check for reviews assigned to them once per day and prioritize reviews -- do them ASAP b/c other work can depend on it.

| Author PR | Reviewer (primary / secondary)                           |
|-----------|-------------------------------------|
| Bob       | Väino / Erik                        |
| Erik      | Bob / Väinö                         |
| Väinö     | Bob / Erik                          |
| other     | Måns / Bob / Väinö assigns reviewer |

## Consequences
Checks on proposed edits to the corpus become more efficient.
