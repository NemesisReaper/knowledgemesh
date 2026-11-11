"""Shared foundational contracts for KnowMesh packages."""
from .ids import new_id, validate_id
from .errors import KnowMeshError, ValidationError, NotFoundError, ConflictError, AuthorizationError, IntegrityError, DependencyUnavailableError
from .config import CoreSettings, load_settings
from .serialization import canonical_json, stable_hash, to_primitive
from .events import DomainEvent, EventEnvelope, EventBus, InMemoryEventBus
from .pagination import Page, PageRequest, paginate
from .result import Result
__all__=["new_id","validate_id","KnowMeshError","ValidationError","NotFoundError",
"ConflictError","AuthorizationError","IntegrityError","DependencyUnavailableError",
"CoreSettings","load_settings","canonical_json","stable_hash","to_primitive",
"DomainEvent","EventEnvelope","EventBus","InMemoryEventBus","Page","PageRequest",
"paginate","Result"]
