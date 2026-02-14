# Evaluation Plan

## Goal
Measure whether the model reliably outputs correct JSON and improves triage accuracy vs baseline.

## Suggested tests
### 1) Schema correctness
- % responses that parse as valid JSON
- % responses that contain all required keys

### 2) Classification accuracy
For a labeled test set:
- Category accuracy
- Priority accuracy
- Route accuracy

### 3) Action quality (human review)
- Is `next_action` actionable?
- Is it safe (no destructive steps without confirmation)?
- Does it match internal playbooks?

## Minimal harness idea
- Create `data/test.jsonl` with `ticket`, `expected_category`, etc.
- Run predictions and compute accuracy + JSON parse rate.

