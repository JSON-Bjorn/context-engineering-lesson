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
