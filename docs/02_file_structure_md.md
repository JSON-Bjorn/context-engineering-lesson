# Context Engineering Lesson - Complete File Structure & Specifications

## Document Purpose
This document defines the exact file structure and technical specifications for every file in the lesson package. Use this as your blueprint when generating code in Claude Code.

---

## Complete File Tree

```
VG_[Firstname]_[Lastname]_[YYYYMMDD].zip
├── index.html                                    # [HTML] Lesson guide (START HERE)
├── run_lesson.sh                                 # [Bash] Main entrypoint
├── README.md                                     # [Markdown] Project overview
├── LICENSE                                       # [Text] Apache 2.0 license
├── DATA_LICENSES.md                              # [Markdown] Third-party licenses
├── .env.example                                  # [Text] Config template (empty)
├── requirements.txt                              # [Text] Pinned dependencies
├── .gitignore                                    # [Text] Git ignore rules
│
├── scripts/
│   ├── setup_venv.sh                             # [Bash] Linux/Mac setup
│   └── setup_venv.bat                            # [Batch] Windows setup
│
├── notebooks/
│   └── context_engineering_lesson.ipynb          # [Jupyter] Main interactive lesson
│
├── src/
│   ├── __init__.py                               # [Python] Package marker
│   ├── verify.py                                 # [Python] Auto-grading CLI
│   ├── context_strategies.py                     # [Python] Student templates
│   ├── token_manager.py                          # [Python] Token utilities
│   ├── evaluation.py                             # [Python] Scoring system
│   └── helpers.py                                # [Python] Utility functions
│
├── data/
│   ├── source_documents.json                     # [JSON] Document corpus
│   ├── evaluation_questions.json                 # [JSON] Test queries + answers
│   └── context_examples.json                     # [JSON] Reference examples
│
└── progress/
    └── .gitkeep                                  # [Text] Ensure folder exists
```

**Total Files:** 20 files
**Estimated Total Size:** ~10 MB (before model downloads)
**Zip Size:** <50 MB (well under 0.5 GB limit)

---

## File Specifications by Category

### Category 1: Entry Points & Documentation

#### `index.html`
- **Type:** HTML5 with embedded CSS
- **Size:** ~15-20 KB
- **Purpose:** Primary starting point for students
- **Sections Required:**
  1. Welcome & Overview
  2. Prerequisites (no API keys!)
  3. Hardware Requirements
  4. Setup Instructions (detailed .venv creation)
  5. Lesson Flow (5 phases with timing)
  6. Running the Lesson
  7. Evaluation Process
  8. Troubleshooting Common Issues
  9. Expected Learning Outcomes
  10. Additional Resources

- **Design Requirements:**
  - Clean, professional styling
  - Readable font (16px body text)
  - Syntax-highlighted code blocks
  - Clear section headers
  - Mobile-responsive
  - No external dependencies (all CSS inline)

#### `README.md`
- **Type:** Markdown
- **Size:** ~5-8 KB
- **Purpose:** Quick overview for developers/instructors
- **Sections Required:**
  1. Project title & description
  2. Quick start (3-4 commands)
  3. Learning objectives
  4. Prerequisites
  5. File structure overview
  6. Evaluation process
  7. Expected outcomes
  8. License information
  9. Contact/support info

#### `LICENSE`
- **Type:** Plain text
- **Content:** Apache License 2.0 full text
- **Size:** ~11 KB
- **Source:** https://www.apache.org/licenses/LICENSE-2.0.txt

#### `DATA_LICENSES.md`
- **Type:** Markdown
- **Size:** ~2-3 KB
- **Purpose:** Document all third-party resources
- **Required Content:**
```markdown
# Third-Party Data & Model Licenses

## Models

### Qwen2.5-3B-Instruct
- **Source:** Hugging Face (Qwen/Qwen2.5-3B-Instruct)
- **License:** Apache 2.0
- **URL:** https://huggingface.co/Qwen/Qwen2.5-3B-Instruct
- **Usage:** Local inference for educational purposes

### all-MiniLM-L6-v2
- **Source:** Hugging Face (sentence-transformers/all-MiniLM-L6-v2)
- **License:** Apache 2.0
- **URL:** https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2
- **Usage:** Document embedding and similarity

## Datasets

### Source Documents
- **Content:** Synthetic technical documents created for this lesson
- **License:** Apache 2.0 (created by lesson author)
- **Purpose:** Educational context engineering examples

### Evaluation Questions
- **Content:** Original Q&A pairs for assessment
- **License:** Apache 2.0 (created by lesson author)
- **Purpose:** Automated evaluation
```

