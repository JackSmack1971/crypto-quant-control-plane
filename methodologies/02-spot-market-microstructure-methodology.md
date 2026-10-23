# 02-spot-market-microstructure-methodology.md

**Title:** Digital-Currency Spot Market Microstructure, Liquidity and Execution-Feasibility Methodology  
**Version:** 1.0.0  
**Research cutoff:** 2026-10-22  
**Status:** Operational research protocol; not a claim of live feed coverage or executable trading access  
**Companion files:** `01-derivatives-methodology.md`; `03-factor-research-methodology.md`; `04-backtesting-methodology.md`; `05-portfolio-risk-methodology.md`; `06-source-provenance-methodology.md`

## TL;DR

This methodology evaluates **how digital currencies actually trade**: available depth, spreads, order-flow, market impact, execution shortfall, queue risk, DEX swap curves, fragmentation, extractable value, data integrity and venue-specific failure modes. Its unit of analysis is **(asset identity, instrument, venue, market mechanism, timestamp, order size, order side)**. Venue eligibility is **discovered from the connected tools in the active environment**, never presumed from an exchange list. A method exposed by a plugin is *not* proof that an instrument, timestamp range, pagination path or complete event stream is available.

**Non-negotiable rules:**
1. Distinguish *quoted*, *displayed*, *executed*, *realized* and *hypothetical* liquidity; a spread or TVL is not executable depth.
2. Use original trade and book events for event-level claims. **Never convert OHLCV candles, aggregated positioning, or a single L2 snapshot into purported historical ticks, queue history, or order-book reconstruction.**
3. Keep **spot CLOB**, **spot AMM**, **RFQ/aggregator**, **on-chain order book**, and **perpetual or synthetic markets** as distinct mechanisms; cross-market derivatives may provide context but are not spot evidence.
4. Every decision-driving output needs a point-in-time data lineage, age, fees, chain/gas assumptions, scope, confidence tier, and sensitivity analysis.
5. When required depth, chronology, executable route, or cost components are unavailable, downgrade the claim or return `INSUFFICIENT_EVIDENCE` / `NOT_EXECUTION_QUALIFIED`, rather than silently extrapolating.

## 1. Scope, boundaries and testable questions

### 1.1 In scope

- Fungible digital currencies and their spot trading pairs, including wrapped representations **only where wrapper/bridge risk and asset identity are explicit**.
- Centralized and decentralized spot venues *only if discovery and a successful read prove coverage through currently connected tools*.
- On-chain constant-product and concentrated-liquidity AMMs; aggregators and intent/RFQ mechanisms where observable; CLOB or auction-based crypto spot books where supported.
- Derivatives books **only as tagged external comparison/lead-lag context**, not as a substitute for spot liquidity. Hyperliquid perpetual, HIP-3 and Lighter derivative feeds may be important cross-market measurements, but the relevant contract specification decides classification.
- Historical research, live observational snapshots, route simulations and **paper-only** execution diagnostics. No authority to place orders, sign transactions, or change portfolio protections.

### 1.2 Questions and estimands

For a precisely defined market, size and time, estimate:

| Question | Estimand / required evidence | Failure condition |
|---|---|---|
| Is the quote competitive? | Effective, quoted and fee-adjusted spread from synchronized bid/ask/trade evidence | Crossed/stale/uncertain quote |
| Can order size Q trade? | Side-specific sweep VWAP, available depth, route capacity and costs | Depth absent or route not accessible |
| What is market impact? | Immediate, temporary and post-trade price response, with benchmarks and uncertainty | No reliable trades/quotes with timing |
| Will a limit order fill? | Fill/cancel probability conditional on queue state, latency and flow | No queue/event evidence: bound only |
| Is flow predictive? | Signed flow / OFI association with **future** changes, out-of-sample | Misaligned timestamps or lookahead |
| Is AMM liquidity usable? | Exact fee-tier/tick/liquidity/pool-state quote at target block, gas and MEV sensitivity | TVL-only estimate or stale reserves |
| Is cross-venue arbitration feasible? | Timestamped net executable bid/ask differential after transfer, route, fees, latency and inventory | Non-transferability or unsynchronized observations |

Research must register *decision time*, forecast horizon, horizon clock (wall, event, block), base/quote units, reference currency, and whether the estimate is descriptive, predictive or causal. Avoid causal language from observational correlations.

## 2. Evidence hierarchy and scientific foundations

**[E] Established/peer-reviewed result; [W] working/preprint evidence; [P] proposed operational control.** These labels characterize support for statements, not a generic score for an asset.

