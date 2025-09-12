# Sample size for Pull Requests

## Context
Previously we used a sample size of 50 to estimate quality of proposed changes to the corpus. Due to some mathematical wizardry, we estimate that we can reduce the sample size while still guaranteeing continued improvement to the corpus (see Yrjänäinen and Magnusson 2025 [bibtex key: YrjanainenMagnusson2025]).

## Decision
On Pull Requests involving edits to data: 

 - author of PR draws a random sample of 20 edits to evaluate
 - author checks sample first before proposing PR with sample
 - 15 of 20 need to be incorrect --> correct edits
 - author opens pr, posts sample, and assigns reviewer
 - reviewer checks sample & posts count of correct vs incorrect
 - if sample is good, author of PR merges PR
 
### reviewers
No one should review their own work. PR authors should suggest a reviewer.

## Consequences
Checks on proposed edits to the corpus become more efficient.
