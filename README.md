# Context Engineering Lesson

A comprehensive, self-contained, interactive lesson on Context Engineering for Large Language Models (LLMs). This package provides hands-on experience with context window management, token budgets, and optimization strategies using local, open-source models.

## Quick Start

```bash
# 1. Clone or extract the package
cd context-engineering-lesson/

# 2. Set up the virtual environment (Linux/Mac)
bash scripts/setup_venv.sh

# Or for Windows:
scripts\setup_venv.bat
```

**Next Steps:**

1. **Open the notebook** in your IDE:
   - File: `notebooks/context_engineering_lesson.ipynb`

2. **Select the Python kernel** from `.venv`:
   - Linux/Mac: `.venv/bin/python`
   - Windows: `.venv\Scripts\python.exe`

3. **Verify your environment** (run in first cell):
   ```python
   import sys
   print(sys.executable)  # Should show path containing .venv
   ```

4. **Start working** through the lesson cells!

**Supported IDEs:** VS Code, PyCharm, JupyterLab, Jupyter Notebook

**Need detailed instructions?** Open `index.html` in a web browser for the complete setup guide.

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
- **5 GB free disk space** (for models and dependencies)
- **No API keys needed** - runs 100% locally!

## File Structure

```
├── index.html                           # START HERE - Lesson guide
├── run_lesson.sh                        # Main entrypoint
├── README.md                            # This file
├── LICENSE                              # Apache 2.0 license
├── DATA_LICENSES.md                     # Third-party licenses
├── .env.example                         # Config template
├── requirements.txt                     # Dependencies
├── .gitignore                           # Git ignore rules
├── scripts/
│   ├── setup_venv.sh                    # Linux/Mac setup
│   └── setup_venv.bat                   # Windows setup
├── notebooks/
│   └── context_engineering_lesson.ipynb # Interactive lesson
├── src/
│   ├── __init__.py                      # Package marker
│   ├── verify.py                        # Auto-grading CLI
│   ├── context_strategies.py            # Student templates
│   ├── token_manager.py                 # Token utilities
│   ├── evaluation.py                    # Scoring system
│   └── helpers.py                       # Utility functions
├── data/
│   ├── source_documents.json            # Document corpus
│   ├── evaluation_questions.json        # Test queries
│   └── context_examples.json            # Reference examples
└── progress/
    └── .gitkeep                         # Progress tracking folder
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

## Expected Outcomes

Upon completion, you will have:

- ✅ Working implementations of 4 context strategies
- ✅ Hands-on experience with token counting
- ✅ Understanding of the "lost in the middle" problem
- ✅ Practical optimization techniques
- ✅ Auto-generated performance report
- ✅ Foundation for building production RAG systems

**Estimated time:** 25-35 minutes (depending on hardware)

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

For detailed troubleshooting, see the **Troubleshooting** section in `index.html`.

## Contact

For questions, issues, or feedback about this lesson:
- Review `index.html` for comprehensive documentation
- Check `src/verify.py` for grading logic details
- Inspect `notebooks/context_engineering_lesson.ipynb` for lesson structure

---

**Ready to learn?** Open `index.html` in your browser to begin!