1. **Order-book event imbalance [E]:** Cont, Kukanov & Stoikov establish that best-quote order-flow imbalance explains short-horizon price changes in their *equity-market sample*. This supplies a candidate mechanism, **not a validated crypto effect size**. Require crypto venue-by-venue replication. [R1]
2. **Trade information and lagged impact [E]:** Hasbrouck distinguishes persistent information-related price effects from contemporaneous trade movements. Price response estimates require quote/trade chronology and an explicit impact horizon. [R2]
3. **Venue-aware order placement [E]:** Cont & Kukanov formalize the trade-off among marketable and resting orders, queues and fees. Empirical fill and latency inputs must be estimated anew for crypto markets. [R3]
4. **Speed and market design [E]:** Budish, Cramton & Shim analyze speed races in continuous limit-order-book markets. Apply as a warning against treating stale cross-venue quotes as risk-free arbitrage, not as a theorem about all blockchains. [R4]
5. **Manipulated reported volume [E]:** Cong et al. find substantial anomalous trading patterns in their studied exchange sample; their exchange-level historical percentages **must not be generalized to today's particular venue**. Apply manipulation screens before volume-based conclusions. [R5]
6. **AMM adverse selection [W/E depending on publication version]:** Milionis et al. formalize loss-versus-rebalancing (LVR) under modeling assumptions; it is a provider-side cost concept, **not identical to impermanent loss or a direct trader quote**. [R6]
7. **On-chain MEV [W]:** Recent empirical work documents measurement difficulties and potential false-positive/false-negative problems for sandwich/arbitrage identification. Do not assert all slippage is malicious MEV. [R7]
8. **Liquidity provision competition [W]:** FLAIR provides a complementary LP-competitiveness perspective; do not present hypothetical LP returns as spot taker execution cost. [R8]

**Transferability warning:** much foundational microstructure work concerns equities. Crypto markets differ in 24/7 operation, fee and incentive schedules, broker/internalizer structure, wash trading, CEX custody and API semantics, block ordering, gas, asynchronous finality and cross-chain interoperability. A direct effect-size transfer is **prohibited** without local validation.

## 3. Connector-defined venues: qualification, not marketing coverage

### 3.1 At-run discovery [P]

Query the tools *actually installed and authorized in this session*. Store each available action signature and return metadata in a capability registry. The following reflects the available tool-name inventory discovered **2026-10-22**, **not successful data retrieval or a promise that each API supports each spot venue**:

| Tool family observed | Relevant actions / likely research role | Hard limitation / verification required |
|---|---|---|
| **0xArchive** | `get_instruments`, `get_instrument`, `get_orderbook`, `get_orderbook_history`, `get_trades`, `get_candles`, `get_freshness`; venue-specific Hyperliquid / HIP-3, Lighter and Robinhood Lighter methods; `get_lighter_l3_orderbook_history`, `get_l4_diffs`, `get_l4_orderbook_history`, `get_order_flow`, `get_l2_orderbook` | **Do not infer spot coverage from derivative support;** query actual instrument and market type. Historical orderbook method ≠ lossless book-event tape. Scope, dates, sequence IDs, granularity, records/page, delays and completeness remain unverified until queried. |
| **fin_data_mcp_http_v2** | `crypto_orderbook`, `crypto_recent_trades`, `crypto_candles`, `crypto_ticker`, `crypto_list_instruments` | Underlying venue and adapter source must be identified; no implicit archive or sequence continuity. |
| **Co-Invest / Liquid** | `search_markets`, `show_orderbook`, `show_market_overview`, `analyze_market` | May expose tradable derivatives, synthesized/integrated indicators or proprietary positioning; do not conflate with spot L2/L3 or raw prints. Reading does not confer trading authority. |
| **Massive** | `search_endpoints`, `call_api`, `query_data` | Verify crypto exchange feed, subscription, data type, timestamps, and licensing at call time. |
| **CoinGecko, CoinPaprika, CMC** | Discovery, identity, exchange/pair metadata, venue corroboration, broad liquidity context | Aggregates and quoted volume are not executable depth or authoritative tick tapes. CoinGecko available methods must be discovered dynamically. |
| **Blockscout** | `get_chains_list`, transactions/transfers, contract ABI/source, token metadata, `direct_api_call` | On-chain evidence and protocol reconstruction **only** if relevant state/event coverage is established; not a native centralized LOB. |
| **Other connected crypto tools** | Discover live availability for DEX pool/reserve/tick swaps, CCXT, DexPaprika, Dexscreener, Alchemy, Helius, Bitquery or other adapters | Prior discussion or proposed config does **not** equal installed/authorized tool. Register only functions actually present. |

