# 08-data-quality-validation-methodology.md

**Title:** Data Quality Validation Methodology for Digital-Currency Quantitative Research  
**Version:** 1.0 | **Research cutoff:** 2026-10-22 | **Status:** Proposed internal research controls, not a claim of production implementation  
**Scope:** Crypto spot, perpetual and dated derivatives, token and blockchain measurements, decentralized liquidity and oracle-derived metrics accessible through currently connected research tools. No live trading authorization.

## 0. Mandate, evidence labels, and relationship to the methodology suite

This document specifies **how to test, characterize, quarantine, repair, release, and monitor data** after source discovery and before factors, backtests, derivatives studies or risk reports consume it. It complements—not replaces—`01-derivatives-methodology.md`, `03-factor-research-methodology.md`, `04-backtesting-methodology.md`, `05-portfolio-risk-methodology.md`, and `06-source-provenance-methodology.md`. The last document controls source identity, evidence lineage, admissibility and point-in-time provenance; this document controls empirical quality tests and use-specific acceptance.

**Evidence labels:** **[STANDARD]** published normative protocol/specification or documented vendor contract; **[PEER-REVIEWED]** published academic result; **[WORKING PAPER]** non-peer-reviewed or not confirmed peer-reviewed; **[INTERNAL]** proposed, configurable operational rule; **[OBSERVED]** outcome of a tool call with dated response; **[UNKNOWN]** not established. Every numerical threshold below is **[INTERNAL]** unless explicitly attributed to a venue specification. Literature findings motivate checks; they do not validate fixed global cutoffs.

**Non-negotiable:** an endpoint existing in a connector's menu is not evidence of accessible venue history, current entitlement, completeness, replayability, historical depth or independent corroboration. A successful test establishes only the specific venue/instrument/period/granularity/pagination tested. Do not equate a quote, candle, historical snapshot, incremental book update, or vendor-derived indicator with a trade-by-trade or lossless market-event feed.

### 0.1 Population and venue discovery

* **Digital-currency identities:** native coins, deployed contract tokens, stablecoins, wrapped/bridged variants, liquid staking or receipt tokens, and derivatives *whose underlying is a digital currency*. Distinguish each economically and technically. Exclude equity, FX, commodity, index and non-crypto HIP-3 exposures except as explicitly labeled **external benchmarks**.
* **Venue eligibility:** the intersection of (a) connected callable tool, (b) discovered venue and instrument, (c) supported operation and timestamp window, (d) pagination and historical retention, (e) usable terms and permission. Maintain an entitlement-specific **capability ledger**; do not infer access to all exchanges aggregated by a service.
* **Connected tool families to probe, not assume:** 0xArchive (Hyperliquid core, HIP-3, Lighter, with Robinhood-related Lighter surface where actually exposed), Co-Invest/Liquid (market views, positioning, charts, order books), Massive (endpoint discovery/data), CoinGecko, CoinPaprika, CMC, DexPaprika/DexScreener where present, Blockscout, fin-data MCP and other verified on-chain/market tools. Tool family availability can differ from operation availability; a server name is not a data guarantee. No source automatically outranks others merely by being attached.
* **0xArchive-specific probe:** `get_instruments`, `get_instrument`, `get_trades`, `get_orderbook_history`, `get_orderbook`, `get_candles`, `get_funding_history`, `get_open_interest_history`, `get_liquidations`, `get_freshness`; venue-specific HIP-3 and Lighter equivalents as applicable. Record whether an order-book history response contains full depth snapshots, incremental events, sampled states or only summary levels. The APIs' names do **not** prove complete event reconstruction. Resolve market identity and the source's timestamp conventions first.
* **Keep access modes separate:** public API vs authenticated account access, current snapshot vs retrospective query, subscription stream vs historical file, derived aggregate vs native observations. A tool that reports a portfolio or positioning does not thereby offer an exchange-level tick archive.

### 0.2 Capability ledger (required before any dataset claim)

