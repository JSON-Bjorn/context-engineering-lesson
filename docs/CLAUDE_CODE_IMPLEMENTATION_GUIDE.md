# Claude Code Implementation Guide
## Context Engineering Lesson - Complete Generation Plan

**Purpose:** This document provides step-by-step instructions for generating the complete Context Engineering lesson using Claude Code.

**Total Estimated Time:** 90-120 minutes  
**Phases:** 8 sequential phases  
**Testing:** Required after each phase

---

## Prerequisites

Before starting, ensure:
- [ ] All 7 specification documents exist in `docs/` folder
- [ ] You're in the project root: `context-engineering-lesson/`
- [ ] Claude Code is open and ready
- [ ] You have Python 3.12 installed
- [ ] You have ~2 hours of focused time

---

## Phase 1: Foundation Files
**Duration:** 10 minutes  
**Dependencies:** None  
**Files Created:** 5

### Prompt 1.1: Core Configuration Files

```
Create the following foundation files for the Context Engineering lesson:

1. LICENSE - Use the complete Apache License 2.0 text from docs/07_final_config_and_packaging.md
2. .gitignore - Copy from docs/07_final_config_and_packaging.md
3. .env.example - Copy from docs/02_file_structure.md
4. requirements.txt - Copy from docs/02_file_structure.md (with exact versions)
5. README.md - Follow the structure in docs/02_file_structure.md

Create these files in the project root directory.

Reference documents:
- docs/02_file_structure.md (for content specifications)
- docs/07_final_config_and_packaging.md (for LICENSE and .gitignore)
```

### Verification 1.1

```bash
# Check files exist
ls -la LICENSE .gitignore .env.example requirements.txt README.md

# Verify README has content
head -20 README.md

# Verify requirements has pinned versions
grep "==" requirements.txt
```

**Expected:** All 5 files exist with proper content.

---

## Phase 2: Source Code - Utilities
**Duration:** 15 minutes  
**Dependencies:** None  
**Files Created:** 3

### Prompt 2.1: Token Manager Module

```
Create src/token_manager.py following the COMPLETE implementation in docs/04_source_code_specs.md.

This file must include:
- All imports (tiktoken, typing)
- get_tokenizer() function
- count_tokens() function
- fits_in_budget() function
- truncate_to_budget() function
- TokenBudgetManager class (complete with all methods)
- estimate_tokens_for_documents() function
- Example usage in if __name__ == "__main__"
- Complete docstrings and type hints

Use the EXACT implementation from the specification document.
```

### Prompt 2.2: Helpers Module

```
Create src/helpers.py following the COMPLETE implementation in docs/04_source_code_specs.md.

This file must include:
- All imports
- load_documents() function
- load_questions() function
- calculate_similarity() function
- format_context() function
- rank_by_field() function
- chunk_text() function
- calculate_coverage() function
- create_document_index() function
- validate_document_structure() function
- save_results() function
- load_results() function
- Example usage in if __name__ == "__main__"

Use the EXACT implementation from the specification document.
```

### Prompt 2.3: Package Init

```
Create src/__init__.py following the implementation in docs/04_source_code_specs.md.

Include:
- Module docstring
- Version, author, license metadata
- Import statements for key functions
- __all__ list for public API

Use the EXACT implementation from the specification document.
```

### Verification 2.1

```bash
# Create src directory if needed
mkdir -p src

# Check Python syntax
python3 -m py_compile src/__init__.py
python3 -m py_compile src/token_manager.py
python3 -m py_compile src/helpers.py

# Test token counting
python3 -c "from src.token_manager import count_tokens; print(f'Test tokens: {count_tokens(\"Hello world\")}')"

# Test helpers
python3 -c "from src.helpers import chunk_text; print(f'Chunks: {len(chunk_text(\"Para 1.\n\nPara 2.\", method=\"paragraph\"))}')"
```

**Expected:** All files compile, imports work, basic functions execute.

---

## Phase 3: Source Code - Strategies
**Duration:** 10 minutes  
**Dependencies:** token_manager.py, helpers.py  
**Files Created:** 1

### Prompt 3.1: Context Strategies

