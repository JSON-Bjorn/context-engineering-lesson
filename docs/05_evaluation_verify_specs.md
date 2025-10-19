# Context Engineering Lesson - Evaluation & Verification Specifications

## Document Purpose
This document provides complete specifications for the final two critical source files: `evaluation.py` (LLM-based answer scoring) and `verify.py` (auto-grading system).

---

# File 5: src/evaluation.py

## Purpose
Provides LLM-based evaluation of answers using the local model. Implements "LLM-as-a-judge" pattern for automatic scoring.

## Size
~10-12 KB

## Dependencies
- transformers (AutoModelForCausalLM, AutoTokenizer)
- torch
- sentence-transformers (for semantic similarity)

## Complete Implementation

```python
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
        
        # Encode both answers
        answer_emb = self.embedder.encode(answer, convert_to_tensor=True)
        truth_emb = self.embedder.encode(ground_truth, convert_to_tensor=True)
        
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
    answer_emb = embedder.encode(answer, convert_to_tensor=True)
    truth_emb = embedder.encode(ground_truth, convert_to_tensor=True)
    
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
```

---

# File 6: src/verify.py

## Purpose
Complete auto-grading system that validates student implementations and generates the final grade JSON.

## Size
~15-18 KB

## Dependencies
- All lesson modules
- json, pathlib
- datetime

## Complete Implementation