| Field | Required contents |
|---|---|
| `assessment_id`, `tested_at_utc`, `tool_name`, `tool_version` | Exact assessment and connector surface, if disclosed |
| `upstream_producer`, `intermediary_provider`, `venue`, `chain_id` | `UNKNOWN` rather than inferred producer or venue |
| `instrument_canonical_id`, `venue_symbol`, `market_type` | Contract/chain and contract specification where applicable |
| `operation`, `unit`, `native_granularity`, `response_schema_hash` | Exact data construct; trades ≠ candles; snapshots ≠ deltas |
| `earliest_returned`, `latest_returned`, `request_window` | Observed bounds only; never claim archive inception absent exhaustive discovery |
| `page_size_observed`, `next_cursor`, `sort_order`, `pagination_exhausted` | Record limits, duplicate overlap and termination evidence |
| `clock_fields`, `timestamp_resolution`, `depth_scope` | Presence/absence of sequence, block IDs, bid/ask depth, time provenance |
| `quota_or_error`, `data_license`, `auth_mode`, `entitlement` | Verified constraints or `UNKNOWN` |
| `completeness_evidence`, `reconstructability`, `test_payload_digest` | `YES` / `NO` / `UNDETERMINED` with justification |
| `assessor`, `review_due`, `changes_since_last_check` | Internal governance fields |

**Reconstructability verdict:** `YES` only if a continuous, contract-valid seed snapshot and every required ordered update (including deletions) are demonstrably available over the stated interval, with gap handling and snapshot reconciliation. `NO` if only candles, periodic snapshots, top-of-book, truncated top-N states or known missing events exist. Otherwise `UNDETERMINED`. Never promote `UNDETERMINED` to `YES`.

## 1. The measurable quality model

Quality is **conditional on use**. A one-minute candle may be adequate for low-frequency exploratory volatility studies but invalid for order-queue simulation, fill probabilities or tick-level slippage. Maintain a vector of dimension-specific diagnostics; **do not average away a hard failure**.

| Dimension | Representative measurements | Typical blocking failures |
|---|---|---|
| Identity and semantics | resolved asset and venue; base/quote; contract multiplier; units; corporate/protocol state | ticker collision, wrong decimals, wrong funding units |
| Structural validity | schema parse, required fields, finite positive prices, admissible size, unique primary keys | corrupted types, mixed schemas or invalid symbols |
| Temporal integrity | UTC parse rate, monotonicity within declared ordering, lag and timestamp granularity | unverifiable PIT availability, negative impossible ordering without documented semantics |
| Completeness | expected vs observed bars/events, trade-ID/sequence gaps, chain-height holes, page coverage | unbounded missingness in outcome-critical intervals |
| Internal consistency | OHLC inequalities, spread, notional equality, depth totals, signed flows | crossed book without auction/venue exception, impossible arithmetic |
| External consistency | paired independent feeds with aligned economic definitions and tolerances | persistent unexplained discrepancy in decision-driving observations |
| Revisions and stability | first-seen vs revised value, restatement incidence, snapshot drift | untracked retroactive replacement |
| Manipulation susceptibility | wash-trading flags, pool concentration, oracle dependency, spoof-sensitive levels | volume or liquidity proxy presented as trustworthy absent tests |
| Representativeness | live/delisted asset coverage, listing inception, dead pools, missing-not-at-random | survivorship and provider coverage selection tied to returns |
| Fitness for research task | interval, depth, as-of availability, resolution, execution relevance | candle-only evidence for market-event replay |

Keep distinct: **raw physical truth**, **venue-published truth**, **provider-transformed representation**, **research-accessible knowledge at decision time**, and **statistical estimate**. They are not interchangeable.

## 2. Canonical record, clocks, and immutable storage

Use the provenance keys required by document 06 rather than competing field names. Every QA run must link to the provenance record and save additional QA fields: `dataset_version`, `raw_payload_sha256`, `parser_git_commit`, `schema_version`, `qa_ruleset_version`, `qa_run_id`, `validation_population`, `failed_rules`, `quality_state`, `repair_log`, `assessor`, and `release_time_utc`.

