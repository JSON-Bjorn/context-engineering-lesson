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