**0xArchive qualification is especially important:** Its operation names cover Hyperliquid, HIP-3 and Lighter market data, with optional advanced L3/L4 book interfaces. Each underlying instrument **may be a perpetual, not spot**. No usable venue, historical earliest/latest time, retention period, tick size, event fidelity, pagination limit, or full reconstructability is asserted without actual probe results. The official Hyperliquid archive separately documents periodically uploaded L2 snapshots and historical fill sources, with missing data and delayed uploads possible [R9]. Historical snapshots alone cannot replay all between-snapshot cancels or queue priority.

### 3.2 Capability probe protocol [P]

For each `(provider, venue, instrument, market type, endpoint)`:

1. Fetch instrument metadata: base and quote **contract addresses when relevant**, network, token decimals, derivative/spot flag, fee tier, tick/lot size, minimum order, trading state and reference-unit mapping.
2. Obtain one recent snapshot and/or trade sample; preserve **raw unaltered response** with retrieval UTC, provider/server timestamp, endpoint, request parameters, response digest and any license constraint.
3. Probe historical slices at specified timestamps (recent, intermediate, old) and paginate across one boundary. Log earliest/latest **observed available timestamps**, not a guessed listing date. Identify exclusive/inclusive end semantics, max records per page, max lookback, bar/record granularity, and symbol delisting behavior.
4. If ordered event replay is claimed, verify snapshot sequence, incremental updates, sequence continuity, changes to size=0, restart/reconnect handling, deterministic checksum or native integrity fields. Rebuild and cross-check a later snapshot. A history of independently sampled L2 snapshots **does not** earn `FULL_BOOK_REPLAY`.
5. Determine server timestamp vs collection timestamp; quantify clock skew, publication delay, duplicates, rate limits, 429 handling and incomplete partitions.
6. Document no-auth/key/subscription requirements without assuming commercial free access; record any requester-pays historical storage or paid data tier.
7. Mark `OBSERVED_PASS`, `OBSERVED_PARTIAL`, `OBSERVED_FAIL`, `UNTESTED`, or `NOT_APPLICABLE`; successful transport alone is not content qualification.

**Machine statuses**: `DISCOVERED_ONLY`, `INSTRUMENT_VERIFIED`, `SNAPSHOT_VERIFIED`, `TRADES_VERIFIED`, `HISTORICAL_EVENTS_VERIFIED`, `BOOK_REPLAY_VERIFIED`, `EXECUTION_ROUTE_VERIFIED`. Statuses accumulate **only for independently proven requirements**. Use `SPOT` only after contract classification. Maintain separate venue and instrument identifiers, not just a ticker.

### 3.3 Evidence tiers and permissible conclusions

| Tier | Data actually verified | Allowed | Not allowed |
|---|---|---|---|
| T0 | Aggregated quotes/volume/OHLCV | Broad market context, bar-level proxies with caveats | Trade signing, queue, book sweeps, microsecond impact |
| T1 | Timestamped current L1/L2 snapshots | Contemporaneous spread/depth **as observed** | Historical or queue dynamics inferred from one snapshot |
| T2 | Independently timestamped trades + repeated L2 snapshots | Sampled realized flow and snapshot-based depth statistics, with gaps | Exact event attribution or full replay |
| T3 | Sequenced trade and order-book deltas + validated snapshots | Book reconstruction, OFI, event studies, replay **within validated complete spans** | True individual order priorities without L3 |
| T4 | Sequenced order-level L3 or equivalent, matching rules and full events | Queue-aware model within venue limitations | Omniscient fill certainty / unobserved hidden liquidity |
| A1 | State-consistent AMM pool snapshots or historical block state | Exact pool curve at stated state and fee assumptions | Guaranteed route, gas price or realized swap |
| A2 | A1 + transaction/log/trace simulation and route/inclusion evidence | Historical route simulation and realized on-chain outcome analysis | Guaranteed MEV-free execution or uncensored pending flow |

Coverage reports must also distinguish historical research from **live trading feasibility**; no current book snapshot proves an executable authenticated route exists.

## 4. Instrument identity, time and comparable units

### 4.1 Identity and mapping

Canonical key: `chain_id | token_address | token_decimals | canonical_asset_id | wrapper/bridge_type | venue | pool_or_market_id | market_type | base | quote | fee_tier | contract_version`. For CEX pairs use its native pair ID and venue asset mapping. `BTC`, `WBTC`, bridged BTC derivatives, wrapped staking assets, and synthetic BTC exposures are **not automatically fungible**. USDT, USDC and other quote tokens are separate settlement assets; convert through **timestamped executable conversion** when material rather than assuming a perpetual $1 peg. Do not combine pools or books with divergent fee / custody / oracle / bridge risks.