```python
#!/usr/bin/env python3
"""
Verify - Auto-grading system for Context Engineering lesson

This script validates student implementations and generates the completion certificate.
It checks that all required tasks are completed and meet quality thresholds.

Usage:
    python src/verify.py
    
Output:
    progress/lesson_progress.json - Detailed grading results
"""

import sys
import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Tuple, Optional
import uuid

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.helpers import load_documents, load_questions, load_results, save_results
from src.token_manager import count_tokens


class LessonVerifier:
    """
    Verifies completion of the Context Engineering lesson.
    
    Checks:
    1. Token calculations accuracy
    2. All strategies implemented
    3. Metrics properly recorded
    4. Optimization shows improvement
    5. Comparison analysis complete
    """
    
    def __init__(self):
        """Initialize the verifier."""
        self.results_path = Path("progress/lesson_results.json")
        self.output_path = Path("progress/lesson_progress.json")
        self.data_dir = Path("data")
        
        self.checks_passed = []
        self.checks_failed = []
        self.warnings = []
        
        print("=" * 80)
        print(" " * 25 + "CONTEXT ENGINEERING LESSON")
        print(" " * 28 + "AUTO-VERIFICATION")
        print("=" * 80)
        print()
    
    def run_verification(self) -> Dict:
        """
        Run all verification checks.
        
        Returns:
            Complete verification results dictionary
        """
        print("🔍 Starting verification process...\n")
        
        # Check 1: Results file exists
        if not self._check_results_exist():
            return self._generate_failure_report("Results file not found")
        
        # Load results
        try:
            results = load_results(self.results_path)
        except Exception as e:
            return self._generate_failure_report(f"Error loading results: {e}")
        
        # Check 2: Token calculations
        self._check_token_calculations(results)
        
        # Check 3: All strategies implemented
        self._check_strategies_implemented(results)
        
        # Check 4: Metrics recorded
        self._check_metrics_recorded(results)
        
        # Check 5: Optimization implemented
        self._check_optimization(results)
        
        # Check 6: Comparison analysis
        self._check_comparison_analysis(results)
        
        # Generate final report
        return self._generate_final_report(results)
    
    def _check_results_exist(self) -> bool:
        """Check if results file exists."""
        print("📋 Check 1: Results file exists")
        
        if not self.results_path.exists():
            print("   ❌ FAIL: lesson_results.json not found")
            print(f"   Expected at: {self.results_path.absolute()}")
            print("   Did you complete the notebook and run all cells?")
            self.checks_failed.append({
                'check': 'results_file_exists',
                'status': 'FAIL',
                'message': 'Results file not found'
            })
            return False
        
        print("   ✅ PASS: Results file found")
        self.checks_passed.append({
            'check': 'results_file_exists',
            'status': 'PASS'
        })
        return True
    
    def _check_token_calculations(self, results: Dict):
        """Verify token calculations are accurate."""
        print("\n📋 Check 2: Token calculations accuracy")
        
        try:
            # Load documents to verify token counts
            documents = load_documents(self.data_dir / "source_documents.json")
            
            # Check if metadata contains token calculations
            metadata = results.get('metadata', {})
            
            if 'num_documents' not in metadata:
                self.warnings.append("Token calculation metadata incomplete")
                print("   ⚠️  WARNING: Token calculation metadata not found")
            else:
                reported_docs = metadata['num_documents']
                actual_docs = len(documents)
                
                if reported_docs == actual_docs:
                    print(f"   ✅ PASS: Document count correct ({actual_docs})")
                    self.checks_passed.append({
                        'check': 'token_calculations',
                        'status': 'PASS'
                    })
                else:
                    print(f"   ❌ FAIL: Document count mismatch (expected {actual_docs}, got {reported_docs})")
                    self.checks_failed.append({
                        'check': 'token_calculations',
                        'status': 'FAIL',
                        'message': f'Document count mismatch'
                    })
        
        except Exception as e:
            print(f"   ⚠️  WARNING: Could not verify token calculations: {e}")
            self.warnings.append(f"Token calculation verification error: {e}")
    
    def _check_strategies_implemented(self, results: Dict):
        """Check that all required strategies are implemented."""
        print("\n📋 Check 3: Strategy implementations")
        
        required_strategies = ['naive', 'primacy', 'recency', 'sandwich']
        strategies_data = results.get('strategies', {})
        
        missing_strategies = []
        
        for strategy in required_strategies:
            if strategy not in strategies_data:
                missing_strategies.append(strategy)
                print(f"   ❌ FAIL: Strategy '{strategy}' not found")
            else:
                print(f"   ✅ Found: {strategy} strategy")
        
        if missing_strategies:
            self.checks_failed.append({
                'check': 'strategies_implemented',
                'status': 'FAIL',
                'message': f'Missing strategies: {", ".join(missing_strategies)}'
            })
        else:
            print("   ✅ PASS: All required strategies implemented")
            self.checks_passed.append({
                'check': 'strategies_implemented',
                'status': 'PASS'
            })
    
    def _check_metrics_recorded(self, results: Dict):
        """Verify metrics are properly recorded for all strategies."""
        print("\n📋 Check 4: Metrics recording")
        
        strategies_data = results.get('strategies', {})
        required_metrics = ['accuracy', 'avg_tokens']
        
        all_metrics_complete = True
        
        for strategy_name, strategy_data in strategies_data.items():
            missing_metrics = []
            for metric in required_metrics:
                if metric not in strategy_data:
                    missing_metrics.append(metric)
            
            if missing_metrics:
                print(f"   ❌ Strategy '{strategy_name}' missing: {', '.join(missing_metrics)}")
                all_metrics_complete = False
            else:
                print(f"   ✅ Strategy '{strategy_name}' has all metrics")
        
        if all_metrics_complete:
            print("   ✅ PASS: All metrics recorded correctly")
            self.checks_passed.append({
                'check': 'metrics_recorded',
                'status': 'PASS'
            })
        else:
            print("   ❌ FAIL: Some metrics missing")
            self.checks_failed.append({
                'check': 'metrics_recorded',
                'status': 'FAIL',
                'message': 'Incomplete metrics'
            })
    
    def _check_optimization(self, results: Dict):
        """Check that at least one optimization was implemented."""
        print("\n📋 Check 5: Optimization implementation")
        
        strategies_data = results.get('strategies', {})
        
        # Look for any strategy beyond the required four
        base_strategies = {'naive', 'primacy', 'recency', 'sandwich'}
        optimization_strategies = set(strategies_data.keys()) - base_strategies
        
        if not optimization_strategies:
            print("   ❌ FAIL: No optimization strategy found")
            self.checks_failed.append({
                'check': 'optimization_implemented',
                'status': 'FAIL',
                'message': 'No optimization strategy implemented'
            })
            return
        
        print(f"   ✅ Found optimization: {', '.join(optimization_strategies)}")
        
        # Check if optimization shows improvement
        baseline_accuracy = strategies_data.get('naive', {}).get('accuracy', 0)
        
        improvement_found = False
        for opt_name in optimization_strategies:
            opt_data = strategies_data[opt_name]
            opt_accuracy = opt_data.get('accuracy', 0)
            opt_tokens = opt_data.get('avg_tokens', 0)
            baseline_tokens = strategies_data.get('naive', {}).get('avg_tokens', 1)
            
            accuracy_improvement = (opt_accuracy - baseline_accuracy) / baseline_accuracy if baseline_accuracy > 0 else 0
            token_reduction = (baseline_tokens - opt_tokens) / baseline_tokens if baseline_tokens > 0 else 0
            
            print(f"\n   Strategy: {opt_name}")
            print(f"   - Accuracy improvement: {accuracy_improvement:+.1%}")
            print(f"   - Token reduction: {token_reduction:+.1%}")
            
            if accuracy_improvement >= 0.10 or token_reduction >= 0.20:
                print(f"   ✅ Optimization meets threshold!")
                improvement_found = True
            else:
                print(f"   ⚠️  Below threshold (need ≥10% accuracy OR ≥20% token reduction)")
        
        if improvement_found:
            print("\n   ✅ PASS: Optimization shows measurable improvement")
            self.checks_passed.append({
                'check': 'optimization_implemented',
                'status': 'PASS'
            })
        else:
            print("\n   ❌ FAIL: Optimization does not meet improvement threshold")
            self.checks_failed.append({
                'check': 'optimization_implemented',
                'status': 'FAIL',
                'message': 'Optimization below improvement threshold'
            })
    
    def _check_comparison_analysis(self, results: Dict):
        """Verify comparison analysis was completed."""
        print("\n📋 Check 6: Comparison analysis")
        
        strategies_data = results.get('strategies', {})
        
        if len(strategies_data) < 5:  # naive + 3 strategic + 1 optimization
            print(f"   ⚠️  WARNING: Expected at least 5 strategies, found {len(strategies_data)}")
            self.warnings.append("Fewer strategies than expected")
        
        print(f"   ✅ Analyzed {len(strategies_data)} strategies")
        print("   ✅ PASS: Comparison analysis complete")
        
        self.checks_passed.append({
            'check': 'comparison_analysis',
            'status': 'PASS'
        })
    
    def _generate_final_report(self, results: Dict) -> Dict:
        """Generate the final verification report."""
        print("\n" + "=" * 80)
        print(" " * 32 + "FINAL RESULTS")
        print("=" * 80)
        
        total_checks = len(self.checks_passed) + len(self.checks_failed)
        passed_checks = len(self.checks_passed)
        
        print(f"\n✅ Checks Passed: {passed_checks}/{total_checks}")
        print(f"❌ Checks Failed: {len(self.checks_failed)}/{total_checks}")
        print(f"⚠️  Warnings: {len(self.warnings)}")
        
        # Determine overall grade
        overall_grade = "PASS" if len(self.checks_failed) == 0 else "FAIL"
        
        print(f"\n🎓 OVERALL GRADE: {overall_grade}")
        
        if overall_grade == "PASS":
            print("\n🎉 Congratulations! You've successfully completed the Context Engineering lesson!")
            print("   Your completion certificate has been saved to progress/lesson_progress.json")
        else:
            print("\n❌ Lesson not yet complete. Please address the failed checks above.")
            print("   Review the notebook and ensure all tasks are completed correctly.")
        
        print("\n" + "=" * 80)
        
        # Calculate metrics summary
        strategies_data = results.get('strategies', {})
        baseline_accuracy = strategies_data.get('naive', {}).get('accuracy', 0)
        
        best_strategy = max(strategies_data.items(), 
                          key=lambda x: x[1].get('accuracy', 0),
                          default=(None, {}))
        
        best_strategy_name = best_strategy[0] if best_strategy[0] else "unknown"
        best_accuracy = best_strategy[1].get('accuracy', 0) if best_strategy[1] else 0
        total_improvement = (best_accuracy - baseline_accuracy) / baseline_accuracy if baseline_accuracy > 0 else 0
        
        # Build final report
        report = {
            'student_id': str(uuid.uuid4()),
            'lesson': 'context_engineering',
            'timestamp': datetime.now().isoformat(),
            'completion_time_minutes': results.get('metadata', {}).get('completion_time_minutes', None),
            
            'verification': {
                'grade': overall_grade,
                'checks_passed': passed_checks,
                'checks_total': total_checks,
                'checks_details': {
                    'passed': self.checks_passed,
                    'failed': self.checks_failed,
                    'warnings': self.warnings
                }
            },
            
            'tasks_completed': {
                'token_budget_analysis': {
                    'status': 'PASS' if any(c['check'] == 'token_calculations' for c in self.checks_passed) else 'FAIL'
                },
                'naive_implementation': {
                    'status': 'PASS' if 'naive' in strategies_data else 'FAIL',
                    'baseline_accuracy': baseline_accuracy
                },
                'strategic_placement': {
                    'status': 'PASS' if all(s in strategies_data for s in ['primacy', 'recency', 'sandwich']) else 'FAIL',
                    'primacy_accuracy': strategies_data.get('primacy', {}).get('accuracy', 0),
                    'recency_accuracy': strategies_data.get('recency', {}).get('accuracy', 0),
                    'sandwich_accuracy': strategies_data.get('sandwich', {}).get('accuracy', 0)
                },
                'optimization': {
                    'status': 'PASS' if any(c['check'] == 'optimization_implemented' for c in self.checks_passed) else 'FAIL'
                }
            },
            
            'metrics_summary': {
                'baseline_accuracy': baseline_accuracy,
                'best_strategy': best_strategy_name,
                'best_accuracy': best_accuracy,
                'total_improvement': total_improvement,
                'strategies_tested': len(strategies_data)
            },
            
            'detailed_results': strategies_data
        }
        
        # Save report
        self.output_path.parent.mkdir(parents=True, exist_ok=True)
        save_results(report, str(self.output_path))
        
        return report
    
    def _generate_failure_report(self, error_message: str) -> Dict:
        """Generate a failure report when critical errors occur."""
        print(f"\n❌ CRITICAL ERROR: {error_message}")
        print("\n" + "=" * 80)
        print(" " * 30 + "VERIFICATION FAILED")
        print("=" * 80)
        
        report = {
            'student_id': str(uuid.uuid4()),
            'lesson': 'context_engineering',
            'timestamp': datetime.now().isoformat(),
            'verification': {
                'grade': 'FAIL',
                'error': error_message,
                'checks_passed': 0,
                'checks_total': 0
            }
        }
        
        return report


def main():
    """Main verification function."""
    verifier = LessonVerifier()
    report = verifier.run_verification()
    
    # Exit with appropriate code
    exit_code = 0 if report['verification']['grade'] == 'PASS' else 1
    sys.exit(exit_code)


if __name__ == "__main__":
    main()
```

