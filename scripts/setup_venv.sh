#!/bin/bash
set -e  # Exit on error

echo "=================================="
echo "Context Engineering Lesson Setup"
echo "Linux/Mac Virtual Environment"
echo "=================================="
echo ""

# Check for Python 3.12
echo "Checking for Python 3.12..."
if command -v python3.12 &> /dev/null; then
    PYTHON_CMD="python3.12"
    echo "✅ Found python3.12"
elif command -v python3 &> /dev/null; then
    VERSION=$(python3 --version 2>&1 | grep -oP '3\.\d+')
    if [ "$VERSION" = "3.12" ]; then
        PYTHON_CMD="python3"
        echo "✅ Found python3 (version 3.12)"
    else
        echo "❌ Error: Python 3.12 required, found Python $VERSION"
        exit 1
    fi
else
    echo "❌ Error: Python 3.12 not found"
    echo "Please install Python 3.12 from https://www.python.org/downloads/"
    exit 1
fi

# Create virtual environment
echo ""
echo "Creating virtual environment (.venv)..."
if [ -d ".venv" ]; then
    echo "⚠️  .venv already exists, removing old environment..."
    rm -rf .venv
fi

$PYTHON_CMD -m venv .venv
echo "✅ Virtual environment created"

# Activate virtual environment
echo ""
echo "Activating virtual environment..."
source .venv/bin/activate
echo "✅ Virtual environment activated"

# Upgrade pip
echo ""
echo "Upgrading pip..."
pip install --upgrade pip --quiet
echo "✅ pip upgraded"

# Install dependencies
echo ""
echo "Installing dependencies (this may take 3-5 minutes)..."
pip install -r requirements.txt
echo "✅ Dependencies installed"

# Verify installation
echo ""
echo "Verifying installation..."
python -c "import transformers; import torch; import sentence_transformers" 2>&1
if [ $? -eq 0 ]; then
    echo "✅ All critical packages installed successfully"
else
    echo "❌ Error: Package verification failed"
    exit 1
fi

# Success message
echo ""
echo "=================================="
echo "✅ Setup Complete!"
echo "=================================="
echo ""
echo "Next steps:"
echo "1. Activate the environment:"
echo "   source .venv/bin/activate"
echo ""
echo "2. Start the lesson:"
echo "   ./run_lesson.sh"
echo ""
echo "   OR manually:"
echo "   jupyter notebook notebooks/context_engineering_lesson.ipynb"
echo ""
