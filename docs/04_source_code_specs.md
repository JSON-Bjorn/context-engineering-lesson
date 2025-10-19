# Context Engineering Lesson - Source Code Specifications

## Document Purpose
This document provides complete specifications for all Python source files in the `src/` directory. These are the core implementation files that power the lesson.

---

## Source Files Overview

```
src/
├── __init__.py              # Package initialization and exports
├── token_manager.py         # Token counting and budget management
├── helpers.py               # Data loading and utility functions
├── context_strategies.py    # Student implementation templates
├── evaluation.py            # LLM-based scoring and evaluation
└── verify.py               # Auto-grading system
```

---

# File 1: src/__init__.py

## Purpose
Package initialization file that makes src/ a proper Python package and exposes key functions for easy importing.

## Size
~1 KB

## Complete Implementation

```python
"""
Context Engineering Lesson - Core Implementation Package

This package contains the infrastructure for the interactive context engineering lesson.
Students will use these utilities while implementing their own context assembly strategies.

Modules:
    token_manager: Token counting and budget management utilities
    helpers: Data loading and general utility functions
    context_strategies: Template implementations for students to complete
    evaluation: LLM-based answer evaluation and scoring
    verify: Auto-grading system for lesson completion

Author: [Your Name]
License: Apache 2.0
Python: 3.12+
"""

__version__ = "1.0.0"
__author__ = "[Your Name]"
__license__ = "Apache 2.0"

# Import key functions for convenient access
from .token_manager import (
    count_tokens,
    fits_in_budget,
    TokenBudgetManager,
)

from .helpers import (
    load_documents,
    load_questions,
    calculate_similarity,
    format_context,
)

from .evaluation import (
    evaluate_answer,
    LLMEvaluator,
)

# Define public API
__all__ = [
    # Token management
    'count_tokens',
    'fits_in_budget',
    'TokenBudgetManager',
    
    # Data utilities
    'load_documents',
    'load_questions',
    'calculate_similarity',
    'format_context',
    
    # Evaluation
    'evaluate_answer',
    'LLMEvaluator',
]
```

---

# File 2: src/token_manager.py

## Purpose
Provides utilities for counting tokens and managing token budgets. Critical for context window management.

## Size
~5-6 KB

## Dependencies
- tiktoken (for accurate token counting)

## Complete Implementation

