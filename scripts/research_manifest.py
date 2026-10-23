#!/usr/bin/env python3
"""Deterministic local SHA-256 manifest of a research scaffold; never contacts providers."""
import argparse
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INCLUDED = ["AGENTS.md", ".codex/config.toml", ".codex/ccxt-mcp.config.json", "docs/tool-registry.md", "docs/mcp-probe-2026-10-23.md", "schemas/research-report.schema.json"]
DIRECTORIES = [".codex/agents", ".agents/skills", "methodologies", "artifacts"]

def build_manifest(root=ROOT):
    paths = [root / item for item in INCLUDED]
    for item in DIRECTORIES:
        paths.extend(p for p in (root / item).rglob("*") if p.is_file() and not p.is_symlink())
    paths = sorted(set(paths))
    result = []
    for path in paths:
        if not path.is_file() or path.is_symlink() or not path.resolve().is_relative_to(root.resolve()):
            raise ValueError(f"unsafe or missing input: {path}")
        data = path.read_bytes()
        result.append({"path": path.relative_to(root).as_posix(), "bytes": len(data), "sha256": hashlib.sha256(data).hexdigest()})
    return {"schema_version": 1, "kind": "local-research-input-manifest", "files": result, "scope_limit": "does not attest effective policy, provider data, or runtime calls"}

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, help="optional JSON output path outside the tracked input files")
    args = parser.parse_args()
    serialized = json.dumps(build_manifest(), indent=2, sort_keys=True) + "\n"
    if args.output:
        path = args.output.resolve()
        if path.is_relative_to(ROOT.resolve()):
            raise SystemExit("Output must be outside the input scaffold to avoid mixing audit artifacts with source")
        path.write_text(serialized, encoding="utf-8")
    else:
        print(serialized, end="")