Preserve where known **event** time, **primary observation** time, **provider publication/availability** time, **research retrieval** time, and **revision** time separately. A vendor returning a historical event timestamp does not establish when that event became available to the research system. If publication time is not observable, mark it `UNKNOWN` and run a sensitivity bound rather than assuming zero lag. Timezone, precision, clock domain and drift are part of the data type. Never silently round milliseconds to seconds, or treat a chain block timestamp as receipt time.

**Storage architecture:** raw immutable response bytes plus metadata → deterministic normalized records → separately versioned corrections/annotations → quality-graded approved datasets → downstream artifacts. Use hash checks as *local integrity evidence*, not attestation by a venue. No silent backfill into original raw rows; retain tombstones, revisions and reversible mappings. Protect licensed/private material and do not assume immutable storage is legally redistributable.

**Point-in-time rule:** A feature used at decision time `t` must have been available no later than `t - operational_latency` under a declared scenario. Eligibility follows recorded first availability or a **conservative, explicit bound**. Backfilled market caps, index constituents, token mappings, chain-finality statuses and revised candles require a historical-as-of view. A current API response is generally insufficient to establish historical availability.

## 3. Validation pipeline and fail-closed release states

| Stage | Mandatory actions | Outcome |
|---|---|---|
| G0 Discovery | Verify connector, venue, identity, entitlement, coverage and task fit | Unsupported → `UNAVAILABLE` |
| G1 Acquisition | Persist raw bytes, query parameters, time, pagination and errors | Partial raw material remains `QUARANTINED` |
| G2 Schema | Validate format, units, required fields, keys and schema revision | Fatal parse/identity defect → `REJECTED` |
| G3 Event integrity | Check clocks, sequence IDs, overlap, missing intervals, finality | Bound gaps or reject use-case |
| G4 Economics | Domain invariants and reconciliation to economically equivalent metrics | Contradiction → investigate, do not normalize away |
| G5 Independent evidence | Compare truly independent upstream producers; explain correlated feeds | `UNVERIFIED` where confirmation required |
| G6 Repair and sensitivity | Reversible transformations; quantify impact on estimates | Restore only task-valid subsets |
| G7 Signoff | Publish manifest, counts, coverage matrix, diagnostics, owner and limitations | `RESEARCH_APPROVED` or `EXECUTION_SIM_APPROVED` with exact scope |

**Dataset states:** `UNAVAILABLE`, `QUARANTINED`, `REJECTED`, `RESEARCH_APPROVED`, `EXECUTION_SIM_APPROVED`, `EXPIRED`. Approval is for `(dataset version, venue, asset set, field, interval, use-case, ruleset version)` not an eternal provider endorsement. `EXECUTION_SIM_APPROVED` requires an adequate order-event/fee/latency surface; a research-approved OHLC dataset alone cannot attain that status for order-book replay. Neither state permits live trading.

**Hard-stop examples [INTERNAL]:** unresolved base/quote or multiplier; uncaught unit change; known book sequence discontinuity for order reconstruction; future-available feature in historical signal; non-final chain state presented as finalized; unbounded primary-key duplication; incompatible prices across instruments mislabeled as one market; inability to reproduce a decision-driving revision. Flag `UNKNOWN`, not a fabricated measurement, for unavailable tests.

## 4. Instrument and identity validation

Use a persistent multikey identity `(chain namespace, chain ID, contract address / native asset ID, token standard, venue, market ID, contract spec revision)`. A ticker is an alias. Also capture name, base/quote, quote currency, decimals, lot and tick sizes, leverage/margin denomination, perpetual funding convention, expiry/settlement for dated futures, oracle/index basis, wrapped token redeemability and bridge origin.

Validate symbol→market mapping at each date. A migration, redenomination, decimal change, airdrop fork, proxy upgrade, stablecoin split, token rebasing or bridge replacement must create a **versioned economic identity event**. Price continuity is not established by the same ticker. Different pools for the same pair can have different fee tiers, liquidity and price impact; they are not fungible observations.

Units must be explicit: quote/base, base/quote, contracts, underlying units, quote notional, USD vs USDT/USDC, percent vs basis points, funding *per interval* vs annualized, open-interest contracts vs coin vs USD. Example invariant when permitted by specification: `quote_notional ≈ base_quantity × price` after contract multiplier and rounding. A USD stablecoin denomination is not automatically USD cash parity.

