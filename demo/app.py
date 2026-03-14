# Agent 1.0: Coding Intelligence
# Developed by Suryanshu Nabheet
# Copyright (c) 2026 Agent AI. All rights reserved.
#
# Licensed under the MIT License. See LICENSE for details.

import os
from threading import Thread
from typing import Iterator

import gradio as gr
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, TextIteratorStreamer

MAX_MAX_NEW_TOKENS = 2048
DEFAULT_MAX_NEW_TOKENS = 1024

MAX_INPUT_TOKEN_LENGTH = int(os.getenv("MAX_INPUT_TOKEN_LENGTH", "4096"))

DESCRIPTION = """\
# Agent 1.0: Coding Intelligence
Built by **Suryanshu Nabheet**, Agent 1.0 is a specialized coding assistant designed for production-grade software development. 
"""

# Configuration
LOCAL_MODEL_PATH = "local_model"
DEFAULT_MODEL = "agent-ai/agent-1.0-1.3b-instruct" # Fallback if local is empty

if os.path.exists(LOCAL_MODEL_PATH) and any(f.endswith(('.bin', '.safetensors', '.json')) for f in os.listdir(LOCAL_MODEL_PATH)):
    model_id = LOCAL_MODEL_PATH
else:
    model_id = os.getenv("MODEL_ID", DEFAULT_MODEL)

BRAND_NAME = "Agent 1.0"
FOUNDER = "Suryanshu Nabheet"

if torch.backends.mps.is_available():
    device = "mps"
    dtype = torch.float16
elif torch.cuda.is_available():
    device = "cuda"
    dtype = torch.bfloat16
else:
    device = "cpu"
    dtype = torch.float32

if device == "mps":
    DESCRIPTION += f"\n<p>Running on Apple Silicon (MPS)  Loading {BRAND_NAME}</p>"
elif device == "cuda":
    DESCRIPTION += f"\n<p>Running on GPU  Loading {BRAND_NAME}</p>"
else:
    DESCRIPTION += f"\n<p>Running on CPU  This may be slow. Loading {BRAND_NAME}</p>"

print(f"Loading model {model_id} on {device}...")

model = AutoModelForCausalLM.from_pretrained(
    model_id, 
    torch_dtype=dtype, 
    device_map="auto" if device != "cpu" else None,
    trust_remote_code=True
)
tokenizer = AutoTokenizer.from_pretrained(model_id, trust_remote_code=True)

if device == "cpu":
    model = model.to(device)

def generate(
    message: str,
    chat_history: list,
    system_prompt: str,
    max_new_tokens: int = 1024,
    temperature: float = 0.6,
    top_p: float = 0.9,
    top_k: int = 50,
    repetition_penalty: float = 1,
) -> Iterator[str]:
    conversation = []
    if system_prompt:
        conversation.append({"role": "system", "content": system_prompt})
    for user, assistant in chat_history:
        conversation.extend([{"role": "user", "content": user}, {"role": "assistant", "content": assistant}])
    conversation.append({"role": "user", "content": message})

    input_ids = tokenizer.apply_chat_template(conversation, return_tensors="pt", add_generation_prompt=True)
    if input_ids.shape[1] > MAX_INPUT_TOKEN_LENGTH:
        input_ids = input_ids[:, -MAX_INPUT_TOKEN_LENGTH:]
        gr.Warning(f"Trimmed input from conversation as it was longer than {MAX_INPUT_TOKEN_LENGTH} tokens.")
    input_ids = input_ids.to(model.device)

    streamer = TextIteratorStreamer(tokenizer, timeout=10.0, skip_prompt=True, skip_special_tokens=True)
    generate_kwargs = dict(
        {"input_ids": input_ids},
        streamer=streamer,
        max_new_tokens=max_new_tokens,
        do_sample=False,
        num_beams=1,
        repetition_penalty=repetition_penalty,
        eos_token_id=tokenizer.eos_token_id
    )
    t = Thread(target=model.generate, kwargs=generate_kwargs)
    t.start()

    outputs = []
    for text in streamer:
        outputs.append(text)
        yield "".join(outputs).replace("<|EOT|>","")


chat_interface = gr.ChatInterface(
    fn=generate,
    additional_inputs=[
        gr.Textbox(
            label="System prompt", 
            lines=6, 
            value="You are Agent 1.0, an advanced AI programming assistant developed by Suryanshu Nabheet. You are a local-first, independent Coding Agent. Focus on providing clean, efficient, and production-ready code in 80+ languages. You only answer questions related to computer science and programming. For any other topics, politely decline."
        ),
        gr.Slider(
            label="Max new tokens",
            minimum=1,
            maximum=MAX_MAX_NEW_TOKENS,
            step=1,
            value=DEFAULT_MAX_NEW_TOKENS,
        ),
        # gr.Slider(
        #     label="Temperature",
        #     minimum=0,
        #     maximum=4.0,
        #     step=0.1,
        #     value=0,
        # ),
        gr.Slider(
            label="Top-p (nucleus sampling)",
            minimum=0.05,
            maximum=1.0,
            step=0.05,
            value=0.9,
        ),
        gr.Slider(
            label="Top-k",
            minimum=1,
            maximum=1000,
            step=1,
            value=50,
        ),
        gr.Slider(
            label="Repetition penalty",
            minimum=1.0,
            maximum=2.0,
            step=0.05,
            value=1,
        ),
    ],
    stop_btn=None,
    examples=[
        ["implement snake game using pygame"],
        ["Can you explain briefly to me what is the Python programming language?"],
        ["write a program to find the factorial of a number"],
    ],
)

with gr.Blocks(css="style.css") as demo:
    gr.Markdown(DESCRIPTION)
    chat_interface.render()

if __name__ == "__main__":
    demo.queue().launch(share=True)
