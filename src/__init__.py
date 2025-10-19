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

# Import from modules that exist
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

# Conditional imports for modules not yet created
try:
    from .evaluation import (
        evaluate_answer,
        LLMEvaluator,
    )
except ImportError:
    # evaluation.py not created yet
    pass

# Update __all__ to only include what's currently available
__all__ = [
    'count_tokens',
    'fits_in_budget',
    'TokenBudgetManager',
    'load_documents',
    'load_questions',
    'calculate_similarity',
    'format_context',
]
