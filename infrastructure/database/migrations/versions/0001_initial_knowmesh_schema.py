"""Initial KnowMesh multi-tenant, node, agent, knowledge, federation, trust, and job schema.

Revision ID: 0001_initial_knowmesh_schema
Revises: None
Create Date: 2026-11-11 00:00:00
"""
from __future__ import annotations

from alembic import op
from knowmesh_knowledge.models import Base

revision: str = "0001_initial_knowmesh_schema"
down_revision: str | None = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    bind = op.get_bind()
    Base.metadata.create_all(bind=bind)


def downgrade() -> None:
    bind = op.get_bind()
    Base.metadata.drop_all(bind=bind)

