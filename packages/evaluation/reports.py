from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime, timezone
from collections.abc import Iterable, Mapping
from .benchmarks import BenchmarkResult
from .task_success import TaskOutcome, evaluate_task_success, TaskSuccessMetrics

@dataclass(frozen=True)
class EvaluationReport:
    report_id: str
    title: str
    generated_at: datetime
    summary: dict[str,object]
    benchmark_results: tuple[BenchmarkResult,...] = ()
    task_metrics: TaskSuccessMetrics | None = None
    notes: tuple[str,...] = ()

    def to_dict(self) -> dict[str,object]:
        return {
            "report_id":self.report_id,"title":self.title,
            "generated_at":self.generated_at.isoformat(),
            "summary":self.summary,
            "benchmark_results":[
                {"case_id":r.case_id,"passed":r.passed,"actual":r.actual,
                 "expected":r.expected,"duration_seconds":r.duration_seconds,"error":r.error}
                for r in self.benchmark_results],
            "task_metrics":None if self.task_metrics is None else {
                "total_tasks":self.task_metrics.total_tasks,
                "successful_tasks":self.task_metrics.successful_tasks,
                "failed_tasks":self.task_metrics.failed_tasks,
                "success_rate":self.task_metrics.success_rate,
                "mean_duration_seconds":self.task_metrics.mean_duration_seconds,
                "mean_retries":self.task_metrics.mean_retries,
                "step_completion_rate":self.task_metrics.step_completion_rate,
                "error_counts":self.task_metrics.error_counts},
            "notes":list(self.notes)}

def build_report(report_id: str, title: str, *,
                 benchmark_results: Iterable[BenchmarkResult]=(),
                 task_outcomes: Iterable[TaskOutcome]=(),
                 summary: Mapping[str,object] | None=None,
                 notes: Iterable[str]=()) -> EvaluationReport:
    if not report_id or not title: raise ValueError("report_id and title are required")
    results=tuple(benchmark_results); outcomes=tuple(task_outcomes)
    benchmark_summary={}
    if results:
        passed=sum(r.passed for r in results)
        benchmark_summary={"case_count":len(results),"passed":passed,
                           "failed":len(results)-passed,"pass_rate":passed/len(results),
                           "mean_latency_seconds":sum(r.duration_seconds for r in results)/len(results)}
    task_metrics=evaluate_task_success(outcomes) if outcomes else None
    merged={**benchmark_summary,**(dict(summary) if summary else {})}
    return EvaluationReport(report_id,title,datetime.now(timezone.utc),merged,
                            results,task_metrics,tuple(notes))
