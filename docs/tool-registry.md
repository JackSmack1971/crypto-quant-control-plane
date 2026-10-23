# Tool adapter registry / migration status

The tools below are available in the originating ChatGPT environment, **not verified to be usable from Codex CLI**. Each external provider must have an authorized, documented MCP endpoint or a separately implemented read-only adapter. Do not fabricate a URL, package name or compatibility.

| Capability | Candidate sources in originating environment | Intended read-only use | Migration state |
|---|---|---|---|
| Liquid market and paper context | Co-Invest / Liquid | quotes, OI, funding, cohorts, books; paper only on explicit request | NOT CONFIGURED |
| Hyperliquid / Lighter market microstructure | 0xArchive | Hyperliquid core perps and spot, HIP-3, HIP-4, Lighter mainnet and Robinhood Lighter: historical books/trades, funding, OI, liquidations, flow, exchange coverage, latency and incidents | REGISTERED_UNVERIFIED |
| Historical/quant market data | Massive | OHLCV, cross-asset history, options | REGISTERED_UNVERIFIED |
| Crypto market data | fin-data | spot/perp bars, order book, funding, OI, macro | NOT CONFIGURED |
| Identity and supply | CoinGecko, CMC, CoinPaprika | canonical IDs, contracts, supply, market context | PARTIAL: CoinGecko/CoinPaprika registered, CMC not configured |
| EVM verification | Blockscout | chains, contracts, source, read-only events | REGISTERED_UNVERIFIED |
| Research discovery | Exa; authoritative primary web | original documentation, research, published releases | NOT CONFIGURED |
| OpenAI documentation | OpenAI Docs MCP | Codex/API documentation only | REGISTERED_UNVERIFIED |

## Credential/access onboarding gate
1. Locate the vendor's official MCP server instructions and verify read-only capability/schema, transport and rate/entitlement restrictions.
2. Prefer a user-scoped credential store or environment variables; never store secret literals in project TOML, source, logs or reports.
3. Review every exposed method for writes; **do not register a finance/wallet server that exposes transactions or orders until method-level read-only restrictions are enforceable**.
4. For each candidate, run harmless metadata/identity queries first, then compare one normalized sample with an independent producer. Record upstream overlap and timestamp drift.
5. Record status as CONNECTED_VERIFIED / CONNECTED_UNVERIFIED / BLOCKED / UNAVAILABLE; only first permits evidence-grade analysis subject to data checks.

Do not assume ChatGPT app/plugin identities, sessions or entitlements transfer to Codex CLI. `codex mcp list` checks registration, not query access or permissions. Project TOML is loaded only for a trusted workspace. The current project deliberately disables sandbox network access until integrations and policies are explicitly reviewed.

## 0xArchive — current ChatGPT exposure (inventory observed 2026-10-22)

The originating environment exposes **176 `mcp__0xArchive__*` methods**; this is tool discovery, **not** a successful provider call or proof of Codex MCP connectivity. Notable research-oriented endpoints include `get_capabilities`, `get_data_quality_status`, `get_data_coverage`, `get_exchange_coverage`, `get_symbol_coverage`, `get_data_incidents`, `get_data_latency`, `get_instruments`, `get_candles`, `get_trades`, `get_orderbook`, `get_orderbook_history`, `get_funding_history`, `get_open_interest_history`, `get_liquidations`, and `get_cvd`. Corresponding `get_hip3_*`, `get_hip4_*`, `get_lighter_*`, `get_rh_lighter_*` and `get_spot_*` families are exposed for their respective product/venue scopes. Lighter L3 books and Hyperliquid L2/L4 streams require explicit depth/sequence/timestamp validation.

**Default-deny action methods:** `create_webhook_endpoint`, `test_webhook_endpoint`, `enable_webhook_endpoint`, `rotate_webhook_endpoint_secret`, `delete_webhook_endpoint`, `create_webhook_subscription`, `update_webhook_subscription`, `delete_webhook_subscription`, `dry_run_webhook_subscription`, `redeliver_webhook_delivery`, `add_webhook_watched_address`, `delete_webhook_watched_address`, `submit_feedback`. A dry run or test may still cause an external effect; do not assume safe from its name. All other methods remain blocked until reviewed individually. Account/position/order-history endpoints are **not permitted by default** even if technically read-only; use only on explicit user request and only after scope/privacy checks. Do not issue any orders, wallet operations, or transactions.