## 5. Timestamp and sequence integrity

1. Parse and preserve native timestamps and timezone metadata. Measure `% null`, precision/rounding (e.g. 10/100/1000 ms buckets), inter-arrival spikes, negative source→receipt lag, publication→ingestion lag percentiles and staleness conditional on volatility.
2. Never sort by time alone if multiple trades share timestamps. Use documented native sequence, trade ID, block/transaction/log indices, or maintain `ordering_unknown=true`. Compare event-time ordering with ingest order and any exchange match sequence.
3. Distinguish legitimate inactivity from missing capture: a no-trade interval is not automatically a gap. Establish expected cadence from the venue feed semantics, a heartbeat/sequence contract or independently observed traffic.
4. For book feeds, validate snapshot-bridge continuity and per-market update ordering against **venue-specific** rules. Binance spot's published diff-depth update IDs and snapshot procedure are a documented example, not a protocol for 0xArchive/Hyperliquid/Lighter. A gap invalidates reconstruction until a new valid snapshot, absent provable lossless backfill.
5. For on-chain rows, retain block hash, height, parent hash, transaction hash/index and log index; flag reorg/orphan and duplicate emission. Require declared confirmation/finality policy, differentiated by chain. “Six blocks” is not a universal finality standard. Rollups may have distinct sequencer, L1 posting and settlement/finality clocks.
6. Derive an **observed** timestamp precision profile by venue and regime. Millisecond timestamps can still reflect batched publication or coarse matching-engine timestamps. Never back-infer trade order from an imprecise timestamp.

Scientific grounding: analysis of raw ticks from 17 exchanges documents slow and imprecise exchange timestamp behavior [R3]. This motivates validation, not a presumption that any named venue has a problem.

## 6. Completeness, continuity and pagination

**Partition** by producer, venue, instrument, field type, date, session/regime and response route. For expected regularly spaced bars: `coverage = observed_distinct_expected_slots / expected_slots`, restricted to the instrument's verified listing and feed operational schedule. Count duplicated and partial bars separately. For event feeds without a known expected count, do not claim percentage completeness; report sequence-gap count, missing ID ranges, observed start/end, reconnection windows and unknown coverage.

**Pagination test:** probe ascending and descending order where supported, request adjacent overlapping windows, compare stable IDs and payload digests, inspect cursor termination, clipping, hard row caps and page repetition. Store `requested_window`, `returned_min/max`, `count`, `cursor`, `has_next`, `first/last_id`, `page_hash`, and `error_or_rate_limit`. If results cap at an API limit, a returned earliest timestamp may be only the **earliest page**, not the earliest available history.

**Missingness classes:** source absent; outside listing lifespan; venue outage; endpoint retention limit; collector disconnect; sparse but valid market; API cap; suppressed/filtered event; chain reorg; unknown. Never fill all classes with zeros. Carry a `missing_reason` and a mask used downstream.

**Repair policy:** Prefer primary-source requery within verified retention, then independent *definition-matched* secondary backfill, with audit trail. Interpolated prices may be acceptable only for explicitly bounded descriptive exploratory charts; they are forbidden as invented executable trades, liquidity, queue states, funding prints or liquidation events. Never fill missing bid/ask depth or trade direction by smoothing. If fill is exploratory, retain raw and imputed series and rerun without imputation.

## 7. Financial and microstructure invariants

