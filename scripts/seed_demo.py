#!/usr/bin/env python3
"""Create small local JSON fixtures for a KnowMesh three-node demo."""
from __future__ import annotations
import argparse
import json
from pathlib import Path
import sys

DEMO = {
    "node-a": {
        "node_id":"node-a", "bundle_id":"demo-water-001", "version":1,
        "title":"Water boiling point at standard pressure",
        "claims":[{"claim_id":"claim-water-001",
                   "statement":"Pure water boils at approximately 100 °C at 1 atmosphere.",
                   "status":"proposed",
                   "evidence_ids":["evidence-water-001"]}],
        "evidence":[{"evidence_id":"evidence-water-001",
                     "source_type":"reference",
                     "description":"Replace this fixture with a verified primary source before evaluation."}]
    },
    "node-b": {
        "node_id":"node-b", "subscriptions":["demo-water-001"],
        "known_bundles":[]
    },
    "node-c": {
        "node_id":"node-c", "subscriptions":[],
        "known_bundles":[]
    }
}

def seed(output: Path, force: bool=False) -> list[Path]:
    output.mkdir(parents=True,exist_ok=True)
    written=[]
    for node_id,payload in DEMO.items():
        destination=output/f"{node_id}.json"
        if destination.exists() and not force:
            raise FileExistsError(f"{destination} exists; pass --force to overwrite")
        temporary=destination.with_suffix(destination.suffix+".tmp")
        temporary.write_text(json.dumps(payload,indent=2,sort_keys=True)+"\n",encoding="utf-8")
        temporary.replace(destination)
        written.append(destination)
    return written

def main(argv=None) -> int:
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output",type=Path,default=Path("data/demo"),
                        help="output directory (default: data/demo)")
    parser.add_argument("--force",action="store_true",help="overwrite existing fixture files")
    args=parser.parse_args(argv)
    output=args.output if args.output.is_absolute() else Path(__file__).resolve().parents[1]/args.output
    try:
        for path in seed(output,args.force): print(f"Wrote {path}")
    except FileExistsError as exc:
        print(f"ERROR: {exc}",file=sys.stderr); return 2
    return 0

if __name__=="__main__":
    raise SystemExit(main())