---

### Category 2: Setup & Configuration Files

#### `requirements.txt`
- **Type:** Plain text (pip format)
- **Size:** ~1 KB
- **Python Version:** 3.12 only
- **Content:**

```text
# Context Engineering Lesson - Python 3.12 Dependencies
# All versions pinned for reproducibility

# Core ML/LLM libraries
transformers==4.45.2
torch==2.4.1
sentence-transformers==3.1.1
accelerate==0.34.2

# Token counting
tiktoken==0.8.0

# Data processing
pandas==2.2.3
numpy==2.1.3

# Jupyter environment
jupyter==1.1.1
notebook==7.2.2
ipykernel==6.29.5
ipywidgets==8.1.5

# Utilities
python-dotenv==1.0.1
tqdm==4.66.6

# Evaluation
scikit-learn==1.5.2

# Visualization (optional but included)
matplotlib==3.9.2
```

**Installation Time:** ~3-5 minutes
**Total Size:** ~2-3 GB installed

#### `.env.example`
- **Type:** Plain text
- **Size:** <1 KB
- **Content:**

```bash
# .env.example - Configuration template
# This lesson runs 100% locally - no API keys needed!

# Model Configuration (defaults are optimal)
# You can override these if you have GPU and want better quality
# MODEL_NAME=Qwen/Qwen2.5-3B-Instruct
# EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2

# Hardware Configuration
# Set to 'cuda' if you have NVIDIA GPU, 'mps' for Apple Silicon, or 'cpu'
# DEVICE=auto

# Generation Parameters (optional tuning)
# MAX_NEW_TOKENS=256
# TEMPERATURE=0.7
# TOP_P=0.9

# Evaluation Settings
# NUM_EVAL_QUESTIONS=10
# SIMILARITY_THRESHOLD=0.7

# Debug mode (set to 1 for verbose logging)
# DEBUG=0
```

**Note:** File exists for consistency but isn't required to run the lesson.

#### `.gitignore`
- **Type:** Plain text
- **Size:** <1 KB
- **Content:**

```text
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
*.egg-info/
dist/
build/

# Virtual Environment
.venv/
venv/
ENV/

# Jupyter
.ipynb_checkpoints/
*.ipynb_checkpoints

# Environment variables
.env

# Progress tracking (generated)
progress/lesson_progress.json

# Model cache (auto-downloaded)
.cache/
models/

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Logs
*.log
```

---

### Category 3: Setup Scripts

#### `scripts/setup_venv.sh`
- **Type:** Bash script
- **Size:** ~1-2 KB
- **Target:** Linux, MacOS
- **Requirements:**
  - Check for Python 3.12
  - Create .venv in project root
  - Activate environment
  - Upgrade pip
  - Install from requirements.txt
  - Verify installation
  - Print success message with next steps

**Key Functions:**
```bash
#!/bin/bash
set -e  # Exit on error

# 1. Validate Python 3.12
# 2. Create venv: python3.12 -m venv .venv
# 3. Activate: source .venv/bin/activate
# 4. Upgrade pip: pip install --upgrade pip
# 5. Install deps: pip install -r requirements.txt
# 6. Test imports: python -c "import transformers; import torch"
# 7. Print instructions
```

#### `scripts/setup_venv.bat`
- **Type:** Windows Batch script
- **Size:** ~1-2 KB
- **Target:** Windows 11
- **Requirements:** Same as above but Windows syntax

**Key Functions:**
```batch
@echo off
REM Windows equivalent of setup_venv.sh
REM Uses python instead of python3.12
REM Uses .venv\Scripts\activate.bat
```

---

### Category 4: Main Entrypoint

