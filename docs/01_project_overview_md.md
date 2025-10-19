# Context Engineering Micro-Lesson - Project Overview

## Document Purpose
This document provides the complete overview and strategy for the Context Engineering interactive lesson. Use this as the foundation when generating code in Claude Code.

---

## Core Concept

**Lesson Title:** Context Engineering - Optimizing LLM Context Windows

**Duration:** ~30 minutes active learner time

**Approach:** 100% FREE - Uses local open-source models (no API costs)

---

## Why This Approach?

The lesson uses **local models** to eliminate API costs and ensure accessibility:

1. **Model:** `Qwen2.5-3B-Instruct` via Hugging Face Transformers
   - Small enough to run on CPU
   - Good quality for educational purposes
   - ~6.5 GB download (within 50 GB external download limit)
   - Runs on 8GB+ RAM systems

2. **Alternative (if GPU available):** `Mistral-7B-Instruct-v0.2`
   - Better performance with GPU
   - Still free and local

3. **Embedding Model:** `sentence-transformers/all-MiniLM-L6-v2`
   - Lightweight (80 MB)
   - Fast on CPU
   - Perfect for similarity calculations

---

## Learning Objectives

Students will:

1. **Understand context windows** - Token limits, counting, budgets
2. **Implement baseline context assembly** - Naive concatenation approach
3. **Test strategic placement** - Primacy, recency, sandwich strategies
4. **Measure the difference** - Quantitative comparison of approaches
5. **Apply optimization** - Context compression or hierarchical structuring

---

## Key Technical Decisions

### Free & Local
- ✅ No API keys required
- ✅ No API costs
- ✅ Works offline after initial model download
- ✅ Reproducible results

### Hardware Requirements
- **Minimum:** 8 GB RAM, CPU only
- **Recommended:** 16 GB RAM + GPU (optional)
- **Disk:** ~10 GB total (7 GB models + 3 GB workspace)

### External Downloads
- Qwen2.5-3B-Instruct: ~6.5 GB (Hugging Face)
- all-MiniLM-L6-v2: ~80 MB (Hugging Face)
- Total: ~6.6 GB (well under 50 GB limit)

---

## Lesson Architecture

### Phase 1: Understanding Context Windows (7 min)
**Concept:** Token mechanics and budget constraints

**Activity:**
- Load 10 sample documents (varied lengths: 200-2000 tokens each)
- Calculate total tokens
- Determine what fits in 2K, 4K, 8K context windows
- Interactive token counter visualization

**Deliverable:** Understanding of token budgets

---

### Phase 2: Baseline Implementation (8 min)
**Concept:** Naive context assembly

**Activity:**
- Implement `naive_context_assembly()` function
- Concatenate documents until token limit
- Test with 5 evaluation questions
- Measure: accuracy, tokens used, latency

**Code Template:**
```python
def naive_context_assembly(documents, query, token_limit=4000):
    """
    TODO: Implement basic context assembly
    - Concatenate documents in order
    - Stop when approaching token_limit
    - Return assembled context string
    """
    # Student fills this in
    pass
```

**Deliverable:** Baseline metrics recorded

---

### Phase 3: Strategic Placement (10 min)
**Concept:** Position matters - "lost in the middle"

**Activity:** Implement THREE strategies

**Strategy A: Primacy** (most relevant first)
```python
def primacy_context_assembly(documents, query, token_limit=4000):
    """
    TODO: Rank documents by relevance to query
    Place most relevant at the BEGINNING
    """
    pass
```

**Strategy B: Recency** (most relevant last)
```python
def recency_context_assembly(documents, query, token_limit=4000):
    """
    TODO: Rank documents by relevance to query
    Place most relevant at the END
    """
    pass
```

**Strategy C: Sandwich** (relevant at both ends)
```python
def sandwich_context_assembly(documents, query, token_limit=4000):
    """
    TODO: Split top-ranked documents
    Place half at START, half at END
    Less relevant in the middle
    """
    pass
```

**Hint System:**
- Hint 1: "Use sentence transformer embeddings to calculate cosine similarity"
- Hint 2: "The paper suggests important info at boundaries performs better"
- Hint 3: "Try placing top 2 docs at start, bottom 2 at end"

**Deliverable:** Comparison table showing which strategy performs best

---

### Phase 4: Optimization Challenge (5 min)
**Concept:** Advanced context engineering

**Activity:** Choose ONE optimization to implement

**Option A: Hierarchical Summarization**
- Summarize less-relevant documents
- Keep full text for most relevant
- Measure token savings vs. quality trade-off