**Integration gate:** obtain 0xArchive's official Codex-compatible MCP transport/config and authorization procedure; inspect exact exposed method schemas and ensure an enforceable allowlist at the proxy/server layer, not merely a natural-language AGENTS.md rule. Then verify metadata access, coverage, retention, time units, venue and instrument identifiers, freshness and upstream independence against a second source. Record call outcomes before upgrading `REGISTERED_UNVERIFIED` status. The official endpoint is now registered in `.codex/config.toml` with a provisional research-only allowlist. OAuth, live tool schemas, plan coverage, and effective authorization still require testing.

## Project MCP integration — 2026-10-22

The canonical Codex configuration is `.codex/config.toml`, **not** Claude's `.mcp.json`, ChatGPT connectors, or the Agents API's `agent.tools` schema. Codex loads project config only when that checkout is trusted. Registration does not establish connectivity, data entitlements, or effective network authorization. `enabled_tools` is a client-side exposure restriction; it does not replace provider controls or runtime policy. For any server whose actual tools/list differs from the allowlist, halt and reconcile exact identifiers, never silently grant more tools.

| Server | Transport | Project state | Primary vendor documentation |
|---|---|---|---|
| OpenAI Docs | hosted HTTP | REGISTERED_UNVERIFIED | https://developers.openai.com/learn/docs-mcp |
| CoinGecko | hosted HTTP | REGISTERED_UNVERIFIED | https://mcp.api.coingecko.com/ |
| CoinPaprika | hosted HTTP | REGISTERED_UNVERIFIED | https://github.com/coinpaprika/coinpaprika-mcp |
| DexPaprika | hosted HTTP | REGISTERED_UNVERIFIED | https://github.com/coinpaprika/dexpaprika-mcp |
| 0xArchive | hosted HTTP OAuth | REGISTERED_UNVERIFIED; narrow initial allowlist | https://github.com/0xArchiveIO/0xarchive-mcp |
| Massive | hosted HTTP OAuth | REGISTERED_UNVERIFIED; entitlement-limited | https://massive.com/docs/ai-tools/clients/codex |
| Blockscout | hosted HTTP, optional env-header PRO credential | REGISTERED_UNVERIFIED | https://github.com/blockscout/mcp-server |
| CCXT | local stdio via npx, public-market allowlist | REGISTERED_UNVERIFIED; Node >=18 required | https://github.com/ccxt/ccxt/wiki/MCP |
| Alchemy | hosted HTTP OAuth | DISABLED_PENDING_TOOL_AUDIT | https://www.alchemy.com/docs/alchemy-mcp-server |
| Helius | local stdio via npx | DISABLED_PENDING_TOOL_AUDIT | https://github.com/helius-labs/core-ai |

**Not included:** Co-Invest/Liquid, fin-data, CMC, Exa and DexScreener: no official Codex-compatible server endpoint and research-safe scope were established during this change. ChatGPT-connected tools are not presumed portable to Codex. The previously mentioned DexScreener integrations are not assumed first-party. Add these only after primary-source confirmation of transport, provenance, and safe exposure.

### Local qualification protocol

1. Run `codex --version`, `codex mcp list` and `codex mcp get <server>` from the trusted repository. Inspect loaded project config vs user/managed overrides. If missing, verify repository trust and restart the Codex session.
2. For `oxarchive`, `massive`, and `alchemy` if enabled later, sign in individually using `codex mcp login <server>`; OAuth credentials stay outside the repo. For Blockscout PRO, set `BLOCKSCOUT_MCP_PRO_API_KEY` in the parent process environment; do not paste a key into TOML. If the env variable is absent and the header prevents free access, remove that header *locally* after confirming anonymous endpoint behavior. Do not commit credential literals.
3. Use `/mcp` and a harmless discovery call. Capture actual `tools/list`, read-only classifications, exact method schemas, version and response. Confirm each exposed operation is within the allowed policy. Disable any unexpected broad write route before use.
4. For CCXT confirm `get_safety_status`, absence of loaded accounts and trading/funds exposure. Do not pass environment credentials or enable private accounts, live trading, or write methods. This repository's `enabled_tools` is an exposure guard, not a server sandbox.
5. Record one live identity query, timestamp, provider limits, provenance, and independent comparator. Only promote a server to CONNECTED_VERIFIED after successful calls and effective policy checks. HTTP proxy and cloud egress restrictions may separately prevent access.

All `mcp_servers.*` registrations are **desired project state**. Server startup, account login, permissions, live data quality and any runtime effect remain unverified here. Official Codex MCP reference: https://developers.openai.com/codex/mcp.
