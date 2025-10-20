#!/bin/bash
set -e  # Exit on error

echo "=================================================="
echo "SMART SETUP - Context Engineering Lesson"
echo "=================================================="
echo ""
echo "This script will:"
echo "  1. Detect your GPU hardware"
echo "  2. Install the optimal PyTorch version"
echo "  3. Set up the lesson environment"
echo ""
echo "=================================================="
echo ""

# Check Python version
echo "Step 1: Checking Python version..."
if command -v python3.12 &> /dev/null; then
    PYTHON_CMD="python3.12"
elif command -v python3 &> /dev/null; then
    PYTHON_CMD="python3"
elif command -v python &> /dev/null; then
    PYTHON_CMD="python"
else
    echo "❌ Error: Python not found"
    echo "Please install Python 3.12 from https://www.python.org/downloads/"
    exit 1
fi

PYTHON_VERSION=$($PYTHON_CMD --version 2>&1 | grep -oE '[0-9]+\.[0-9]+')
echo "✅ Found Python $PYTHON_VERSION"

# Check if Python 3.8+
MAJOR=$(echo $PYTHON_VERSION | cut -d. -f1)
MINOR=$(echo $PYTHON_VERSION | cut -d. -f2)

if [ "$MAJOR" -lt 3 ] || ([ "$MAJOR" -eq 3 ] && [ "$MINOR" -lt 8 ]); then
    echo "❌ Error: Python 3.8 or higher required (found $PYTHON_VERSION)"
    exit 1
fi

echo ""

# Create virtual environment
echo "Step 2: Creating virtual environment..."
if [ ! -d ".venv" ]; then
    $PYTHON_CMD -m venv .venv
    echo "✅ Virtual environment created"
else
    echo "✅ Virtual environment already exists"
fi

echo ""

# Activate virtual environment
echo "Step 3: Activating virtual environment..."
if [ -f ".venv/Scripts/activate" ]; then
    # Windows (Git Bash)
    source .venv/Scripts/activate
elif [ -f ".venv/bin/activate" ]; then
    # POSIX
    source .venv/bin/activate
else
    echo "❌ Error: Cannot find activation script"
    exit 1
fi
echo "✅ Virtual environment activated"

echo ""

# Upgrade pip
echo "Step 4: Upgrading pip..."
pip install --upgrade pip --quiet
echo "✅ Pip upgraded"

echo ""

# Detect GPU
echo "Step 5: Detecting GPU hardware..."
echo ""
python scripts/detect_gpu.py

if [ ! -f ".gpu_config.json" ]; then
    echo "❌ Error: GPU detection failed"
    exit 1
fi

echo ""

# Install PyTorch based on detection
echo "Step 6: Installing PyTorch (optimized for your hardware)..."
echo ""

# Read PyTorch command from config
PYTORCH_CMD=$(python -c "import json; config = json.load(open('.gpu_config.json')); print(config['pytorch_command'])")
PYTORCH_DESC=$(python -c "import json; config = json.load(open('.gpu_config.json')); print(config['description'])")

echo "Installing: $PYTORCH_DESC"
echo "Command: $PYTORCH_CMD"
echo ""

# Execute PyTorch installation
eval $PYTORCH_CMD

if [ $? -ne 0 ]; then
    echo "❌ Error: PyTorch installation failed"
    exit 1
fi

echo "✅ PyTorch installed successfully"

echo ""

# Install other dependencies (excluding torch)
echo "Step 7: Installing other dependencies..."
echo ""

# Create temporary requirements without torch
grep -v "^torch" requirements.txt > .temp_requirements.txt

pip install -r .temp_requirements.txt

if [ $? -ne 0 ]; then
    echo "❌ Error: Dependency installation failed"
    exit 1
fi

rm .temp_requirements.txt

echo "✅ All dependencies installed"

echo ""

# Verify installation
echo "Step 8: Verifying installation..."
python -c "
import torch
import transformers
from sentence_transformers import SentenceTransformer

print('✅ PyTorch:', torch.__version__)
print('✅ Transformers:', transformers.__version__)

# Check GPU availability
if torch.cuda.is_available():
    print('✅ CUDA Available: Yes')
    print(f'   GPU: {torch.cuda.get_device_name(0)}')
elif torch.backends.mps.is_available():
    print('✅ MPS Available: Yes (Apple Silicon)')
else:
    print('⚠️  GPU: CPU-only mode')
"

echo ""
echo "=================================================="
echo "✅ Setup Complete!"
echo "=================================================="
echo ""
echo "Your system is configured with:"

# Show what was detected
python -c "
import json
config = json.load(open('.gpu_config.json'))
print(config['description'])
"

echo ""
echo "Next steps:"
echo ""
echo "1. Open the notebook in your IDE:"
echo "   📁 File: notebooks/context_engineering_lesson.ipynb"
echo ""
echo "2. Select the Python kernel from .venv:"
if [ -f ".venv/Scripts/activate" ]; then
    echo "   🐍 Kernel: .venv\\Scripts\\python.exe"
else
    echo "   🐍 Kernel: .venv/bin/python"
fi
echo ""
echo "3. Verify the correct environment (run in first cell):"
echo "   import sys"
echo "   print(sys.executable)"
echo ""
echo "4. Start working through the lesson cells!"
echo ""

# Show expected performance
python -c "
import json
config = json.load(open('.gpu_config.json'))
gpu_info = config['gpu_info']

if gpu_info['nvidia_gpu'] or gpu_info['amd_gpu'] or gpu_info['apple_silicon']:
    print('🚀 Expected Performance:')
    print('   Time per evaluation: ~5-10 seconds')
    print('   Total lesson time: ~5-10 minutes')
else:
    print('💡 Performance Note:')
    print('   Time per evaluation: ~20-40 seconds')
    print('   Total lesson time: ~15-25 minutes')
"

echo ""
echo "=================================================="
echo ""