#### `run_lesson.sh`
- **Type:** Bash script
- **Size:** ~2-3 KB
- **Purpose:** One-command lesson start
- **Flow:**
  1. Print welcome banner
  2. Check Python 3.12 exists
  3. Check/create .venv if missing
  4. Activate .venv
  5. Verify dependencies installed
  6. Create progress/ directory
  7. Print lesson info (duration, objectives)
  8. Launch Jupyter notebook to specific file
  9. On notebook close, remind to run verify.py

**Error Handling:**
- Python not found → exit with error message
- Dependencies missing → auto-install
- .venv missing → auto-create
- Jupyter fails → print troubleshooting steps

**User Experience:**
- Clear progress indicators
- Estimated times shown
- Friendly error messages
- Next step suggestions

---

### Category 5: Core Source Code Structure

#### `src/__init__.py`
- **Type:** Python module marker
- **Size:** <1 KB
- **Content:**

```python
"""
Context Engineering Lesson - Core Implementation Module

This package contains the main lesson infrastructure:
- verify.py: Auto-grading system
- context_strategies.py: Student implementation templates
- token_manager.py: Token counting and budget management
- evaluation.py: LLM-based scoring
- helpers.py: Utility functions

Author: [Your Name]
License: Apache 2.0
"""

__version__ = "1.0.0"
__author__ = "[Your Name]"

# Expose key functions for easy imports
from .token_manager import count_tokens, fits_in_budget
from .helpers import load_documents, load_questions
from .evaluation import evaluate_answer

__all__ = [
    'count_tokens',
    'fits_in_budget', 
    'load_documents',
    'load_questions',
    'evaluate_answer',
]
```

---

### Category 6: Data Files Structure

#### `data/source_documents.json`
- **Type:** JSON
- **Size:** ~50-100 KB
- **Content:** 10 synthetic technical documents
- **Schema:**

```json
{
  "documents": [
    {
      "id": "doc_001",
      "title": "Introduction to Context Windows",
      "content": "Full document text here (200-2000 tokens)...",
      "tokens": 847,
      "category": "fundamentals",
      "relevance_keywords": ["context", "window", "tokens", "limits"]
    },
    // ... 9 more documents
  ],
  "metadata": {
    "total_documents": 10,
    "total_tokens": 8453,
    "categories": ["fundamentals", "strategies", "optimization", "case_studies"],
    "created": "2025-10-19",
    "purpose": "Context engineering educational corpus"
  }
}
```

**Document Topics:**
1. Context window fundamentals
2. Token counting mechanics
3. The "lost in the middle" problem
4. Context placement strategies
5. RAG system context assembly
6. Memory management techniques
7. Cost optimization strategies
8. Multi-turn conversation context
9. Real-world case study: customer support
10. Real-world case study: document Q&A

#### `data/evaluation_questions.json`
- **Type:** JSON
- **Size:** ~10-15 KB
- **Content:** 10 test questions with ground truth
- **Schema:**

```json
{
  "questions": [
    {
      "id": "q_001",
      "question": "What is the primary challenge of the 'lost in the middle' phenomenon?",
      "ground_truth_answer": "LLMs have difficulty attending to information in the middle of long contexts, showing better recall for content at the beginning and end.",
      "relevant_doc_ids": ["doc_001", "doc_003"],
      "difficulty": "easy",
      "question_type": "factual"
    },
    {
      "id": "q_002",
      "question": "Compare primacy and recency placement strategies for context assembly.",
      "ground_truth_answer": "Primacy places important information at the start, leveraging the model's attention to early content. Recency places it at the end, capitalizing on immediate context. Research shows recency often outperforms primacy for factual retrieval.",
      "relevant_doc_ids": ["doc_004", "doc_005"],
      "difficulty": "medium",
      "question_type": "comparison"
    },
    // ... 8 more questions covering all difficulty levels
  ],
  "metadata": {
    "total_questions": 10,
    "difficulty_distribution": {
      "easy": 3,
      "medium": 5,
      "hard": 2
    },
    "question_types": ["factual", "comparison", "application", "reasoning"]
  }
}
```

**Question Distribution:**
- 3 easy (single-document factual)
- 5 medium (multi-document comparison/application)
- 2 hard (multi-hop reasoning/synthesis)

