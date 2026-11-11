# KnowMesh Simulation

Python simulation primitives for testing network behavior and controlled
counterfactuals without contacting real nodes.

## Modules

- `scenarios.py`: declarative scenario steps, dependencies, action registry,
  deterministic topological execution.
- `failure_models.py`: seeded probabilistic failure injection and state effects.
- `network_models.py`: graph topology, availability, connected components,
  density, degree and latency-weighted shortest paths.
- `counterfactual.py`: isolated baseline/intervention evaluation using safe,
  declarative dictionary operations.

## Quick start

```python
from packages.simulation import (
    NetworkModel, NetworkNode, NetworkEdge,
    FailureModel, FailureType, sample_failure, apply_failure,
)

network = NetworkModel()
network.add_node(NetworkNode("node-a"))
network.add_node(NetworkNode("node-b"))
network.add_edge(NetworkEdge("node-a", "node-b", latency_ms=25))

print(network.snapshot().metrics)

model = FailureModel("outage-1", FailureType.NODE_UNAVAILABLE, probability=1.0)
event = sample_failure(model, seed=42, target_id="node-a")
state = apply_failure({"available": True}, event)
print(state)
```

## Limitations and safety

- These are local simulation primitives, not a distributed simulator.
- Scenario actions must be registered by trusted application code; scenario
  files cannot execute arbitrary Python.
- Network edges are undirected and use a simplified latency-only shortest path.
- Failure models express simulated effects; they do not alter real services.
- Counterfactual outcomes are only as meaningful as the evaluator supplied.
- Results are not predictions or guarantees about production behavior.
- The package does not include discrete-event scheduling, packet-level
  networking, consensus simulation, or a calibrated stochastic model.