**Option B: Semantic Chunking**
- Split documents at semantic boundaries (paragraphs)
- Only include most relevant chunks
- Better than arbitrary cutoffs

**Option C: Dynamic Token Allocation**
- Allocate tokens proportional to relevance scores
- High-relevance docs get more tokens
- Ensures critical info isn't truncated

**Deliverable:** Optimization shows ≥10% improvement OR ≥20% token reduction

---

### Phase 5: Auto-Grading (Automatic)
**Concept:** Verify learning objectives met

**Command:** `python src/verify.py`

**Checks:**
1. ✅ Token calculations within ±5% accuracy
2. ✅ All four strategies implemented (naive + 3 strategic)
3. ✅ Metrics recorded for all strategies
4. ✅ At least one optimization implemented
5. ✅ Optimization shows measurable improvement

**Output:** `progress/lesson_progress.json`

---

## Evaluation Methodology

### Ground Truth Q&A Pairs
- 10 questions covering the document corpus
- Questions require multi-document reasoning
- Human-verified correct answers

### Automated Scoring
Uses local LLM as judge:
1. Generate answer with each context strategy
2. Compare to ground truth using semantic similarity
3. Score 0-1 (0=wrong, 1=perfect)
4. Average across all 10 questions

### Metrics Tracked
| Metric | Description |
|--------|-------------|
| Accuracy | Avg score across all questions (0-1) |
| Token Usage | Avg tokens in assembled context |
| Token Efficiency | Accuracy per 1000 tokens |
| Latency | Avg response time per query |

---

## Expected Results

Based on research literature, students should see:

| Strategy | Expected Accuracy | Insight |
|----------|------------------|---------|
| Naive | 0.65-0.72 | Baseline - no optimization |
| Primacy | 0.70-0.77 | +5-8% - good but not optimal |
| Recency | 0.75-0.82 | +10-15% - leverages recency bias |
| Sandwich | 0.78-0.85 | +15-20% - avoids "lost in middle" |
| Optimized | 0.80-0.88 | +20-25% - best performance |

These ranges account for model variability and dataset differences.

---

## Technical Stack

### Required Libraries
```
transformers==4.45.2        # Hugging Face models
torch==2.4.1               # PyTorch backend
sentence-transformers==3.1.1  # Embeddings
tiktoken==0.8.0            # Token counting
accelerate==0.34.2         # Fast inference
pandas==2.2.3              # Data handling
numpy==2.1.3               # Numerical ops
jupyter==1.1.1             # Notebook interface
python-dotenv==1.0.1       # Config (optional, no API keys needed)
tqdm==4.66.6               # Progress bars
scikit-learn==1.5.2        # Metrics
```

### Model Downloads (Automatic via Hugging Face)
- `Qwen/Qwen2.5-3B-Instruct` - Main LLM
- `sentence-transformers/all-MiniLM-L6-v2` - Embeddings

---

## Success Criteria

### Passing the Lesson
Students must:
1. Complete all implementation tasks
2. Run all experiments
3. Record metrics accurately
4. Show measurable improvement with optimization
5. Pass auto-grading verification

### Learning Outcomes Achieved
Students will be able to:
- Calculate token budgets for any context window
- Explain the "lost in the middle" problem
- Choose appropriate context strategies for different scenarios
- Measure and optimize context engineering decisions
- Apply these techniques to real-world LLM applications

---

## File Generation Priority

When moving to Claude Code, generate in this order:

### Priority 1 (Critical Path)
1. `requirements.txt` - Dependencies
2. `data/source_documents.json` - Document corpus
3. `data/evaluation_questions.json` - Test queries
4. `notebooks/context_engineering_lesson.ipynb` - Main lesson

### Priority 2 (Core Functionality)
5. `src/token_manager.py` - Token utilities
6. `src/context_strategies.py` - Implementation templates
7. `src/evaluation.py` - Scoring system
8. `src/helpers.py` - Utility functions

### Priority 3 (Supporting Files)
9. `src/verify.py` - Auto-grading
10. `index.html` - Lesson guide
11. `run_lesson.sh` - Entrypoint
12. `scripts/setup_venv.sh` - Environment setup

### Priority 4 (Documentation)
13. `README.md` - Project overview
14. `LICENSE` - Apache 2.0
15. `DATA_LICENSES.md` - Third-party licenses
16. `.env.example` - Config template (empty, kept for consistency)

---

## Next Steps

1. Save this document as `docs/01_project_overview.md`
2. Review and confirm the free/local approach works for you
3. Request next chunk: File Structure & Technical Specifications

---

**Ready for the next chunk when you are!**
