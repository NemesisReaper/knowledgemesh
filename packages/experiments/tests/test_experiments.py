from experiments import (
    ExecutionAttempt,
    ExecutionStatus,
    ExperimentProtocol,
    Hypothesis,
    HypothesisStatus,
    ProtocolStep,
    ReproducibilityManifest,
    assess_reproducibility,
    evaluate_outcome,
)


def test_experiment_lifecycle_and_reproducibility():
    hyp = Hypothesis(
        hypothesis_id="h-1",
        statement="Hybrid RRF search achieves MRR >= 0.80",
        expected_metric="mrr",
        expected_threshold=0.80,
        comparison=">=",
    )
    protocol = ExperimentProtocol(
        protocol_id="proto-1",
        hypothesis_id="h-1",
        name="Hybrid RRF Benchmark",
        steps=(ProtocolStep("s1", "Run benchmark", "evaluate"),),
        required_metrics=("mrr",),
        minimum_trials=2,
    )
    a1 = ExecutionAttempt("proto-1")
    a1.start()
    a1.add_log("Trial 1 complete")
    a1.complete({"mrr": 0.84})

    a2 = ExecutionAttempt("proto-1")
    a2.start()
    a2.complete({"mrr": 0.86})

    assert a1.status == ExecutionStatus.COMPLETED
    outcome = evaluate_outcome(hyp, protocol, [a1, a2])
    assert outcome.verdict == HypothesisStatus.SUPPORTED
    assert outcome.completed_trials == 2

    repro = assess_reproducibility([a1, a2], metric="mrr", tolerance=0.05)
    assert repro.reproducible

    manifest = ReproducibilityManifest(seed=42, environment_fingerprint="py311-linux")
    assert manifest.digest().startswith("sha256:")