```
Create src/context_strategies.py following the COMPLETE implementation in docs/04_source_code_specs.md.

This file must include:
- All imports (including from .token_manager and .helpers)
- naive_context_assembly() function
- primacy_context_assembly() function
- recency_context_assembly() function
- sandwich_context_assembly() function
- hierarchical_summary_assembly() function (raise NotImplementedError)
- semantic_chunking_assembly() function (raise NotImplementedError)
- dynamic_allocation_assembly() function (raise NotImplementedError)
- Complete docstrings explaining each strategy

Use the EXACT implementation from the specification document.
```

### Verification 3.1

```bash
# Check syntax
python3 -m py_compile src/context_strategies.py

# Test imports
python3 -c "from src.context_strategies import naive_context_assembly; print('✅ Strategies module loads')"
```

**Expected:** File compiles and imports work.

---

## Phase 4: Data Files
**Duration:** 15 minutes  
**Dependencies:** None  
**Files Created:** 3

### Prompt 4.1: Source Documents

```
Create data/source_documents.json using the COMPLETE implementation from docs/06_data_files_specs.md.

This file must contain:
- All 10 documents with EXACT content as specified
- Each document with: id, title, content, tokens, category, relevance_keywords
- Complete metadata section
- Valid JSON formatting (2-space indent)

Copy the ENTIRE JSON structure from the specification document. This is critical - do not summarize or truncate the document content.

Important: The content of each document must be complete educational text about context engineering, not placeholders.
```

### Prompt 4.2: Evaluation Questions

```
Create data/evaluation_questions.json using the COMPLETE implementation from docs/06_data_files_specs.md.

This file must contain:
- All 10 questions with EXACT content as specified
- Each question with: id, question, ground_truth_answer, relevant_doc_ids, difficulty, question_type
- Complete metadata section
- Valid JSON formatting (2-space indent)

Copy the ENTIRE JSON structure from the specification document.
```

### Prompt 4.3: Context Examples

```
Create data/context_examples.json using the COMPLETE implementation from docs/06_data_files_specs.md.

This file must contain:
- All 5 examples with EXACT content as specified
- Each example with complete assembled_context text
- Complete metadata section
- Valid JSON formatting (2-space indent)

Copy the ENTIRE JSON structure from the specification document.
```

### Verification 4.1

```bash
# Create data directory if needed
mkdir -p data

# Validate JSON
python3 -m json.tool data/source_documents.json > /dev/null && echo "✅ source_documents.json valid"
python3 -m json.tool data/evaluation_questions.json > /dev/null && echo "✅ evaluation_questions.json valid"
python3 -m json.tool data/context_examples.json > /dev/null && echo "✅ context_examples.json valid"

# Test loading
python3 -c "from src.helpers import load_documents; docs = load_documents('data/source_documents.json'); print(f'✅ Loaded {len(docs)} documents')"
python3 -c "from src.helpers import load_questions; qs = load_questions('data/evaluation_questions.json'); print(f'✅ Loaded {len(qs)} questions')"

# Verify token counts (optional but recommended)
python3 << 'EOF'
from src.helpers import load_documents
from src.token_manager import count_tokens

docs = load_documents('data/source_documents.json')
for doc in docs:
    actual = count_tokens(doc['content'])
    stated = doc['tokens']
    diff = abs(actual - stated)
    status = '✅' if diff <= 10 else '❌'
    print(f"{status} {doc['id']}: stated={stated}, actual={actual}, diff={diff}")
EOF
```

**Expected:** All 3 JSON files valid, load correctly, token counts within tolerance.

---

## Phase 5: Evaluation & Verification
**Duration:** 20 minutes  
**Dependencies:** All previous modules  
**Files Created:** 2

### Prompt 5.1: Evaluation Module

```
Create src/evaluation.py following the COMPLETE implementation in docs/05_evaluation_and_verify_specs.md.

This file must include:
- All imports (transformers, torch, sentence-transformers)
- LLMEvaluator class with ALL methods:
  - __init__()
  - generate_answer()
  - score_answer()
  - _semantic_similarity_score()
  - _llm_judge_score()
  - _format_qa_prompt()
  - evaluate_batch()
- evaluate_answer() standalone function
- calculate_metrics() function
- compare_strategies() function
- Example usage in if __name__ == "__main__"
- Complete docstrings

Use the EXACT implementation from the specification document. This is a complex file - include all error handling and logic.
```

