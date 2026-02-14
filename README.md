# 🔎 Ticket Triage LoRA
Fine-Tuned LLM for IT Incident Classification & Routing

---

## Overview

This project implements a LoRA fine-tuned Large Language Model (LLM)
designed to automatically classify IT service desk tickets into
structured routing decisions.

It converts raw natural language tickets into deterministic JSON outputs including:

- category
- priority
- route_to
- next_action

The model is served via FastAPI and can be consumed as an internal microservice.

---

## Problem

Manual IT ticket triage is:
- Time-consuming
- Inconsistent
- Difficult to scale
- Dependent on human expertise

This project demonstrates parameter-efficient fine-tuning (LoRA)
to adapt a base LLM for structured classification tasks.

---

## Architecture

User Ticket
    ↓
Prompt Builder
    ↓
LoRA Fine-Tuned Model
    ↓
Structured JSON Extraction
    ↓
FastAPI Endpoint (/predict)

---

## Tech Stack

- Python 3.11
- FastAPI
- Uvicorn
- HuggingFace Transformers
- PEFT (LoRA)
- PyTorch

---

## Project Structure

ticket-triage-lora/
├── src/
│   └── serve.py
├── adapter_model/
├── data/
├── requirements.txt
└── README.md

---

## Running Locally

1. Create virtual environment:

python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

2. Start API:

uvicorn src.serve:app --reload --port 8001

3. Test endpoint:

curl -X POST http://localhost:8001/predict \
  -H "Content-Type: application/json" \
  -d '{"ticket":"User cannot approve MFA prompt on new phone, sign-in blocked."}'

---

## Example Response

{
  "category": "Identity > MFA",
  "priority": "P3",
  "route_to": "Identity Team",
  "next_action": "Check Entra sign-in logs and user account settings; confirm MFA policy and remediation."
}

---

## Model Configuration

- temperature = 0.0
- do_sample = False
- Deterministic generation
- JSON post-processing extraction

This ensures reliable structured outputs suitable for automation.

---

## Future Improvements

- Add evaluation metrics (accuracy, F1 score)
- Add confidence scoring
- Add batch inference
- Deploy publicly
- Integrate with ticketing platforms
- Add monitoring & logging

---

## Purpose

This project demonstrates:

- Practical LLM fine-tuning
- Parameter-efficient adaptation (LoRA)
- Production-style API serving
- Structured output control
- Applied AI in IT operations

---

