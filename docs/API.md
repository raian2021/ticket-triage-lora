# API

Base URL: `http://localhost:8001`

## Endpoints

### POST /predict
Classifies a ticket and returns structured triage output.

#### Request
```json
{
  "ticket": "User cannot approve MFA prompt on new phone, sign-in blocked."
}

{
  "category": "Identity > MFA",
  "priority": "P3",
  "route_to": "Identity Team",
  "next_action": "Check Entra sign-in logs and user account settings; confirm MFA policy and remediation."
}



---

### C) `MODEL_CARD.md` (in repo root)
```bash
nano MODEL_CARD.md


# Model Card — Ticket Triage LoRA

## Summary
This project fine-tunes a base LLM using LoRA to output structured IT ticket triage decisions.

## Intended use
- Service desk triage assistance
- Routing suggestions
- Drafting next actions for common IT incidents

## Output schema
- `category`: string
- `priority`: string (e.g., P1–P4)
- `route_to`: string (team/queue)
- `next_action`: string (short actionable instruction)

## Data
- Training data lives in `data/` (format depends on your dataset pipeline).
- Ensure no sensitive/production customer data is committed.

## Limitations
- May hallucinate if ticket is vague or out-of-domain
- Output quality depends on coverage of training examples
- Should be reviewed before automated closure / irreversible actions

## Safety
Do not use to make security-impacting changes automatically.
Keep a human-in-the-loop for high-risk actions.