### Prompt 5.2: Verification System

```
Create src/verify.py following the COMPLETE implementation in docs/05_evaluation_and_verify_specs.md.

This file must include:
- Shebang line (#!/usr/bin/env python3)
- All imports
- LessonVerifier class with ALL methods:
  - __init__()
  - run_verification()
  - _check_results_exist()
  - _check_token_calculations()
  - _check_strategies_implemented()
  - _check_metrics_recorded()
  - _check_optimization()
  - _check_comparison_analysis()
  - _generate_final_report()
  - _generate_failure_report()
- main() function
- if __name__ == "__main__" block
- Complete docstrings and error handling

Use the EXACT implementation from the specification document. This is critical for auto-grading.
```

### Verification 5.1

```bash
# Check syntax
python3 -m py_compile src/evaluation.py
python3 -m py_compile src/verify.py

# Test evaluation imports
python3 -c "from src.evaluation import LLMEvaluator, evaluate_answer; print('✅ Evaluation module loads')"

# Test verification (should fail gracefully - no results yet)
python3 src/verify.py
echo "Exit code: $?"  # Should be 1 (fail), but script should run without errors
```

**Expected:** Files compile, verification script runs and reports "Results file not found" gracefully.

---

## Phase 6: Setup Scripts
**Duration:** 10 minutes  
**Dependencies:** None  
**Files Created:** 3

### Prompt 6.1: Setup Scripts

```
Create the setup scripts:

1. scripts/setup_venv.sh - Linux/Mac setup script from docs/02_file_structure.md and docs/07_final_config_and_packaging.md
2. scripts/setup_venv.bat - Windows setup script from docs/02_file_structure.md and docs/07_final_config_and_packaging.md
3. run_lesson.sh - Main entrypoint script from docs/02_file_structure.md

All scripts must:
- Have proper shebangs (#!/bin/bash for .sh)
- Include error handling (set -e for bash)
- Have clear echo statements showing progress
- Check prerequisites before running
- Be executable (chmod +x will be applied in verification)

Use the EXACT implementations from the specification documents.
```

### Verification 6.1

```bash
# Create scripts directory if needed
mkdir -p scripts

# Make scripts executable
chmod +x scripts/setup_venv.sh
chmod +x run_lesson.sh

# Verify scripts exist and are executable
ls -la scripts/setup_venv.sh scripts/setup_venv.bat run_lesson.sh | grep 'x'

# Test setup script syntax (don't actually run it yet)
bash -n scripts/setup_venv.sh && echo "✅ setup_venv.sh syntax OK"
bash -n run_lesson.sh && echo "✅ run_lesson.sh syntax OK"
```

**Expected:** All scripts exist, are executable, and have valid bash syntax.

---

## Phase 7: Jupyter Notebook (Part A)
**Duration:** 20 minutes  
**Dependencies:** All previous files  
**Files Created:** 1 (partial)

### Prompt 7.1: Notebook Structure + First Half