### 4.2 Chronology and freshness [P]

Record `event_time`, `exchange_time`, `block_time`, `observed_at`, `received_at`, `ingestion_time`, `decision_time` (UTC), `block_number`, `block_hash`, `sequence_id` and `chain_finality_state` as applicable. Preserve original precision; no invented subsecond ordering for block timestamps. Define deterministic join rules, expected max staleness and missingness; report actual lag distribution. Synchronize to **information available by decision time**, not data published later. Reorged transactions require rollback and replay. Exchange timestamps may be unsynchronized; measure offsets where possible and exclude unsupported lead-lag claims.

### 4.3 Data screening

Flag rather than silently discard: negative/nonfinite quantities, zero/crossed L1, nonmonotonic sequence, off-tick price, impossible size/decimals, time reversals, duplicates, gaps, jumps at symbol migrations, stale snapshots, reorgs and pool reserve discontinuities. Separate actual outages, halted/depegged instruments, legitimate volatility and corrupt records. Maintain raw rows, exclusion reasons and resulting sample counts; conduct with/without-filter sensitivity checks.

## 5. Core CLOB measures and exact formulas

Let `b_t` and `a_t` be best executable bid/ask in quote per base asset, `m_t=(a_t+b_t)/2`, and all quantities be in **base units** unless otherwise stated. Invalid if `a_t<b_t` without identified crossed market mechanics.

**Quoted spread:** `S_t=a_t-b_t`; `S_bps=10,000*(a_t-b_t)/m_t`.

**Microprice:** `mu_t=(a_t * q_bid + b_t * q_ask)/(q_bid+q_ask)` (best-level quantities; undefined if denominator zero). **Book imbalance:** `I_t=(D_bid-D_ask)/(D_bid+D_ask)` where depth sums use declared price-band or N-level window; ranges differ with tick normalization. A microprice is a *descriptive estimator*, not a fair-value guarantee.

**Top-of-book order-flow imbalance (OFI)** for consecutive valid book observations `(t-1,t)`:

`e_t = 1[b_t >= b_{t-1}]q^B_t - 1[b_t <= b_{t-1}]q^B_{t-1} - 1[a_t <= a_{t-1}]q^A_t + 1[a_t >= a_{t-1}]q^A_{t-1}`.

Sum `OFI_[u,v]=Σ e_t` over **continuous reconstructed event data**; sampled snapshots yield `snapshot-OFI proxy`, never a full event-flow statistic. Regime- and depth-standardize, check overlapping labels and serial dependence. Estimate relation to *future* return with rolling out-of-sample evaluation, uncertainty and confounders (market beta, volatility, spread, session, funding/cross-market moves).

**Aggressor sign:** prefer venue-native aggressor flag validated against prints and quotes. The tick rule and Lee–Ready-style quote matching are **approximations**; explicitly estimate unclassified and disagreement shares and sensitivity to latency.

**Depth:** `D^ask_t(δ)=Σ_{p≤a_t(1+δ)} p*q_p` in quote currency, with analogous bid band; always disclose whether δ is %/bps, N levels, or quote notional. A displayed limit order can vanish before reaching it; depth is **indicative**.

**Order book marketable buy sweep:** For requested `Q` base units, consume ask levels ascending; `VWAP_buy=Σ(p_i f_i)/Σ f_i`, `Σf_i=min(Q,Σq_i)`. Explicitly record unfilled remainder; never price unavailable depth at the worst known level. Sell analog consumes bids descending. Add taker fees, rebates (if contractually qualifying), quote conversions, transfer, expected slippage beyond sampled depth and risk buffer. For limit orders, model execution rather than assuming a fill at the limit.

**Realized spread / effective spread:** with trade price `P_i`, pre-trade synchronized midpoint `m_i`, trade sign `s_i∈{+1,-1}`: `EffectiveSpread_i=2*s_i*(P_i-m_i)`; `RealizedSpread_i(H)=2*s_i*(P_i-m_{i+H})`; `PriceImpact_i(H)=2*s_i*(m_{i+H}-m_i)`; these satisfy the decomposition under matched conventions. Report in prices or normalized bps with the same denominator, finite horizon, valid matches and sign accuracy. Do not interpret a single trade's price change as *caused* by that trade.

**Response function:** `R(H)=E[s_i*(m_{i+H}-m_i)]`; specify event/wall-clock horizon, conditioning, block bootstrap or HAC uncertainty, and clustered events. Segment normal flow versus liquidations and time-of-day regimes.

