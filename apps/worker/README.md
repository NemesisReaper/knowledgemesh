# KnowMesh Worker
Deterministic local job functions and stdin JSON CLI. Install with `pip install -e '.[test]'`; run e.g. `echo '{"age_days":7}' | python -m knowmesh_worker.main decay_prediction`.

No queue consumer, scheduler, retry policy, durable job state, distributed lock or supervisor is included. Adversarial review and claim extraction are heuristics, not security enforcement or semantic AI.
