# Architecture

## High-level flow

Ticket text
  → Prompt builder
  → Tokenizer
  → Base model + LoRA adapter
  → Deterministic generation (temp=0, do_sample=False)
  → JSON extraction / validation
  → FastAPI response

## Components

### API (FastAPI)
- `POST /predict`
- Accepts: `{ "ticket": "<string>" }`
- Returns a strict JSON object: category, priority, route_to, next_action

### Inference
- Loads tokenizer + base model
- Loads PEFT LoRA adapter from `adapter_model/`
- Runs `generate()` with deterministic settings to reduce drift

### Output control
- Model is instructed to emit a JSON block
- Server extracts JSON tail after a delimiter (e.g. `JSON:`)
- Parser validates expected keys and returns clean JSON

## Why LoRA
LoRA fine-tunes a small number of adapter weights instead of updating the full model,
keeping training and iteration cheap while still adapting the model to a domain task.