**Trading-cost decomposition:** expected signed implementation shortfall vs arrival mid/benchmark equals marketable spread + market impact + venue fees + route/gas/MEV/bridge costs + delay/opportunity cost and quote conversion, without double-counting components. Clearly separate *ex ante estimated* from *ex post realized* cost and filled vs cancelled quantity.

## 6. Limit-order queues, resilience and impact estimation

### 6.1 Queue position [P]

At T1–T2, depth ahead is not observed exactly; provide **optimistic/pessimistic bounds** only. T3 L2 event replay can approximate queue depletion if exchange priority rules, hidden orders, amendments and own order timestamp are modeled; **T4 true order-event data** is preferred. Model price-time versus pro-rata matching explicitly; consider cancellations ahead versus behind and latency to accepted order. Historical candle touches **do not equal fills**.

### 6.2 Fill model

Register `P(fill by H | price distance, spread, queue estimate, OFI, trade intensity, volatility, time-of-day, order age, latency, regime)`, plus `P(adverse price move | fill)` and cancel/replacement costs. Use walk-forward calibration, reliability diagrams, Brier/log loss, fill-rate uncertainty, censoring and realistic submission latency. No learnable fill model without order acknowledgements or sufficiently granular reconstruction; paper scenarios use bounds, not exact probabilities.

### 6.3 Impact and resilience

Estimate side/size-conditional cost curves from contemporaneous book sweeps and matched trade episodes. Compare immediate and post-horizon moves, replenishment half-life and recovery fraction relative to pre-event depth. Condition on volatility, flow direction, news and reference-market return. Test convex versus approximately square-root functional forms; **do not impose a universal square-root law** on crypto or small-cap pools. Require uncertainty intervals, independent days/regimes and robust losses. Separate mechanical book walk (instantaneous) from realized price response and signal-induced selection bias.

## 7. DEX and AMM-specific methodology

### 7.1 Exact constant-product pool baseline

For a fee-free constant-product pair `x*y=k`, quote-out for base-in `Δx` is `Δy=y*Δx/(x+Δx)`. With fractional input fee `f`, replace `Δx` inside the invariant by `Δx_eff=Δx*(1-f)`; the wallet debits the full `Δx`. A *real pool quote* must additionally use protocol-specific rounding and integer token units, fee-on-transfer behavior, router path, protocol fees and actual contract implementation. Do not apply V2 equations blindly to stable-swap, concentrated liquidity, weighted pools, hooks, dynamic fees or specialized designs.

### 7.2 Concentrated liquidity

For a CLMM, reconstruct initialized ticks, active liquidity, square-root price, tick spacing, exact fee tier and block-consistent contract state. Simulate tick crossing, active-liquidity changes, fee accounting and integer rounding using protocol-native math. For pools only available via an aggregate price/TVL API, label `APPROXIMATE_POOL_PROXY`; refuse exact $Q swap-impact claims. Compare same block or finalized block state; chain heads may reorg.

### 7.3 Router and on-chain frictions

Quotes require path identity, token input/output amounts, exact-input versus exact-output, pool sequence, deadline, approval costs where relevant, gas in native units and converted quote value, network congestion, failed/reverted transaction probability, inclusion time, private vs public order flow, slippage tolerance, chain reorg/finality, bridged transfer time and sequencer censorship risk. Distinguish **quoted expected output, minimum-out floor and realized receipt**. No claims of guaranteed MEV protection for private RPCs. Test transaction reordering/sandwich risks and slippage deterioration as *scenarios*, not assumed observations.

### 7.4 LP economics are distinct from trading costs

When studying LP-side participation, report gross fees, inventory return, divergence loss versus holding, loss-versus-rebalancing (under assumptions), incentive rewards, active-range rebalancing, gas, opportunity cost and competition. This is not interchangeable with a taker-side best-execution report. Put LP capital-at-risk measures under the companion portfolio-risk framework.

## 8. Fragmentation, price discovery and cross-venue comparisons

1. Establish **fungible, reachable asset identity**, location of inventory, eligibility, settlement and restrictions. Cross-chain quoted differences are not immediately arbitrageable without bridge time/risk/capital.
2. Align venue observations by information time and effective staleness. Prefer lead-lag bounds or Epps-effect-aware horizons rather than nanosecond claims from mismatched timestamps.
3. Compute effective executable prices for identical base amount and side, including pool curve, fee tier, fixed gas, quote conversion and lot sizes. When no direct route, present indicative difference **only**.
4. Track price-discovery and volatility contribution by venue with robust out-of-sample tests; structural breaks around listings, delistings, major protocol changes, depegs and chain congestion.
5. Treat oracle/index prices as **reference prices**, never evidence of executable liquidity. Derivative prices/funding/liquidations are supplementary factors, tagged separately.
6. Score venue resiliency separately from cheapness: outages, API quality, reported-volume concerns, fragmented depth, asset freezes, custody, MEV, chain halt, withdrawal and network fees.