```python
"""
Token Manager - Utilities for token counting and budget management

This module provides functions to count tokens accurately and manage token budgets
when assembling contexts for LLMs.
"""

import tiktoken
from typing import List, Dict, Union


# Initialize tokenizer (cl100k_base is used by GPT-4, GPT-3.5, and is a good general-purpose encoder)
_TOKENIZER = None

def get_tokenizer(model_name: str = "cl100k_base"):
    """
    Get or create tokenizer instance.
    
    Args:
        model_name: Tokenizer encoding to use
        
    Returns:
        tiktoken.Encoding instance
    """
    global _TOKENIZER
    if _TOKENIZER is None:
        _TOKENIZER = tiktoken.get_encoding(model_name)
    return _TOKENIZER


def count_tokens(text: str, model_name: str = "cl100k_base") -> int:
    """
    Count the number of tokens in a text string.
    
    Args:
        text: The text to tokenize
        model_name: Tokenizer encoding to use
        
    Returns:
        Number of tokens as integer
        
    Examples:
        >>> count_tokens("Hello, world!")
        4
        >>> count_tokens("Context engineering is important.")
        6
    """
    if not text:
        return 0
    
    tokenizer = get_tokenizer(model_name)
    tokens = tokenizer.encode(text)
    return len(tokens)


def fits_in_budget(text: str, budget: int, model_name: str = "cl100k_base") -> bool:
    """
    Check if text fits within a token budget.
    
    Args:
        text: The text to check
        budget: Maximum number of tokens allowed
        model_name: Tokenizer encoding to use
        
    Returns:
        True if text fits, False otherwise
        
    Examples:
        >>> fits_in_budget("Short text", 100)
        True
        >>> fits_in_budget("Very long text..." * 1000, 100)
        False
    """
    return count_tokens(text, model_name) <= budget


def truncate_to_budget(text: str, budget: int, model_name: str = "cl100k_base", 
                       from_end: bool = False) -> str:
    """
    Truncate text to fit within token budget.
    
    Args:
        text: The text to truncate
        budget: Maximum number of tokens
        model_name: Tokenizer encoding to use
        from_end: If True, truncate from end; if False, truncate from beginning
        
    Returns:
        Truncated text that fits within budget
        
    Examples:
        >>> truncate_to_budget("This is a long sentence that needs truncation", 5)
        "This is a long sentence"
    """
    if fits_in_budget(text, budget, model_name):
        return text
    
    tokenizer = get_tokenizer(model_name)
    tokens = tokenizer.encode(text)
    
    if from_end:
        truncated_tokens = tokens[:budget]
    else:
        truncated_tokens = tokens[-budget:]
    
    return tokenizer.decode(truncated_tokens)


class TokenBudgetManager:
    """
    Manages token budgets for context assembly.
    
    Helps track token usage as documents are added to context,
    ensuring the total stays within limits.
    
    Examples:
        >>> manager = TokenBudgetManager(max_tokens=4000, overhead=300)
        >>> manager.can_add(500)
        True
        >>> manager.add(500)
        >>> manager.remaining
        3200
    """
    
    def __init__(self, max_tokens: int, overhead: int = 300, model_name: str = "cl100k_base"):
        """
        Initialize token budget manager.
        
        Args:
            max_tokens: Maximum total tokens allowed
            overhead: Tokens to reserve for query, response, instructions
            model_name: Tokenizer encoding to use
        """
        self.max_tokens = max_tokens
        self.overhead = overhead
        self.model_name = model_name
        self.used_tokens = 0
        self.available_tokens = max_tokens - overhead
        
    @property
    def remaining(self) -> int:
        """Get remaining token budget."""
        return self.available_tokens - self.used_tokens
    
    @property
    def utilization(self) -> float:
        """Get budget utilization as percentage (0-1)."""
        return self.used_tokens / self.available_tokens if self.available_tokens > 0 else 0
    
    def can_add(self, tokens: Union[int, str]) -> bool:
        """
        Check if tokens/text can be added within budget.
        
        Args:
            tokens: Either number of tokens (int) or text to count (str)
            
        Returns:
            True if addition fits, False otherwise
        """
        if isinstance(tokens, str):
            tokens = count_tokens(tokens, self.model_name)
        
        return self.used_tokens + tokens <= self.available_tokens
    
    def add(self, tokens: Union[int, str]) -> bool:
        """
        Add tokens to the budget tracker.
        
        Args:
            tokens: Either number of tokens (int) or text to count (str)
            
        Returns:
            True if added successfully, False if would exceed budget
        """
        if isinstance(tokens, str):
            token_count = count_tokens(tokens, self.model_name)
        else:
            token_count = tokens
        
        if self.used_tokens + token_count <= self.available_tokens:
            self.used_tokens += token_count
            return True
        return False
    
    def reset(self):
        """Reset the budget tracker to zero usage."""
        self.used_tokens = 0
    
    def __repr__(self):
        return (f"TokenBudgetManager(max={self.max_tokens}, "
                f"used={self.used_tokens}, "
                f"remaining={self.remaining}, "
                f"utilization={self.utilization:.1%})")


def estimate_tokens_for_documents(documents: List[Dict], 
                                  include_formatting: bool = True) -> int:
    """
    Estimate total tokens needed for a list of documents.
    
    Args:
        documents: List of document dicts with 'content' or 'tokens' field
        include_formatting: Whether to add overhead for separators and formatting
        
    Returns:
        Estimated total tokens
    """
    total = 0
    formatting_overhead_per_doc = 10  # For separators, titles, etc.
    
    for doc in documents:
        # Use pre-calculated tokens if available, otherwise count
        if 'tokens' in doc:
            total += doc['tokens']
        else:
            total += count_tokens(doc.get('content', ''))
        
        if include_formatting:
            total += formatting_overhead_per_doc
    
    return total


# Example usage and tests
if __name__ == "__main__":
    # Test token counting
    test_text = "Context engineering is the practice of optimizing how information is structured for LLMs."
    token_count = count_tokens(test_text)
    print(f"Text: '{test_text}'")
    print(f"Tokens: {token_count}")
    print()
    
    # Test budget manager
    manager = TokenBudgetManager(max_tokens=4000, overhead=300)
    print(f"Budget manager initialized: {manager}")
    
    manager.add(500)
    print(f"After adding 500 tokens: {manager}")
    
    print(f"Can add 3000 more? {manager.can_add(3000)}")
    print(f"Can add 3500 more? {manager.can_add(3500)}")
    
    print("\n✅ Token manager tests complete!")
```

