"""
Evaluation - LLM-based answer evaluation and scoring

This module provides functionality to:
- Generate answers using the local LLM
- Score answers against ground truth using LLM-as-judge
- Calculate semantic similarity for evaluation
- Track evaluation metrics
"""

import torch
from typing import Dict, List, Tuple, Optional
from transformers import AutoModelForCausalLM, AutoTokenizer
from sentence_transformers import SentenceTransformer
import numpy as np


class LLMEvaluator:
    """
    LLM-based evaluator for answer generation and scoring.

    Uses a local LLM to generate answers and evaluate them against ground truth.
    Implements the "LLM-as-a-judge" pattern for automatic grading.

    Examples:
        >>> evaluator = LLMEvaluator(model, tokenizer)
        >>> answer = evaluator.generate_answer(context, question)
        >>> score = evaluator.score_answer(answer, ground_truth)
    """

    def __init__(self,
                 model: AutoModelForCausalLM,
                 tokenizer: AutoTokenizer,
                 embedder: Optional[SentenceTransformer] = None,
                 device: Optional[str] = None):
        """
        Initialize the evaluator.

        Args:
            model: Loaded LLM for generation
            tokenizer: Tokenizer for the model
            embedder: Optional embedding model for semantic similarity
            device: Device to use (cuda/cpu/mps), auto-detected if None
        """
        self.model = model
        self.tokenizer = tokenizer
        self.embedder = embedder

        if device is None:
            if torch.cuda.is_available():
                self.device = "cuda"
            elif torch.backends.mps.is_available():
                self.device = "mps"
            else:
                self.device = "cpu"
        else:
            self.device = device

        print(f"✅ LLMEvaluator initialized on device: {self.device}")

    def generate_answer(self,
                       context: str,
                       question: str,
                       max_new_tokens: int = 256,
                       temperature: float = 0.7,
                       top_p: float = 0.9) -> str:
        """
        Generate an answer to a question given context.

        Args:
            context: Background information/documents
            question: Question to answer
            max_new_tokens: Maximum tokens in response
            temperature: Sampling temperature (0.0 = deterministic)
            top_p: Nucleus sampling parameter

        Returns:
            Generated answer as string
        """
        # Format prompt
        prompt = self._format_qa_prompt(context, question)

        # Tokenize
        inputs = self.tokenizer(prompt, return_tensors="pt", truncation=True, max_length=4096)
        inputs = {k: v.to(self.device) for k, v in inputs.items()}

        # Generate
        with torch.no_grad():
            outputs = self.model.generate(
                **inputs,
                max_new_tokens=max_new_tokens,
                temperature=temperature,
                top_p=top_p,
                do_sample=temperature > 0,
                pad_token_id=self.tokenizer.eos_token_id
            )

        # Decode only the new tokens
        answer = self.tokenizer.decode(
            outputs[0][inputs['input_ids'].shape[1]:],
            skip_special_tokens=True
        ).strip()

        return answer

    def score_answer(self,
                    generated_answer: str,
                    ground_truth: str,
                    method: str = "hybrid") -> float:
        """
        Score a generated answer against ground truth.

        Args:
            generated_answer: Answer produced by the model
            ground_truth: Correct/reference answer
            method: Scoring method ("semantic", "llm_judge", "hybrid")

        Returns:
            Score from 0.0 to 1.0
        """
        if method == "semantic":
            return self._semantic_similarity_score(generated_answer, ground_truth)
        elif method == "llm_judge":
            return self._llm_judge_score(generated_answer, ground_truth)
        elif method == "hybrid":
            # Combine both methods (average)
            semantic_score = self._semantic_similarity_score(generated_answer, ground_truth)
            llm_score = self._llm_judge_score(generated_answer, ground_truth)
            return (semantic_score + llm_score) / 2
        else:
            raise ValueError(f"Unknown scoring method: {method}")

    def _semantic_similarity_score(self, answer: str, ground_truth: str) -> float:
        """
        Score based on semantic similarity of embeddings.

        Args:
            answer: Generated answer
            ground_truth: Reference answer

        Returns:
            Similarity score 0.0-1.0
        """
        if self.embedder is None:
            raise ValueError("Embedder required for semantic similarity scoring")

        # Encode both answers (ensure CPU for SentenceTransformer compatibility)
        answer_emb = self.embedder.encode(answer, convert_to_tensor=True).cpu()
        truth_emb = self.embedder.encode(ground_truth, convert_to_tensor=True).cpu()

        # Calculate cosine similarity
        similarity = torch.nn.functional.cosine_similarity(
            answer_emb.unsqueeze(0),
            truth_emb.unsqueeze(0)
        ).item()

        # Normalize to 0-1 range (cosine similarity is -1 to 1)
        score = (similarity + 1) / 2

        return max(0.0, min(1.0, score))

    def _llm_judge_score(self, answer: str, ground_truth: str) -> float:
        """
        Score using LLM-as-a-judge approach.

        The LLM evaluates how well the answer matches the ground truth.

        Args:
            answer: Generated answer
            ground_truth: Reference answer

        Returns:
            Score 0.0-1.0
        """
        # Format judging prompt
        judge_prompt = f"""You are an expert evaluator. Compare the following two answers and rate how similar they are in meaning.

Reference Answer: {ground_truth}

Generated Answer: {answer}

Rate the similarity on a scale from 0 to 10, where:
- 0 = Completely different or wrong
- 5 = Partially correct, captures some key points
- 10 = Essentially the same meaning, fully correct

Provide ONLY a single number from 0-10 as your response.

Rating:"""

        # Generate score
        inputs = self.tokenizer(judge_prompt, return_tensors="pt", truncation=True, max_length=2048)
        inputs = {k: v.to(self.device) for k, v in inputs.items()}

        with torch.no_grad():
            outputs = self.model.generate(
                **inputs,
                max_new_tokens=5,
                temperature=0.1,  # Low temperature for consistent scoring
                do_sample=False,
                pad_token_id=self.tokenizer.eos_token_id
            )

        # Decode response
        response = self.tokenizer.decode(
            outputs[0][inputs['input_ids'].shape[1]:],
            skip_special_tokens=True
        ).strip()

        # Extract numeric score
        try:
            # Try to parse first number found
            import re
            numbers = re.findall(r'\d+\.?\d*', response)
            if numbers:
                raw_score = float(numbers[0])
                # Normalize to 0-1
                score = min(10.0, max(0.0, raw_score)) / 10.0
            else:
                # Default to 0.5 if parsing fails
                score = 0.5
        except Exception:
            score = 0.5

        return score

    def _format_qa_prompt(self, context: str, question: str) -> str:
        """
        Format a question-answering prompt.

        Args:
            context: Background information
            question: Question to answer

        Returns:
            Formatted prompt string
        """
        prompt = f"""Based on the following context, answer the question concisely and accurately.

Context:
{context}

Question: {question}

Answer:"""
        return prompt

    def evaluate_batch(self,
                      contexts: List[str],
                      questions: List[str],
                      ground_truths: List[str],
                      show_progress: bool = True) -> List[Dict]:
        """
        Evaluate a batch of questions.

        Args:
            contexts: List of context strings
            questions: List of questions
            ground_truths: List of reference answers
            show_progress: Whether to show progress bar

        Returns:
            List of result dicts with 'answer', 'score', 'question' keys
        """
        from tqdm.auto import tqdm

        results = []
        iterator = zip(contexts, questions, ground_truths)

        if show_progress:
            iterator = tqdm(list(iterator), desc="Evaluating")

        for context, question, ground_truth in iterator:
            answer = self.generate_answer(context, question)
            score = self.score_answer(answer, ground_truth)

            results.append({
                'question': question,
                'answer': answer,
                'ground_truth': ground_truth,
                'score': score
            })

        return results


