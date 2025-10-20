#!/bin/bash
set -e  # Exit on error

# Welcome banner
echo ""
echo "╔════════════════════════════════════════════════════════════╗"
echo "║                                                            ║"
echo "║         CONTEXT ENGINEERING INTERACTIVE LESSON             ║"
echo "║                                                            ║"
echo "║  Learn how to optimize LLM context windows for better     ║"
echo "║  accuracy, lower costs, and improved performance          ║"
echo "║                                                            ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""
echo "Duration: ~30 minutes"
echo "No API keys required - runs 100% locally!"
echo ""
echo "=================================="
echo ""

# Check for Python 3.12
echo "Checking prerequisites..."
if command -v python3.12 &> /dev/null; then
    PYTHON_CMD="python3.12"
    echo "✅ Python 3.12 found"
elif command -v python3 &> /dev/null; then
    VERSION=$(python3 --version 2>&1 | grep -oP '3\.\d+')
    if [ "$VERSION" = "3.12" ]; then
        PYTHON_CMD="python3"
        echo "✅ Python 3.12 found"
    else
        echo "❌ Error: Python 3.12 required, found Python $VERSION"
        echo "Please install Python 3.12 from https://www.python.org/downloads/"
        exit 1
    fi
else
    echo "❌ Error: Python 3.12 not found"
    echo "Please install Python 3.12 from https://www.python.org/downloads/"
    exit 1
fi

# Check/create virtual environment
if [ ! -d ".venv" ]; then
    echo ""
    echo "Virtual environment not found. Setting up now..."
    bash scripts/setup_venv.sh
    if [ $? -ne 0 ]; then
        echo "❌ Setup failed. Please check errors above."
        exit 1
    fi
fi

# Activate virtual environment
echo ""
echo "Activating virtual environment..."
if [ -f ".venv/Scripts/activate" ]; then
    # Windows (Git Bash) virtualenv layout
    source .venv/Scripts/activate
elif [ -f ".venv/bin/activate" ]; then
    # POSIX virtualenv layout
    source .venv/bin/activate
else
    echo "❌ Error: Failed to activate virtual environment"
    echo "Try running: bash scripts/setup_venv.sh"
    exit 1
fi
echo "✅ Virtual environment activated"

# Verify dependencies
echo ""
echo "Verifying dependencies..."
python -c "import transformers; import torch; import jupyter" 2>&1
if [ $? -ne 0 ]; then
    echo "❌ Error: Dependencies not installed correctly"
    echo "Installing dependencies now..."
    pip install -r requirements.txt
    if [ $? -ne 0 ]; then
        echo "❌ Installation failed. Please run: bash scripts/setup_venv.sh"
        exit 1
    fi
fi
echo "✅ Dependencies verified"

# Create progress directory
echo ""
echo "Preparing lesson environment..."
mkdir -p progress
echo "✅ Progress tracking ready"

# Display lesson info
echo ""
echo "=================================="
echo "LESSON OVERVIEW"
echo "=================================="
echo ""
echo "You will learn:"
echo "  1. Token counting and budget management"
echo "  2. Naive context assembly (baseline)"
echo "  3. Primacy strategy (important info first)"
echo "  4. Recency strategy (important info last)"
echo "  5. Sandwich strategy (important info at both ends)"
echo "  6. Advanced optimization techniques"
echo ""
echo "Expected outcomes:"
echo "  • Understand context window limitations"
echo "  • Implement 4 different context strategies"
echo "  • Achieve 15-25% accuracy improvement"
echo "  • Reduce token usage by 20-30%"
echo ""
echo "=================================="
echo ""

# Launch Jupyter
echo "Starting Jupyter Notebook..."
echo ""
echo "The lesson will open in your browser shortly."
echo "If it doesn't, look for the URL in the output below."
echo ""
echo "⚠️  IMPORTANT: Keep this terminal window open!"
echo "    Press Ctrl+C when you're done to stop Jupyter."
echo ""
echo "=================================="
echo ""

# Launch Jupyter and wait
python -m notebook notebooks/context_engineering_lesson.ipynb

# On Jupyter close
echo ""
echo "=================================="
echo "Lesson Session Ended"
echo "=================================="
echo ""
echo "Next steps:"
echo ""
echo "1. If you completed the lesson exercises, verify your work:"
echo "   python src/verify.py"
echo ""
echo "2. Your progress is saved in:"
echo "   progress/lesson_progress.json"
echo ""
echo "3. To restart the lesson later:"
echo "   ./run_lesson.sh"
echo ""
echo "Happy learning! 🚀"
echo ""
