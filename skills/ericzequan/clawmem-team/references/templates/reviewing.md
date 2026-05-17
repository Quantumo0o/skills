# Reviewing Template

Use this reference when the user wants a review-oriented Team built on top of ClawMem.

## Best fit

Use this template for:
- code review
- PR review
- design review
- architecture review
- policy or document inspection

## Design choices

Choose one of two tracking models:
- one-off review
  - best for occasional requests
  - lighter setup
- queue-backed review
  - best for repeated review intake
  - better when multiple reviewers rotate

## Recommended blueprint shape

Define:
- review requester
- lead reviewer or coordinating agent
- reviewer set
- review artifact location
- completion rule

## Bootstrap path

1. Confirm whether review work is one-off or recurring.
2. Create or reuse the repo that will store review requests.
3. Create or reuse the actors and access model.
4. Write the canonical review contract.
5. Seed one review request if the user wants a live demo.

## Minimal demo

One minimal demo should show:
1. create one review request
2. one reviewer records findings
3. a completion status is recorded
4. the result is visible from the chosen artifact
