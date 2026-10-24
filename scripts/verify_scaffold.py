#!/usr/bin/env python3
"""Offline evidence checks only. Does not attest Codex runtime or upstream data."""
from pathlib import Path
import json
import re
import hashlib
import tomllib

ROOT = Path(__file__).resolve().parents[1]

# Names that must not appear in any enabled_tools list. Webhook and feedback matches
# are also rejected by substring so a newly spelled variant fails closed.
FORBIDDEN_ENABLED_TOOLS = {
    "create_order", "edit_order", "cancel_order", "cancel_all_orders",
    "set_leverage", "set_margin_mode", "call_write_method", "call_implicit_write",
    "withdraw", "transfer", "get_deposit_address",
    "get_balance", "get_orders", "get_my_trades", "get_positions", "list_accounts",
    "direct_api_call",
    "heliusWrite", "heliusStreaming", "heliusAccount",
    "get_account_positions", "get_account_positions_history", "get_account_position_changes",
    "get_market_positions", "get_market_positions_summary", "get_lighter_accounts",
    "submitFeedback", "submit_feedback",
}

def assert_mcp_tool_policy(config):
    for name, server in config["mcp_servers"].items():
        args = server.get("args") or []
        assert all("@latest" not in str(arg) for arg in args), name
        if server.get("command") == "npx":
            packages = [arg for arg in args if isinstance(arg, str) and not arg.startswith("-")]
            assert packages, name
            for package in packages:
                assert "@" in package and not package.endswith("@latest"), package
                version = package.rsplit("@", 1)[1]
                assert version and version[0].isdigit(), package
        for tool in server.get("enabled_tools") or []:
            lowered = tool.lower()
            assert "webhook" not in lowered and "feedback" not in lowered, (name, tool)
            assert tool not in FORBIDDEN_ENABLED_TOOLS, (name, tool)

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
    assert_mcp_tool_policy(config)
    ccxt = config["mcp_servers"]["ccxt"]
    assert ccxt["args"] == ["-y", "ccxt-mcp@0.1.3"]
    assert ccxt["env"] == {"CCXT_MCP_CONFIG": ".codex/ccxt-mcp.config.json"}
    assert ccxt["enabled_tools"] == ["list_exchanges", "describe_exchange", "describe_method", "search_markets", "get_tickers", "get_orderbook", "get_ohlcv", "get_trades", "search_events", "get_safety_status"]
    assert "create_order" in ccxt["disabled_tools"] and "withdraw" in ccxt["disabled_tools"]
    ccxt_file = json.loads((root / ".codex/ccxt-mcp.config.json").read_text(encoding="utf-8"))
    assert ccxt_file["accounts"] == {}
    assert ccxt_file["settings"]["hideDisabledTools"] is True and ccxt_file["settings"]["loadEnvKeys"] is False
    ox = config["mcp_servers"]["oxarchive"]
    assert ox["scopes"] == ["mcp:market.read"]
    assert ox["enabled_tools"] == ["get_summary", "get_candles", "get_funding_current", "get_lighter_funding_current", "get_hip3_summary", "get_hip4_outcomes", "get_data_incidents", "get_symbol_coverage"]
    assert "get_account_positions" in ox["disabled_tools"] and "get_data_coverage" not in ox["enabled_tools"]
    helius = config["mcp_servers"]["helius"]
    assert helius["args"] == ["-y", "helius-mcp@2.3.0"]
    assert set(helius["disabled_tools"]) >= {"heliusWrite", "heliusStreaming", "heliusAccount"}
    blockscout = config["mcp_servers"]["blockscout"]
    assert "direct_api_call" not in blockscout["enabled_tools"] and "direct_api_call" in blockscout["disabled_tools"]
    assert "__unlock_blockchain_analysis__" in blockscout["enabled_tools"]
    coingecko = config["mcp_servers"]["coingecko"]
    assert coingecko["enabled_tools"] == ["execute", "search_docs"]
    assert coingecko["default_tools_approval_mode"] == "prompt"
    assert coingecko["tools"]["execute"]["approval_mode"] == "approve"
    assert "submitFeedback" not in config["mcp_servers"]["coinpaprika"]["enabled_tools"]
    assert "submitFeedback" in config["mcp_servers"]["coinpaprika"]["disabled_tools"]
    assert "submitFeedback" not in config["mcp_servers"]["dexpaprika"]["enabled_tools"]
    docs = config["mcp_servers"]["openaiDeveloperDocs"]
    assert docs["url"] == "https://developers.openai.com/mcp"
    assert docs["enabled_tools"] == ["search_openai_docs", "list_openai_docs", "fetch_openai_doc", "list_api_endpoints", "get_openapi_spec"]
    allowed_server_keys = {"url", "command", "args", "enabled", "enabled_tools", "disabled_tools", "env", "env_http_headers", "scopes", "default_tools_approval_mode", "tools"}
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
    registry = (root / "docs/tool-registry.md").read_text(encoding="utf-8")
    assert "REGISTERED_UNVERIFIED" in registry and "RESPONDS_NO_AUTH" in registry and "NEEDS_AUTH" in registry
    assert "DOCS_DERIVED_UNVERIFIED" in registry and "mcp:market.read" in registry
    probe = (root / "docs/mcp-probe-2026-10-23.md").read_text(encoding="utf-8")
    assert "hideDisabledTools" in probe and "10/08/2026" in probe and "CONNECTED_VERIFIED" in probe
    from research_manifest import build_manifest
    manifest = build_manifest(root)
    assert len(manifest["files"]) >= 25 and len({f["path"] for f in manifest["files"]}) == len(manifest["files"])
    return manifest

if __name__ == "__main__":
    result = validate()
    print(f"PASS: offline scaffold, policy invariants, agent schemas, and {len(result['files'])} manifest inputs")
    print("UNVERIFIED: live Codex config/trust, MCP authorization, network, market data and telemetry")