def evaluate_answer(answer: str,
                   ground_truth: str,
                   embedder: SentenceTransformer) -> float:
    """
    Standalone function to evaluate an answer against ground truth.

    Convenience function for quick evaluation without full evaluator setup.

    Args:
        answer: Generated answer
        ground_truth: Reference answer
        embedder: SentenceTransformer model

    Returns:
        Similarity score 0.0-1.0
    """
    answer_emb = embedder.encode(answer, convert_to_tensor=True).cpu()
    truth_emb = embedder.encode(ground_truth, convert_to_tensor=True).cpu()

    similarity = torch.nn.functional.cosine_similarity(
        answer_emb.unsqueeze(0),
        truth_emb.unsqueeze(0)
    ).item()

    # Normalize to 0-1
    score = (similarity + 1) / 2
    return max(0.0, min(1.0, score))


def calculate_metrics(results: List[Dict]) -> Dict[str, float]:
    """
    Calculate aggregate metrics from evaluation results.

    Args:
        results: List of result dicts from evaluate_batch

    Returns:
        Dictionary of metrics
    """
    scores = [r['score'] for r in results]

    metrics = {
        'mean_score': np.mean(scores),
        'median_score': np.median(scores),
        'std_score': np.std(scores),
        'min_score': np.min(scores),
        'max_score': np.max(scores),
        'num_evaluated': len(scores)
    }

    return metrics


def compare_strategies(strategy_results: Dict[str, List[Dict]]) -> Dict:
    """
    Compare results from multiple strategies.

    Args:
        strategy_results: Dict mapping strategy names to their results

    Returns:
        Comparison dictionary with metrics for each strategy
    """
    comparison = {}

    for strategy_name, results in strategy_results.items():
        metrics = calculate_metrics(results)
        comparison[strategy_name] = metrics

    return comparison


# Example usage and testing
if __name__ == "__main__":
    print("Evaluation module loaded.")
    print("This module provides LLM-based answer evaluation.")
    print("\nExample usage:")
    print("""
    evaluator = LLMEvaluator(model, tokenizer, embedder)
    answer = evaluator.generate_answer(context, question)
    score = evaluator.score_answer(answer, ground_truth)
    """)
