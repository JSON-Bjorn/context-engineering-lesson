# Hint for sandwich_context_assembly implementation

def sandwich_context_assembly(documents, query, token_limit=4000, embedder=None):
    """
    Sandwich placement: Relevant docs at BOTH ends, less relevant in middle.
    """
    if embedder is None:
        return naive_context_assembly(documents, query, token_limit)

    # Rank documents by relevance
    ranked_docs = rank_documents_by_relevance(documents, query, embedder)

    # First, determine how many docs we can fit
    available_tokens = token_limit - 50
    fitting_docs = []
    used_tokens = 0

    for doc, score in ranked_docs:
        if used_tokens + doc['tokens'] <= available_tokens:
            fitting_docs.append((doc, score))
            used_tokens += doc['tokens']
        else:
            break

    if len(fitting_docs) <= 2:
        # Not enough docs to sandwich, just use primacy
        context_parts = [f"Document: {doc['title']}\n{doc['content']}"
                        for doc, score in fitting_docs]
        return "\n\n".join(context_parts)

    # Split top 40% of docs between start and end
    sandwich_size = max(1, int(len(fitting_docs) * 0.4))

    # Top docs for sandwich
    top_docs = fitting_docs[:sandwich_size * 2]
    # Remaining middle docs
    middle_docs = fitting_docs[sandwich_size * 2:]

    # Assemble: first half of top docs + middle + second half of top docs
    start_docs = top_docs[:sandwich_size]
    end_docs = top_docs[sandwich_size:sandwich_size * 2]

    context_parts = []

    # Add start docs
    for doc, score in start_docs:
        context_parts.append(f"Document: {doc['title']}\n{doc['content']}")

    # Add middle docs
    for doc, score in middle_docs:
        context_parts.append(f"Document: {doc['title']}\n{doc['content']}")

    # Add end docs
    for doc, score in end_docs:
        context_parts.append(f"Document: {doc['title']}\n{doc['content']}")

    return "\n\n".join(context_parts)