#### `data/context_examples.json`
- **Type:** JSON
- **Size:** ~5-10 KB
- **Content:** Reference examples of good context engineering
- **Schema:**

```json
{
  "examples": [
    {
      "id": "ex_001",
      "scenario": "User query with 5 relevant documents and 4K token limit",
      "query": "What are the best practices for context window management?",
      "strategy": "sandwich",
      "assembled_context": "Example of well-structured context...",
      "rationale": "Top 2 docs at start, bottom 2 at end, less relevant in middle",
      "tokens_used": 3847,
      "quality_score": 0.89
    },
    // ... 4 more examples
  ]
}
```

---

### Category 7: Progress Tracking

#### `progress/.gitkeep`
- **Type:** Empty file
- **Purpose:** Ensure progress/ directory exists in git
- **Note:** `lesson_progress.json` is auto-generated by verify.py

#### `progress/lesson_progress.json` (Generated)
- **Type:** JSON (auto-generated)
- **Size:** ~2-5 KB
- **Schema:**

```json
{
  "student_id": "auto_generated_uuid",
  "lesson": "context_engineering",
  "timestamp": "2025-10-19T14:30:00Z",
  "completion_time_minutes": 28,
  "tasks_completed": {
    "token_budget_analysis": {
      "status": "PASS",
      "accuracy": 0.98,
      "attempts": 1
    },
    "naive_implementation": {
      "status": "PASS",
      "baseline_accuracy": 0.72
    },
    "primacy_strategy": {
      "status": "PASS",
      "accuracy": 0.76,
      "improvement_vs_baseline": 0.06
    },
    "recency_strategy": {
      "status": "PASS",
      "accuracy": 0.81,
      "improvement_vs_baseline": 0.13
    },
    "sandwich_strategy": {
      "status": "PASS",
      "accuracy": 0.85,
      "improvement_vs_baseline": 0.18
    },
    "optimization": {
      "status": "PASS",
      "method": "hierarchical_summarization",
      "accuracy": 0.87,
      "token_reduction": 0.23,
      "improvement_vs_baseline": 0.21
    }
  },
  "metrics_summary": {
    "best_strategy": "sandwich",
    "best_accuracy": 0.87,
    "total_improvement": 0.21,
    "avg_token_efficiency": 0.000226,
    "all_checks_passed": true
  },
  "verification": {
    "grade": "PASS",
    "checks_passed": 5,
    "checks_total": 5,
    "issues": []
  }
}
```

---

## File Generation Order for Claude Code

### Phase 1: Foundation (Generate First)
1. `requirements.txt`
2. `LICENSE`
3. `DATA_LICENSES.md`
4. `.env.example`
5. `.gitignore`
6. `README.md`

### Phase 2: Data Files (Generate Second)
7. `data/source_documents.json`
8. `data/evaluation_questions.json`
9. `data/context_examples.json`

### Phase 3: Core Code (Generate Third)
10. `src/__init__.py`
11. `src/token_manager.py`
12. `src/helpers.py`
13. `src/context_strategies.py`
14. `src/evaluation.py`
15. `src/verify.py`

### Phase 4: Interactive Content (Generate Fourth)
16. `notebooks/context_engineering_lesson.ipynb`

### Phase 5: Entry Points (Generate Fifth)
17. `scripts/setup_venv.sh`
18. `scripts/setup_venv.bat`
19. `run_lesson.sh`
20. `index.html`

### Phase 6: Final Touches
21. `progress/.gitkeep`

---

## Size Validation Checklist

Before zipping, verify:

- [ ] Total uncompressed size < 100 MB (should be ~15-20 MB)
- [ ] After zip compression < 50 MB (should be ~5-10 MB)
- [ ] No model files included in zip (downloaded separately)
- [ ] All text files use UTF-8 encoding
- [ ] All scripts have proper line endings (LF for .sh, CRLF for .bat)
- [ ] All Python files have proper docstrings
- [ ] All JSON files are valid and formatted

---

## Next Steps

1. Save this document as `docs/02_file_structure.md`
2. Review the file tree and structure
3. Request Chunk 3: Detailed specifications for index.html and notebook

**Ready for Chunk 3 when you are!**
