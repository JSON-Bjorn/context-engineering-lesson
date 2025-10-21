#!/bin/bash
set -e  # Exit on error

echo "=================================="
echo "Context Engineering Lesson Setup"
echo "Linux/Mac/Windows (Git Bash) Setup"
echo "=================================="
echo ""

# Function to check if a command is a valid Python 3.12.x
check_python_version() {
    local cmd=$1
    if command -v "$cmd" &> /dev/null; then
        local version=$("$cmd" --version 2>&1 | grep -oE '[0-9]+\.[0-9]+\.[0-9]+' | head -1)
        if [[ "$version" =~ ^3\.12\. ]]; then
            echo "$cmd"
            return 0
        fi
    fi
    return 1
}

# Function to print installation instructions
print_install_instructions() {
    echo ""
    echo "╔════════════════════════════════════════════════════════════════╗"
    echo "║  Python 3.12.x Not Found - Installation Required              ║"
    echo "╚════════════════════════════════════════════════════════════════╝"
    echo ""
    echo "Please install Python 3.12.x from:"
    echo "  🔗 https://www.python.org/downloads/"
    echo ""
    echo "Platform-specific instructions:"
    echo ""
    echo "📦 Linux (Ubuntu/Debian):"
    echo "  sudo apt update"
    echo "  sudo apt install python3.12 python3.12-venv"
    echo ""
    echo "📦 Linux (Fedora/RHEL):"
    echo "  sudo dnf install python3.12"
    echo ""
    echo "🍺 macOS (Homebrew):"
    echo "  brew install python@3.12"
    echo ""
    echo "🪟 Windows:"
    echo "  1. Download from https://www.python.org/downloads/"
    echo "  2. Run installer"
    echo "  3. ✅ Check 'Add Python to PATH'"
    echo "  4. ✅ Check 'Install for all users' (optional)"
    echo ""
    echo "After installation, restart your terminal and run this script again."
    echo ""
}

# Check for Python 3.12
echo "Searching for Python 3.12.x..."

PYTHON_CMD=""

# Method 1: Check python3.12 command
if [ -z "$PYTHON_CMD" ]; then
    if PYTHON_CMD=$(check_python_version "python3.12"); then
        echo "✅ Found python3.12 ($(python3.12 --version 2>&1))"
    fi
fi

# Method 2: Check python3 command
if [ -z "$PYTHON_CMD" ]; then
    if PYTHON_CMD=$(check_python_version "python3"); then
        echo "✅ Found python3 ($(python3 --version 2>&1))"
    fi
fi

# Method 3: Check python command
if [ -z "$PYTHON_CMD" ]; then
    if PYTHON_CMD=$(check_python_version "python"); then
        echo "✅ Found python ($(python --version 2>&1))"
    fi
fi

# Method 4: Check common Windows paths (for Git Bash on Windows)
if [ -z "$PYTHON_CMD" ]; then
    # Build array with proper escaping for paths with spaces/parentheses
    WINDOWS_PATHS=()
    WINDOWS_PATHS+=("/c/Python312/python.exe")

    # Check for LOCALAPPDATA and APPDATA paths if on Windows
    if [ -n "$LOCALAPPDATA" ]; then
        WINDOWS_PATHS+=("$LOCALAPPDATA/Programs/Python/Python312/python.exe")
    fi
    if [ -n "$APPDATA" ]; then
        WINDOWS_PATHS+=("$APPDATA/Python/Python312/python.exe")
    fi

    # Add Program Files paths (Git Bash translates these automatically)
    WINDOWS_PATHS+=("/c/Program Files/Python312/python.exe")
    WINDOWS_PATHS+=("/c/Program Files (x86)/Python312/python.exe")

    for py_path in "${WINDOWS_PATHS[@]}"; do
        if [ -f "$py_path" ]; then
            if PYTHON_CMD=$(check_python_version "$py_path"); then
                echo "✅ Found Python at $py_path ($("$py_path" --version 2>&1))"
                break
            fi
        fi
    done
fi

# If still not found, error out with instructions
if [ -z "$PYTHON_CMD" ]; then
    echo "❌ Error: Python 3.12.x not found"
    print_install_instructions
    exit 1
fi

# Verify the Python version one more time
FULL_VERSION=$($PYTHON_CMD --version 2>&1 | grep -oE '[0-9]+\.[0-9]+\.[0-9]+')
echo ""
echo "Using Python $FULL_VERSION at: $(command -v $PYTHON_CMD || echo $PYTHON_CMD)"
echo ""

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
# Windows (Git Bash) uses Scripts instead of bin
if [ -f ".venv/Scripts/activate" ]; then
    source .venv/Scripts/activate
elif [ -f ".venv/bin/activate" ]; then
    source .venv/bin/activate
else
    echo "❌ Error: Could not find activation script"
    exit 1
fi
echo "✅ Virtual environment activated"

# Upgrade pip
echo ""
echo "Upgrading pip..."
"$PYTHON_CMD" -m pip install --upgrade pip --quiet
echo "✅ pip upgraded"

# Detect GPU and install correct PyTorch version
echo ""
echo "=================================="
echo "Detecting GPU Hardware..."
echo "=================================="
echo ""
"$PYTHON_CMD" scripts/detect_gpu.py
if [ $? -ne 0 ]; then
    echo "❌ Error: GPU detection failed"
    exit 1
fi
echo ""

# Read GPU config and install PyTorch
echo "Installing PyTorch optimized for your hardware..."
PYTORCH_CMD=$("$PYTHON_CMD" -c "import json; config = json.load(open('.gpu_config.json')); print(config['pytorch_command'])")
echo "Command: $PYTORCH_CMD"
echo ""
eval $PYTORCH_CMD
if [ $? -ne 0 ]; then
    echo "❌ Error: PyTorch installation failed"
    exit 1
fi
echo "✅ PyTorch installed successfully"
echo ""

# Install other dependencies (excluding torch)
echo ""
echo "Installing other dependencies (this may take 2-3 minutes)..."
pip install -r requirements.txt
echo "✅ Dependencies installed"

# Verify installation
echo ""
echo "Verifying installation..."
"$PYTHON_CMD" -c "
import transformers
import torch
import sentence_transformers

print('✅ PyTorch version:', torch.__version__)
print('✅ Transformers version:', transformers.__version__)
print('✅ CUDA available:', torch.cuda.is_available())
if torch.cuda.is_available():
    print('✅ GPU:', torch.cuda.get_device_name(0))
elif hasattr(torch.backends, 'mps') and torch.backends.mps.is_available():
    print('✅ GPU: Apple Silicon (MPS)')
else:
    print('⚠️  GPU: CPU-only mode')
" 2>&1
if [ $? -eq 0 ]; then
    echo ""
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
echo "   In VS Code: Click kernel selector in top-right"
echo "   In PyCharm: Settings → Project → Python Interpreter"
echo "   In JupyterLab: Kernel → Change Kernel"
echo ""
echo "3. Verify the correct environment (run in first cell):"
echo "   import sys"
echo "   print(sys.executable)"
echo ""
echo "   Should show path to .venv/bin/python or .venv\\Scripts\\python.exe"
echo ""
echo "4. Start working through the lesson cells!"
echo ""
echo "💡 Tip: For a quick verification script, run:"
if [ -f "run_lesson.sh" ]; then
    echo "   ./run_lesson.sh"
else
    echo "   bash scripts/run_lesson.sh"
fi
echo ""