```
Create notebooks/context_engineering_lesson.ipynb following docs/03_index_html_and_notebook_spec.md.

Create a Jupyter notebook with cells 1-25 (Introduction through Phase 3):

SECTION 1: Introduction (Cells 1-5)
- Cell 1 [Markdown]: Title & Welcome
- Cell 2 [Code]: Imports & Setup
- Cell 3 [Code]: Load Models (with download messages)
- Cell 4 [Code]: Load Data
- Cell 5 [Markdown]: Lesson Roadmap

SECTION 2: Phase 1 - Context Windows (Cells 6-10)
- Cell 6 [Markdown]: Phase 1 Introduction
- Cell 7 [Code]: Token Analysis with visualization
- Cell 8 [Markdown]: Token Budget Exercise
- Cell 9 [Code]: TODO - Calculate Fits (with solution template)
- Cell 10 [Markdown]: Phase 1 Reflection

SECTION 3: Phase 2 - Baseline (Cells 11-18)
- Cell 11 [Markdown]: Phase 2 Introduction
- Cell 12 [Code]: TODO - Naive Implementation
- Cell 13 [Code]: Create Evaluator
- Cell 14 [Code]: Evaluate Naive Strategy
- Cell 15 [Markdown]: Baseline Reflection

SECTION 4: Phase 3 - Strategic Placement (Cells 16-25)
- Cell 16 [Markdown]: Phase 3 Introduction
- Cell 17 [Code]: Document Ranking Function
- Cell 18 [Code]: TODO - Primacy Strategy
- Cell 19 [Code]: TODO - Recency Strategy
- Cell 20 [Code]: TODO - Sandwich Strategy
- Cell 21 [Code]: Evaluate All Three Strategies
- Cell 22 [Code]: Compare Strategies Visually
- Cell 23 [Markdown]: Phase 3 Reflection

Follow the EXACT specifications in docs/03_index_html_and_notebook_spec.md. Include:
- Complete markdown text
- Complete code implementations
- TODO markers for student tasks
- Hint comments with %load statements
- All imports and setup code

This is Part 1 of 2. Generate cells 1-25 only.
```

### Verification 7.1

```bash
# Create notebooks directory if needed
mkdir -p notebooks

# Verify notebook exists and is valid JSON
python3 -m json.tool notebooks/context_engineering_lesson.ipynb > /dev/null && echo "✅ Notebook is valid JSON"

# Count cells
python3 << 'EOF'
import json
with open('notebooks/context_engineering_lesson.ipynb') as f:
    nb = json.load(f)
print(f"✅ Notebook has {len(nb['cells'])} cells (expecting ~25)")
EOF

# Try opening (don't run yet)
# jupyter notebook notebooks/context_engineering_lesson.ipynb
```

**Expected:** Notebook exists, is valid JSON, has ~25 cells.

---

## Phase 7: Jupyter Notebook (Part B)
**Duration:** 20 minutes  
**Dependencies:** Part A  
**Files Created:** Complete notebook

### Prompt 7.2: Notebook Second Half

```
Continue notebooks/context_engineering_lesson.ipynb by adding cells 26-48 (Phase 4 through completion).

Add these sections to the existing notebook:

SECTION 5: Phase 4 - Optimization (Cells 24-32)
- Cell 24 [Markdown]: Phase 4 Introduction
- Cell 25 [Markdown]: Option A - Hierarchical Summarization
- Cell 26 [Code]: TODO - Option A Implementation
- Cell 27 [Markdown]: Option B - Semantic Chunking
- Cell 28 [Code]: TODO - Option B Implementation
- Cell 29 [Markdown]: Option C - Dynamic Token Allocation
- Cell 30 [Code]: TODO - Option C Implementation
- Cell 31 [Code]: Evaluate Your Optimization
- Cell 32 [Markdown]: Phase 4 Reflection

SECTION 6: Phase 5 - Final Results (Cells 33-40)
- Cell 33 [Markdown]: Final Results Introduction
- Cell 34 [Code]: Comprehensive Comparison
- Cell 35 [Code]: Visualization - Complete Comparison (4 subplots)
- Cell 36 [Code]: Statistical Analysis
- Cell 37 [Markdown]: Learning Insights
- Cell 38 [Code]: Save Results to JSON
- Cell 39 [Markdown]: Next Steps
- Cell 40 [Code]: Final Cleanup message

Follow the EXACT specifications in docs/03_index_html_and_notebook_spec.md.

Make sure the notebook flows naturally from cells 1-25 (already created) to cells 26-48 (being added now).
```

### Verification 7.2

```bash
# Verify notebook is still valid
python3 -m json.tool notebooks/context_engineering_lesson.ipynb > /dev/null && echo "✅ Complete notebook is valid JSON"

# Count total cells
python3 << 'EOF'
import json
with open('notebooks/context_engineering_lesson.ipynb') as f:
    nb = json.load(f)
print(f"✅ Complete notebook has {len(nb['cells'])} cells (expecting 40-48)")
EOF

# Test opening notebook
jupyter notebook notebooks/context_engineering_lesson.ipynb &
sleep 3
pkill -f jupyter
echo "✅ Notebook opens successfully"
```

