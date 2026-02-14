import json
import re
import torch
from fastapi import FastAPI
from pydantic import BaseModel
from transformers import AutoTokenizer, AutoModelForCausalLM
from peft import PeftModel

BASE_MODEL = "Qwen/Qwen2.5-0.5B-Instruct"
ADAPTER_DIR = "adapter_model"

app = FastAPI(title="Ticket Triage LoRA", version="0.1.0")

class TicketIn(BaseModel):
    ticket: str

def build_prompt(ticket: str) -> str:
    return (
        "You are an IT service desk triage classifier.\n"
        "Given a ticket, output STRICT JSON with keys:\n"
        "category, priority, route_to, next_action\n"
        "No extra text.\n\n"
        f"TICKET: {ticket}\n"
        "JSON:"
    )

def extract_json(text: str) -> dict:
    # Find first {...} block
    m = re.search(r"\{.*\}", text, flags=re.S)
    if not m:
        return {"error": "No JSON found", "raw": text}
    try:
        return json.loads(m.group(0))
    except Exception:
        return {"error": "Invalid JSON", "raw": m.group(0)}

def load_model():
    device = "mps" if torch.backends.mps.is_available() else ("cuda" if torch.cuda.is_available() else "cpu")

    tok = AutoTokenizer.from_pretrained(ADAPTER_DIR, use_fast=True)
    if tok.pad_token is None:
        tok.pad_token = tok.eos_token

    base = AutoModelForCausalLM.from_pretrained(
        BASE_MODEL,
        torch_dtype=torch.float16 if device in ("cuda", "mps") else torch.float32,
    )
    model = PeftModel.from_pretrained(base, ADAPTER_DIR)
    model.to(device)
    model.eval()
    return device, tok, model

DEVICE, TOKENIZER, MODEL = load_model()

@app.get("/health")
def health():
    return {"ok": True, "device": DEVICE}

@app.post("/predict")
def predict(inp: TicketIn):
    prompt = build_prompt(inp.ticket)
    inputs = TOKENIZER(prompt, return_tensors="pt").to(DEVICE)

    with torch.no_grad():
        out = MODEL.generate(
            **inputs,
            max_new_tokens=200,
            do_sample=False,
            temperature=0.0,
            pad_token_id=TOKENIZER.eos_token_id,
        )

    decoded = TOKENIZER.decode(out[0], skip_special_tokens=True)

    # Return only generated tail after "JSON:"
    tail = decoded.split("JSON:", 1)[-1].strip()

    parsed = extract_json(tail)

    return parsed