| Observation | Validator | Exception handling |
|---|---|---|
| OHLCV | `low ≤ min(open, close) ≤ max(open, close) ≤ high`; nonnegative volume; valid price range | Special settlement/zero-price cases require source documentation |
| Best bid/ask | finite valid quotes, `bid ≤ ask`, sizes nonnegative | Crossed books in auctions, batch feeds or transient non-atomic views need venue context |
| L2 book | price-level monotonicity, tick/lot constraints, zero-size delete semantics, checksum/sequence where supplied | Snapshot-only or top-N feed cannot imply hidden depth |
| Trades | unique native IDs when guaranteed, nonnegative quantity, sensible notional after multiplier | Duplicate fills can be legitimate across distinct IDs or split reports |
| Funding | signed rate, exact accrual interval, timestamp of funding **realization** vs indication/forecast | Funding rates from different intervals are not directly comparable |
| OI | contracts vs underlying vs quote units; mapping to multiplier | Open interest from different venues/collateral regimes not additive without normalization |
| Liquidation | event provenance, duplicate handling, side/price/size semantics | Estimated liquidation *levels* are **not** executed liquidations |
| DEX swap | transaction/log/order IDs, token decimals, pool address, reserves, fee tier, exact-in/out status | Reverted and MEV-related legs need event-level handling |
| On-chain transfer | log index, emitting contract, canonical block state and address/bridge classification | Transfers ≠ unique users; bridge flows ≠ necessarily new demand |
| Supply/market cap | circulating vs total vs fully diluted supply, effective timestamps, dilution/locks | market cap is constructed and often retrospectively revised |

**Critical distinction:** a point-in-time `get_orderbook` response establishes a snapshot, not all events between snapshots. A sampled historical book is usable for coarse spread/depth summaries with interval-censoring limitations, not FIFO matching/queue priority or complete market impact simulation. Likewise a candle series cannot replace requested tick trades.

## 8. Cross-provider reconciliation and independence

Before comparing, align `(canonical asset, actual trading venue or explicit consolidated universe, market type, quote denomination, event window, time semantics, aggregation rule, price definition, market status)`. Compare native trades with native trades; book states at matched times; spot mid with spot mid; funding paid with funding paid. A Binance spot last-trade price and Hyperliquid perpetual mark price are different constructs, **not** a quality conflict per se.

Calculate, as applicable: median absolute relative discrepancy `median(|xA-xB| / max(|xA|,|xB|,epsilon))`, signed bias, tail discrepancies, volatility/regime-stratified errors, missingness overlap, disagreement persistence, and revision frequency. For stablecoin quotes, report the time-matched conversion reference and its independent source. Preserve disagreement bands rather than selecting a preferred feed solely because it supports a desired thesis.

**Independence matrix:** primary producer → aggregator/indexer → connector → research payload. Two tools relaying one exchange feed are not independent validations. Blockscout and another indexer can independently transform the same public chain state, but not independently establish economic wallet ownership. Independence is **claim-relative**: independent serialization, capture infrastructure, chain verification, or price discovery may differ.

**Disagreement workflow:** validate identity and units → align clocks → inspect stale/capped pages → identify shared upstream → inspect venue halts/market regime → query primary producer where available → label unresolved observations `CONTESTED`. Do not automatically average suspect providers. For robust aggregation, only experiment with outlier-resistant methods after specifying identification assumptions; record source-selection bias and conduct leave-one-provider-out sensitivity.

Academic grounding: Schwenkler, Shah and Yang report cryptocurrency vendor identifier instability and pricing/volume inconsistencies in a March 2026 revision [R4]; treat it as a **working paper**, not a regulatory standard or evidence that every current provider is wrong.

## 9. Manipulation, adversarial contamination and DEX-specific checks

Wash trading, spoofing, self-dealing and repeated/ephemeral liquidity can bias volume, realized spread, apparent execution capacity and factors. Cong et al. (2023) document significant wash-trading signatures across sampled exchanges [R1]; their **sample-specific** magnitude is not a valid percentage adjustment for a new venue. Sila et al. (2026) further study volatility/sentiment associations [R2]. Use trade-size rounding, digit distributions, tail behavior, zero/near-zero price impact, repeated counterparty patterns *where observable*, order-lifetime distributions and volume-vs-depth divergences as **screening diagnostics, never definitive legal proof**. Control for tick sizes, lot sizes, maker incentives, bots, listing phases and fragmentation; establish reference distributions per instrument/venue/regime.

For AMMs: verify pool contract and fee tier, reserve arithmetic or concentrated-liquidity state at a specific block, actual executable route and fees, pool creation time, transaction ordering, gas/MEV costs, flash liquidity, privileged swaps, protocol upgrades and LP concentration. Differentiate displayed TVL, net economically available exit liquidity and volume. A token pair's quoted price from a dust-sized pool is not automatically an investable market price. Replay historical impact only with adequate historical state and route information.

