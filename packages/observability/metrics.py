"""Thread-safe in-process metrics and Prometheus text exposition."""

from __future__ import annotations

from dataclasses import dataclass
import math
import re
import threading
from typing import Iterable, Mapping


class MetricsError(ValueError):
    pass


_NAME_RE = re.compile(r"^[a-zA-Z_:][a-zA-Z0-9_:]*$")
_LABEL_RE = re.compile(r"^[a-zA-Z_][a-zA-Z0-9_]*$")


def _validate_name(name: str) -> None:
    if not _NAME_RE.match(name):
        raise MetricsError(f"invalid metric name: {name!r}")


def _labels(labels: Mapping[str, str] | None) -> tuple[tuple[str, str], ...]:
    result = []
    for key, value in (labels or {}).items():
        if not _LABEL_RE.match(key) or key == "__name__":
            raise MetricsError(f"invalid label name: {key!r}")
        result.append((key, str(value)))
    return tuple(sorted(result))


@dataclass(frozen=True, slots=True)
class MetricSample:
    name: str
    value: float
    labels: tuple[tuple[str, str], ...] = ()


class _Metric:
    def __init__(self, name: str, help_text: str, label_names: Iterable[str] = ()) -> None:
        _validate_name(name)
        self.name, self.help = name, help_text
        self.label_names = tuple(sorted(label_names))
        if len(set(self.label_names)) != len(self.label_names):
            raise MetricsError("duplicate label names")
        for label in self.label_names:
            if not _LABEL_RE.match(label):
                raise MetricsError(f"invalid label name: {label}")
        self._lock = threading.RLock()

    def _key(self, labels: Mapping[str, str] | None) -> tuple[tuple[str, str], ...]:
        key = _labels(labels)
        if tuple(name for name, _ in key) != self.label_names:
            raise MetricsError(f"{self.name} requires labels {self.label_names}")
        return key


class Counter(_Metric):
    def __init__(self, name: str, help_text: str = "", label_names=()) -> None:
        if name.endswith("_total"):
            raise MetricsError("counter name should omit _total suffix")
        super().__init__(name, help_text, label_names)
        self._values: dict[tuple, float] = {}

    def inc(self, amount: float = 1, *, labels: Mapping[str, str] | None = None) -> None:
        amount = float(amount)
        if not math.isfinite(amount) or amount < 0:
            raise MetricsError("counter increment must be finite and non-negative")
        key = self._key(labels)
        with self._lock:
            self._values[key] = self._values.get(key, 0.0) + amount

    def samples(self) -> list[MetricSample]:
        with self._lock:
            values = dict(self._values)
        return [MetricSample(self.name + "_total", value, key)
                for key, value in sorted(values.items())]


class Gauge(_Metric):
    def __init__(self, name: str, help_text: str = "", label_names=()) -> None:
        super().__init__(name, help_text, label_names)
        self._values: dict[tuple, float] = {}

    def set(self, value: float, *, labels: Mapping[str, str] | None = None) -> None:
        value = float(value)
        if not math.isfinite(value):
            raise MetricsError("gauge value must be finite")
        key = self._key(labels)
        with self._lock:
            self._values[key] = value

    def inc(self, amount: float = 1, *, labels: Mapping[str, str] | None = None) -> None:
        key = self._key(labels)
        with self._lock:
            self._values[key] = self._values.get(key, 0.0) + float(amount)

    def dec(self, amount: float = 1, *, labels: Mapping[str, str] | None = None) -> None:
        self.inc(-float(amount), labels=labels)

    def samples(self) -> list[MetricSample]:
        with self._lock:
            values = dict(self._values)
        return [MetricSample(self.name, value, key)
                for key, value in sorted(values.items())]


class Histogram(_Metric):
    def __init__(self, name: str, help_text: str = "", label_names=(),
                 buckets=(0.005, 0.01, 0.025, 0.05, 0.1, 0.25, 0.5, 1.0, 2.5, 5.0, 10.0)) -> None:
        super().__init__(name, help_text, label_names)
        values = tuple(float(x) for x in buckets)
        if not values or any(not math.isfinite(x) for x in values):
            raise MetricsError("histogram buckets must be finite and non-empty")
        if tuple(sorted(set(values))) != values:
            raise MetricsError("histogram buckets must be strictly increasing")
        self.buckets = values
        self._observations: dict[tuple, list[float]] = {}

    def observe(self, value: float, *, labels: Mapping[str, str] | None = None) -> None:
        value = float(value)
        if not math.isfinite(value):
            raise MetricsError("histogram observation must be finite")
        key = self._key(labels)
        with self._lock:
            self._observations.setdefault(key, []).append(value)

    def samples(self) -> list[MetricSample]:
        with self._lock:
            snapshot = {key: list(values) for key, values in self._observations.items()}
        result = []
        for labels, values in sorted(snapshot.items()):
            for bucket in self.buckets:
                count = sum(value <= bucket for value in values)
                result.append(MetricSample(self.name + "_bucket", float(count),
                                           labels + (("le", str(bucket)),)))
            result.append(MetricSample(self.name + "_bucket", float(len(values)),
                                       labels + (("le", "+Inf"),)))
            result.append(MetricSample(self.name + "_sum", sum(values), labels))
            result.append(MetricSample(self.name + "_count", float(len(values)), labels))
        return result


class MetricRegistry:
    def __init__(self) -> None:
        self._metrics: dict[str, _Metric] = {}
        self._lock = threading.RLock()

    def register(self, metric: _Metric):
        with self._lock:
            if metric.name in self._metrics:
                raise MetricsError(f"metric already registered: {metric.name}")
            self._metrics[metric.name] = metric
        return metric

    def counter(self, name: str, help_text: str = "", label_names=()) -> Counter:
        return self.register(Counter(name, help_text, label_names))

    def gauge(self, name: str, help_text: str = "", label_names=()) -> Gauge:
        return self.register(Gauge(name, help_text, label_names))

    def histogram(self, name: str, help_text: str = "", label_names=(),
                  buckets=(0.005, 0.01, 0.025, 0.05, 0.1, 0.25, 0.5, 1.0, 2.5, 5.0, 10.0)) -> Histogram:
        return self.register(Histogram(name, help_text, label_names, buckets))

    def metrics(self) -> tuple[_Metric, ...]:
        with self._lock:
            return tuple(self._metrics.values())

    def clear(self) -> None:
        with self._lock:
            self._metrics.clear()


def _escape(value: str) -> str:
    return value.replace("\\", "\\\\").replace("\n", "\\n").replace('"', '\\"')


def render_prometheus(registry: MetricRegistry) -> str:
    """Render a Prometheus-compatible text exposition."""
    lines = []
    for metric in sorted(registry.metrics(), key=lambda item: item.name):
        metric_type = "counter" if isinstance(metric, Counter) else (
            "gauge" if isinstance(metric, Gauge) else "histogram"
        )
        lines.append(f"# HELP {metric.name} {metric.help.replace(chr(10), ' ')}")
        lines.append(f"# TYPE {metric.name} {metric_type}")
        for sample in metric.samples():
            label_text = ""
            if sample.labels:
                label_text = "{" + ",".join(
                    f'{key}="{_escape(value)}"' for key, value in sample.labels
                ) + "}"
            lines.append(f"{sample.name}{label_text} {sample.value:g}")
    return "\n".join(lines) + ("\n" if lines else "")


default_registry = MetricRegistry()
