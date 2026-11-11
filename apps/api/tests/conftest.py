"""Test configuration for KnowMesh API tests."""

from __future__ import annotations

import importlib.util
from pathlib import Path

_root = Path(__file__).resolve().parents[3] / "conftest.py"
if _root.exists():
    spec = importlib.util.spec_from_file_location("_knowmesh_root_conftest", _root)
    if spec and spec.loader:
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