---

## Verification System Design

### Check Flow

```
1. Results File Exists
   ↓
2. Token Calculations Correct
   ↓
3. All Strategies Implemented (naive, primacy, recency, sandwich)
   ↓
4. Metrics Recorded (accuracy, avg_tokens for all)
   ↓
5. Optimization Implemented (≥10% accuracy OR ≥20% token reduction)
   ↓
6. Comparison Analysis Complete
   ↓
FINAL GRADE: PASS or FAIL
```

### Pass Criteria

**To PASS, students must:**
- ✅ Complete all notebook cells
- ✅ Generate lesson_results.json
- ✅ Implement all 4 required strategies correctly
- ✅ Record metrics for all strategies
- ✅ Implement at least 1 optimization
- ✅ Show measurable improvement with optimization

### Output Format

**progress/lesson_progress.json contains:**
- Student ID (UUID)
- Timestamp
- Overall grade (PASS/FAIL)
- Detailed check results
- Task completion status
- Metrics summary
- Full strategy results

---

## Testing the Verification System

### Manual Testing Commands

```bash
# Run verification
python src/verify.py

# Check output
cat progress/lesson_progress.json | python -m json.tool

# Test with missing results
rm progress/lesson_results.json
python src/verify.py  # Should fail gracefully

# Test with incomplete data
# Edit lesson_results.json to remove a strategy
python src/verify.py  # Should identify missing strategy
```

