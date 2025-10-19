# Claude Code Prompts - Quick Reference
## Copy-Paste These Prompts in Order

---

## Phase 1: Foundation Files (10 min)

### Prompt 1.1
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

**Test:**
```bash
ls -la LICENSE .gitignore .env.example requirements.txt README.md
```

---

## Phase 2: Source Code Utilities (15 min)

### Prompt 2.1
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

### Prompt 2.2
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

### Prompt 2.3
```
Create src/__init__.py following the implementation in docs/04_source_code_specs.md.

Include:
- Module docstring
- Version, author, license metadata
- Import statements for key functions
- __all__ list for public API

Use the EXACT implementation from the specification document.
```

**Test:**
```bash
python3 -m py_compile src/*.py
python3 -c "from src.token_manager import count_tokens; print(count_tokens('test'))"
```

---

## Phase 3: Context Strategies (10 min)

### Prompt 3.1
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

**Test:**
```bash
python3 -c "from src.context_strategies import naive_context_assembly; print('✅ OK')"
```

---

## Phase 4: Data Files (15 min)

### Prompt 4.1
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

### Prompt 4.2
```
Create data/evaluation_questions.json using the COMPLETE implementation from docs/06_data_files_specs.md.

This file must contain:
- All 10 questions with EXACT content as specified
- Each question with: id, question, ground_truth_answer, relevant_doc_ids, difficulty, question_type
- Complete metadata section
- Valid JSON formatting (2-space indent)

Copy the ENTIRE JSON structure from the specification document.
```

### Prompt 4.3
```
Create data/context_examples.json using the COMPLETE implementation from docs/06_data_files_specs.md.

This file must contain:
- All 5 examples with EXACT content as specified
- Each example with complete assembled_context text
- Complete metadata section
- Valid JSON formatting (2-space indent)

Copy the ENTIRE JSON structure from the specification document.
```

**Test:**
```bash
python3 -m json.tool data/source_documents.json > /dev/null && echo "✅ Valid"
python3 -c "from src.helpers import load_documents; print(f'Loaded {len(load_documents(\"data/source_documents.json\"))} docs')"
```

---

## Phase 5: Evaluation & Verification (20 min)

### Prompt 5.1
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

### Prompt 5.2
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

**Test:**
```bash
python3 -m py_compile src/evaluation.py src/verify.py
python3 src/verify.py  # Should fail gracefully
```

---

## Phase 6: Setup Scripts (10 min)

### Prompt 6.1
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

**Test:**
```bash
chmod +x scripts/setup_venv.sh run_lesson.sh
bash -n scripts/setup_venv.sh && echo "✅ Valid syntax"
```

---

## Phase 7A: Notebook First Half (20 min)

### Prompt 7.1
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

**Test:**
```bash
python3 -m json.tool notebooks/context_engineering_lesson.ipynb > /dev/null && echo "✅ Valid"
```

---

## Phase 7B: Notebook Second Half (20 min)

### Prompt 7.2
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

**Test:**
```bash
python3 << 'EOF'
import json
with open('notebooks/context_engineering_lesson.ipynb') as f:
    nb = json.load(f)
print(f"✅ Total cells: {len(nb['cells'])}")
EOF
```

---

## Phase 8: Entry Point & Final Files (15 min)

### Prompt 8.1
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

### Prompt 8.2
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

**Test:**
```bash
open index.html  # macOS
# xdg-open index.html  # Linux
grep "Context Engineering" index.html && echo "✅ Found"
```

---

## Final Verification (10 min)

### Run Complete Package Test
```bash
# Structure check
find . -type f ! -path "./.git/*" ! -path "./.venv/*" | wc -l
echo "Expected: 21 files"

# Python compilation
python3 -m py_compile src/*.py

# JSON validation
for f in data/*.json notebooks/*.ipynb; do
    python3 -m json.tool "$f" > /dev/null && echo "✅ $f"
done

# Module imports
python3 -c "from src import count_tokens, load_documents; print('✅ Imports OK')"

# Data loading
python3 -c "from src.helpers import load_documents; print(f'✅ {len(load_documents(\"data/source_documents.json\"))} docs')"

# Verify script
python3 src/verify.py

echo "✅ Package complete!"
```

---

## Create Zip File

```bash
cd ..
DATE=$(date +%Y%m%d)
zip -r VG_[Firstname]_[Lastname]_${DATE}.zip context-engineering-lesson/ \
  -x "*.git*" -x "*__pycache__*" -x "*.pyc" -x "*/.venv/*" -x "*/progress/lesson_*.json"

ls -lh VG_*.zip
echo "Expected: <50 MB"
```

---

## Summary: Execution Order

1. **Phase 1** → Foundation files (LICENSE, .gitignore, requirements.txt, README.md, .env.example)
2. **Phase 2** → Source utilities (token_manager.py, helpers.py, __init__.py)
3. **Phase 3** → Context strategies (context_strategies.py)
4. **Phase 4** → Data files (3 JSON files)
5. **Phase 5** → Evaluation system (evaluation.py, verify.py)
6. **Phase 6** → Setup scripts (3 scripts)
7. **Phase 7A** → Notebook first half (cells 1-25)
8. **Phase 7B** → Notebook second half (cells 26-48)
9. **Phase 8** → Entry point (index.html, DATA_LICENSES.md, .gitkeep)
10. **Final** → Verify and package

**Total Time: ~2 hours**

---

## Quick Troubleshooting

**Claude truncates content?** → Ask it to generate in smaller sections
**Import errors?** → Check relative imports use `.` (from .token_manager)
**JSON invalid?** → Use `python3 -m json.tool file.json > temp.json && mv temp.json file.json`
**Scripts not executable?** → Run `chmod +x script.sh`

---

## Success Checklist

- [ ] 21 files exist
- [ ] All Python files compile
- [ ] All JSON valid
- [ ] Notebook opens
- [ ] index.html displays
- [ ] Scripts executable
- [ ] Data loads
- [ ] verify.py runs
- [ ] Zip < 50 MB

**Ready to submit! 🎉**