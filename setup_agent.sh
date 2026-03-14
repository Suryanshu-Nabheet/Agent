#!/bin/bash
echo "--------------------------------------------------"
echo "Agent 1.0: Setup by Suryanshu Nabheet"
echo "--------------------------------------------------"

# Remove old environment if exists
if [ -d "venv" ]; then
    echo "Cleaning up old environment..."
    rm -rf venv
fi

# Create new virtual environment
echo "Creating virtual environment..."
python3 -m venv venv
source venv/bin/activate

# Install dependencies from requirements.txt
echo "Installing Agent 1.0 dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

echo "Agent 1.0 setup complete."
echo "Run './run_demo.sh' to start."