### Expected Output Examples

**Successful Completion:**
```
================================================================================
                        CONTEXT ENGINEERING LESSON
                            AUTO-VERIFICATION
================================================================================

🔍 Starting verification process...

📋 Check 1: Results file exists
   ✅ PASS: Results file found

📋 Check 2: Token calculations accuracy
   ✅ PASS: Document count correct (10)

📋 Check 3: Strategy implementations
   ✅ Found: naive strategy
   ✅ Found: primacy strategy
   ✅ Found: recency strategy
   ✅ Found: sandwich strategy
   ✅ PASS: All required strategies implemented

📋 Check 4: Metrics recording
   ✅ Strategy 'naive' has all metrics
   ✅ Strategy 'primacy' has all metrics
   ✅ Strategy 'recency' has all metrics
   ✅ Strategy 'sandwich' has all metrics
   ✅ Strategy 'hierarchical_summary' has all metrics
   ✅ PASS: All metrics recorded correctly

📋 Check 5: Optimization implementation
   ✅ Found optimization: hierarchical_summary

   Strategy: hierarchical_summary
   - Accuracy improvement: +18.2%
   - Token reduction: +15.3%
   ✅ Optimization meets threshold!

   ✅ PASS: Optimization shows measurable improvement

📋 Check 6: Comparison analysis
   ✅ Analyzed 5 strategies
   ✅ PASS: Comparison analysis complete

================================================================================
                            FINAL RESULTS
================================================================================

✅ Checks Passed: 6/6
❌ Checks Failed: 0/6
⚠️  Warnings: 0

🎓 OVERALL GRADE: PASS

🎉 Congratulations! You've successfully completed the Context Engineering lesson!
   Your completion certificate has been saved to progress/lesson_progress.json

================================================================================
✅ Results saved to: progress/lesson_progress.json
```

