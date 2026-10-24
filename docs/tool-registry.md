# Tool adapter registry / migration status

The tools below are available in the originating ChatGPT environment, **not verified to be usable from Codex CLI**. Each external provider must have an authorized, documented MCP endpoint or a separately implemented read-only adapter. Do not fabricate a URL, package name or compatibility.

Probe vocabulary used below, from the 2026-10-23 external read-only probe in `docs/mcp-probe-2026-10-23.md`. None of these are `CONNECTED_VERIFIED`. Codex was not the client.

| Status | Meaning |
|---|---|
| `REGISTERED_UNVERIFIED` | Desired project registration before a live tool list. Kept as the pre-probe label. |
| `RESPONDS_NO_AUTH` | Unauthenticated initialize and a harmless read succeeded on 2026-10-23 from the probe client. |
| `NEEDS_AUTH` | The endpoint returned HTTP 401. `tools/list` was not obtained. |
| `DOCS_DERIVED_UNVERIFIED` | Allowlist names come from vendor docs, not from `tools/list`. |
| `DISABLED_PENDING_TOOL_AUDIT` | `enabled = false` until a tool-scope audit. |
| `DISABLED_PROBED` | Still disabled; the probe inspected startup or an auth challenge only. |
| `NOT CONFIGURED` | No project MCP entry. |

`CONNECTED_VERIFIED` remains the only status that would permit evidence-grade use, and only after Codex itself completes the qualification protocol below. This probe does not grant it.

| Capability | Candidate sources in originating environment | Intended read-only use | Migration state |
|---|---|---|---|
| Liquid market and paper context | Co-Invest / Liquid | quotes, OI, funding, cohorts, books; paper only on explicit request | NOT CONFIGURED |
| Hyperliquid / Lighter market microstructure | 0xArchive | Hyperliquid core perps and spot, HIP-3, HIP-4, Lighter mainnet and Robinhood Lighter: historical books/trades, funding, OI, liquidations, flow, exchange coverage, latency and incidents | NEEDS_AUTH; allowlist DOCS_DERIVED_UNVERIFIED (2026-10-23) |
| Historical/quant market data | Massive | OHLCV, cross-asset history, options | NEEDS_AUTH (2026-10-23); tools not listed |
| Crypto market data | fin-data | spot/perp bars, order book, funding, OI, macro | NOT CONFIGURED |
| Identity and supply | CoinGecko, CMC, CoinPaprika | canonical IDs, contracts, supply, market context | PARTIAL: CoinGecko and CoinPaprika RESPONDS_NO_AUTH on 2026-10-23; CMC not configured |
| EVM verification | Blockscout | chains, contracts, source, read-only events | RESPONDS_NO_AUTH (2026-10-23); PRO key notice not yet enforced that day |
| Research discovery | Exa; authoritative primary web | original documentation, research, published releases | NOT CONFIGURED |
| OpenAI documentation | OpenAI Docs MCP | Codex/API documentation only | RESPONDS_NO_AUTH (2026-10-23) |

## Credential/access onboarding gate
1. Locate the vendor's official MCP server instructions and verify read-only capability/schema, transport and rate/entitlement restrictions.
2. Prefer a user-scoped credential store or environment variables; never store secret literals in project TOML, source, logs or reports.
3. Review every exposed method for writes; **do not register a finance/wallet server that exposes transactions or orders until method-level read-only restrictions are enforceable**.
4. For each candidate, run harmless metadata/identity queries first, then compare one normalized sample with an independent producer. Record upstream overlap and timestamp drift.
5. Record status as CONNECTED_VERIFIED / CONNECTED_UNVERIFIED / BLOCKED / UNAVAILABLE; only first permits evidence-grade analysis subject to data checks. `RESPONDS_NO_AUTH` and `NEEDS_AUTH` are probe observations, not those four live-Codex statuses.

Do not assume ChatGPT app/plugin identities, sessions or entitlements transfer to Codex CLI. `codex mcp list` checks registration, not query access or permissions. Project TOML is loaded only for a trusted workspace. The current project deliberately disables sandbox network access until integrations and policies are explicitly reviewed.

A generic HTTP User-Agent (`Python-urllib`) drew Cloudflare 403 error 1010 from CoinGecko, CoinPaprika, DexPaprika, Blockscout, and Alchemy on 2026-10-23. A custom User-Agent received normal responses. Codex's client was not part of that test, and this repo does not set a User-Agent header as a stand-in.

## 0xArchive — current ChatGPT exposure (inventory observed 2026-10-22)

