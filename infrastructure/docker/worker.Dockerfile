FROM python:3.11-slim

WORKDIR /workspace

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH="/workspace:/workspace/apps/api/src:/workspace/apps/worker/src"

RUN pip install --no-cache-dir \
    pydantic>=2.6.0 \
    sqlalchemy>=2.0.25 \
    cryptography>=42.0.0 \
    httpx>=0.27.0 \
    pyyaml>=6.0.1

COPY packages ./packages
COPY apps/worker ./apps/worker

CMD ["python", "-m", "knowmesh_worker.main"]