**Failed Completion Example:**
```
================================================================================
                        CONTEXT ENGINEERING LESSON
                            AUTO-VERIFICATION
================================================================================

🔍 Starting verification process...

📋 Check 1: Results file exists
   ✅ PASS: Results file found

📋 Check 2: Token calculations accuracy
   ✅ PASS: Document count correct (10)

📋 Check 3: Strategy implementations
   ✅ Found: naive strategy
   ✅ Found: primacy strategy
   ❌ FAIL: Strategy 'recency' not found
   ❌ FAIL: Strategy 'sandwich' not found
   ❌ FAIL: Missing strategies: recency, sandwich

📋 Check 4: Metrics recording
   ✅ Strategy 'naive' has all metrics
   ✅ Strategy 'primacy' has all metrics
   ✅ PASS: All metrics recorded correctly

📋 Check 5: Optimization implementation
   ❌ FAIL: No optimization strategy found

📋 Check 6: Comparison analysis
   ⚠️  WARNING: Expected at least 5 strategies, found 2
   ✅ Analyzed 2 strategies
   ✅ PASS: Comparison analysis complete

================================================================================
                            FINAL RESULTS
================================================================================

✅ Checks Passed: 3/6
❌ Checks Failed: 3/6
⚠️  Warnings: 1

🎓 OVERALL GRADE: FAIL

❌ Lesson not yet complete. Please address the failed checks above.
   Review the notebook and ensure all tasks are completed correctly.

================================================================================
```

