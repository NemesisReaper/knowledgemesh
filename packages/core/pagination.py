from __future__ import annotations
from dataclasses import dataclass
from typing import Generic, TypeVar, Sequence

T=TypeVar("T")

@dataclass(frozen=True)
class PageRequest:
    limit: int=20
    offset: int=0
    def __post_init__(self):
        if self.limit < 1: raise ValueError("limit must be positive")
        if self.offset < 0: raise ValueError("offset cannot be negative")

@dataclass(frozen=True)
class Page(Generic[T]):
    items: tuple[T,...]
    total: int
    limit: int
    offset: int
    @property
    def has_next(self): return self.offset+len(self.items)<self.total
    @property
    def next_offset(self): return self.offset+len(self.items) if self.has_next else None

def paginate(items: Sequence[T], request: PageRequest, *, max_limit: int=100) -> Page[T]:
    if request.limit > max_limit: raise ValueError(f"limit exceeds maximum of {max_limit}")
    total=len(items)
    selected=tuple(items[request.offset:request.offset+request.limit])
    return Page(selected,total,request.limit,request.offset)
