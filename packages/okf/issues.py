"""Structured validation and parsing issue definitions for the Open Knowledge Format (OKF)."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Mapping


class IssueSeverity(str, Enum):
    ERROR = "error"
    WARNING = "warning"
    INFO = "info"


class OKFError(ValueError):
    """Raised when an OKF bundle or manifest cannot be parsed or resolved."""


@dataclass(frozen=True, slots=True)
class OKFIssue:
    code: str
    message: str
    severity: IssueSeverity = IssueSeverity.ERROR
    path: str = ""
    details: Mapping[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not self.code or not self.message:
            raise ValueError("issue code and message are required")
        object.__setattr__(self, "severity", IssueSeverity(self.severity))

    def to_dict(self) -> dict[str, Any]:
        return {
            "code": self.code,
            "message": self.message,
            "severity": self.severity.value,
            "path": self.path,
            "details": dict(self.details),
        }