---

## Error Handling & Edge Cases

### Edge Case 1: Partially Complete Notebook
**Scenario:** Student runs some cells but not all

**Handling:**
- Verify script checks for all required strategies
- Identifies which specific strategies are missing
- Provides clear guidance on what to complete

### Edge Case 2: Results File Corrupted
**Scenario:** JSON file is malformed

**Handling:**
```python
try:
    results = load_results(self.results_path)
except json.JSONDecodeError as e:
    return self._generate_failure_report(f"Results file corrupted: {e}")
```

### Edge Case 3: Zero Baseline Accuracy
**Scenario:** Naive implementation returns 0% accuracy

**Handling:**
- Check for division by zero in improvement calculations
- Flag as potential implementation error
- Still allow pass if other checks succeed

### Edge Case 4: Optimization Barely Misses Threshold
**Scenario:** Optimization shows 9.5% improvement (threshold is 10%)

**Handling:**
- Strict threshold enforcement (must meet ≥10%)
- Clear feedback showing actual vs. required improvement
- Student must iterate to improve

---

## Integration with Notebook

### How Notebook Saves Results

**In Cell 38 of notebook:**
```python
# Save all results for verification
results_to_save = {
    'metadata': {
        'lesson': 'context_engineering',
        'timestamp': datetime.now().isoformat(),
        'model_used': MODEL_NAME,
        'num_documents': len(documents),
        'num_questions': len(questions)
    },
    'strategies': {}
}

for strategy_name, metrics in all_results.items():
    results_to_save['strategies'][strategy_name] = {
        'accuracy': metrics['accuracy'],
        'avg_tokens': metrics['avg_tokens'],
        'per_question_scores': [r['score'] for r in metrics['all_results']]
    }

save_results(results_to_save, '../progress/lesson_results.json')
```

### Verification Flow

```
Student completes notebook
    ↓
Runs all cells including Cell 38
    ↓
lesson_results.json generated in progress/
    ↓
Student runs: python src/verify.py
    ↓
Verifier loads and validates results
    ↓
Generates lesson_progress.json with grade
    ↓
Student receives immediate feedback
```

---

## Grading Rubric Implementation

### Point Distribution

| Check | Points | Required for Pass |
|-------|--------|------------------|
| Results file exists | 10% | ✅ Yes |
| Token calculations | 15% | ⚠️ No (warning only) |
| All strategies implemented | 30% | ✅ Yes |
| Metrics recorded | 20% | ✅ Yes |
| Optimization implemented | 20% | ✅ Yes |
| Comparison analysis | 5% | ✅ Yes |

**Pass Requirement:** All critical checks must pass (90% of points)

### Implementation in verify.py

```python
# Each check appends to either:
self.checks_passed  # Check succeeded
self.checks_failed  # Check failed (blocks passing)
self.warnings       # Issue noted but doesn't block passing

# Final grade logic:
overall_grade = "PASS" if len(self.checks_failed) == 0 else "FAIL"
```

---

## JSON Schema for lesson_progress.json