---

# File 3: src/helpers.py

## Purpose
General utility functions for loading data, calculating similarity, and formatting context.

## Size
~6-8 KB

## Dependencies
- json, pathlib (built-in)
- torch, numpy
- sentence-transformers (for similarity)

## Complete Implementation

```python
"""
Helpers - Utility functions for the context engineering lesson

This module provides helper functions for:
- Loading documents and questions from JSON
- Calculating semantic similarity
- Formatting context strings
- General utilities
"""

import json
from pathlib import Path
from typing import List, Dict, Tuple, Optional
import torch
import numpy as np


def load_documents(filepath: str) -> List[Dict]:
    """
    Load documents from JSON file.
    
    Args:
        filepath: Path to JSON file containing documents
        
    Returns:
        List of document dictionaries
        
    Raises:
        FileNotFoundError: If file doesn't exist
        json.JSONDecodeError: If file is not valid JSON
    """
    filepath = Path(filepath)
    
    if not filepath.exists():
        raise FileNotFoundError(f"Document file not found: {filepath}")
    
    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Handle both formats: {'documents': [...]} and direct [...]
    if isinstance(data, dict) and 'documents' in data:
        documents = data['documents']
    elif isinstance(data, list):
        documents = data
    else:
        raise ValueError("Invalid document file format")
    
    print(f"✅ Loaded {len(documents)} documents from {filepath.name}")
    return documents


def load_questions(filepath: str) -> List[Dict]:
    """
    Load evaluation questions from JSON file.
    
    Args:
        filepath: Path to JSON file containing questions
        
    Returns:
        List of question dictionaries
        
    Raises:
        FileNotFoundError: If file doesn't exist
        json.JSONDecodeError: If file is not valid JSON
    """
    filepath = Path(filepath)
    
    if not filepath.exists():
        raise FileNotFoundError(f"Question file not found: {filepath}")
    
    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Handle both formats: {'questions': [...]} and direct [...]
    if isinstance(data, dict) and 'questions' in data:
        questions = data['questions']
    elif isinstance(data, list):
        questions = data
    else:
        raise ValueError("Invalid question file format")
    
    print(f"✅ Loaded {len(questions)} questions from {filepath.name}")
    return questions


def calculate_similarity(embedding1: torch.Tensor, 
                        embedding2: torch.Tensor,
                        method: str = 'cosine') -> torch.Tensor:
    """
    Calculate similarity between two embeddings.
    
    Args:
        embedding1: First embedding tensor
        embedding2: Second embedding tensor
        method: Similarity method ('cosine' or 'dot')
        
    Returns:
        Similarity score as tensor
    """
    if method == 'cosine':
        # Cosine similarity
        similarity = torch.nn.functional.cosine_similarity(
            embedding1.unsqueeze(0), 
            embedding2.unsqueeze(0)
        )
    elif method == 'dot':
        # Dot product similarity
        similarity = torch.dot(embedding1.flatten(), embedding2.flatten())
    else:
        raise ValueError(f"Unknown similarity method: {method}")
    
    return similarity


def format_context(documents: List[Dict], 
                   include_titles: bool = True,
                   separator: str = "\n\n---\n\n") -> str:
    """
    Format a list of documents into a context string.
    
    Args:
        documents: List of document dicts with 'content' and optionally 'title'
        include_titles: Whether to include document titles
        separator: String to separate documents
        
    Returns:
        Formatted context string
    """
    formatted_parts = []
    
    for i, doc in enumerate(documents):
        if include_titles and 'title' in doc:
            part = f"Document {i+1}: {doc['title']}\n\n{doc['content']}"
        else:
            part = doc['content']
        
        formatted_parts.append(part)
    
    return separator.join(formatted_parts)


def rank_by_field(items: List[Dict], 
                  field: str, 
                  ascending: bool = False) -> List[Dict]:
    """
    Rank items by a specific field value.
    
    Args:
        items: List of dictionaries
        field: Field name to rank by
        ascending: If True, rank low to high; if False, high to low
        
    Returns:
        Sorted list of items
    """
    return sorted(items, key=lambda x: x.get(field, 0), reverse=not ascending)


def chunk_text(text: str, 
               method: str = 'paragraph',
               max_chunk_size: Optional[int] = None) -> List[str]:
    """
    Split text into chunks using various strategies.
    
    Args:
        text: Text to chunk
        method: Chunking method ('paragraph', 'sentence', 'fixed')
        max_chunk_size: Maximum characters per chunk (for 'fixed' method)
        
    Returns:
        List of text chunks
    """
    if method == 'paragraph':
        # Split on double newlines
        chunks = [p.strip() for p in text.split('\n\n') if p.strip()]
    
    elif method == 'sentence':
        # Simple sentence splitting (could be enhanced with nltk)
        import re
        sentences = re.split(r'[.!?]+\s+', text)
        chunks = [s.strip() for s in sentences if s.strip()]
    
    elif method == 'fixed':
        # Fixed-size chunks
        if max_chunk_size is None:
            max_chunk_size = 500
        chunks = [text[i:i+max_chunk_size] 
                 for i in range(0, len(text), max_chunk_size)]
    
    else:
        raise ValueError(f"Unknown chunking method: {method}")
    
    return chunks


def calculate_coverage(selected_docs: List[Dict], 
                       all_docs: List[Dict]) -> float:
    """
    Calculate what percentage of total content is covered by selected documents.
    
    Args:
        selected_docs: Documents that were selected
        all_docs: All available documents
        
    Returns:
        Coverage percentage (0-1)
    """
    selected_tokens = sum(doc.get('tokens', 0) for doc in selected_docs)
    total_tokens = sum(doc.get('tokens', 0) for doc in all_docs)
    
    return selected_tokens / total_tokens if total_tokens > 0 else 0


def create_document_index(documents: List[Dict]) -> Dict[str, Dict]:
    """
    Create an index of documents by ID for quick lookup.
    
    Args:
        documents: List of document dicts with 'id' field
        
    Returns:
        Dictionary mapping doc IDs to document dicts
    """
    return {doc['id']: doc for doc in documents if 'id' in doc}


def validate_document_structure(documents: List[Dict]) -> Tuple[bool, List[str]]:
    """
    Validate that documents have required fields.
    
    Args:
        documents: List of document dicts to validate
        
    Returns:
        Tuple of (is_valid, list_of_errors)
    """
    required_fields = ['content']
    recommended_fields = ['id', 'title', 'tokens']
    
    errors = []
    
    for i, doc in enumerate(documents):
        # Check required fields
        for field in required_fields:
            if field not in doc:
                errors.append(f"Document {i} missing required field: {field}")
        
        # Warn about recommended fields
        for field in recommended_fields:
            if field not in doc:
                errors.append(f"Document {i} missing recommended field: {field}")
    
    is_valid = len([e for e in errors if 'required' in e]) == 0
    return is_valid, errors


def save_results(results: Dict, filepath: str):
    """
    Save results dictionary to JSON file.
    
    Args:
        results: Dictionary to save
        filepath: Output file path
    """
    filepath = Path(filepath)
    filepath.parent.mkdir(parents=True, exist_ok=True)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Results saved to {filepath}")


def load_results(filepath: str) -> Dict:
    """
    Load results from JSON file.
    
    Args:
        filepath: Path to results file
        
    Returns:
        Results dictionary
    """
    filepath = Path(filepath)
    
    if not filepath.exists():
        raise FileNotFoundError(f"Results file not found: {filepath}")
    
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)


# Example usage
if __name__ == "__main__":
    print("Testing helper functions...\n")
    
    # Test text chunking
    sample_text = """This is paragraph one.
It has multiple sentences.

This is paragraph two.
It also has content.

And here's paragraph three."""
    
    chunks = chunk_text(sample_text, method='paragraph')
    print(f"Chunked into {len(chunks)} paragraphs:")
    for i, chunk in enumerate(chunks, 1):
        print(f"  {i}. {chunk[:50]}...")
    
    print("\n✅ Helper function tests complete!")
```

