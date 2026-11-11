#!/usr/bin/env python3
"""Run Alembic migrations from a repository with an explicit Alembic config."""
from __future__ import annotations
import argparse
import os
from pathlib import Path
import shutil
import subprocess
import sys

def find_config(root: Path, explicit: str | None = None) -> Path:
    if explicit:
        path=(root / explicit).resolve() if not Path(explicit).is_absolute() else Path(explicit)
        if not path.is_file(): raise FileNotFoundError(f"Alembic config not found: {path}")
        return path
    candidates=(root/"alembic.ini",root/"apps"/"api"/"alembic.ini")
    for candidate in candidates:
        if candidate.is_file(): return candidate
    raise FileNotFoundError(
        "No alembic.ini found. Add an Alembic environment and migration revisions before running migrations."
    )

def main(argv=None) -> int:
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("revision",nargs="?",default="head",help="Alembic target revision (default: head)")
    parser.add_argument("--config",help="Alembic config path, relative to repository root or absolute")
    parser.add_argument("--sql",action="store_true",help="Emit SQL instead of applying migrations")
    parser.add_argument("--check",action="store_true",help="Check configuration and Alembic availability only")
    args=parser.parse_args(argv)
    root=Path(__file__).resolve().parents[1]
    try:
        config=find_config(root,args.config)
    except FileNotFoundError as exc:
        print(f"ERROR: {exc}",file=sys.stderr); return 2
    alembic=shutil.which("alembic")
    if not alembic:
        print("ERROR: Alembic CLI not found. Install requirements.txt in the active environment.",file=sys.stderr)
        return 2
    if args.check:
        print(f"Alembic config: {config}")
        print(f"Alembic executable: {alembic}")
        return 0
    command=[alembic,"-c",str(config),"upgrade",args.revision]
    if args.sql: command.append("--sql")
    env=os.environ.copy()
    result=subprocess.run(command,cwd=str(root),env=env,check=False)
    return result.returncode

if __name__=="__main__":
    raise SystemExit(main())