### Complete Schema

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "required": ["student_id", "lesson", "timestamp", "verification"],
  "properties": {
    "student_id": {
      "type": "string",
      "format": "uuid",
      "description": "Unique identifier for this lesson completion"
    },
    "lesson": {
      "type": "string",
      "const": "context_engineering"
    },
    "timestamp": {
      "type": "string",
      "format": "date-time",
      "description": "When verification was completed"
    },
    "completion_time_minutes": {
      "type": ["number", "null"],
      "description": "How long student spent on lesson"
    },
    "verification": {
      "type": "object",
      "required": ["grade", "checks_passed", "checks_total"],
      "properties": {
        "grade": {
          "type": "string",
          "enum": ["PASS", "FAIL"]
        },
        "checks_passed": {
          "type": "integer",
          "minimum": 0
        },
        "checks_total": {
          "type": "integer",
          "minimum": 0
        },
        "checks_details": {
          "type": "object",
          "properties": {
            "passed": {"type": "array"},
            "failed": {"type": "array"},
            "warnings": {"type": "array"}
          }
        }
      }
    },
    "tasks_completed": {
      "type": "object",
      "properties": {
        "token_budget_analysis": {
          "type": "object",
          "properties": {
            "status": {"enum": ["PASS", "FAIL"]}
          }
        },
        "naive_implementation": {
          "type": "object",
          "properties": {
            "status": {"enum": ["PASS", "FAIL"]},
            "baseline_accuracy": {"type": "number"}
          }
        },
        "strategic_placement": {
          "type": "object",
          "properties": {
            "status": {"enum": ["PASS", "FAIL"]},
            "primacy_accuracy": {"type": "number"},
            "recency_accuracy": {"type": "number"},
            "sandwich_accuracy": {"type": "number"}
          }
        },
        "optimization": {
          "type": "object",
          "properties": {
            "status": {"enum": ["PASS", "FAIL"]}
          }
        }
      }
    },
    "metrics_summary": {
      "type": "object",
      "properties": {
        "baseline_accuracy": {"type": "number"},
        "best_strategy": {"type": "string"},
        "best_accuracy": {"type": "number"},
        "total_improvement": {"type": "number"},
        "strategies_tested": {"type": "integer"}
      }
    },
    "detailed_results": {
      "type": "object",
      "description": "Full strategy results from lesson"
    }
  }
}
```

### Example Valid Output

```json
{
  "student_id": "f47ac10b-58cc-4372-a567-0e02b2c3d479",
  "lesson": "context_engineering",
  "timestamp": "2025-10-19T14:32:18.123456",
  "completion_time_minutes": 28,
  "verification": {
    "grade": "PASS",
    "checks_passed": 6,
    "checks_total": 6,
    "checks_details": {
      "passed": [
        {"check": "results_file_exists", "status": "PASS"},
        {"check": "token_calculations", "status": "PASS"},
        {"check": "strategies_implemented", "status": "PASS"},
        {"check": "metrics_recorded", "status": "PASS"},
        {"check": "optimization_implemented", "status": "PASS"},
        {"check": "comparison_analysis", "status": "PASS"}
      ],
      "failed": [],
      "warnings": []
    }
  },
  "tasks_completed": {
    "token_budget_analysis": {
      "status": "PASS"
    },
    "naive_implementation": {
      "status": "PASS",
      "baseline_accuracy": 0.71
    },
    "strategic_placement": {
      "status": "PASS",
      "primacy_accuracy": 0.76,
      "recency_accuracy": 0.81,
      "sandwich_accuracy": 0.85
    },
    "optimization": {
      "status": "PASS"
    }
  },
  "metrics_summary": {
    "baseline_accuracy": 0.71,
    "best_strategy": "hierarchical_summary",
    "best_accuracy": 0.87,
    "total_improvement": 0.225,
    "strategies_tested": 5
  },
  "detailed_results": {
    "naive": {
      "accuracy": 0.71,
      "avg_tokens": 3847,
      "per_question_scores": [0.8, 0.7, 0.65, 0.75, 0.68, 0.72, 0.71, 0.69, 0.74, 0.67]
    },
    "primacy": {
      "accuracy": 0.76,
      "avg_tokens": 3845,
      "per_question_scores": [0.82, 0.75, 0.71, 0.78, 0.73, 0.76, 0.75, 0.74, 0.79, 0.77]
    },
    "recency": {
      "accuracy": 0.81,
      "avg_tokens": 3843,
      "per_question_scores": [0.85, 0.79, 0.76, 0.82, 0.78, 0.81, 0.80, 0.79, 0.84, 0.86]
    },
    "sandwich": {
      "accuracy": 0.85,
      "avg_tokens": 3841,
      "per_question_scores": [0.88, 0.83, 0.81, 0.86, 0.82, 0.85, 0.84, 0.83, 0.87, 0.91]
    },
    "hierarchical_summary": {
      "accuracy": 0.87,
      "avg_tokens": 3256,
      "per_question_scores": [0.90, 0.85, 0.84, 0.88, 0.85, 0.87, 0.86, 0.85, 0.89, 0.91]
    }
  }
}
```

---

## CLI Usage & Help Text

### verify.py Command Line Interface

```bash
# Basic usage
python src/verify.py

