from __future__ import annotations

from datetime import datetime, timezone
from enum import Enum
from typing import Any
from uuid import uuid4


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


class ExecutionStatus(str, Enum):
    CREATED = "created"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class ExecutionAttempt:
    def __init__(
        self,
        experiment_id: str,
        environment: dict[str, Any] | None = None,
        parameters: dict[str, Any] | None = None,
        reproducibility: dict[str, Any] | None = None,
    ) -> None:
        self.attempt_id = str(uuid4())
        self.experiment_id = experiment_id
        self.status = ExecutionStatus.CREATED
        self.environment = environment or {}
        self.parameters = parameters or {}
        self.reproducibility = reproducibility or {}
        self.created_at = utc_now()
        self.started_at: str | None = None
        self.completed_at: str | None = None
        self.logs: list[str] = []
        self.output: dict[str, Any] | None = None
        self.error: str | None = None

    def start(self) -> None:
        self.status = ExecutionStatus.RUNNING
        self.started_at = utc_now()

    def complete(self, output: dict[str, Any] | None = None) -> None:
        self.status = ExecutionStatus.COMPLETED
        self.completed_at = utc_now()
        self.output = output or {}

    def fail(self, error: str) -> None:
        self.status = ExecutionStatus.FAILED
        self.completed_at = utc_now()
        self.error = error

    def cancel(self) -> None:
        self.status = ExecutionStatus.CANCELLED
        self.completed_at = utc_now()

    def add_log(self, message: str) -> None:
        self.logs.append(f"[{utc_now()}] {message}")

    def to_dict(self) -> dict[str, Any]:
        return {
            "attempt_id": self.attempt_id,
            "experiment_id": self.experiment_id,
            "status": self.status.value,
            "environment": self.environment,
            "parameters": self.parameters,
            "reproducibility": self.reproducibility,
            "created_at": self.created_at,
            "started_at": self.started_at,
            "completed_at": self.completed_at,
            "logs": self.logs,
            "output": self.output,
            "error": self.error,
        }
