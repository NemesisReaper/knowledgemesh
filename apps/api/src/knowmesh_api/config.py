from __future__ import annotations

from dataclasses import dataclass
import os


@dataclass(frozen=True)
class Settings:
    app_name: str = os.getenv("KNOWMESH_APP_NAME", "KnowMesh API")
    environment: str = os.getenv("KNOWMESH_ENVIRONMENT", "development")
    api_prefix: str = os.getenv("KNOWMESH_API_PREFIX", "/api/v1")
    node_id: str = os.getenv("KNOWMESH_NODE_ID", "node-a")
    node_name: str = os.getenv("KNOWMESH_NODE_NAME", "KnowMesh Primary Node")
    node_endpoint: str = os.getenv("KNOWMESH_NODE_ENDPOINT", "http://127.0.0.1:8000")
    database_url: str = os.getenv(
        "KNOWMESH_DATABASE_URL",
        os.getenv("DATABASE_URL", "sqlite:///./knowmesh.db"),
    )
    secret_key: str = os.getenv(
        "KNOWMESH_SECRET_KEY",
        "knowmesh-dev-hmac-key-change-in-production-0123456789abcdef",
    )
    access_token_ttl_seconds: int = int(os.getenv("KNOWMESH_ACCESS_TOKEN_TTL", "3600"))
    refresh_token_ttl_seconds: int = int(os.getenv("KNOWMESH_REFRESH_TOKEN_TTL", "86400"))
    rate_limit_per_minute: int = int(os.getenv("KNOWMESH_RATE_LIMIT_PER_MINUTE", "600"))
    max_request_bytes: int = int(os.getenv("KNOWMESH_MAX_REQUEST_BYTES", "2097152"))
    allow_local_peers: bool = os.getenv("KNOWMESH_ALLOW_LOCAL_PEERS", "true").lower() in {
        "1",
        "true",
        "yes",
    }
    cors_origins: tuple[str, ...] = (
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:3001",
    )


settings = Settings()
