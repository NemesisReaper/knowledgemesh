# KnowMesh Knowledge Models

SQLAlchemy 2.x persistence models for KnowMesh. Uses SQLAlchemy's portable `Uuid` and `JSON` types so metadata can be created on SQLite for development and PostgreSQL for deployment.

## Install

```bash
pip install -e ./packages/knowledge
```

## Create a development schema

```python
from sqlalchemy import create_engine
from knowmesh_knowledge.models import Base

engine = create_engine("sqlite:///knowmesh.db")
Base.metadata.create_all(engine)
```

For production, use Alembic migrations rather than `create_all`.