## 9. Manipulation, toxic flow and hostile liquidity

**Screens (diagnostic, not conclusive):** trade-size clustering, digit/round-number distribution, abnormal repetitive alternating prints, suspiciously high volume-to-depth, self-trade flags where available, sudden depth appearance/disappearance, repeat spoof-like patterns, orphaned liquidity, pool wash swaps, concentrated counterparties and impossible cross-source discrepancies. These are *indicators* requiring false-positive controls; no accusations of manipulation based on one heuristic. Flag protocol incentives, bot arbitrage, internalized prints and benign market-making as alternative explanations.

Operational defenses: deweight suspect volume and unstable book walls, report results excluding suspicious intervals, reserve capacity for sudden liquidity withdrawal, use a robust reference basket where constituents are independently verifiable, and never let a single venue's wash-prone reported volume determine trading capacity.

## 10. Empirical study design and statistical validation

### 10.1 Pre-registration [P]

Document before inspecting outcomes: hypothesis, unit, venue selection, asset survival rules, date windows, event definitions, costs, reference mid, effect magnitude of interest, power assumptions, train/validation/test splits, multiple testing budget and expected failure modes. Compare at least: naive mid-price, spread-plus-fees baseline, static book sweep, and latency-aware model (when data qualifies).

### 10.2 Tests

- Use **purged, embargoed chronological** splits where labels overlap; evaluate later regimes and fresh venues. Do not random-shuffle dependent events.
- Use day- and venue-clustered uncertainty where appropriate, block/stationary bootstrap or HAC with justified bandwidth; report effective sample and confidence intervals, not only p-values.
- Correct for asset/venue/horizon/window hyperparameter search (e.g. Holm/BH when suitable, or a designated research-family multiple-testing method). Record rejected variants.
- Stratify by liquidity deciles, volatility, UTC hour/weekend, fee tier, pool size, asset age, protocol upgrade, macro event and stressed periods. Show training-period versus genuinely unseen test results.
- Conduct robustness to clock skew, quote lag, event subsampling, wrong aggressor labels, outliers, missing snapshots, fee schedule change, gas spikes and delayed cancellation.
- Measure practical improvement in **net implementation shortfall** and fill-adjusted realized execution, not only directional predictability or R².
- Simulation fidelity must match evidence tier. Event-driven limit-order simulators need event ordering, fees, latency and queue rules; book-snapshot or bar simulations must explicitly discount their optimistic bias.

**Minimum rejection triggers:** leakage of future book state, undefined book/quote clock, unverified spot instrument, material undocumented book gaps, missing fee component that can overturn result, inability to produce source lineage, result driven by one day/venue, or positive gross but unassessable net benefit.

## 11. Executable workflow: research-to-decision protocol

**Stage 0 — Authority:** Declare read-only/paper research; identify any execution request as a separate permission workflow. Never infer authority from tool availability.

**Stage 1 — Instrument discovery:** Query connector tool inventory, market lists and metadata. Resolve chain/address/wrapper, spot-versus-derivative, base/quote, contract specifications and trading state.

**Stage 2 — Probe and custody:** Fetch original records, observe history bounds/pagination, stamp retrieval, confirm rate/license restrictions; hash raw datasets and record transformations under provenance methodology 06.

**Stage 3 — Validation:** Check chronology, completeness, market states, chain reorgs, snapshots/deltas, costs and quote conversions. Produce evidence tier and explicitly unavailable dimensions.

**Stage 4 — Measurement:** Calculate side-specific spread, depth, capacity, book imbalance, execution cost and resiliency. Select only indicators permitted by evidence tier; include uncertainty.

**Stage 5 — Cross-check:** Independently corroborate identity/price where feasible. Independent aggregates sharing an upstream venue feed **are not independent corroboration**.

**Stage 6 — Stress:** Evaluate at least normal / stressed liquidity and adverse move, costs and route latency. A user-specified size may be tested against deeper book/AMM curve; do not silently scale linearly.

**Stage 7 — Decision:** Issue one of `RESEARCH_SUPPORTED`, `INDICATIVE_ONLY`, `INSUFFICIENT_EVIDENCE`, `NOT_EXECUTION_QUALIFIED`, `REJECTED_DATA_INTEGRITY`, with reason codes and claim-level evidence. The first status is **not** permission to trade.

