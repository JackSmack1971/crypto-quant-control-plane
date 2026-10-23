# Crypto Quant Analyst — Codex CLI control plane

Portable **project scaffold**, not a verified deployment. Converts the project authority and nine domain methodologies and the archived research artifact into a Codex repository structure. The nine domain methodologies are copied verbatim under `methodologies/`; the prior VVV report is retained unchanged as an archival artifact.

## Structure
- `AGENTS.md`: project operating contract and mandatory research gates.
- `.codex/config.toml`: cautious project-level Codex defaults; trusted projects only.
- `.codex/agents/`: seven optional delegated research/verification roles.
- `.agents/skills/`: seven focused skills with separate triggers for coordination, provenance, microstructure, factors, backtesting, risk and on-chain research.
- `methodologies/`: canonical methodologies, unchanged from supplied input.
- `docs/tool-registry.md`: integration inventory and permission gates.
- `schemas/`: machine-readable research-report minimum schema.
- `artifacts/`: preserved VVV report, not live evidence.
- `scripts/verify_scaffold.py`: offline policy/structure checks, with negative-case regression tests in `tests/`.
- `scripts/research_manifest.py`: deterministic local input hashes; not a runtime policy snapshot.
- `docs/control-plane-audit.md`: 12-axis findings, remediations and unresolved acceptance gates.

## Onboarding
1. Unzip into a **new repository** (do not overwrite an existing repository's `AGENTS.md` or `.codex/`). Review it before `git init` or committing.
2. Check installed Codex CLI version with `codex --version` and read official Codex documentation for your version.
3. From the repo root, run `python3 scripts/verify_scaffold.py` and `python3 -m unittest discover -s tests -v`. Review `git status --short` after initialization.
4. Start `codex` from the repository root. Trust the project only if you have reviewed its instructions and MCP config. Inspect `/mcp` or `codex mcp list`.
5. Review sandbox network policy before any external read-only integration. Do **not** turn on network and register financial MCP servers without method-level no-write enforcement.
6. Establish vendor-specific MCP endpoints and auth *outside versioned files*, following `docs/tool-registry.md` (including the 0xArchive Hyperliquid/Lighter inventory and denylisted management methods). Independently test source semantics and capability limitations.
7. Run a constrained first task: asset identity and two independent read-only quotes, return INCONCLUSIVE on failed coverage; then a historical PIT test; then a paper-only analytical report.

## Important boundaries
This project cannot automatically import ChatGPT app credentials, server-side tools or conversation memory; neither agent metadata nor a tool name proves compatibility. Only OpenAI documentation MCP is configured, and connectivity has not been exercised. No trading or wallet transactions are allowed. Network access is off in the default workspace sandbox. A human must manage tool onboarding and trust.

## Audit status
See `docs/control-plane-audit.md` (2026-10-22). The documented legacy `workspace-write` sandbox remains network-off; any higher-level Codex policy or host environment must be checked separately. The nine supplied methodologies and prior VVV artifact are preserved verbatim. The archive contains no active market-data MCP registrations or credentials.

## Coordination and workflow selection
The primary routes to the smallest relevant skill; specialists receive bounded, read-only tasks under `docs/orchestration-contract.md`. Dispatch and handoffs are behavioral conventions, not a newly implemented runtime orchestration service. No user-account or trading capability is conferred by installing the scaffold.

## Verification scope
The offline validator inventories all nine methodologies and seven skills/agents; it does not prove the installed Codex CLI interprets custom agents, loads skills, honors policy or connects to MCP providers.

## Project-scoped MCP servers

Official-source Codex MCP registrations are in `.codex/config.toml`. Review `docs/tool-registry.md` before onboarding OAuth/credentials or enabling disabled servers. These configurations do not inherit ChatGPT connector auth, do not grant trading privileges, and have **not** been tested live in Codex. On trusted local checkouts use `codex mcp list` and `/mcp` to verify each server; project-local changes may require a new session.