For oracles and derived pricing: capture observation source, publication cadence, heartbeat/deviation constraints, stale value behavior, constituent composition, governance upgrades and uncertainty from centralized reporting. On-chain verifiability of a posted oracle value does **not** independently validate its off-chain economic measurement.

## 10. Revisions, on-chain reorgs and bitemporal reproducibility

Every restatement generates a new revision with `effective_event_time`, `first_seen_at`, `replaced_at`, prior/new value, source explanation, revision ID and changed-dataset digest. Preserve as-observed (first-available) and latest-corrected datasets; backtests use the former or explicitly justified realistic availability lags. Quantify revision impact on factor ranks, signal flips, portfolio decisions and performance, not just mean absolute revision size.

A removed/reorganized chain event must be tombstoned in canonical-chain views but remain visible in raw capture and forensic views. Maintain separate statuses `OBSERVED_UNFINALIZED`, `CANONICAL_AT_DEPTH_N`, `FINALIZED_PER_CHAIN_POLICY`, `ORPHANED`, `UNKNOWN`. Chain-specific finality and indexing lag require qualification at use time. Historical wallet labels and circulating supply classifications may be revised long after chain finality; do not equate consensus finality with interpretive-data finality.

## 11. Calibration, scorecards and conditional acceptance

A quality *scorecard* informs diagnosis; it does **not** override hard gates. Each use case specifies `decision_horizon`, expected signal magnitude, loss sensitivity, granularity, allowable lag, tolerable missingness and methodological alternative. Calibrate thresholds on an independent validation sample, with costs of false acceptance and false rejection, ideally stratified by volatility and liquidity regime. Avoid “95% complete” or “within 2%” as universal requirements.

**Suggested initial operational thresholds [INTERNAL, UNCALIBRATED]:** zero unresolved identity/unit conflicts for any decision-driving row; zero *known* unrepaired sequence gaps in intervals advertised as fully reconstructable; no `UNKNOWN` point-in-time availability for a claimed historical execution decision unless conservative latency bound passes; all material repairs traceable to originals. Other tolerances must be justified in a preregistered analysis plan rather than supplied as unearned defaults.

A release manifest must report: observed/event window; validated universe and excluded entities; rule pass/fail/unknown counts; coverage *denominator* and gaps; timestamp resolution and lag percentiles; revision count; reconciliation statistics; independent-upstream count; manipulation flags; interpolation/backfill extent; use-case-specific vetoes; stress/sensitivity results; responsible reviewer and expiry trigger. If a metric is uncomputable, record `NOT_MEASURABLE` and why, never zero.

**Quality-adjusted research:** propagate masks and uncertainty into estimates. Compare results on (i) raw admissible observations, (ii) conservative complete-case subset, (iii) alternative matched provider where available, (iv) bounded time shifts, (v) excluded suspect volume/venues, and (vi) revision-aware PIT panel. Report sign/rank changes, interval estimates and sample attrition. Non-random missingness may make complete-case estimation biased; do not declare robustness solely because performance remains positive.

## 12. Concrete acceptance tests and regression fixtures

Build deterministic fixtures that **fail** on: wrong USDT/USD conversion; two contracts sharing a ticker; reversed quote units; token decimal migration; unannounced contract multiplier switch; duplicate page boundary; cursor loops; 1,000-row silent truncation; event-order inversion; WebSocket sequence hole; stale snapshot bridged to deltas; wrong top-N depth claim; millisecond-to-second truncation; revised supply leaked backward; orphaned log treated as final; missed delisting; nontrading candles forward-filled as actual trades; funding annualization mismatch; liquidation estimate reported as print; fake volume passing a naive cross-provider check because providers share an upstream; same symbol on Lighter versus Hyperliquid mistaken for one venue.

**Positive fixtures:** sparse but genuinely inactive asset; legitimate partial candle; zero-size book deletion; exchange-specific matching timestamp ties; documented source revision captured as bitemporal state; DEX liquidity migration with explicit pool identity switch; hard pagination limit detected without asserting coverage completeness.

