from __future__ import annotations

from contextlib import asynccontextmanager
from dataclasses import dataclass
from collections.abc import AsyncIterator, Mapping
import os
from typing import Any

from sqlalchemy import text
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

def normalize_async_database_url(url: str) -> str:
    """Normalize common PostgreSQL/SQLite URLs to async SQLAlchemy drivers."""
    value = url.strip()
    if not value:
        raise ValueError("database URL cannot be empty")
    if value.startswith("postgres://"):
        return "postgresql+asyncpg://" + value[len("postgres://"):]
    if value.startswith("postgresql://"):
        return "postgresql+asyncpg://" + value[len("postgresql://"):]
    if value.startswith("sqlite://") and not value.startswith("sqlite+"):
        return "sqlite+aiosqlite://" + value[len("sqlite://"):]
    if value.startswith(("postgresql+asyncpg://", "sqlite+aiosqlite://")):
        return value
    if "://" not in value:
        raise ValueError("database URL must include a SQLAlchemy driver scheme")
    if value.startswith(("mysql://", "mysql+")):
        raise ValueError("MySQL async driver support is not configured")
    return value

@dataclass(frozen=True)
class DatabaseSettings:
    """Validated database configuration. Prefer DATABASE_URL in deployment."""
    url: str
    echo: bool = False
    pool_pre_ping: bool = True
    pool_size: int = 5
    max_overflow: int = 10
    pool_timeout_seconds: float = 30.0
    pool_recycle_seconds: int = 1800

    def __post_init__(self):
        normalized = normalize_async_database_url(self.url)
        object.__setattr__(self, "url", normalized)
        if self.pool_size < 1:
            raise ValueError("pool_size must be positive")
        if self.max_overflow < 0:
            raise ValueError("max_overflow cannot be negative")
        if self.pool_timeout_seconds <= 0:
            raise ValueError("pool_timeout_seconds must be positive")
        if self.pool_recycle_seconds < 1:
            raise ValueError("pool_recycle_seconds must be positive")

    @classmethod
    def from_env(cls, environ: Mapping[str, str] | None = None) -> "DatabaseSettings":
        env = os.environ if environ is None else environ
        url = env.get("DATABASE_URL") or env.get("KNOWMESH_DATABASE_URL")
        if not url:
            raise ValueError("DATABASE_URL or KNOWMESH_DATABASE_URL must be configured")
        return cls(
            url=url,
            echo=env.get("DATABASE_ECHO", "false").lower() in {"1", "true", "yes"},
            pool_size=int(env.get("DATABASE_POOL_SIZE", "5")),
            max_overflow=int(env.get("DATABASE_MAX_OVERFLOW", "10")),
            pool_timeout_seconds=float(env.get("DATABASE_POOL_TIMEOUT", "30")),
            pool_recycle_seconds=int(env.get("DATABASE_POOL_RECYCLE", "1800")),
        )

class Database:
    """Owns one async SQLAlchemy engine and its session factory.

    Construct once per application process and call ``dispose`` during shutdown.
    """
    def __init__(self, settings: DatabaseSettings, *,
                 engine: AsyncEngine | None = None,
                 engine_options: Mapping[str, Any] | None = None):
        self.settings = settings
        options: dict[str, Any] = {
            "echo": settings.echo,
            "pool_pre_ping": settings.pool_pre_ping,
        }
        # SQLite's async dialect uses a different pool; don't pass QueuePool options.
        if not settings.url.startswith("sqlite+"):
            options.update({
                "pool_size": settings.pool_size,
                "max_overflow": settings.max_overflow,
                "pool_timeout": settings.pool_timeout_seconds,
                "pool_recycle": settings.pool_recycle_seconds,
            })
        if engine_options:
            options.update(dict(engine_options))
        self.engine = engine or create_async_engine(settings.url, **options)
        self.sessions = async_sessionmaker(
            bind=self.engine,
            class_=AsyncSession,
            expire_on_commit=False,
            autoflush=False,
        )

    async def ping(self) -> bool:
        """Return True if a lightweight database round-trip succeeds."""
        async with self.engine.connect() as connection:
            await connection.execute(text("SELECT 1"))
        return True

    @asynccontextmanager
    async def session(self) -> AsyncIterator[AsyncSession]:
        """Yield a session; roll back on errors and always close it."""
        async with self.sessions() as session:
            try:
                yield session
            except Exception:
                await session.rollback()
                raise

    @asynccontextmanager
    async def transaction(self) -> AsyncIterator[AsyncSession]:
        """Yield a session inside an explicit transaction."""
        async with self.sessions() as session:
            async with session.begin():
                yield session

    async def dispose(self) -> None:
        await self.engine.dispose()

def create_database(settings: DatabaseSettings | None = None, *,
                    environ: Mapping[str, str] | None = None,
                    engine_options: Mapping[str, Any] | None = None) -> Database:
    """Create a Database from explicit settings or environment variables."""
    config = settings or DatabaseSettings.from_env(environ)
    return Database(config, engine_options=engine_options)

async def get_session(database: Database) -> AsyncIterator[AsyncSession]:
    """FastAPI-compatible async dependency factory."""
    async with database.session() as session:
        yield session

def get_database(app: Any) -> Database:
    """Read the Database instance stored in ``app.state.database``."""
    database = getattr(getattr(app, "state", None), "database", None)
    if not isinstance(database, Database):
        raise RuntimeError("app.state.database is not configured with a Database instance")
    return database
