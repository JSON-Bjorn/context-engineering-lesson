# Hint for naive_context_assembly implementation

def naive_context_assembly(documents, query, token_limit=4000):
    """
    Naive context assembly: concatenate documents in order until token limit.
    """
    context_parts = []
    used_tokens = 0
    available_tokens = token_limit - 50  # Reserve for query

    for doc in documents:
        # Check if adding this document would exceed the limit
        if used_tokens + doc['tokens'] > available_tokens:
            break  # Stop if we'd exceed the limit

        # Add document content with formatting
        doc_text = f"Document: {doc['title']}\n{doc['content']}"
        context_parts.append(doc_text)
        used_tokens += doc['tokens']

    return "\n\n".join(context_parts)