Each test records exact fixture digest, ruleset commit, expected status, observed status and execution result. Do not claim these tests ran merely because this document specifies them. Property-based and metamorphic tests are useful: reordering non-sequenced responses should not alter unique-key counts; scaling units with corresponding multiplier change should preserve economic notional; duplicating a page must not raise distinct trade count; a late restatement must not affect a past-as-of view.

## 13. Worked audit playbook: 0xArchive Hyperliquid BTC/RUNE and Lighter

1. Resolve **exact instrument ID and venue**, distinguishing native Hyperliquid markets, HIP-3 deployer namespaces and Lighter markets. Do not infer RUNE coverage from BTC coverage or symbol resemblance.
2. Query instrument metadata, then bounded recent and historical trades; record requested vs returned timestamps, raw IDs, field definitions, response truncation, page size and cursor. Repeat with overlapping windows to test whether every exposed row can be enumerated.
3. Separately query **historical book** operations. Inspect if each row is a full book snapshot, top-N sample, event delta, or aggregate. Search for sequence IDs/checksums/continuity contracts; verify whether a seed snapshot exists for each claimed reconstructable interval.
4. Run timestamp precision, monotonicity, key uniqueness, native quantity/price and book invariant checks. Measure changes in coverage around reconnects/outages and record unidentified gaps without false certainty.
5. Query freshness and adjacent fields (trades/candles/OI/funding) only as **cross-checks**; candles cannot repair missing trades or book events. Compare genuinely equivalent data with a second independent feed if callable.
6. Publish separate judgments: `TRADES_HISTORICAL_COVERAGE`, `BOOK_SNAPSHOT_COVERAGE`, `LOSSLESS_BOOK_RECONSTRUCTION`, `DERIVATIVES_SERIES_COVERAGE`, each with scope, first/last **observed** times and `YES/NO/UNDETERMINED`.
7. Re-audit if connector changes, upstream schema changes, quota behavior changes, retention rolls, or a relevant discrepancy emerges. Do not hardcode vendor retention based on an undocumented assumption.

This playbook is **not evidence that these queries succeeded in this writing session**. It operationalizes the accessible 0xArchive tool families without inventing historical coverage or entitlement.

## 14. Output contract: every research dataset carries a QA appendix

```yaml
quality_manifest_version: "1.0"
status: QUARANTINED  # or REJECTED / RESEARCH_APPROVED / EXECUTION_SIM_APPROVED / EXPIRED
purpose: "<precise permissible research use>"
provenance_record_ref: "<document-06-compatible ID>"
tested_at_utc: "<timestamp>"
provider: "<service>"
original_producer: UNKNOWN
venue: "<verified venue>"
asset_id: "<canonical chain/contract/instrument identity>"
market_type: "<spot|perpetual|dated_future|onchain_metric>"
observation_type: "<trades|l2_snapshot|l2_delta|ohlcv|funding|...>"
window_requested_utc: ["<start>", "<end>"]
window_observed_utc: ["<first>", "<last>"]
timestamp_resolution: UNKNOWN
point_in_time_availability: UNKNOWN
pagination:
  row_limit_observed: null
  exhausted: false
  overlap_deduplicated: null
completeness:
  denominator_definition: UNKNOWN
  coverage_fraction: null
  gap_intervals: []
orderbook_reconstruction: UNDETERMINED
external_reconciliation:
  independent_upstream_count: 0
  unresolved_disagreements: []
revision_count: null
rule_results: [] # rule_id, status: PASS|FAIL|UNKNOWN|NOT_APPLICABLE, evidence_ref
repairs: []
sensitivity_results: []
raw_payload_digest: "<sha256>"
normalized_dataset_digest: null
ruleset_version: "<git hash/version>"
limitations: []
reviewer: "<name/role>"
release_timestamp_utc: null
```

**Reviewer decision template:** “For `[asset, venue, period, field]`, `[N]` records returned in `[M]` pages; `[X]` known gaps; timestamp semantics `[... ]`; primary completeness `[verified/not measurable]`; independent reconciliation `[performed/not available]`; use-case `[approved/rejected]`; order-book reconstruction `[YES/NO/UNDETERMINED]`; unresolved issues `[... ]`.” Never label a dataset “clean” without specifying scope and test population.

