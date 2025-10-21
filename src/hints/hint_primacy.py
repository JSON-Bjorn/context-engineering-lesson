# Hint for primacy_context_assembly implementation

def primacy_context_assembly(documents, query, token_limit=4000, embedder=None):
    """
    Primacy placement: Most relevant documents at the START.
    """
    if embedder is None:
        # Fallback to naive if no embedder
        return naive_context_assembly(documents, query, token_limit)

    # Rank documents by relevance to query
    ranked_docs = rank_documents_by_relevance(documents, query, embedder)

    # Assemble context with highest-ranked docs first
    context_parts = []
    used_tokens = 0
    available_tokens = token_limit - 50  # Reserve for query

    for doc, score in ranked_docs:
        if used_tokens + doc['tokens'] > available_tokens:
            break

        doc_text = f"Document: {doc['title']}\n{doc['content']}"
        context_parts.append(doc_text)
        used_tokens += doc['tokens']

    return "\n\n".join(context_parts)
