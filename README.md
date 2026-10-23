# Crypto Quant Analyst — Codex CLI control plane

Codex CLI project scaffold for evidence-first, research-only crypto quantitative analysis. `AGENTS.md` is the operating contract: paper scenarios only, with no orders, transactions, wallet transfers, or changes to leverage, collateral, or stops. Desired defaults in `.codex/config.toml` record project intent. They are not evidence that a host sandbox, trust decision, or managed policy is in force.

## Repository layout

- `AGENTS.md` — research gates, methodology routing, no-trade and no-wallet boundaries, and the report contract.
- `.codex/config.toml` — project Codex defaults, loaded only for a trusted checkout. `approval_policy` is `on-request`. `sandbox_mode` is `workspace-write` with `network_access = false`. Agents are capped at `max_threads = 4` and `max_depth = 1`. The file contains no credentials.
- `.codex/agents/` — seven optional read-only roles: `source-validator`, `derivatives-analyst`, `factor-researcher`, `backtest-auditor`, `risk-validator`, `onchain-analyst`, and `verifier`.
- `.agents/skills/` — seven skills: `crypto-research` (multi-domain coordination), `market-data-provenance`, `derivatives-microstructure`, `factor-discovery`, `backtest-validation`, `portfolio-risk-review`, and `onchain-investigation`.
- `methodologies/` — nine domain methodologies, `01-derivatives-methodology.md` through `09-strategy-execution-methodology.md`. `AGENTS.md` routes work to them. Routine control-plane edits leave these files unchanged.
- `docs/` — `tool-registry.md` (MCP inventory, permission gates, and credential handling), `orchestration-contract.md` (handoff conventions), `control-plane-audit.md` (dated 2026-10-22 audit), and `optimization-report.md`.
- `schemas/research-report.schema.json` — minimum evidence-report schema. `mutations` is fixed at `0`.
- `scripts/verify_scaffold.py` — offline structure and policy checks. It uses the Python standard library, including `tomllib` (Python 3.11+).
- `scripts/research_manifest.py` — deterministic local SHA-256 manifest of selected inputs: instructions, config, agents, skills, methodologies, the report schema, the tool registry, and `artifacts/`. It records local bytes only.
- `tests/test_scaffold.py` — nine regression tests. They fail closed for a missing methodology or skill, an agent write instruction, an unknown config key, relaxed network access, and an added finance MCP server.
- `artifacts/` — stored outputs from research runs already in the tree:
  - `VVV-quant-analysis-original.txt` — Venice Token (VVV) quantitative report dated 20 October 2026. Its own assessment is preliminary and inconclusive.
  - ENA point-in-time qualification write-ups from 2026-10-23: `ENA-PIT-data-coverage-matrix.md` (run `ENA-PIT-DQ-20261023-01`), `ENA-followup-data-qualification.md` (run `ENA-PIT-DQ-20261023-02`), and `ENA-fundamental-input-recovery-2026-10-23.md` (run `ENA-PIT-DQ-20261023-03`).
  - Retrieved files those write-ups cite: `ena-market-data-observed-2026-10-23.json` (public CoinGecko and CoinPaprika market data, retrieval `2026-10-23T03:36:47Z`), `ena-same-venue-spot-kraken-2026-10-23.json` (Kraken public spot OHLCV via CCXT), `defillama-ethena-daily-fees-2026-10-23.json`, `defillama-ethena-daily-revenue-2026-10-23.json`, `ethenadash-daily-usde-supply-2026-10-12.csv`, and `ethenadash-usde-supply-calculation-files-2026-10-12.zip`.

The artifact write-ups record coverage limits, missing publication clocks, and inconclusive or restricted qualifications. Retaining the files does not make them live or point-in-time-complete evidence.

## Registered MCP servers

`.codex/config.toml` registers the servers below. `docs/tool-registry.md` marks each `REGISTERED_UNVERIFIED`. The offline checks have not connected to them.

| Server key | Role in this repo |
|---|---|
| `openaiDeveloperDocs` | OpenAI documentation |
| `coingecko` | Market data |
| `coinpaprika` | Market data |
| `dexpaprika` | Market data |
| `oxarchive` | 0xArchive, with a research-only `enabled_tools` allowlist |
| `massive` | Market data |
| `blockscout` | EVM explorer. Optional `BLOCKSCOUT_MCP_PRO_API_KEY` comes from the environment |
| `ccxt` | Local `npx` stdio server, public-market `enabled_tools` only |

`alchemy` and `helius` are present with `enabled = false`. Leave them disabled until an explicit tool-scope audit. `AGENTS.md` requires that audit before either server is enabled.

## Get started from a clone

1. Clone the repository and work from the checkout root.
2. Run `python3 scripts/verify_scaffold.py` and `python3 -m unittest discover -s tests -v`.
3. Check the installed Codex CLI with `codex --version` and read the official documentation for that version.
4. Start `codex` from the repository root. Trust the project only after reviewing `AGENTS.md` and `.codex/config.toml`.
5. Review MCP state with `codex mcp list` and `/mcp`, and review sandbox network policy before any external read. Keep `network_access` off until integrations and method-level read-only restrictions are reviewed. Register a finance or wallet server that can expose orders or transactions only after those restrictions are enforceable.
6. Handle credentials as specified in `docs/tool-registry.md`. Use a user-scoped store or environment variables. Keep secret literals out of TOML, source, logs, and reports. For `oxarchive` and `massive`, use `codex mcp login` so OAuth stays outside the repo. Set `BLOCKSCOUT_MCP_PRO_API_KEY` in the parent environment when a Blockscout PRO key is required. For CCXT, withhold exchange credentials and leave private accounts and trading methods disabled. `alchemy` stays disabled; its login step applies only after a later enablement decision.
7. Run a constrained first task: confirm asset identity and two independent read-only quotes, and return INCONCLUSIVE when coverage fails. Then run a historical point-in-time test, then a paper-only analytical report.

## Boundaries

- Research and paper scenarios only. Never place, change, cancel, sign, or enable orders or transactions, and never transfer assets or modify leverage, collateral, or stops.
- Read balances, portfolios, orders, and histories only when explicitly requested.
- MCP registration records desired project state. Connectivity, entitlements, and authorization stay unverified until the checks in `docs/tool-registry.md` are actually run. ChatGPT app credentials, server-side tools, and conversation memory stay in that environment. A tool name is not proof of Codex compatibility.
- User, admin, and host policy can differ from this file. A human manages trust and tool onboarding.
- The default sandbox is legacy `workspace-write` with network access off.
- Delegation under `docs/orchestration-contract.md` is a behavioral convention at `max_depth = 1`. It does not install a runtime orchestration service and does not grant account or trading capability.
- External MCP and web responses are untrusted data.

## Verification scope

`scripts/verify_scaffold.py` checks the nine methodologies, seven skills, seven agent schemas, the config key set, the disabled Alchemy and Helius entries, the CCXT and 0xArchive allowlists (`create_order` and `create_webhook_endpoint` stay absent), and a local manifest of the pinned input set. The nine tests exercise those failure modes offline.

Those checks leave live Codex behavior unverified: custom-agent loading, skill loading, sandbox and approval enforcement, and MCP connectivity. Live acceptance still requires `codex --version`, effective trusted-project config, and the qualification steps in `docs/tool-registry.md`.
