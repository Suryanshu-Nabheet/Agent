## Fine-tuning Agent 1.0

Agent 1.0 supports sophisticated fine-tuning for specialized downstream tasks. We provide the `finetune_agent.py` script to facilitate this process.

### 1. Prerequisites
Install the required training dependencies, including [DeepSpeed](https://github.com/microsoft/DeepSpeed):

```bash
pip install -r requirements.txt
```

### 2. Data Preparation
Your training data should follow a JSON-L format where each line is a JSON object with `instruction` and `output` fields.

### 3. Execution
Use the following template to start fine-tuning. Ensure you specify your `DATA_PATH` and `OUTPUT_PATH`.

```bash
DATA_PATH="<your_data_path>"
OUTPUT_PATH="<your_output_path>"
MODEL_PATH="agent-ai/agent-1.0-6.7b-instruct" # Source weights for Agent 1.0 base

deepspeed finetune_agent.py \
    --model_name_or_path $MODEL_PATH \
    --data_path $DATA_PATH \
    --output_dir $OUTPUT_PATH \
    --num_train_epochs 3 \
    --model_max_length 1024 \
    --per_device_train_batch_size 16 \
    --per_device_eval_batch_size 1 \
    --gradient_accumulation_steps 4 \
    --evaluation_strategy "no" \
    --save_strategy "steps" \
    --save_steps 100 \
    --save_total_limit 100 \
    --learning_rate 2e-5 \
    --warmup_steps 10 \
    --logging_steps 1 \
    --lr_scheduler_type "cosine" \
    --gradient_checkpointing True \
    --report_to "tensorboard" \
    --deepspeed configs/ds_config_zero3.json \
    --bf16 True
```

### 4. Model Variants
Agent 1.0 is available in several sizes to balance performance and hardware availability:
- **1.3B**: Optimized for local development on consumer laptops (8GB+ RAM).
- **7B**: The sweet spot for high-quality instruction following and code generation.
- **33B**: Production-grade reasoning, ideal for cluster deployments.

### 5. Best Practices
- **Dataset Quality**: Ensure your `instruction` fields are concise and your `output` code is linted and idiomatic. Agent 1.0 is sensitive to code quality in the fine-tuning set.
- **Learning Rate**: For smaller models (1.3B), a slightly higher learning rate (5e-5) may be beneficial, while larger models (33B) perform better with lower rates (1e-5).
- **Local First**: We recommend training on hardware with at least 24GB VRAM for 7B models using ZeRO-3 for maximum efficiency.

*Agent 1.0 Fine-tuning Suite — Suryanshu Nabheet*