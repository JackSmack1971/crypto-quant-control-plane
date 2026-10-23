#!/usr/bin/env python3
"""Offline evidence checks only. Does not attest Codex runtime or upstream data."""
from pathlib import Path
import json
import re
import hashlib
import tomllib

ROOT = Path(__file__).resolve().parents[1]

def validate(root=ROOT):
    paths = sorted((root / "methodologies").glob("*.md"))
    assert {p.name for p in paths} == {f"{n}-{label}-methodology.md" for n, label in [("01", "derivatives"), ("02", "spot-market-microstructure"), ("03", "factor-research"), ("04", "backtesting"), ("05", "portfolio-risk"), ("06", "source-provenance"), ("07", "onchain-intelligence"), ("08", "data-quality-validation"), ("09", "strategy-execution")]}
    assert all(p.stat().st_size > 1000 for p in paths)
    config = tomllib.loads((root / ".codex/config.toml").read_text(encoding="utf-8"))
    assert set(config) == {"approval_policy", "sandbox_mode", "sandbox_workspace_write", "agents", "mcp_servers"}, "unexpected project config keys"
    assert config["approval_policy"] == "on-request"
    assert config["sandbox_mode"] == "workspace-write"
    assert config["sandbox_workspace_write"] == {"network_access": False}
    assert config["agents"] == {"max_threads": 4, "max_depth": 1}
    assert set(config["mcp_servers"]) == {"openaiDeveloperDocs", "coingecko", "coinpaprika", "dexpaprika", "oxarchive", "massive", "blockscout", "ccxt", "alchemy", "helius"}
    assert config["mcp_servers"]["alchemy"]["enabled"] is False and config["mcp_servers"]["helius"]["enabled"] is False
    assert config["mcp_servers"]["ccxt"]["enabled_tools"] and "create_order" not in config["mcp_servers"]["ccxt"]["enabled_tools"]
    assert config["mcp_servers"]["oxarchive"]["enabled_tools"] and "create_webhook_endpoint" not in config["mcp_servers"]["oxarchive"]["enabled_tools"]
    assert config["mcp_servers"]["openaiDeveloperDocs"] == {"url": "https://developers.openai.com/mcp"}
    allowed_server_keys = {"url", "command", "args", "enabled", "enabled_tools", "env_http_headers"}
    assert all(set(server) <= allowed_server_keys for server in config["mcp_servers"].values()), "unrecognized MCP server configuration"
    agents = sorted((root / ".codex/agents").glob("*.toml"))
    assert len(agents) == 7
    names = set()
    for agent in agents:
        data = tomllib.loads(agent.read_text(encoding="utf-8"))
        assert set(data) == {"name", "description", "developer_instructions"}, agent
        assert all(isinstance(data[key], str) and data[key].strip() for key in data), agent
        assert data["name"] == agent.stem and data["name"] not in names
        names.add(data["name"])
    instructions = (root / "AGENTS.md").read_text(encoding="utf-8")
    assert len(instructions.encode()) < 32768
    assert "Never place, change, cancel" in instructions
    assert "not evidence of effective sandbox" in instructions
    skills = sorted((root / ".agents/skills").glob("*/SKILL.md"))
    assert len(skills) == 7
    expected = {"crypto-research", "market-data-provenance", "derivatives-microstructure", "factor-discovery", "backtest-validation", "portfolio-risk-review", "onchain-investigation"}
    assert {p.parent.name for p in skills} == expected
    for path in skills:
        data = path.read_text(encoding="utf-8")
        assert data.startswith("---\n") and "\n---\n" in data[4:], path
        assert re.search(r"(?m)^name: " + re.escape(path.parent.name) + r"$", data), path
        assert re.search(r"(?m)^description: .+", data), path
        assert len(data) < 12000, path
    assert (root / "docs/orchestration-contract.md").is_file()
    contract = (root / "docs/orchestration-contract.md").read_text(encoding="utf-8")
    assert "synthesis barrier" in contract and "NOT_RUN" in contract
    assert all("Do not edit files" in tomllib.loads(p.read_text())["developer_instructions"] for p in agents)
    schema = json.loads((root / "schemas/research-report.schema.json").read_text(encoding="utf-8"))
    assert schema["$schema"].endswith("2020-12/schema")
    assert schema["additionalProperties"] is False
    assert schema["properties"]["mutations"] == {"const": 0}
    assert set(schema["required"]) <= set(schema["properties"])
    assert (root / "artifacts/VVV-quant-analysis-original.txt").stat().st_size > 1000
    assert (root / "docs/control-plane-audit.md").stat().st_size > 1000
    assert "REGISTERED_UNVERIFIED" in (root / "docs/tool-registry.md").read_text(encoding="utf-8")
    from research_manifest import build_manifest
    manifest = build_manifest(root)
    assert len(manifest["files"]) >= 25 and len({f["path"] for f in manifest["files"]}) == len(manifest["files"])
    return manifest

if __name__ == "__main__":
    result = validate()
    print(f"PASS: offline scaffold, policy invariants, agent schemas, and {len(result['files'])} manifest inputs")
    print("UNVERIFIED: live Codex config/trust, MCP authorization, network, market data and telemetry")
