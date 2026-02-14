import os
import torch
from datasets import load_dataset
from transformers import (
    AutoTokenizer,
    AutoModelForCausalLM,
    TrainingArguments,
    Trainer,
    DataCollatorForLanguageModeling,
)
from peft import LoraConfig, get_peft_model, TaskType

MODEL_NAME = "Qwen/Qwen2.5-0.5B-Instruct"

def format_example(ex):
    # Standard causal LM format: prompt + completion
    text = ex["prompt"] + ex["completion"]
    return {"text": text}

def main():
    ds = load_dataset("json", data_files={"train": "data/train.jsonl", "eval": "data/eval.jsonl"})
    ds = ds.map(format_example, remove_columns=ds["train"].column_names)

    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME, use_fast=True)
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token

    def tokenize(batch):
        return tokenizer(
            batch["text"],
            truncation=True,
            max_length=512,
            padding="max_length",
        )

    tokenized = ds.map(tokenize, batched=True)

    device = "mps" if torch.backends.mps.is_available() else ("cuda" if torch.cuda.is_available() else "cpu")

    model = AutoModelForCausalLM.from_pretrained(
        MODEL_NAME,
        torch_dtype=torch.float16 if device in ("cuda", "mps") else torch.float32,
    )
    model.to(device)

    lora = LoraConfig(
        task_type=TaskType.CAUSAL_LM,
        r=8,
        lora_alpha=16,
        lora_dropout=0.05,
        target_modules=["q_proj", "k_proj", "v_proj", "o_proj"],  # works for Qwen-style attention
    )
    model = get_peft_model(model, lora)
    model.print_trainable_parameters()

    args = TrainingArguments(
        output_dir="out",
        per_device_train_batch_size=1,
        per_device_eval_batch_size=1,
        gradient_accumulation_steps=8,
        num_train_epochs=2,
        learning_rate=2e-4,
        logging_steps=20,
        eval_strategy="steps",
        eval_steps=100,
        save_steps=100,
        save_total_limit=2,
        report_to="none",
        fp16=(device == "cuda"),  # mps fp16 training via Trainer can be flaky; keep false
    )

    collator = DataCollatorForLanguageModeling(tokenizer=tokenizer, mlm=False)

    trainer = Trainer(
        model=model,
        args=args,
        train_dataset=tokenized["train"],
        eval_dataset=tokenized["eval"],
        data_collator=collator,
    )

    trainer.train()

    # Save adapter + tokenizer
    model.save_pretrained("adapter_model")
    tokenizer.save_pretrained("adapter_model")
    print("Saved LoRA adapter to ./adapter_model")

if __name__ == "__main__":
    main()