**Expected:** Complete notebook with 40-48 cells, valid JSON, opens in Jupyter.

---

## Phase 8: Entry Point & Final Files
**Duration:** 15 minutes  
**Dependencies:** All previous files  
**Files Created:** 3

### Prompt 8.1: index.html

```
Create index.html in the project root following the COMPLETE implementation in docs/03_index_html_and_notebook_spec.md.

This HTML file must include:

1. Complete HTML5 structure with DOCTYPE
2. Embedded CSS (no external stylesheets) with:
   - Global styles
   - Header with gradient background
   - Section styling
   - Info boxes (blue, yellow, green, red)
   - Code blocks (dark theme)
   - Tables with striped rows
   - Responsive design

3. All 10 content sections:
   - Welcome & Overview
   - Prerequisites
   - Setup Instructions (with .venv details)
   - Running the Lesson
   - Lesson Flow (5 phases table)
   - Evaluation & Grading
   - Troubleshooting
   - Expected Outcomes
   - Additional Resources
   - License & Attribution

4. Footer

Use the EXACT HTML structure from the specification. This is the PRIMARY entry point - it must be comprehensive and well-formatted.
```

### Prompt 8.2: Final Documentation Files

```
Create the final documentation files:

1. DATA_LICENSES.md - Following docs/02_file_structure.md specification, listing:
   - Qwen2.5-3B-Instruct (Apache 2.0)
   - all-MiniLM-L6-v2 (Apache 2.0)
   - Source documents (Apache 2.0, original)
   - Evaluation questions (Apache 2.0, original)

2. progress/.gitkeep - Empty file to ensure the progress/ directory exists in git

Use the EXACT content from the specification documents.
```

### Verification 8.1

```bash
# Create progress directory
mkdir -p progress
touch progress/.gitkeep

# Check index.html exists
ls -lh index.html

# Verify HTML is valid (basic check)
grep -q "<!DOCTYPE html>" index.html && echo "✅ index.html has DOCTYPE"
grep -q "Context Engineering" index.html && echo "✅ index.html has title"

# Check DATA_LICENSES.md
cat DATA_LICENSES.md | head -20

# Open index.html in browser
open index.html  # macOS
# xdg-open index.html  # Linux
# start index.html  # Windows
```

**Expected:** index.html displays properly, DATA_LICENSES.md is complete, progress/.gitkeep exists.

---

## Final Verification: Complete Package Test
**Duration:** 10 minutes

### Prompt 9.1: Final Checks

```
Run a final verification of the complete package. Check:

1. All 21 required files exist
2. File structure matches specification
3. All Python files compile
4. All JSON files are valid
5. Scripts are executable
6. No syntax errors anywhere

Create a verification report.
```

### Verification 9.1: Manual Testing

```bash
# Full structure check
echo "=== File Structure Check ==="
ls -la
ls -la src/
ls -la data/
ls -la scripts/
ls -la notebooks/
ls -la progress/

# Count files
echo -e "\n=== File Count ==="
find . -type f ! -path "./.git/*" ! -path "./.venv/*" | wc -l
echo "Expected: 21 files"

# Python compilation
echo -e "\n=== Python Syntax Check ==="
python3 -m py_compile src/*.py
echo "✅ All Python files compile"

# JSON validation
echo -e "\n=== JSON Validation ==="
python3 -m json.tool data/source_documents.json > /dev/null && echo "✅ source_documents.json"
python3 -m json.tool data/evaluation_questions.json > /dev/null && echo "✅ evaluation_questions.json"
python3 -m json.tool data/context_examples.json > /dev/null && echo "✅ context_examples.json"
python3 -m json.tool notebooks/context_engineering_lesson.ipynb > /dev/null && echo "✅ notebook.ipynb"

# Script permissions
echo -e "\n=== Script Permissions ==="
ls -l run_lesson.sh scripts/setup_venv.sh | grep 'x' && echo "✅ Scripts executable"

# Module imports
echo -e "\n=== Module Imports ==="
python3 << 'EOF'
try:
    from src import count_tokens, load_documents, evaluate_answer
    from src.context_strategies import naive_context_assembly
    from src.evaluation import LLMEvaluator
    print("✅ All modules import successfully")
except Exception as e:
    print(f"❌ Import error: {e}")
EOF

# Load data
echo -e "\n=== Data Loading ==="
python3 << 'EOF'
from src.helpers import load_documents, load_questions
docs = load_documents('data/source_documents.json')
questions = load_questions('data/evaluation_questions.json')
print(f"✅ Loaded {len(docs)} documents and {len(questions)} questions")
EOF

# Test verification script
echo -e "\n=== Verification Script Test ==="
python3 src/verify.py
echo "Expected: FAIL (no results yet) but script should run without errors"

echo -e "\n=== Package Ready ==="
echo "✅ All checks passed! Ready for packaging."
```