**Stage 8 — Handoff:** Pass documented friction distributions and limitations to backtesting 04, allocation limits and tail exposures to risk 05, candidate signals to factor research 03, derivatives-only context to 01, and raw custody details to provenance 06. Avoid duplicating companion documents' controls.

## 12. Minimal machine-readable record [P]

```yaml
schema_version: "spot-microstructure-1.0"
as_of_utc: "<ISO8601>"
research_cutoff: "2026-10-22"
asset:
  canonical_id: "<verified identity>"
  chain_id: null
  contract_address: null
  decimals: null
instrument:
  venue: "<actual venue>"
  provider: "<connected tool>"
  market_id: "<native identifier>"
  market_type: "SPOT|PERPETUAL|AMM_POOL|RFQ|OTHER"
  mechanism: "CLOB|CPAMM|CLMM|OTHER"
  base: "<base>"
  quote: "<quote>"
  fee_schedule_verified: false
capability:
  discovered_method: "<tool operation>"
  tested: false
  observed_earliest_utc: null
  observed_latest_utc: null
  granularity: null
  max_page_records_observed: null
  pagination_complete: false
  event_sequence_verified: false
  replay_verified: false
  tier: "T0|T1|T2|T3|T4|A1|A2|UNQUALIFIED"
lineage:
  retrieval_utc: "<ISO8601>"
  source_timestamp_utc: null
  raw_digest_sha256: "<digest>"
  source_uri_or_tool_request_id: "<trace>"
  upstream_feed: null
  licensing_notes: null
analysis:
  side: "BUY|SELL"
  base_quantity: null
  spread_bps: null
  displayed_depth_quote: null
  sweep_vwap: null
  unfilled_base_quantity: null
  fee_quote: null
  gas_quote: null
  expected_shortfall_bps: null
  confidence_interval: null
  missing_components: []
  assumed_components: []
  status: "INSUFFICIENT_EVIDENCE"
  reason_codes: []
```

**Schema controls:** null means unmeasured, **not zero**. Never use synthetic example numbers as live observations. Additional route details, publication delays, queue parameters and chain-finality evidence should be versioned extensions rather than guessed defaults.

## 13. Worked hypothetical example (not a market observation)

Suppose a fictional **spot** book displays bid 99.90 for 2 units and ask 100.10 for 1 unit, with the next ask 100.30 for 2 units. A hypothetical marketable buy for 2 units takes 1 at 100.10 and 1 at 100.30: `VWAP=(100.10+100.30)/2=100.20`, while midpoint is `100.00`. **Displayed sweep cost** is `(100.20/100.00 - 1)*10,000 = 20 bps` before fees, latency and any depth removal. The **quoted spread** is `(100.10-99.90)/100.00*10,000 = 20 bps`. These two 20-bps values have **different meanings**: one is a one-sided size-specific execution cost versus midpoint, the other the full top-of-book spread. Neither establishes a realized 2-unit fill or predicts impact from future price changes.

For a hypothetical constant-product pool with reserves 1,000 base and 100,000 quote, **base-in** 10 units would receive approximately `100,000*10/1,010=990.099` quote units **before fees**. This is a sell of base into a quote pool; it must not be compared to the CLOB **buy-base** example as though they represent the same trade side. Fee tier, exact integer precision and protocol details are unspecified, so it is not an executable quote.

## 14. Quality gates, reproducibility and reporting checklist

- [ ] Connector and real underlying venue/instrument **verified in this session**; derivative/spot distinction explicit.
- [ ] Data classification T0–T4/A1–A2 documented with raw source and retention/granularity probes.
- [ ] Earliest/latest observed historical data, pagination and continuity recorded; no guessed archival depth.
- [ ] Canonical asset/token/quote/chain/pool IDs and wrapper distinctions confirmed.
- [ ] Timestamps and point-in-time availability validated; no future state leakage.
- [ ] Venue fees, bid/ask direction, route/gas/quote conversions and quantity units explicit.
- [ ] Depth and slippage tied to a side **and exact size**; missing levels are unfilled, not extrapolated.
- [ ] Queue/OFI/impact claims match evidence tier; no candle-as-tick substitution.
- [ ] DEX exact invariant/range math and block consistency, or explicit approximate label.
- [ ] Manipulation, MEV, concentration, stress and latency sensitivity reported when material.
- [ ] Cross-source dependence identified; no false claims of independent validation.
- [ ] Sample counts, failures, missingness, uncertainty and alternative explanations reported.
- [ ] Action is research-only/paper-only; any real execution is outside the authority of this file.
- [ ] Source lineage, raw hashes, method version and results reproducible from stored inputs.

## 15. Claim-to-source and evidence matrix

