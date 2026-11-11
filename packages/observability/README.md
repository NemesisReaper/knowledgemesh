# KnowMesh Observability

A Python observability package built on the standard library. It provides:

- Structured JSON logging with async/task-local context.
- Thread-safe counters, gauges and histograms.
- Prometheus text exposition.
- Lightweight spans and W3C `traceparent` parsing/propagation.
- Liveness/readiness health checks with per-check timeouts.
- Function and HTTP request instrumentation helpers.

## Quick start

```python
from packages.observability import (
    configure_logging, get_logger, MetricRegistry, Tracer,
    InMemoryTraceExporter, HealthRegistry, HealthCheck,
)

configure_logging()
log = get_logger("knowmesh.api")
log.info("node started", node_id="node-a")

metrics = MetricRegistry()
requests = metrics.counter("knowmesh_requests", "Requests", ("route",))
requests.inc(labels={"route": "/search"})

exporter = InMemoryTraceExporter()
tracer = Tracer("knowmesh-api", exporter)
with tracer.start_as_current_span("search", attributes={"component": "discovery"}):
    pass

health = HealthRegistry([HealthCheck("database", lambda: True)]).run()
print(health.to_dict())
```

## Exporting metrics

```python
from packages.observability import render_prometheus
print(render_prometheus(metrics))
```

## Integration notes

The package does not force FastAPI, OpenTelemetry SDK, Prometheus client,
or a hosted telemetry backend. An application can expose `render_prometheus`
from its own metrics endpoint and bridge spans/logs to its chosen collector.

## Security and operational notes

- Never log credentials, tokens, private keys, personal data or raw request
  bodies. Structured logging does not automatically redact secrets.
- Use route templates rather than raw URLs as metric labels to avoid
  high-cardinality metrics and accidental data exposure.
- In-memory metrics and traces are process-local and reset on restart.
- The tracer implements a minimal trace-context subset, not the full
  OpenTelemetry SDK or complete W3C Trace Context validation.
- A timed-out health-check thread cannot be forcibly killed; check functions
  should be bounded, non-blocking and safe to run in worker threads.
