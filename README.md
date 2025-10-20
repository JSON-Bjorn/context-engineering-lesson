# Context Engineering Lesson

A comprehensive, self-contained, interactive lesson on Context Engineering for Large Language Models (LLMs). This package provides hands-on experience with context window management, token budgets, and optimization strategies using local, open-source models.

## Quick Start

```bash
# 1. Clone the repository
git clone <repository-url>
cd context-engineering-lesson/

# 2. Set up the virtual environment
bash scripts/setup_venv.sh    # Linux/Mac
# OR
scripts\setup_venv.bat       # Windows

# 3. Run the main entrypoint
./run_lesson.sh              # Linux/Mac
# OR
bash run_lesson.sh           # Windows (Git Bash)
```

**The `run_lesson.sh` script will guide you through the complete lesson workflow.**

## How It Works

### Step 1: Read the Guide
Open `index.html` in your web browser for comprehensive documentation, prerequisites, and detailed setup instructions.

### Step 2: Run the Entrypoint
Execute `run_lesson.sh` which will:
- ✅ Check that your virtual environment is ready
- ✅ Provide lesson overview and learning objectives
- ✅ Guide you to the interactive notebook
- ✅ Show you how to select the correct Python kernel
- ✅ Explain the completion and grading process

### Step 3: Work Through the Lesson
1. **Open the notebook** in your IDE: `notebooks/context_engineering_lesson.ipynb`
2. **Select the Python kernel** from `.venv`:
   - Linux/Mac: `.venv/bin/python`
   - Windows: `.venv\Scripts\python.exe`
3. **Verify your environment** (run in first cell):
   ```python
   import sys
   print(sys.executable)  # Should show path containing .venv
   ```
4. **Complete the 5 phases** of interactive exercises (~30 minutes)

### Step 4: Get Graded
```bash
python src/verify.py
```
This generates your completion certificate in `progress/lesson_progress.json`.

**Supported IDEs:** VS Code, PyCharm, JupyterLab, Jupyter Notebook

## Learning Objectives

By completing this 30-minute interactive lesson, you will:

1. **Understand token budgets** - Learn how to count tokens and work within context limits
2. **Master context strategies** - Implement 4 key strategies (naive, primacy, recency, sandwich)
3. **Optimize context assembly** - Apply advanced techniques to maximize information density
4. **Evaluate performance** - Use automated grading to measure strategy effectiveness
5. **Gain practical skills** - Build a foundation for real-world RAG and LLM applications

## Prerequisites

- **Python 3.12** (required)
- **8 GB RAM minimum** (16 GB recommended)
- **10 GB free disk space** (for models and dependencies)
- **No API keys needed** - runs 100% locally!

**First run downloads:** ~6.6 GB of models (Qwen2.5-3B-Instruct + all-MiniLM-L6-v2)

## File Structure

```
├── index.html                           # Comprehensive lesson guide (START HERE)
├── run_lesson.sh                        # Main entrypoint script
├── README.md                            # This file
├── LICENSE                              # Apache 2.0 license
├── DATA_LICENSES.md                     # Third-party licenses
├── .env.example                         # Environment variables template
├── requirements.txt                     # Pinned dependencies
├── .gitignore                           # Git ignore rules
├── scripts/
│   ├── setup_venv.sh                    # Linux/Mac setup
│   └── setup_venv.bat                   # Windows setup
├── notebooks/
│   └── context_engineering_lesson.ipynb # Interactive lesson content
├── src/
│   ├── __init__.py                      # Package marker
│   ├── verify.py                        # Auto-grading CLI
│   ├── context_strategies.py            # Student implementation templates
│   ├── token_manager.py                 # Token counting utilities
│   ├── evaluation.py                    # Scoring system
│   └── helpers.py                       # Utility functions
├── data/
│   ├── source_documents.json            # Document corpus
│   ├── evaluation_questions.json        # Test queries and answers
│   └── context_examples.json            # Reference examples
└── progress/
    └── lesson_progress.json             # Generated completion certificate
```

## Evaluation Process

After completing the lesson notebook, verify your work:

```bash
python src/verify.py
```

The auto-grader will:
- Check all implemented strategies
- Calculate accuracy scores
- Generate a progress report
- Provide feedback on improvements

**Passing criteria:**
- All 5 phases completed
- Baseline accuracy ≥ 0.70
- At least one strategy improves on baseline
- Token budgets respected

## Lesson Flow

The lesson consists of 5 phases:

1. **Context Windows** (7 min) - Token counting and budget analysis
2. **Baseline Implementation** (8 min) - Naive context assembly
3. **Strategic Placement** (10 min) - Primacy, recency, sandwich strategies
4. **Optimization** (5 min) - Advanced techniques
5. **Evaluation** (Auto) - Automated grading and reporting

## Expected Outcomes

Upon completion, you will have:

- ✅ Working implementations of 4 context strategies
- ✅ Hands-on experience with token counting
- ✅ Understanding of the "lost in the middle" problem
- ✅ Practical optimization techniques
- ✅ Auto-generated performance report
- ✅ Foundation for building production RAG systems

**Estimated time:** 30 minutes active work (plus setup time)

## Supported Environments

- **IDEs:** VS Code, PyCharm, JupyterLab, Jupyter Notebook
- **Operating Systems:** Linux, macOS, Windows
- **Hardware:** CPU-only (8GB+ RAM) or GPU-accelerated (16GB+ VRAM)

## License Information

This lesson package is licensed under the **Apache License 2.0**.

- **Lesson code & data:** Apache 2.0 (see LICENSE)
- **Third-party models:** Apache 2.0 (see DATA_LICENSES.md)
- **Models used:**
  - Qwen2.5-3B-Instruct (Apache 2.0)
  - all-MiniLM-L6-v2 (Apache 2.0)

All components are free to use for educational and commercial purposes.

## Support & Troubleshooting

**Common issues:**

1. **"Python 3.12 not found"** - Install from [python.org](https://www.python.org/)
2. **"Out of memory"** - Close other applications, or use a machine with more RAM
3. **"Module not found"** - Ensure virtual environment is activated
4. **Slow inference** - Expected on CPU; use GPU for faster results
5. **Models downloading slowly** - Be patient, it's a one-time 6.6 GB download

For detailed troubleshooting, see the **Troubleshooting** section in `index.html`.

## Contact

For questions, issues, or feedback about this lesson:
- Review `index.html` for comprehensive documentation
- Check `src/verify.py` for grading logic details
- Inspect `notebooks/context_engineering_lesson.ipynb` for lesson structure

---

**Ready to learn?** 

1. Open `index.html` in your browser for the complete guide
2. Run `./run_lesson.sh` to start the lesson
3. Follow the guided workflow to completion

**This lesson runs 100% locally - no API keys or external services required!**
