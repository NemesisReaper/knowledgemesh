import io
import json
import logging
import unittest

from packages.observability import (
    configure_logging, get_logger, bind_log_context, clear_log_context,
    MetricRegistry, render_prometheus, Tracer, InMemoryTraceExporter,
    parse_traceparent, traceparent_from_context,
    HealthRegistry, HealthCheck, HealthStatus, observe_request,
)


class ObservabilityTests(unittest.TestCase):
    def test_json_logging_context(self):
        stream = io.StringIO()
        configure_logging(level="INFO", stream=stream, logger_name="test.km")
        bind_log_context(request_id="req-1")
        try:
            get_logger("test.km").info("hello", node_id="node-a")
        finally:
            clear_log_context()
        payload = json.loads(stream.getvalue().strip())
        self.assertEqual(payload["request_id"], "req-1")
        self.assertEqual(payload["node_id"], "node-a")

    def test_metrics_prometheus(self):
        registry = MetricRegistry()
        counter = registry.counter("km_events", "Events", ("kind",))
        counter.inc(labels={"kind": "publish"})
        histogram = registry.histogram("km_latency_seconds", "Latency", buckets=(0.1, 1.0))
        histogram.observe(0.2)
        output = render_prometheus(registry)
        self.assertIn("km_events_total", output)
        self.assertIn("km_latency_seconds_bucket", output)

    def test_tracing_context(self):
        exporter = InMemoryTraceExporter()
        tracer = Tracer("test-service", exporter)
        with tracer.start_as_current_span("root") as context:
            header = traceparent_from_context()
            self.assertEqual(parse_traceparent(header), context)
        self.assertEqual(len(exporter.spans()), 1)

    def test_health_registry(self):
        registry = HealthRegistry([
            HealthCheck("ready", lambda: True),
            HealthCheck("dependency", lambda: False, critical=False),
        ])
        report = registry.run()
        self.assertEqual(report.status, HealthStatus.DEGRADED)

    def test_http_metrics_helper(self):
        registry = MetricRegistry()
        observe_request(registry, method="get", route="/nodes/{id}",
                        status_code=200, duration_seconds=0.03)
        output = render_prometheus(registry)
        self.assertIn("knowmesh_http_requests_total", output)


if __name__ == "__main__":
    unittest.main()