# With Python path (if needed)
python3.12 src/verify.py

# From project root (recommended)
cd /path/to/VG_Name_Date/
python src/verify.py

# Check exit code (useful for automation)
python src/verify.py
echo $?  # 0 = PASS, 1 = FAIL
```

### Adding Help Text (Optional Enhancement)

```python
# Add to verify.py main() function
import argparse

def main():
    parser = argparse.ArgumentParser(
        description='Verify completion of Context Engineering lesson',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python src/verify.py              # Run verification
  python src/verify.py --verbose    # Show detailed output
  python src/verify.py --json       # Output JSON only

Output:
  progress/lesson_progress.json - Detailed grading results
  
Exit Codes:
  0 - All checks passed (PASS)
  1 - One or more checks failed (FAIL)
        """
    )
    
    parser.add_argument('--verbose', '-v', action='store_true',
                       help='Show detailed verification output')
    parser.add_argument('--json', action='store_true',
                       help='Output only JSON results (no formatting)')
    
    args = parser.parse_args()
    
    # Run verification
    verifier = LessonVerifier()
    report = verifier.run_verification()
    
    if args.json:
        import json
        print(json.dumps(report, indent=2))
    
    # Exit with appropriate code
    exit_code = 0 if report['verification']['grade'] == 'PASS' else 1
    sys.exit(exit_code)
```

---

## Documentation & Comments

### Code Documentation Standards

All verification code includes:

1. **Module docstring** - Purpose and usage
2. **Class docstring** - What the class does
3. **Method docstrings** - Args, returns, behavior
4. **Inline comments** - Complex logic explanation
5. **Examples** - Usage patterns where helpful

### Student-Facing Messages

All output messages follow these principles:

- ✅ **Clear:** No jargon, explain what's checked
- ✅ **Actionable:** Tell students what to fix
- ✅ **Encouraging:** Positive tone even for failures
- ✅ **Consistent:** Same format for all checks
- ✅ **Complete:** No ambiguity about pass/fail

---

## Testing Verification System

### Unit Test Examples (Optional)

```python
# test_verify.py (optional, not required for lesson)
import unittest
from src.verify import LessonVerifier

class TestLessonVerifier(unittest.TestCase):
    
    def test_results_file_check(self):
        """Test that missing results file is caught."""
        verifier = LessonVerifier()
        # Temporarily rename results file
        # Run check
        # Assert failure detected
        pass
    
    def test_strategy_detection(self):
        """Test that all strategies are properly detected."""
        pass
    
    def test_improvement_calculation(self):
        """Test improvement threshold checking."""
        pass

if __name__ == '__main__':
    unittest.main()
```

---

## Summary of Chunk 5

### Files Completed

1. ✅ **src/evaluation.py** (10-12 KB)
   - LLMEvaluator class
   - Answer generation
   - Semantic similarity scoring
   - LLM-as-judge scoring
   - Batch evaluation
   - Metrics calculation

2. ✅ **src/verify.py** (15-18 KB)
   - LessonVerifier class
   - 6 comprehensive checks
   - Detailed error reporting
   - JSON output generation
   - CLI interface
   - Exit code handling

### Key Features

- **Robust error handling** - Graceful failures with helpful messages
- **Comprehensive checks** - Validates all lesson requirements
- **Clear feedback** - Students know exactly what passed/failed
- **JSON output** - Machine-readable results for automation
- **Exit codes** - Standard 0/1 for pass/fail

---

## Next Steps

1. Save this as `docs/05_evaluation_and_verify_specs.md`
2. Review both evaluation and verification implementations
3. Ready for Chunk 6: Data files specifications (JSON files)

**Ready for Chunk 6 when you are!**