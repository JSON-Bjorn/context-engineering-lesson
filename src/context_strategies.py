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