| Claim or design choice | Evidence | Transfer limitation |
|---|---|---|
| OFI is a useful candidate LOB explanatory variable | [R1] peer-reviewed equity market | Must validate for specific crypto market/event feed |
| Trade effects have informative persistence | [R2] peer-reviewed equity study | Not universally causal or same horizon for crypto |
| Queue, flow and fees affect order placement | [R3] peer-reviewed modeling | Venue matching and crypto fill data are needed |
| Speed can induce mechanical arbitrage races | [R4] peer-reviewed analysis | Depends on CLOB design and clock synchronization |
| Some venues' reported volume can be manipulated | [R5] peer-reviewed crypto empirical study | Historic sample ≠ a current venue estimate |
| AMMs incur adverse-selection economics for LPs | [R6] theoretical work | Assumptions/protocol/funding differ materially |
| Sandwich identification requires careful methodology | [R7] empirical preprint | Classifier errors, chain/protocol time dependence |
| Hyperliquid public historical sources can be incomplete or delayed | [R9] official docs | Does not establish 0xArchive instrument-level coverage |
| Evidence tier/probe/fail-closed gates | [P] this document | Operational requirements, not scientific laws |

## 16. Bibliography and primary-source links

**[R1]** Cont, R., Kukanov, A., & Stoikov, S. (2014). *The Price Impact of Order Book Events*. Journal of Financial Econometrics, 12(1), 47–88. Preprint: https://arxiv.org/abs/1011.6402

**[R2]** Hasbrouck, J. (1991). *Measuring the Information Content of Stock Trades*. The Journal of Finance, 46(1), 179–207. https://doi.org/10.1111/j.1540-6261.1991.tb03749.x

**[R3]** Cont, R., & Kukanov, A. (2017). *Optimal Order Placement in Limit Order Markets*. Quantitative Finance, 17(1), 21–39. https://doi.org/10.1080/14697688.2016.1190030

**[R4]** Budish, E., Cramton, P., & Shim, J. (2015). *The High-Frequency Trading Arms Race: Frequent Batch Auctions as a Market Design Response*. Quarterly Journal of Economics, 130(4), 1547–1621. https://ericbudish.org/publication/the-high-frequency-trading-arms-race-frequent-batch-auctions-as-a-market-design-response/

**[R5]** Cong, L. W., Li, X., Tang, K., & Yang, Y. (2023). *Crypto Wash Trading*. Management Science, 69(11), 6427–6454. https://doi.org/10.1287/mnsc.2021.02709

**[R6]** Milionis, J., Moallemi, C. C., Roughgarden, T., & Zhang, A. L. (2022 preprint / subsequent publication). *Automated Market Making and Loss-Versus-Rebalancing*. https://arxiv.org/abs/2208.06046

**[R7]** Chi, T., He, N., Hu, X., & Wang, H. (2024 preprint). *Remeasuring the Arbitrage and Sandwich Attacks of Maximal Extractable Value in Ethereum*. https://arxiv.org/abs/2405.17944

**[R8]** Milionis, J., Wan, X., & Adams, A. (2023 preprint). *FLAIR: A Metric for Liquidity Provider Competitiveness in Automated Market Makers*. https://arxiv.org/abs/2306.09421

**[R9]** Hyperliquid official documentation, *Historical data* and *Info endpoint*: https://hyperliquid.gitbook.io/hyperliquid-docs/historical-data ; https://hyperliquid.gitbook.io/Hyperliquid-docs/for-developers/api/info-endpoint . Official archive warns that uploads may be delayed and data absent, and describes L2 snapshots versus node fills separately.

## 17. Update triggers and change log

Requalify before relying on a new venue/instrument, connector upgrade, new trading mechanism, changed fee tier or rate limit, liquidity crisis, token redenomination, bridge migration, reorg/finality rule, data schema revision, major oracle deviation, or materially contradictory independent evidence. Re-evaluate methodological citations and emerging empirical crypto research at least quarterly. **A tool endpoint suddenly becoming available is not retrospective proof that its older observations were accessible at past decision times.**

**v1.0.0 — 2026-10-22:** Initial dedicated spot-market microstructure methodology created to fill the `02` gap without duplicating derivatives (01), predictive factor research (03), backtest validation (04), portfolio risk (05) or evidence provenance (06). Introduces connector-defined market universe, conservative 0xArchive qualification, tiered data claims, side/size-specific cost calculations, spot CLOB and AMM separation, falsifiable execution models, chain-aware chronology, research gates and documented scientific sources. No live tool endpoints were called for instrument-specific observations in this document; the tool inventory was inspected, and venue data coverage remains **unverified** until requested in a concrete research run.
