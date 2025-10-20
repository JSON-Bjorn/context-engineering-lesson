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
