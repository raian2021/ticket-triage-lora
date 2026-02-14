# Design decisions

## Why LoRA
Parameter-efficient fine-tuning to adapt an instruction model without full training cost.

## Why JSON output
Deterministic integration with systems (ServiceNow, Jira) and easy evaluation.

## Why Qwen2.5-0.5B-Instruct
Small enough to train and run locally; still strong instruction-following baseline.

## Data
Synthetic tickets used to create a consistent label space.
Documented as synthetic; in real usage replace with anonymised/approved historical tickets.
