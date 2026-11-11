from __future__ import annotations
from dataclasses import dataclass, field
from collections.abc import Callable, Iterable, Mapping
from time import perf_counter
from typing import Any

@dataclass(frozen=True)
class BenchmarkCase:
    case_id: str
    input: Any
    expected: Any = None
    metadata: Mapping[str,Any] = field(default_factory=dict)
    def __post_init__(self):
        if not self.case_id: raise ValueError("case_id required")

@dataclass(frozen=True)
class BenchmarkResult:
    case_id: str
    passed: bool
    actual: Any
    expected: Any
    duration_seconds: float
    error: str | None = None

@dataclass(frozen=True)
class BenchmarkSuite:
    name: str
    cases: tuple[BenchmarkCase,...]
    def __post_init__(self):
        if not self.name: raise ValueError("suite name required")
        if len({c.case_id for c in self.cases}) != len(self.cases):
            raise ValueError("benchmark case IDs must be unique")

def run_benchmark(suite: BenchmarkSuite, system: Callable[[Any],Any], *,
                  comparator: Callable[[Any,Any],bool] | None=None) -> tuple[BenchmarkResult,...]:
    """Run a synchronous system against cases and capture per-case latency/errors."""
    compare=comparator or (lambda actual,expected: actual == expected)
    results=[]
    for case in suite.cases:
        start=perf_counter()
        try:
            actual=system(case.input)
            passed=bool(compare(actual,case.expected))
            results.append(BenchmarkResult(case.case_id,passed,actual,case.expected,
                                           perf_counter()-start))
        except Exception as exc:
            results.append(BenchmarkResult(case.case_id,False,None,case.expected,
                                           perf_counter()-start,
                                           f"{type(exc).__name__}: {exc}"))
    return tuple(results)
