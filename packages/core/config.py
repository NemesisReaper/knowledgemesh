from __future__ import annotations
from dataclasses import dataclass
import os

@dataclass(frozen=True)
class CoreSettings:
    service_name: str="knowmesh-node"
    environment: str="development"
    log_level: str="INFO"
    request_timeout_seconds: float=10.0
    max_page_size: int=100
    default_page_size: int=20
    def __post_init__(self):
        if not self.service_name.strip(): raise ValueError("service_name is required")
        if self.environment not in {"development","test","staging","production"}:
            raise ValueError("environment must be development, test, staging or production")
        if self.request_timeout_seconds <= 0: raise ValueError("request timeout must be positive")
        if self.max_page_size < 1: raise ValueError("max_page_size must be positive")
        if not 1 <= self.default_page_size <= self.max_page_size:
            raise ValueError("default_page_size must be within max_page_size")

def load_settings(environ=None) -> CoreSettings:
    """Load core settings from an explicit mapping or process environment."""
    env=os.environ if environ is None else environ
    return CoreSettings(
        service_name=env.get("KNOWMESH_SERVICE_NAME","knowmesh-node"),
        environment=env.get("KNOWMESH_ENVIRONMENT","development").lower(),
        log_level=env.get("KNOWMESH_LOG_LEVEL","INFO").upper(),
        request_timeout_seconds=float(env.get("KNOWMESH_REQUEST_TIMEOUT_SECONDS","10")),
        max_page_size=int(env.get("KNOWMESH_MAX_PAGE_SIZE","100")),
        default_page_size=int(env.get("KNOWMESH_DEFAULT_PAGE_SIZE","20")),
    )