The originating environment exposes **176 `mcp__0xArchive__*` methods**; this is tool discovery, **not** a successful provider call or proof of Codex MCP connectivity. Notable research-oriented endpoints include `get_capabilities`, `get_data_quality_status`, `get_data_coverage`, `get_exchange_coverage`, `get_symbol_coverage`, `get_data_incidents`, `get_data_latency`, `get_instruments`, `get_candles`, `get_trades`, `get_orderbook`, `get_orderbook_history`, `get_funding_history`, `get_open_interest_history`, `get_liquidations`, and `get_cvd`. Corresponding `get_hip3_*`, `get_hip4_*`, `get_lighter_*`, `get_rh_lighter_*` and `get_spot_*` families are exposed for their respective product/venue scopes. Lighter L3 books and Hyperliquid L2/L4 streams require explicit depth/sequence/timestamp validation.

Those ChatGPT names are not the hosted MCP allowlist. On 2026-10-23, `https://mcp.0xarchive.io/mcp` returned HTTP 401 before `tools/list`. The hosted page `https://docs.0xarchive.io/mcp-server` says a tool name guessed from a REST route will fail, and its examples use `get_symbol_coverage` and `get_data_incidents` rather than `get_data_coverage`. Of the previous 10 `enabled_tools` names, that page states `get_candles`. The others are unverified against the hosted server.

**Default-deny action methods** in the ChatGPT inventory: `create_webhook_endpoint`, `test_webhook_endpoint`, `enable_webhook_endpoint`, `rotate_webhook_endpoint_secret`, `delete_webhook_endpoint`, `create_webhook_subscription`, `update_webhook_subscription`, `delete_webhook_subscription`, `dry_run_webhook_subscription`, `redeliver_webhook_delivery`, `add_webhook_watched_address`, `delete_webhook_watched_address`, `submit_feedback`. A dry run or test may still cause an external effect; do not assume safe from its name. Account/position/order-history endpoints are **not permitted by default** even if technically read-only. Do not issue any orders, wallet operations, or transactions.

**Integration gate:** The hosted endpoint is registered in `.codex/config.toml`. Its `enabled_tools` list is `DOCS_DERIVED_UNVERIFIED`: `get_summary`, `get_candles`, `get_funding_current`, `get_lighter_funding_current`, `get_hip3_summary`, `get_hip4_outcomes`, `get_data_incidents`, `get_symbol_coverage`. Documented account and position tools (`get_account_positions`, `get_account_positions_history`, `get_account_position_changes`, `get_market_positions`, `get_market_positions_summary`, `get_lighter_accounts`) are on `disabled_tools`. Protected-resource metadata advertises `mcp:market.read`, `mcp:webhooks.read`, `mcp:webhooks.write`, and `mcp:feedback.write`. Config requests only `mcp:market.read` via the documented `scopes` key. Decline webhook and feedback scopes on the consent screen. That scope request was not exercised in Codex. Replace the allowlist only from an authenticated `tools/list`, then verify coverage, time units, venue identifiers, and an independent comparator before any status above `NEEDS_AUTH`.

## Project MCP integration — updated 2026-10-23

The canonical Codex configuration is `.codex/config.toml`, **not** Claude's `.mcp.json`, ChatGPT connectors, or the Agents API's `agent.tools` schema. Codex loads project config only when that checkout is trusted. Registration does not establish connectivity, data entitlements, or effective network authorization. `enabled_tools` is a client-side exposure restriction; `disabled_tools` is applied after it. Neither replaces provider controls. For any server whose actual `tools/list` differs from the allowlist, halt and reconcile exact identifiers.

