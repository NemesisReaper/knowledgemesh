FROM python:3.11-slim

WORKDIR /workspace

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH="/workspace:/workspace/apps/api/src:/workspace/apps/worker/src"

RUN pip install --no-cache-dir \
    fastapi>=0.110.0 \
    uvicorn[standard]>=0.27.0 \
    pydantic>=2.6.0 \
    sqlalchemy>=2.0.25 \
    alembic>=1.13.0 \
    cryptography>=42.0.0 \
    httpx>=0.27.0 \
    pyyaml>=6.0.1

COPY packages ./packages
COPY apps/api ./apps/api
COPY nodes ./nodes
COPY alembic.ini ./alembic.ini
COPY infrastructure ./infrastructure

EXPOSE 8000

CMD ["uvicorn", "knowmesh_api.main:app", "--host", "0.0.0.0", "--port", "8000"]

