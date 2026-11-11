from __future__ import annotations
from dataclasses import dataclass
from typing import Generic, TypeVar

T=TypeVar("T")
E=TypeVar("E")

@dataclass(frozen=True)
class Result(Generic[T,E]):
    """Small explicit success/failure value; exactly one branch must be populated."""
    value: T | None=None
    error: E | None=None
    def __post_init__(self):
        if (self.value is None) == (self.error is None):
            raise ValueError("exactly one of value or error must be set")
    @property
    def is_ok(self): return self.error is None
    @property
    def is_err(self): return self.error is not None
    def unwrap(self) -> T:
        if self.error is not None: raise RuntimeError(f"cannot unwrap failed result: {self.error}")
        return self.value