| Server | Transport | Project state | Primary vendor documentation |
|---|---|---|---|
| OpenAI Docs | hosted HTTP | RESPONDS_NO_AUTH 2026-10-23; five probed read tools allowlisted | https://developers.openai.com/learn/docs-mcp |
| CoinGecko | hosted HTTP | RESPONDS_NO_AUTH 2026-10-23; `execute` and `search_docs` only. `execute` runs arbitrary JS. `intent` is vendor-logged: do not put secrets or sensitive context in it. `approval_mode = approve` on `execute`; server default is `prompt` | https://mcp.api.coingecko.com/ |
| CoinPaprika | hosted HTTP | RESPONDS_NO_AUTH 2026-10-23; allowlist excludes `submitFeedback`. `rationale` is required and the server logs it. Do not put PII, secrets, or sensitive context in `rationale` | https://github.com/coinpaprika/coinpaprika-mcp |
| DexPaprika | hosted HTTP | RESPONDS_NO_AUTH 2026-10-23; same `submitFeedback` exclusion and `rationale` logging rule | https://github.com/coinpaprika/dexpaprika-mcp |
| 0xArchive | hosted HTTP OAuth | NEEDS_AUTH 2026-10-23; allowlist DOCS_DERIVED_UNVERIFIED; request `mcp:market.read` only | https://github.com/0xArchiveIO/0xarchive-mcp and https://docs.0xarchive.io/mcp-server |
| Massive | hosted HTTP OAuth | NEEDS_AUTH 2026-10-23. Metadata scopes `openid`, `offline_access`, `account`. No scope list is configured until tools and the `account` scope are reviewed | https://massive.com/docs/ai-tools/clients/codex |
| Blockscout | hosted HTTP, optional env-header PRO credential | RESPONDS_NO_AUTH 2026-10-23. Unlock text says a PRO API key is required for all requests starting 10/08/2026; keyless calls still worked on 2026-10-23. `direct_api_call` (POST passthrough) is disabled. Keep `BLOCKSCOUT_MCP_PRO_API_KEY` in the environment only | https://github.com/blockscout/mcp-server |
| CCXT | local stdio via npx | RESPONDS_NO_AUTH 2026-10-23 as `ccxt-mcp@0.1.3` (ccxt 4.5.89). Node >= 18 per upstream docs. `enabled_tools` is the client guard (10 market tools the probe confirmed). The server listed 22 more tools, including `create_order`, `edit_order`, `cancel_order`, `cancel_all_orders`, `set_leverage`, `set_margin_mode`, `call_write_method`, `call_implicit_write`, `withdraw`, `transfer`, and balance/position/order tools. With no accounts those tiers were off (`trading`/`funds`/`implicitWrites` false) while `hideDisabledTools` was false, so the tools were visible. `.codex/ccxt-mcp.config.json` sets `hideDisabledTools` true, `loadEnvKeys` false, and no accounts, and `CCXT_MCP_CONFIG` points at it. That file was not re-probed. Do not export exchange keys or `CCXT_MCP_LOAD_ENV_KEYS` into the Codex process | https://docs.ccxt.com/docs/mcp |
| Alchemy | hosted HTTP OAuth | DISABLED_PENDING_TOOL_AUDIT and DISABLED_PROBED. HTTP 401 on 2026-10-23; no tool list | https://www.alchemy.com/docs/alchemy-mcp-server |
| Helius | local stdio via npx | DISABLED_PENDING_TOOL_AUDIT and DISABLED_PROBED. Pinned to `helius-mcp@2.3.0` (the build `@latest` installed on 2026-10-23). A dependency (`commander@15`) requires Node >= 22.12; the probe host was v20.19.2 and npm reported `EBADENGINE` plus peer-dependency warnings, then still listed tools. Denied families: `heliusWrite` (SOL/token transfer and staking), `heliusStreaming` (webhook create/update/delete), `heliusAccount` (signup, API keys, billing). `heliusChain` includes `simulateTransaction` and stays unreachable while the server is disabled | https://github.com/helius-labs/core-ai |

**Not included:** Co-Invest/Liquid, fin-data, CMC, Exa and DexScreener: no official Codex-compatible server endpoint and research-safe scope were established. ChatGPT-connected tools are not presumed portable to Codex.

### Local qualification protocol

1. Run `codex --version`, `codex mcp list` and `codex mcp get <server>` from the trusted repository. Inspect loaded project config vs user/managed overrides. If missing, verify repository trust and restart the Codex session. Start Codex from the repository root so the relative `CCXT_MCP_CONFIG` path can resolve; that cwd behavior is unverified.
2. For `oxarchive` and `massive`, and for `alchemy` only after a later enablement decision, sign in with `codex mcp login <server>`. For 0xArchive, request `mcp:market.read` and decline `mcp:webhooks.write`, `mcp:webhooks.read`, and `mcp:feedback.write`. OAuth credentials stay outside the repo. For Blockscout PRO, set `BLOCKSCOUT_MCP_PRO_API_KEY` in the parent process environment when the announced key requirement is actually enforced; do not paste a key into TOML.
3. Use `/mcp` and a harmless discovery call. Capture actual `tools/list`, read-only classifications, exact method schemas, version and response. Confirm each exposed operation is within the allowed policy. Disable any unexpected broad write route before use. Reconcile the 0xArchive docs-derived names before calling them.
4. For CCXT confirm `get_safety_status`, absence of loaded accounts, and trading/funds/implicitWrites off. Confirm whether `hideDisabledTools: true` removed the disabled tiers from `tools/list`. `enabled_tools` remains the client-side guard either way. Do not pass exchange credentials or enable private accounts, live trading, or write methods. The 2026-10-23 probe saw Binance HTTP 451 from its host and a Kraken public ticker; treat geo-blocks as host facts, not as a config success.
5. For CoinGecko, treat `execute` as a code-execution surface even when a call is a public quote. Keep sensitive context out of `intent`. For CoinPaprika and DexPaprika, keep sensitive context out of `rationale`.
6. Record one live identity query, timestamp, provider limits, provenance, and independent comparator. Only promote a server to CONNECTED_VERIFIED after successful Codex calls and effective policy checks. HTTP proxy and cloud egress restrictions may separately prevent access.

All `mcp_servers.*` registrations are **desired project state** plus the 2026-10-23 probe notes above. Server startup inside Codex, account login, permissions, live data quality and any runtime effect of this config remain unverified here. Official Codex MCP reference: https://developers.openai.com/codex/mcp. Config keys used for the new restrictions are the documented `enabled_tools`, `disabled_tools`, `scopes`, `env`, `default_tools_approval_mode`, and `tools.<tool>.approval_mode` entries.