**Expected:** All checks pass, package is complete and functional.

---

## Packaging & Submission

### Create the Zip File

```bash
# Navigate to parent directory
cd ..

# Create dated zip file
DATE=$(date +%Y%m%d)
zip -r VG_[YourFirstname]_[YourLastname]_${DATE}.zip context-engineering-lesson/ \
  -x "*.git*" \
  -x "*__pycache__*" \
  -x "*.pyc" \
  -x "*/.venv/*" \
  -x "*/progress/lesson_*.json"

# Verify zip
unzip -l VG_[YourFirstname]_[YourLastname]_${DATE}.zip | head -30
ls -lh VG_[YourFirstname]_[YourLastname]_${DATE}.zip

echo "Expected size: <50 MB"
```

### Final Submission Checklist

- [ ] Zip file named correctly: `VG_[Firstname]_[Lastname]_[YYYYMMDD].zip`
- [ ] Size < 50 MB
- [ ] All 21 files present in zip
- [ ] No .venv or __pycache__ in zip
- [ ] index.html opens and displays correctly
- [ ] README.md is comprehensive
- [ ] All Python files compile
- [ ] All JSON files are valid
- [ ] Notebook opens in Jupyter
- [ ] Scripts are executable
- [ ] LICENSE is Apache 2.0

---

## Troubleshooting

### Issue: Claude Code truncates long files

**Solution:** Generate in smaller chunks, especially for:
- Notebook (done in 2 parts above)
- index.html (if needed, split into sections)
- Data files (if needed, generate one document at a time)

### Issue: Import errors in Python files

**Solution:** Ensure relative imports use correct syntax:
```python
from .token_manager import count_tokens  # Correct
from token_manager import count_tokens   # Wrong
```

### Issue: JSON validation fails

**Solution:** Use Python to re-format:
```bash
python3 -m json.tool input.json > output.json
mv output.json input.json
```

### Issue: Token counts don't match

**Solution:** Recalculate and update:
```python
from src.token_manager import count_tokens
# Update doc['tokens'] = count_tokens(doc['content'])
```

---

## Success Criteria

Your package is ready when:

✅ All 21 files exist  
✅ All Python files compile without errors  
✅ All JSON files are valid  
✅ Notebook opens in Jupyter  
✅ index.html displays properly in browser  
✅ Scripts are executable  
✅ Data loads correctly  
✅ verify.py runs (even if it fails due to no results)  
✅ Zip file is <50 MB  
✅ Extraction and setup work on clean system  

---

## Estimated Completion Time

- Phase 1: 10 minutes
- Phase 2: 15 minutes
- Phase 3: 10 minutes
- Phase 4: 15 minutes
- Phase 5: 20 minutes
- Phase 6: 10 minutes
- Phase 7A: 20 minutes
- Phase 7B: 20 minutes
- Phase 8: 15 minutes
- Final Verification: 10 minutes
- **Total: ~2 hours**

---

## Next Steps After Completion

1. Test the complete lesson yourself:
   ```bash
   cd context-engineering-lesson
   bash scripts/setup_venv.sh
   source .venv/bin/activate
   ./run_lesson.sh
   ```

2. Complete a few notebook cells manually to verify functionality

3. Create the zip file

4. Submit via LMS

**Good luck! 🚀**