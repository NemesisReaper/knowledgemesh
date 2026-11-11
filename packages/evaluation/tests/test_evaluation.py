import pytest
from evaluation import *

def test_utility_weighted_score():
    result=evaluate_utility({"relevance":1,"novelty":0},weights={"relevance":3,"novelty":1})
    assert result.overall == .75

def test_claim_quality_missing_dimensions_renormalized():
    result=evaluate_claim_quality({"clarity":1,"specificity":.5})
    assert result.overall == pytest.approx(.75)
    assert "evidence_traceability" in result.missing_dimensions

def test_task_success_metrics():
    outcomes=[TaskOutcome("a",True,2,2,2),TaskOutcome("b",False,4,4,2,retries=1,error_category="timeout")]
    result=evaluate_task_success(outcomes)
    assert result.success_rate == .5
    assert result.mean_duration_seconds == 3
    assert result.step_completion_rate == pytest.approx(4/6)
    assert result.error_counts == {"timeout":1}

def test_benchmark_runner_and_report():
    suite=BenchmarkSuite("math",(BenchmarkCase("one",2,4),BenchmarkCase("two",3,9)))
    results=run_benchmark(suite,lambda x:x*x)
    assert all(r.passed for r in results)
    report=build_report("r1","Math",benchmark_results=results)
    assert report.summary["pass_rate"] == 1
    assert report.to_dict()["benchmark_results"][0]["case_id"] == "one"

def test_benchmark_captures_errors_and_validates_ids():
    suite=BenchmarkSuite("errors",(BenchmarkCase("x",1,1),))
    result=run_benchmark(suite,lambda _:1/0)[0]
    assert not result.passed and "ZeroDivisionError" in result.error
    with pytest.raises(ValueError):
        BenchmarkSuite("bad",(BenchmarkCase("x",1),BenchmarkCase("x",2)))
