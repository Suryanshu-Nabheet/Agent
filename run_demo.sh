#!/bin/bash
echo "--------------------------------------------------"
echo "Starting Agent 1.0 by Suryanshu Nabheet"
echo "Project: Coding Agent"
echo "--------------------------------------------------"

# Activate virtual environment
if [ -d "venv" ]; then
    source venv/bin/activate
else
    echo "Error: Virtual environment not found. Please run './setup_agent.sh' first."
    exit 1
fi

# Run the Agent 1.0 Demo
# Default model: Agent-1.3B (Optimized for local performance)
export MODEL_ID="agent-ai/agent-1.0-1.3b-instruct"

echo "Launching Agent 1.0 Demo..."
python3 demo/app.py
