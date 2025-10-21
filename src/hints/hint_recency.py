# Hint for recency_context_assembly implementation

def recency_context_assembly(documents, query, token_limit=4000, embedder=None):
    """
    Recency placement: Most relevant documents at the END.
    """
    if embedder is None:
        return naive_context_assembly(documents, query, token_limit)

    # Rank documents by relevance
    ranked_docs = rank_documents_by_relevance(documents, query, embedder)

    # Build context in reverse order, then reverse at the end
    # This puts most relevant documents at the end
    context_parts = []
    used_tokens = 0
    available_tokens = token_limit - 50

    # Add documents starting from most relevant
    for doc, score in ranked_docs:
        if used_tokens + doc['tokens'] > available_tokens:
            break

        doc_text = f"Document: {doc['title']}\n{doc['content']}"
        context_parts.append(doc_text)
        used_tokens += doc['tokens']

    # Reverse so most relevant is at the end
    context_parts.reverse()

    return "\n\n".join(context_parts)
