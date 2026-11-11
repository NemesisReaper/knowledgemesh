# KnowMesh Evaluation

Evaluation primitives for measuring the utility and quality of knowledge artifacts,
claim quality, task outcomes, and system benchmark performance.

## Modules
- `knowledge_utility.py`: weighted, caller-assessed utility dimensions.
- `claim_quality.py`: configurable claim-quality rubric.
- `task_success.py`: success rate, latency, retries, step completion and error counts.
- `benchmarks.py`: reusable benchmark cases and synchronous benchmark runner.
- `reports.py`: aggregate evaluation report with JSON-serializable output.

## Quick start
```python
from evaluation import BenchmarkCase, BenchmarkSuite, run_benchmark, build_report

suite = BenchmarkSuite("retrieval-v1", (
    BenchmarkCase("case-1", "query", expected=["claim-7"]),
))
results = run_benchmark(suite, system=lambda query: ["claim-7"])
report = build_report("run-001", "Retrieval evaluation",
                      benchmark_results=results)
print(report.to_dict()["summary"])
```

## Boundaries
- Scores are only as reliable as the assessors and test data supplied by callers.
- Missing rubric dimensions are omitted and remaining weights renormalized; they are not zeros.
- Benchmark execution is synchronous and local; no distributed load generation or statistical significance testing.
- This package does not define a universal ground-truth dataset or domain-specific acceptance threshold.
- Latency measurements are wall-clock observations from one run; use repeated trials for robust comparisons.
- Evaluation scores must not be interpreted as truth, provenance, authenticity, or trust.
