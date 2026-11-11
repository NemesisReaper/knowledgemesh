# KnowMesh repository scripts

These scripts replace the four empty files found under `knowledgemesh/scripts/` in
the supplied repository archive. They preserve those filenames.

## Commands

### Install Python dependencies
```bash
bash scripts/setup.sh
```
Creates `.venv` unless `VENV_DIR` is set, then installs the root `requirements.txt`.
Override the interpreter with `PYTHON_BIN=python3.12`.

### Start three local API processes
```bash
bash scripts/start_nodes.sh
```
Defaults to node-a/node-b/node-c on ports 8001, 8002 and 8003, bound to `127.0.0.1`.
Useful overrides:
- `KNOWMESH_HOST`
- `KNOWMESH_BASE_PORT`
- `KNOWMESH_APP_IMPORT` (defaults to `knowmesh_api.main:app`)
- `PYTHON_BIN`
- `KNOWMESH_LOG_DIR`
- `KNOWMESH_PID_DIR`

The script expects an importable ASGI `app` at the configured import path. It starts
three processes but does not provision isolated databases or node configuration.

### Run database migrations
```bash
python scripts/migrate.py
python scripts/migrate.py --check
python scripts/migrate.py head --sql
```
Requires an Alembic installation and an `alembic.ini` at the repository root or
`apps/api/alembic.ini`. The original archive contains neither an Alembic config nor
migration revisions, so migration execution is intentionally blocked until those
are added.

### Generate demo fixtures
```bash
python scripts/seed_demo.py
python scripts/seed_demo.py --output /tmp/knowmesh-demo
```
Creates local JSON fixture files for three nodes. It does not insert records into a
database or publish data to a network. The example evidence description is explicitly
a placeholder, not a verified citation. Existing files are not overwritten unless
`--force` is passed.

## Safety
- The startup script binds to localhost by default; do not expose nodes publicly without
  authentication, TLS, request limits, and network-level controls.
- The migration script invokes the Alembic executable without shell interpolation.
- The seeder writes only into the requested output directory and refuses overwrites by default.