---

# File 4: src/context_strategies.py

## Purpose
Template implementations for context assembly strategies. Students will complete the TODO sections.

## Size
~8-10 KB

## Complete Implementation

```python
"""
Context Strategies - Template implementations for students

This module contains skeleton implementations of various context assembly strategies.
Students will complete the TODO sections as part of the lesson.

NOTE: This file contains TEMPLATE code with TODOs. The completed versions
should be in the lesson notebook, not here.
"""

from typing import List, Dict, Optional
from .token_manager import TokenBudgetManager, count_tokens
from .helpers import format_context


def naive_context_assembly(documents: List[Dict], 
                           query: str,
                           token_limit: int = 4000) -> str:
    """
    TEMPLATE: Naive context assembly - concatenate in order until limit.
    
    Students implement this in the notebook. This is a reference implementation
    for the verification system.
    
    Args:
        documents: List of document dicts
        query: Question being asked
        token_limit: Maximum tokens for context
        
    Returns:
        Assembled context string
    """
    budget_manager = TokenBudgetManager(max_tokens=token_limit, overhead=50)
    context_parts = []
    
    for doc in documents:
        doc_text = f"Document: {doc.get('title', 'Untitled')}\n\n{doc['content']}"
        
        if budget_manager.can_add(doc_text):
            budget_manager.add(doc_text)
            context_parts.append(doc_text)
        else:
            break
    
    return "\n\n---\n\n".join(context_parts)


def primacy_context_assembly(documents: List[Dict],
                             query: str,
                             token_limit: int = 4000,
                             embedder=None) -> str:
    """
    TEMPLATE: Primacy placement - most relevant documents at start.
    
    Students implement this in the notebook. This is a reference implementation.
    
    Args:
        documents: List of document dicts
        query: Question being asked
        token_limit: Maximum tokens
        embedder: SentenceTransformer model for ranking
        
    Returns:
        Assembled context string
    """
    if embedder is None:
        raise ValueError("Embedder required for primacy strategy")
    
    # Rank documents by relevance
    query_embedding = embedder.encode(query, convert_to_tensor=True)
    ranked_docs = []
    
    for doc in documents:
        doc_embedding = embedder.encode(doc['content'], convert_to_tensor=True)
        from .helpers import calculate_similarity
        similarity = calculate_similarity(query_embedding, doc_embedding)
        ranked_docs.append((doc, similarity.item()))
    
    # Sort by similarity (highest first)
    ranked_docs.sort(key=lambda x: x[1], reverse=True)
    
    # Assemble context with most relevant first
    budget_manager = TokenBudgetManager(max_tokens=token_limit, overhead=50)
    context_parts = []
    
    for doc, score in ranked_docs:
        doc_text = f"Document: {doc.get('title', 'Untitled')}\n\n{doc['content']}"
        
        if budget_manager.can_add(doc_text):
            budget_manager.add(doc_text)
            context_parts.append(doc_text)
        else:
            break
    
    return "\n\n---\n\n".join(context_parts)


def recency_context_assembly(documents: List[Dict],
                             query: str,
                             token_limit: int = 4000,
                             embedder=None) -> str:
    """
    TEMPLATE: Recency placement - most relevant documents at end.
    
    Students implement this in the notebook. This is a reference implementation.
    
    Args:
        documents: List of document dicts
        query: Question being asked
        token_limit: Maximum tokens
        embedder: SentenceTransformer model for ranking
        
    Returns:
        Assembled context string
    """
    if embedder is None:
        raise ValueError("Embedder required for recency strategy")
    
    # Rank documents by relevance
    query_embedding = embedder.encode(query, convert_to_tensor=True)
    ranked_docs = []
    
    for doc in documents:
        doc_embedding = embedder.encode(doc['content'], convert_to_tensor=True)
        from .helpers import calculate_similarity
        similarity = calculate_similarity(query_embedding, doc_embedding)
        ranked_docs.append((doc, similarity.item()))
    
    # Sort by similarity (lowest first, so highest end up at end)
    ranked_docs.sort(key=lambda x: x[1], reverse=False)
    
    # Assemble context
    budget_manager = TokenBudgetManager(max_tokens=token_limit, overhead=50)
    context_parts = []
    
    for doc, score in ranked_docs:
        doc_text = f"Document: {doc.get('title', 'Untitled')}\n\n{doc['content']}"
        
        if budget_manager.can_add(doc_text):
            budget_manager.add(doc_text)
            context_parts.append(doc_text)
        else:
            break
    
    return "\n\n---\n\n".join(context_parts)


def sandwich_context_assembly(documents: List[Dict],
                              query: str,
                              token_limit: int = 4000,
                              embedder=None) -> str:
    """
    TEMPLATE: Sandwich placement - relevant docs at both ends.
    
    Students implement this in the notebook. This is a reference implementation.
    
    Args:
        documents: List of document dicts
        query: Question being asked
        token_limit: Maximum tokens
        embedder: SentenceTransformer model for ranking
        
    Returns:
        Assembled context string
    """
    if embedder is None:
        raise ValueError("Embedder required for sandwich strategy")
    
    # Rank documents by relevance
    query_embedding = embedder.encode(query, convert_to_tensor=True)
    ranked_docs = []
    
    for doc in documents:
        doc_embedding = embedder.encode(doc['content'], convert_to_tensor=True)
        from .helpers import calculate_similarity
        similarity = calculate_similarity(query_embedding, doc_embedding)
        ranked_docs.append((doc, similarity.item()))
    
    # Sort by similarity (highest first)
    ranked_docs.sort(key=lambda x: x[1], reverse=True)
    
    # Determine how many docs to include
    budget_manager = TokenBudgetManager(max_tokens=token_limit, overhead=50)
    
    # Collect docs that fit
    docs_to_include = []
    for doc, score in ranked_docs:
        doc_text = f"Document: {doc.get('title', 'Untitled')}\n\n{doc['content']}"
        if budget_manager.can_add(doc_text):
            budget_manager.add(doc_text)
            docs_to_include.append((doc, score))
        else:
            break
    
    if len(docs_to_include) < 3:
        # Too few docs, just use primacy
        context_parts = [f"Document: {doc.get('title', 'Untitled')}\n\n{doc['content']}" 
                        for doc, _ in docs_to_include]
        return "\n\n---\n\n".join(context_parts)
    
    # Split into three groups: high relevance at start, middle, high relevance at end
    num_high_relevance = max(2, len(docs_to_include) // 3)
    
    start_docs = docs_to_include[:num_high_relevance//2]
    end_docs = docs_to_include[num_high_relevance//2:num_high_relevance]
    middle_docs = docs_to_include[num_high_relevance:]
    
    # Assemble: start + middle + end
    all_ordered = start_docs + middle_docs + end_docs
    
    context_parts = [f"Document: {doc.get('title', 'Untitled')}\n\n{doc['content']}" 
                    for doc, _ in all_ordered]
    
    return "\n\n---\n\n".join(context_parts)


# Placeholder for optimization strategies (students implement one)
def hierarchical_summary_assembly(documents: List[Dict],
                                 query: str,
                                 token_limit: int = 4000,
                                 embedder=None) -> str:
    """
    TEMPLATE: Hierarchical summarization optimization.
    
    Students implement their chosen optimization in the notebook.
    This is a reference implementation for verification.
    """
    # Reference implementation - summarize less relevant docs
    # Students will implement this themselves
    raise NotImplementedError("Students implement this in the notebook")


def semantic_chunking_assembly(documents: List[Dict],
                               query: str,
                               token_limit: int = 4000,
                               embedder=None) -> str:
    """
    TEMPLATE: Semantic chunking optimization.
    
    Students implement their chosen optimization in the notebook.
    """
    raise NotImplementedError("Students implement this in the notebook")


def dynamic_allocation_assembly(documents: List[Dict],
                                query: str,
                                token_limit: int = 4000,
                                embedder=None) -> str:
    """
    TEMPLATE: Dynamic token allocation optimization.
    
    Students implement their chosen optimization in the notebook.
    """
    raise NotImplementedError("Students implement this in the notebook")


if __name__ == "__main__":
    print("Context strategy templates loaded.")
    print("These are reference implementations for the verification system.")
    print("Students complete their own versions in the notebook.")
```

---

## File Organization Notes

These first 4 files provide the foundation. The next chunk (Chunk 5) will cover:
- `evaluation.py` - LLM-based scoring system
- `verify.py` - Complete auto-grading implementation

---

## Next Steps

1. Save this as `docs/04_source_code_specs.md`
2. Review the implementations
3. Ready for Chunk 5: evaluation.py and verify.py specifications

**Ready for Chunk 5 when you are!**