## 15. Responsibility, change control and limitations

Data stewards own identity and raw acquisition; quantitative researchers own construct validity and sensitivity; execution-research owners own event-level adequacy; an independent reviewer signs research release. Separate those roles where team size permits; otherwise explicitly record role overlap. Trigger revalidation on connector version change, schema change, venue listing/migration, chain fork or reorg, anomalous discrepancy, provider correction, new research horizon, or expiration of an approved sampling window. Audit only legally accessible data; never attempt to bypass controls or quotas.

**Known limitations:** Some tools return curated indicators without full raw lineage; some venue trade IDs are not globally consecutive; high-quality independent feeds may be unavailable; historical API availability cannot always be reconstructed; wash-trade diagnostics are imperfect; block explorers are not consensus proofs; multiple correlated vendors do not produce independent truth. Quality classification describes evidence limitations and is not assurance of future reliability or profitable execution.

## 16. Research and technical references (retrieved/checked 2026-10-22)

**[R1, PEER-REVIEWED]** Cong, L. W., Li, X., Tang, K., & Yang, Y. (2023), “Crypto Wash Trading,” *Management Science* 69(11), 6427–6454. https://doi.org/10.1287/mnsc.2021.02709 — empirically documents anomalous volume signatures in a sampled population of crypto exchanges; not a universal wash-volume adjustment.

**[R2, PEER-REVIEWED]** Sila, J., Kocenda, E., Kristoufek, L., & Kukacka, J. (2026), “Determinants of wash trading in major cryptoexchanges,” *International Review of Financial Analysis* 117, 105283. https://doi.org/10.1016/j.irfa.2026.105283 — evaluates trade roundness and Benford-type diagnostics and their determinants.

**[R3, PEER-REVIEWED]** “Not so fast: Identifying and remediating slow and imprecise cryptocurrency exchange data,” *Finance Research Letters* 51 (2023), 103401. https://doi.org/10.1016/j.frl.2022.103401 — evidence for heterogeneity in exchange matching timestamps and induced liquidity measurement error.

**[R4, WORKING PAPER]** Schwenkler, G., Shah, A., & Yang, D., “Aggregate Confusion In Crypto Market Data,” SSRN, revised March 9, 2026. https://papers.ssrn.com/sol3/papers.cfm?abstract_id=4673905 — cross-vendor audit; publication/peer-review status not verified.

**[R5, STANDARD / OFFICIAL VENUE DOCUMENTATION]** Binance Spot API, “WebSocket Streams — How to manage a local order book correctly.” https://github.com/binance/binance-spot-api-docs/blob/master/web-socket-streams.md — illustrates venue-specific snapshot/delta synchronization; do not transpose its sequence rules to other exchanges.

**[R6, OFFICIAL VENUE DOCUMENTATION]** Coinbase Exchange WebSocket feed guidance. https://help.coinbase.com/en/developer-platform/websocket-feeds/exchange — distinguishes market-data channel semantics and level2 feeds.

**[R7, STANDARD]** W3C, *PROV-DM: The PROV Data Model* (2013). https://www.w3.org/TR/prov-dm/ — provenance graph vocabulary, not a quality guarantee.

**[R8, REGULATORY GUIDANCE]** IOSCO, *Policy Recommendations for Crypto and Digital Asset Markets* (November 2023). https://www.iosco.org/news/pdf/IOSCONEWS712.pdf — market integrity and manipulation concerns, not dataset-specific test thresholds.

**[R9, PROVIDER DISCLOSURE]** CryptoHFTData, “Known Data Gaps & Corrections.” https://www.cryptohftdata.com/docs/data-gaps-and-corrections — example of collector reconnect gaps and venue-specific missingness; not an audit of the connected 0xArchive service.

### Versioning note

This document is a research methodology, **not** a completed live-provider capability audit. Current tool menus were inspected to inform the connector-specific work program. No historical 0xArchive trades/order-book query was executed as part of this document; actual timestamp bounds, pagination and full reconstructability remain to be tested per instrument and period.
