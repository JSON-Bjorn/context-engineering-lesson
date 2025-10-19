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
