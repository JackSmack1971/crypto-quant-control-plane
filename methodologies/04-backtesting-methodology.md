# 04-backtesting-methodology.md

**Document purpose:** Authoritative methodology for scientifically defensible evaluation of cryptocurrency trading strategies.  
**Version:** 1.1.0  
**Evidence cutoff:** October 22, 2026  
**Primary scope:** Digital currencies and their tradeable spot, perpetual, dated-futures, on-chain pool, and tokenized/outcome-linked markets only where a connected research provider actually exposes the relevant venue and instrument. CEX and on-chain execution are separate simulation regimes. A plugin connection is not itself evidence of historical depth, licensing, account permissions, completeness, or executable access.  
**Prohibition:** This methodology does not authorize trading, does not convert a simulated result into an observed result, and does not permit hypothetical examples to be represented as empirical findings.

## Scope, evidence hierarchy, and research design

### Governing principle

A backtest is an **historical experiment under an explicit information set and an explicit execution model**, not a reconstruction of profits that would necessarily have been earned. The object of validation is therefore not merely a return series. It is the complete chain

\[
\text{historically available information}
\rightarrow
\text{decision rule}
\rightarrow
\text{order}
\rightarrow
\text{execution model}
\rightarrow
\text{position/accounting state}
\rightarrow
\text{net outcome}.
\]

This distinction is necessary because repeated model search can generate apparently exceptional strategies by chance; the usual single-hypothesis significance conventions do not account for the strategy universe searched; serial dependence changes Sharpe-ratio inference; and cryptocurrency markets add venue fragmentation, heterogeneous timestamp quality, manipulated volume, funding, leverage, liquidation, delisting, and unusually important execution frictions. Foundational econometric work on data snooping, multiple testing, Sharpe-ratio inference, and backtest overfitting therefore applies directly, while cryptocurrency microstructure evidence strengthens the case for conservative execution modeling. citeturn24search0turn24search2turn24search4turn0search5turn27search9

### Evidence hierarchy

This file distinguishes evidence types rather than treating every citation as equally authoritative.

| Evidence class | Treatment in this methodology |
|---|---|
| **Peer-reviewed foundational econometrics / finance** | Highest evidentiary weight for inference, multiple testing, bootstrap methods, Sharpe-ratio statistics, market impact, and data-snooping controls. |
| **Peer-reviewed cryptocurrency evidence** | Used to establish crypto-specific empirical risks such as cross-venue fragmentation, data-quality problems, delistings, funding, liquidation, wash trading, and execution sensitivity. |
| **Scholarly monograph / proposed methodology** | Used where important procedures such as purged cross-validation and CPCV originated outside a peer-reviewed journal. Such methods are not treated as universal theorems. |
| **Working paper / SSRN / preprint** | Provisional evidence. It may motivate robustness checks but must not establish a mandatory scientific conclusion by itself. |
| **In-press / journal pre-proof** | Stronger than an informal preprint but still explicitly provisional until final issue publication and any corrections. |
| **Operational control proposed here** | A conservative research-governance rule derived from the cited evidence. It is identified as a protocol rule rather than misrepresented as a published theorem. |

For example, White's Reality Check, Hansen's SPA test, Romano–Wolf stepdown inference, and Harvey–Liu–Zhu's multiple-testing analysis are peer-reviewed econometric evidence. citeturn24search2turn24search3turn20search3turn24search4 Purged cross-validation and combinatorial purged cross-validation are prominently specified in López de Prado's 2018 monograph; a later peer-reviewed synthetic comparison by Arian, Norouzi Mobarekeh, and Seco found CPCV advantageous in its experimental environment, but that result does not prove universal superiority for every financial process. citeturn28search3turn28search0 Recent crypto-specific SSRN studies by Kim and Nefedov are useful warning evidence but remain provisional, whereas Pindza's 2026 study is peer-reviewed and AutoQuant was still an in-press journal pre-proof at the evidence cutoff. citeturn25search0turn25search2turn25search3turn25search4

### Connected-provider venue qualification (October 22, 2026)

**Definition.** An eligible venue is a named matching engine, exchange, or on-chain protocol/chain-pool combination for which at least one connected tool can return verifiable market-specific data. A research provider, token aggregator, or analytics portal is **not** a trading venue. Instrument-by-instrument data scope, not a blanket provider-wide claim, governs backtest eligibility. The actual universe SHALL be materialized at experiment time; this inventory is a discovery map, not a certificate of complete historical access.

| Tool surface discovered in this environment | Venue/data implication | Permitted inference before a test query |
|---|---|---|
| **0xArchive** | Hyperliquid core perpetuals, Hyperliquid Spot, HIP-3 builder markets, HIP-4 outcome markets, Lighter, and a separately exposed Robinhood-connected Lighter API scope (`rh-lighter`). Offers trade, L2, L4 and/or L3 data by market, history, diffs, funding, OI, and coverage/incident tools. | **DISCOVERABLE**, not necessarily replay-complete. Check symbol-specific entitlement, earliest/latest data, pagination, gaps, and update semantics. Do not assume every dataset applies to every scope. |
| **Co-Invest / Liquid** | Liquid-listed instruments with market/positioning/order analyses; venue/instrument catalog must be inspected before inclusion. | Analysis coverage or an instrument listing does **not** demonstrate historical exchange ticks, executable quotes, fills, or qualified order access. |
| **Massive and fin-data MCP** | Market/time-series sources selected by their endpoint catalogs. | Provider endpoint and actual market provenance must be recorded. Aggregated instruments are not a fungible exchange-specific book. |
| **CoinGecko, CoinMarketCap, CoinPaprika, DexPaprika, Dexscreener** where accessible | Identity, market aggregation, DEX pool discovery, quotes and sometimes OHLCV/liquidity. | Discovery/sanity checks only until original venue/pool, history, time and execution data are qualified. |
| **Blockscout, crypto chain analytics, 0xArchive on-chain-adjacent scopes** | Supported EVM chain traces, transaction logs, token and contract information subject to chain/tool availability. | Chain observations can verify transfers/swaps but cannot alone reconstruct mempool order, private order flow, AMM reserves at all decision times, or gas inclusion. |
| **Other discovered crypto/market MCPs** | Potential additional venues or information feeds. | Include only after read-only tool discovery and a per-market capability proof; do not infer capabilities from brand names. |

**Qualification gate (SHALL run before the experiment freezes its eligible universe):**

1. Discover read-only tools and exact argument/response contracts; distinguish connection, authentication, plan entitlement, and dataset availability. Record tool name, version if exposed, account-independent scope, queried UTC window and response time; never store secrets.
2. Discover instrument using native venue identifiers; verify exchange scope, spot/perpetual/future/pool/outcome kind, collateral, settlement, contract version, and eligibility at historical timestamp.
3. Run representative *bounded* historical queries for trades and executable quotes/book (where needed), funding, liquidations, and chain state where applicable. Record actual earliest/latest observation, native granularity, effective record limit, next-cursor behavior, source clock, gaps, revision behavior, deduplication keys, truncation and latency. Tool schema maximum is not proof of accessible history.
4. Run coverage and incident endpoints independently of payload sampling. For 0xArchive prefer `get_symbol_coverage` and `get_data_coverage`, plus dataset-specific freshness/incidents where supported. Reconcile claimed record counts against fully consumed pages; `nextCursor` means the requested range is not yet complete.
5. Mark each `(venue, instrument, data_type, interval)` as **VERIFIED_COMPLETE**, **VERIFIED_PARTIAL**, **SNAPSHOT_ONLY**, **AGGREGATED_ONLY**, **NOT_ENTITLED**, **UNAVAILABLE**, or **UNTESTED**. Only VERIFIED_COMPLETE supplies unqualified historical event replay within the certified interval. VERIFIED_PARTIAL can support explicitly bounded sensitivity analyses, never assertions of full reconstruction.
6. Freeze the completed provenance/coverage report with hashes; if a provider is unavailable, label the test unverified rather than synthesizing reassuring coverage claims.

**0xArchive-specific order-book rule.** Hyperliquid L4 order diffs may include queue-priority insertion metadata (`insert_before` for certain add-liquidity-only events, documented from July 21, 2026 onward). Reconstruct ordering only where the actual captured event stream and initial checkpoint include the necessary order identifiers, insertions, cancellations, fills, and monotonically reconciled state. Lighter L3 checkpoints expose order-level state but checkpoints alone are **not** a continuous historical event log. L2 snapshots do not establish hidden queue priority. Every replay window must verify checkpoint-to-diff linkage, sequence gaps, price/size invariants, depth truncation, pagination exhaustion and, where possible, independent later checkpoints. Never substitute OHLCV, L2 snapshots, or sampled L3 states for missing tick-level order events.

**Consequence:** provider reachability, historical research validity, paper execution qualification, and permission to submit orders are four distinct states. This document authorizes the first two as read-only research tasks only.

### Mandatory research design

Every confirmatory backtest SHALL begin from a frozen **research protocol**. The protocol must identify the hypothesis, estimand, strategy family, decision horizon, holding period, benchmark, data universe, execution model, validation architecture, primary metric, statistical family, robustness tests, and untouched final-test interval before the final test is opened. This requirement operationalizes the central lesson of the data-snooping literature: a result selected after searching many models is statistically different from a single pre-specified hypothesis. citeturn24search0turn24search2turn24search4turn27search0

**Hypothesis.** The protocol must state an economically meaningful null and alternative. A preferred general form is

\[
H_0:\Delta \le \delta_0,
\qquad
H_1:\Delta > \delta_0,
\]

where

\[
\Delta=\theta(S;E)-\theta(B;E)
\]

is the difference between strategy \(S\) and benchmark \(B\) under the **same declared execution environment \(E\)**, and \(\delta_0\) is a predeclared no-value or minimum-relevant-effect boundary. It need not be zero. It must come from the economic use case rather than from a generic Sharpe-ratio convention.

Possible primary estimands include net mean excess return, net expected log-growth increment, a downside-risk-adjusted quantity, certainty-equivalent improvement, or a predeclared forecast-loss difference. Sharpe may be the estimand, but a rule such as “Sharpe above 1” SHALL NOT be treated as a universal scientific validity threshold. Sharpe inference itself depends on sampling uncertainty, non-normality, track-record length, serial dependence, and strategy-selection multiplicity. citeturn0search5turn27search12turn27search0

**Benchmarks.** Benchmarks must be determined before optimization and should represent plausible alternatives for the stated economic question. Examples include buy-and-hold in the same underlying, a cash/collateral benchmark, a volatility-matched passive exposure, a simple momentum/reversal rule, a random-walk forecast, or a factor-matched comparator. Benchmark costs and financing must be modeled consistently with strategy costs. Crypto venue fragmentation means a benchmark on one venue is not automatically interchangeable with an apparently identical instrument on another. citeturn23search1turn23search3

**Experimental unit.** “One bar” SHALL NOT automatically be treated as one independent observation. The experimental unit must follow the estimand and dependence structure: a forecast-decision event for predictive loss, a completed nonoverlapping trade for some trade-level analyses, or preferably common calendar blocks for portfolio-return inference when observations overlap or assets co-move. Serial dependence invalidates naïve independent-observation Sharpe inference, and overlapping labels can mechanically multiply nominal sample size without multiplying independent information. citeturn0search5turn21search1turn22search2

**Strategy universe.** The complete family of tried specifications must be recorded. This includes discarded indicators, assets, venues, lookbacks, thresholds, feature sets, model classes, objective functions, stop rules, cost assumptions, training windows, random seeds where they materially change selection, and manual researcher interventions. White's and Sullivan–Timmermann–White's results make the relevant comparison the family actually searched, not merely the winning model finally disclosed. citeturn24search0turn24search2

**Prediction horizon and holding period.** These are distinct. A five-minute return prediction can support a one-minute, five-minute, or conditional holding rule. Both must be frozen. Label end time \(t_i^{end}\) must be explicitly represented because it determines overlap and purging requirements.

**Discovery versus confirmation.** Discovery may be exploratory, but every experiment must remain in the trial ledger. Once data or an interval has influenced feature selection, model choice, cost assumptions, parameter bounds, asset selection, or stopping decisions, it is no longer untouched confirmatory evidence. A confirmatory phase freezes those choices and applies them to genuinely unconsulted data. Repeatedly checking a “holdout” turns it into part of the training process; an apparent holdout is not protected merely because the optimizer did not receive it directly. This problem motivates both data-snooping tests and alternative Bayesian treatments of backtest overfitting. citeturn24search2turn28search1

**Pre-registration.** Public registration is optional; immutability is not. At minimum, the project should timestamp and hash a machine-readable manifest before final testing. The hash, author, timestamp, version, planned tests, and final-holdout boundaries must be retained in the experiment record.

### Formal information constraint

Let \(\mathcal F_t\) denote the information genuinely available to the modeled trading system by time \(t\). A strategy decision at \(t_d\) must satisfy

\[
D_{t_d}=g(\mathcal F_{t_d}),
\]

and every feature entering \(g\) must be reproducible using only records whose historical availability precedes the decision.

An order cannot execute at \(t_d\) merely because the decision is timestamped \(t_d\). Its earliest eligible venue-arrival time is

\[
t_a =
t_d +
L_{\text{data}}
+
L_{\text{compute}}
+
L_{\text{network}},
\]

with the components either historically observed or explicitly modeled. At high frequency this distinction is economically meaningful: crypto trade records can have heterogeneous timestamp precision and matching-engine delays, and 2026 sub-second evidence documents economically informative trading activity at the 100-millisecond scale. citeturn20search1turn20search6

## Point-in-time data, chronology, and bias controls

### Point-in-time data model

Each research datum should be represented conceptually as a bitemporal or multitemporal record:

```text
instrument_id
venue
valid_from
valid_to
event_time
publication_time
known_at
ingestion_time
source_version
revision_status
value
```

`event_time` is when the economic/market event occurred. `publication_time` is when the source first exposed it. `known_at` is the earliest time the modeled strategy could reasonably have possessed it. `ingestion_time` is when the research system captured the record. `source_version` identifies the revision or backfill used.

The strict as-of join for a decision \(t_d\) is therefore not “give me the latest record whose economic date is before \(t_d\).” It is

\[
x(t_d)=
\operatorname*{arg\,max}_{j}
\{\text{valid\_from}_j:
\text{valid\_from}_j\le t_d,\;
\text{known\_at}_j\le t_d\}.
\]

When historical revisions exist, the permissible record is the version that would have been observable as of \(t_d\), not today's corrected value.

**Protocol rule:** no signal calculation may perform an ordinary database join on timestamp when the right-hand dataset can be revised, reported late, aggregated after the fact, or backfilled. It must use an availability-aware as-of join.

### Historical universe integrity

Cryptocurrency universes are unusually vulnerable to survivorship problems because assets can become inactive, temporarily untradable, or formally delisted. Peer-reviewed 2026 research explicitly studies “zombie” cryptocurrencies that remain nominally extant while becoming untradable, while a separate 2026 Binance study analyzes formal delisting risk. A non-refereed working paper by Ammann and coauthors specifically documents cryptocurrency survivorship and delisting bias and should be treated as provisional supporting evidence rather than definitive peer-reviewed evidence. citeturn26search1turn26search6turn26search8

The universe at time \(t\) SHALL therefore be reconstructed from the instruments eligible **at time \(t\)**. It must not be generated by taking today's exchange list, current market-cap rankings, surviving CoinMarketCap/CoinGecko identifiers, or assets with complete present-day histories and backcasting them into the past.

For each instrument, retain at minimum:

| Required history | Rule |
|---|---|
| Listing time | First realistically tradable timestamp, not merely announcement date. |
| Delisting/suspension time | Last point at which the modeled order could realistically execute. |
| Venue membership | Reconstructed independently for every exchange. |
| Instrument identity | Use stable IDs rather than ticker text; ticker reuse and migrations must not merge unrelated histories. |
| Contract version | Track linear/inverse format, multiplier, quote/settlement currency, tick, lot, margin, and settlement changes. |
| Eligibility | Apply only criteria knowable at the historical selection timestamp. |
| Dead assets | Retain them in earlier universe snapshots and in subsequent loss/exit accounting. |

### Timestamp normalization

Store native exchange timestamp, timestamp precision, receive timestamp if available, and normalized UTC timestamp. Never infer false precision: a source rounded to one second must not be rewritten as if sequencing within that second were known. Foley, Krekel, Mollica, and Svec document materially different matching-engine speeds and timestamp precision across 17 crypto exchanges and show that such issues can distort microstructure measures. citeturn20search1turn20search5

For coincident events whose true ordering is unknown, the simulator must use a deterministic conservative tie-break rule and run alternative orderings when the outcome is sensitive to them. Sub-second cryptocurrency price-discovery evidence further implies that “same second” is not a harmless equivalence class for low-latency strategies. citeturn20search6

### Asset, token, and contract events

The data layer must preserve forks, migrations, redenominations, token swaps, airdrops, chain changes, contract replacements, index composition changes, settlement-currency changes, and other economically material events.

Back-adjustment is permitted for descriptive continuity only when it does not leak future knowledge into the signal. Tradable simulation should instead represent what a historical holder actually owned and when a conversion or entitlement became available.

For derivatives, the point-in-time instrument specification must include at least multiplier, inverse-versus-linear payoff convention, quote/settlement currency, mark/index methodology where relevant, funding schedule, maintenance margin, leverage limits, tick size, quantity step, minimum order rules, expiry/settlement if applicable, and liquidation conventions. Liquidation research on bitcoin derivatives shows why leverage and tail behavior cannot safely be reduced to ordinary unlevered return arithmetic. citeturn20search0turn13search8

### Outages, missing data, revisions, and anomalies

**Missing data is not zero return.** The ingestion pipeline must distinguish:

1. a genuinely quiet market;
2. no trades but valid quotes;
3. exchange outage;
4. WebSocket/API/feed interruption;
5. local recorder failure;
6. historical vendor gap;
7. delisted or suspended instrument.

Forward-filling an executable price through an outage can create impossible exits. For execution simulation, a missing executable quote means execution is unavailable unless another historically eligible venue was explicitly part of the strategy.

**Revisions and backfills** must generate new immutable source versions. A corrected historical candle or funding record may be useful for later accounting but must not retroactively enter an earlier information set unless the correction itself was historically available.

**Price anomalies** may not be deleted merely because they damage performance. Anomaly rules must be specified independently of strategy P&L—for example, impossible negative values, exchange-confirmed bad ticks, or predeclared multi-source consistency checks. Results should normally be shown under both raw and corrected datasets when correction changes conclusions.

Reported cryptocurrency volume also deserves special skepticism. Peer-reviewed studies document large-scale wash trading, direct evidence of self-trading in leaked exchange records, and incentives for centralized exchanges to inflate reported volume. Thus, reported historical volume is an observation about the dataset, not proof that equivalent external liquidity was executable. citeturn29search1turn29search2turn29search3

### Funding settlement and derivatives chronology

A perpetual-futures backtest must distinguish:

\[
\text{forecast/indicative funding information}
\neq
\text{final settlement funding rate}
\neq
\text{funding cash flow}.
\]

A strategy may use only the funding information actually published before its decision. The final settlement value cannot be used to decide whether to hold through that same settlement unless that value was already deterministically known under the venue's historical specification.

For the common sign convention in which positive funding is paid by longs, a simplified linear-contract cash flow is

\[
CF^{fund}_k=-N_k f_k,
\]

where signed notional \(N_k>0\) for a long position and \(f_k\) is the settlement rate. The actual implementation MUST substitute the venue's historical contract-specific formula. Inverse contracts and venues with different mark/notional definitions require different accounting.

Funding is not a minor decoration to derivative returns. Recent research treats it explicitly as a recurring cost/transfer mechanism and finds it time-varying; Inan's paper, available online October 17, 2026, provides particularly recent evidence on the dynamics and out-of-sample predictability of BTC perpetual funding rates across Binance and Bybit. citeturn29search0

### Bias register: detection, example, prevention

The following failures are independent enough that passing one control does not establish absence of the others. Data snooping and multiple testing have extensive formal treatment in the econometrics literature; crypto's changing universe and microstructure add additional implementation channels. citeturn24search0turn24search2turn24search3turn27search0

| Failure | Concrete failure example | Detection | Required prevention |
|---|---|---|---|
| **Look-ahead bias** | Signal uses the completed 12:00 candle and fills at that candle's 12:00 close. | Trace feature dependency and first-availability time to fill timestamp. | Earliest execution is after feature availability, computation, and latency. |
| **Survivorship bias** | Build a 2021 portfolio using the coins that still trade in 2026. | Reconstruct historical exchange/universe membership and inspect missing dead assets. | Point-in-time universe including later delistings and failures. |
| **Selection bias** | Try ten exchanges and publish only the venue with the strongest result. | Compare trial registry with reported strategy family. | Log all venues/markets examined; multiplicity family includes selection dimensions. |
| **Data snooping** | Repeatedly adjust an indicator after inspecting the same OOS period. | Audit code/config timestamps against OOS access history. | Once inspected, the period becomes development data; obtain a new untouched test. |
| **Multiple testing** | Evaluate 500 rules and quote the winner's unadjusted \(p<0.05\). | Count effective trial family and researcher degrees of freedom. | Use family-aware inference: RC, SPA, Romano–Wolf, Holm, DSR, or other predeclared method. |
| **Publication bias** | Failed models are deleted from notebooks before reporting. | Immutable trial ledger versus final report. | Preserve every material run, including negative results. |
| **Overlapping labels** | Every hour predicts the next 24-hour return, then 24 adjacent labels are treated as 24 independent observations. | Compute interval intersections between label windows. | Purging, embargo where needed, and dependence-aware inference/bootstrap. |
| **Target leakage** | Standardize features using full-sample mean/variance or rank coins using future market-cap revisions. | Fit-transform lineage audit; recompute features fold by fold. | All transformations fit strictly inside training information sets. |
| **Optimistic fill assumptions** | A limit order is counted fully filled whenever bar low touches its price. | Replay against quotes/trades/depth; identify touch-only fills. | Queue/depletion or conservative trade-through rules; no automatic full touch fill. |
| **Hyperparameter overfitting** | Tune lookback, threshold, model depth, stop distance, and transaction cost against the “test” period. | Trial ledger, sensitivity surface, nested-validation audit. | Tune only inside training/inner validation; outer and final tests remain untouched. |

A particularly important distinction is that **look-ahead** means future information entered one run, whereas **data snooping/overfitting** can occur even when every individual run is chronologically valid: repeated valid experiments on the same history still select noise. White, Sullivan–Timmermann–White, Harvey–Liu–Zhu, DSR, and PBO address related but different parts of that problem. citeturn24search0turn24search2turn24search4turn27search0turn27search9

## Simulation engines and execution realism

### Simulator classes

| Engine | Appropriate use | Faithful capabilities | What it cannot establish |
|---|---|---|---|
| **Vectorized** | Low-frequency strategies where position at \(t+1\) is a deterministic function of information available by \(t\), and execution can reasonably be reduced to a predeclared price-plus-cost rule. | Fast portfolio arithmetic, simple rebalancing, broad parameter sweeps, accounting checks. | Queue priority, partial fills, asynchronous orders, order cancellation races, liquidation path, intrabar order, venue downtime state, realistic low-latency fills. |
| **Bar-based** | Strategies using OHLCV or similar aggregated observations where intrabar mechanics are not central or are deliberately approximated. | Stops/limits under explicit intrabar conventions, turnover and fee accounting, coarser execution stress tests. | True price path within a bar; order of high/low; whether volume traded before or after an order; exact queue depletion; sub-bar latency. |
| **Event-driven** | Limit-order, market-making, low-latency, leveraged, multi-venue, derivatives, partial-fill, or liquidation-sensitive strategies. | Explicit event order, orders, acknowledgements, cancels, fills, funding, margin, outages, asynchronous venue state. | It still cannot recover information absent from the historical record: hidden liquidity, exact queue identifiers without L3 data, unrecorded exchange internals, or the counterfactual market impact of the strategy's own orders. |

An event-driven engine is therefore **necessary but not sufficient** for many microstructure strategies. Crypto research documents venue-dependent price discovery, heterogeneous matching engines, adverse selection, order-flow impact, and sub-second information processing; a sophisticated software architecture does not make unobserved queue state or counterfactual impact become historical facts. citeturn23search1turn20search1turn3search4turn22search5turn20search6

### Formal accounting

Let \(Q_{j,t}\) be signed position in instrument \(j\), \(M_{j,t}\) its valid mark under the strategy's declared accounting convention, and \(C_t\) cash/collateral. Simplified equity is

\[
E_t=C_t+\sum_j Q_{j,t}M_{j,t}+A_t-L_t,
\]

where \(A_t\) and \(L_t\) include any other receivables, liabilities, borrow, or venue-specific collateral adjustments.

For trade \(i\) changing position by \(\Delta Q_i\) at fill price \(P_i^{fill}\),

\[
\Delta C_i
=
-\Delta Q_i P_i^{fill}
-
Fee_i.
\]

A useful accounting decomposition over a period is

\[
\Delta E
=
\underbrace{\sum_j Q_{j,t^-}\Delta M_{j,t}}_{\text{market move}}
+
\underbrace{\sum_i (M_i-P_i^{fill})\Delta Q_i}_{\text{execution relative to reference}}
-
\underbrace{\sum_i Fee_i}_{\text{fees}}
+
\underbrace{CF^{fund}}_{\text{funding}}
-
\underbrace{CF^{borrow}}_{\text{borrow}}
+
\underbrace{CF^{events}}_{\text{asset/contract events}}
+
\underbrace{CF^{liq}}_{\text{liquidation/forced exit}}.
\]

The decomposition reference \(M_i\) must be specified—typically contemporaneous mid, arrival mid, or another predeclared benchmark—and components must not be double counted.

### Observed facts versus modeled assumptions

A core validation requirement is to label each execution input as **historically observed**, **derived from observed data**, or **modeled**.

| Component | Prefer historical observation | Typical modeled remainder |
|---|---|---|
| Bid/ask | Quotes or L2/L3 snapshots | Spread proxy if quotes unavailable |
| Fees | Point-in-time maker/taker schedule and simulated fee tier | Conservative fee schedule if history missing |
| Slippage | Historical fill versus arrival benchmark when own fills exist | Distribution conditional on size/volatility/spread |
| Market impact | Empirical order-flow/depth calibration | Counterfactual own-order impact |
| Partial fills | L3/order replay where available | Probabilistic/depth-based fill model |
| Queue priority | Exact order identifiers if genuinely available | Initial queue percentile and depletion model |
| Latency | Historical telemetry | Empirical or stress distribution |
| Tick/lot/minimum | Historical contract specification | None; absent history is a data-quality gap |
| Borrow | Historical availability/rate/recall where captured | Stress assumptions |
| Funding | Historical settlement and rules | Forecast availability before settlement |
| Margin/liquidation | Historical specification and mark | Gap/impact during forced execution |
| Downtime | Venue/feed status history | Conservative outage scenario |
| Delisting | Historical suspension/delisting record | Forced-exit recovery assumption if no executable quote |

Market impact is inherently counterfactual because the researcher's hypothetical order did not exist historically. Classical optimal-execution research distinguishes temporary/permanent impact, and empirical order-book research links short-horizon price changes to order-flow imbalance and market depth. These results justify an impact model but do not supply a universal crypto impact coefficient. citeturn22search3turn22search5

### Spread, fees, slippage, and impact

For a buy market order, the correct frictionless comparator is not automatically the last trade or candle close. At minimum, it is the executable ask after strategy latency; larger orders should walk historical depth where such depth exists.

For quantity \(q\) consuming ask levels \((p_\ell,v_\ell)\),

\[
P^{VWAP}(q)
=
\frac{\sum_\ell p_\ell \min(v_\ell,q_\ell^{remaining})}{q},
\]

up to the quantity visible in the recorded book.

If historical depth is insufficient, the strategy must either cap simulated size at observable capacity or introduce a separately identified impact model. It must not silently assume unlimited liquidity at top-of-book.

Maker/taker fee schedules should be point-in-time. If fee tier depends on trailing volume, the tier must arise from simulated historical volume rather than today's account status.

Crypto-specific evidence that reported exchange volume can be fabricated means reported volume alone is not an acceptable capacity proof. citeturn29search1turn29search2turn29search3

### Limit orders, partial fills, and queue priority

The default rule SHALL be:

> **Price touched is not equivalent to order filled.**

When L3 queue data are available, reconstruct position in queue and subsequent executions/cancellations to the extent data semantics allow.

With L2 only, queue location is unobserved. The baseline should model a declared queue assumption and present sensitivity across plausible queue positions. A conservative fill generally requires sufficient subsequent opposite-side marketable flow/depletion after order arrival; “low price ≤ limit price” on an OHLC bar is an upper-bound fill assumption, not a realistic baseline.

Partial fills must persist as partial positions. A simulator may not convert a one-unit executable quantity into a ten-unit completed trade merely because the price level was reached.

Adverse selection should also be recognized: getting filled is not random with respect to subsequent prices. Tiniç finds economically meaningful adverse-selection contributions to crypto effective spreads, while broader order-book research links price changes to order-flow imbalance. citeturn3search4turn22search5

### Latency

At minimum,

\[
L_{total}
=
L_{market\ data}
+
L_{feature}
+
L_{decision}
+
L_{network}
+
L_{venue}.
\]

A strategy may fill only against messages/events that occur after eligible arrival at the venue. Latency should be estimated from historical telemetry where available; otherwise the backtest should use a declared distribution and stress slower alternatives.

This requirement becomes stricter as sampling frequency approaches market-event frequency. Cryptocurrency matching-engine timestamp problems documented by Foley et al. and 100-millisecond price-discovery patterns documented by Shynkevich make subsecond strategies particularly sensitive to unrealistic zero-latency assumptions. citeturn20search1turn20search6

### Borrow, funding, collateral, margin, and liquidation

A short spot position is permissible only when the relevant asset was historically borrowable under the modeled account, with applicable borrow fees and recall/availability constraints. “Shorting” a spot return series without borrowing is not an executable position.

Perpetual funding must be booked at actual settlement eligibility and using the historical contract formula. Funding signs, intervals, mark values, and rate information available before settlement must be separately modeled. citeturn29search0

Leveraged portfolios must maintain a stateful margin account. The simulator should represent, as applicable:

\[
\text{equity},
\quad
\text{initial margin},
\quad
\text{maintenance margin},
\quad
\text{available collateral},
\quad
\text{unrealized P\&L},
\quad
\text{funding},
\quad
\text{fees},
\quad
\text{mark price},
\quad
\text{liquidation threshold}.
\]

Cross margin and isolated margin are not interchangeable. Liquidation uses the venue's historical mark/reference logic rather than an arbitrary candle close. Forced-liquidation research on bitcoin futures and work on automatic liquidation show that leverage and tail events materially change the economics of derivatives positions. citeturn20search0turn13search8

### Downtime, suspension, and forced exits

If a venue is unavailable, the simulator cannot assume orders can be submitted or cancelled there. A position may continue gaining or losing mark-to-market value while the strategy cannot act. If venue mechanics permit liquidation while user order entry is impaired, the model must represent that asymmetry when historical rules support it.

At a delisting or trading suspension, the backtest must not invent a convenient terminal sale at a later reference price. The baseline exit should use the last realistically executable opportunity consistent with notice, strategy latency, and liquidity. If no executable exit exists, the research report must carry an unresolved recovery assumption or conservative loss scenario rather than silently deleting the asset. Evidence that crypto-assets may become untradable before or without straightforward formal disappearance makes this especially important. citeturn26search1turn26search6

### On-chain pool execution and settlement controls

For an AMM/DEX strategy, the executable venue is a **specific chain + protocol + pool/router version + fee tier**; symbol-only identification is insufficient. The event-driven simulator SHALL represent historical pool reserves/liquidity ticks or liquidity positions, swap fee, exact input/output route, price impact, transaction simulation state, gas bid and paid fee, inclusion delay, reverted/dropped transactions, nonce ordering, and block/reorganization finality consistent with chain rules. Bridges add separate settlement, delay, counterparty and depeg risk. Router paths through multiple pools require the correct intermediate token states and fees.

An observed finalized swap is **not** automatically the price available to an order formed earlier: the pre-decision pool state and feasible block inclusion must be reconstructed. Private mempool data and validator/sequencer ordering not recorded historically are unobservable; MEV and sandwich exposure should therefore be stress scenarios, not a fabricated reconstructed fact. Empirical blockchain-currency research finds gas frictions and trader heterogeneity affect DEX execution, and 2026 peer-reviewed MEV evidence documents persistent transaction-ordering risk. [Ranaldo, Viswanath-Natraj & Wang (2026)](https://www.cambridge.org/core/journals/journal-of-financial-and-quantitative-analysis/article/blockchain-currency-markets/31C8A865840FCC2EE51CC667381F9FE1); [*Blockchain: Research and Applications* (2026)](https://www.sciencedirect.com/science/article/pii/S2096720925000673).

**Fail closed:** without point-in-time state and a defensible inclusion model, report a pool-price/route *indicative simulation*, not an executable DEX backtest. A block explorer's successful historical transaction cannot prove that a hypothetical independent order would have obtained the same ordering or price.

### Capacity

Capacity is a strategy property, not a scalar copied from historical volume.

For size \(q\), define net performance

\[
\theta(q)
=
\theta_{\text{gross}}(q)
-
C_{\text{spread}}(q)
-
C_{\text{fees}}(q)
-
C_{\text{slippage}}(q)
-
C_{\text{impact}}(q)
-
C_{\text{funding/borrow}}(q).
\]

A capacity study varies \(q\) while applying realistic participation, depth, queue, and impact constraints. It must stop extrapolating when simulated quantity exceeds defensible market observations. Cross-exchange bitcoin research demonstrates both fragmentation and persistent price differences, so liquidity on one venue cannot simply be pooled with another unless the strategy historically held capital and had executable access there. citeturn23search3

## Validation architecture and statistical inference

### Validation methods

No validation architecture is universally optimal. Each addresses a different failure mode.

| Method | Valid use | Main strength | Main limitation |
|---|---|---|---|
| **Chronological holdout** | Train/tune on earlier history, test once on later history. | Directly mimics time direction. | One test period may be dominated by one regime; repeated inspection contaminates it. |
| **Rolling walk-forward** | Fixed-length training window followed by later test window, repeatedly advanced. | Adapts to nonstationarity and aging data. | Discards older data and creates dependent/possibly overlapping OOS observations. |
| **Anchored/expanding walk-forward** | Training begins at fixed origin and expands before each later test. | Uses increasing sample size. | Old regimes can dominate when relationships drift. |
| **Nested optimization** | Inner loop tunes hyperparameters; outer chronological folds estimate selection performance. | Separates tuning from evaluation. | Computationally expensive; outer folds are still research data if repeatedly interpreted. |
| **Purged CV** | Training observations whose label intervals overlap test labels are removed. | Prevents direct label-overlap leakage. | Does not itself guarantee time-direction realism or solve multiple testing. |
| **Embargo** | Removes an additional region adjacent to a test block. | Reduces leakage from persistent features/information extending beyond labels. | Embargo length is problem-dependent and must not be arbitrary. |
| **CPCV** | Generates many purged train/test combinations and multiple OOS paths. | Characterizes a distribution of OOS outcomes rather than one lucky split. | Some combinations are inferential resamples, not literal chronological deployment histories. |
| **CSCV/PBO** | Measures whether an IS selection process tends to pick models that rank poorly OOS. | Direct diagnostic of selection overfitting. | Depends on a sufficiently rich matrix of strategy trials and stable interpretation of blocks. |

Purged CV and CPCV are associated primarily with López de Prado's monograph; later peer-reviewed research has compared them experimentally, including a 2024 synthetic study that found CPCV strong in its controlled setting. That evidence supports their use as tools, not as an instruction to replace chronological testing automatically. citeturn28search3turn28search0

**Critical distinction:** CPCV can provide valuable inferential distributions while not representing a single historical trading path. A combinatorial split may train on blocks chronologically later than another block included as test. Consequently, this methodology uses purged/CPCV analysis as a robustness and selection diagnostic and requires a separate chronological simulation for claims about deployability.

### Purging rule

For sample \(i\), store its complete information/label interval

\[
I_i=[t_i^{start},t_i^{end}].
\]

If test sample \(j\) has interval \(I_j\), exclude training sample \(i\) whenever

\[
I_i\cap I_j\neq\varnothing.
\]

Purging is therefore determined by interval overlap, not by an arbitrary count of rows.

An embargo may additionally remove training observations whose information windows are sufficiently close to the test interval that state persistence or feature construction could leak test information. Its length should follow the longest relevant feature/label dependency and be predeclared. A “5% embargo” with no substantive basis is not inherently scientific.

### Untouched final test

Every serious confirmatory program should preserve a chronologically latest test interval \(T_F\) that is not used for:

- parameter selection;
- feature engineering;
- venue or asset choice;
- cost-model calibration;
- hyperparameter bounds;
- model-class selection;
- stopping rules;
- metric choice;
- robustness-rule design.

Opening \(T_F\) is a one-way event. After its results have influenced a strategy change, it becomes ordinary research data. A subsequent confirmatory claim requires genuinely new untouched evidence, which may be a later historical period as time accrues or forward paper/shadow testing.

### Sharpe ratio and serial dependence

Let \(x_t=r_t-r_{f,t}\) be the strategy's net excess return at the declared sampling frequency.

\[
\widehat{SR}
=
\frac{\bar x}{s_x}.
\]

The familiar \(\sqrt{q}\) annualization,

\[
\widehat{SR}_{annual}
=
\sqrt q\,\widehat{SR},
\]

is valid only under restrictive scaling assumptions. Lo shows that serial correlation changes Sharpe scaling and can materially alter inference. citeturn0search5

For autocovariance \(\gamma_k=\operatorname{Cov}(x_t,x_{t-k})\), the variance of a \(q\)-period aggregate is

\[
\operatorname{Var}
\left(
\sum_{i=1}^{q}x_i
\right)
=
q\gamma_0+
2\sum_{k=1}^{q-1}(q-k)\gamma_k.
\]

Thus a dependence-aware \(q\)-period Sharpe can be written

\[
SR_q
=
\frac{q\mu}
{\sqrt{
q\gamma_0+
2\sum_{k=1}^{q-1}(q-k)\gamma_k
}}.
\]

For statistical inference, long-run variance may instead be estimated using HAC methods such as Newey–West or by a time-series bootstrap. Newey and West provide the classic heteroskedasticity-and-autocorrelation-consistent covariance estimator; Ledoit and Wolf specifically advocate robust time-series-bootstrap inference for Sharpe-ratio comparisons when returns are heavy-tailed or serially dependent. citeturn21search3turn22search2

### Sortino ratio

For minimum acceptable return \(\tau\),

\[
\widehat{Sortino}
=
\frac{\bar r-\tau}
{
\sqrt{
\frac1T
\sum_{t=1}^{T}
\min(0,r_t-\tau)^2
}
}.
\]

The target \(\tau\), return frequency, and annualization rule must be stated. Sortino and van der Meer developed the downside-risk motivation underlying this family of measures. The statistic is not immune to small-sample error, dependence, threshold choice, or backtest selection merely because it ignores upside volatility. citeturn22search0

### Probabilistic Sharpe Ratio

Bailey and López de Prado define the Probabilistic Sharpe Ratio for benchmark \(SR^*\) as

\[
PSR(SR^*)
=
\Phi
\left[
\frac{
(\widehat{SR}-SR^*)\sqrt{T-1}
}
{
\sqrt{
1
-\hat\gamma_3\widehat{SR}
+
\frac{\hat\gamma_4-1}{4}\widehat{SR}^2
}
}
\right],
\]

where \(\hat\gamma_3\) is sample skewness, \(\hat\gamma_4\) is raw kurtosis, \(T\) is track-record length, and \(\Phi\) is the standard-normal CDF. It is designed to incorporate estimation uncertainty and non-normal higher moments rather than treating an observed Sharpe as exact. citeturn17view0turn27search12

The PSR should normally be computed at the native return frequency used by the derivation rather than by first applying an unjustified IID annualization. Serial dependence, unstable higher moments, structural breaks, and extreme-tail behavior remain material limitations. citeturn0search5turn27search12

### Minimum Track Record Length

For confidence level \(\alpha\), the corresponding minimum track-record approximation is

\[
MinTRL
=
1+
\left[
1
-\hat\gamma_3\widehat{SR}
+
\frac{\hat\gamma_4-1}{4}\widehat{SR}^2
\right]
\left[
\frac{Z_\alpha}
{\widehat{SR}-SR^*}
\right]^2,
\]

with \(Z_\alpha=\Phi^{-1}(\alpha)\). citeturn17view1turn27search12

This is an evidence-sufficiency calculation, not a guarantee that the process is stationary. If returns are strongly dependent, the nominal \(T\) exaggerates independent information. In that case inference should use a dependence-aware effective sample interpretation, lower-frequency nonoverlapping observations where justified, or block/bootstrap methods.

### Deflated Sharpe Ratio

The Deflated Sharpe Ratio addresses two sources of Sharpe inflation: non-normality and selecting a winner from multiple trials. citeturn27search0turn27view0

For \(N\) independent trial Sharpe ratios with variance \(V[\widehat{SR}_n]\), a zero-skill expected-maximum threshold is approximated by

\[
SR_0
=
\sqrt{V[\widehat{SR}_n]}
\left[
(1-\gamma_E)
\Phi^{-1}\left(1-\frac1N\right)
+
\gamma_E
\Phi^{-1}
\left(
1-\frac1{Ne}
\right)
\right],
\]

where \(\gamma_E\approx0.5772\) is the Euler–Mascheroni constant. citeturn20view0

DSR then evaluates

\[
DSR
=
PSR(SR_0)
=
\Phi
\left[
\frac{
(\widehat{SR}-SR_0)\sqrt{T-1}
}{
\sqrt{
1-\hat\gamma_3\widehat{SR}
+\frac{\hat\gamma_4-1}{4}\widehat{SR}^{2}
}
}
\right].
\]

citeturn27view0turn27search0

Real strategy trials are generally correlated, so \(N\) should not automatically equal the raw count of configurations. The complete correlation structure and effective-trial treatment must be reported. DSR does not replace a sealed final holdout: it is a correction for selection evidence, not a license to inspect future data repeatedly.

### Probability of Backtest Overfitting

Bailey, Borwein, López de Prado, and Zhu's PBO framework applies combinatorially symmetric cross-validation to the **strategy-selection process** rather than simply asking whether one return series has a positive mean. citeturn27search9turn27search31

For each CSCV split \(c\):

1. select the strategy with the highest in-sample criterion;
2. compute its percentile rank \(\omega_c\) among strategies out of sample, with higher percentile defined here as better;
3. optionally transform it as

\[
\lambda_c
=
\log
\frac{\omega_c}{1-\omega_c};
\]

4. estimate

\[
\widehat{PBO}
=
\frac1C
\sum_{c=1}^{C}
\mathbf 1(\omega_c\le0.5)
=
\frac1C
\sum_{c=1}^{C}
\mathbf 1(\lambda_c\le0).
\]

A high PBO means that the model-selection process frequently picks an in-sample winner that becomes below-median out of sample. It is a diagnostic, not a universal rejection probability for all kinds of strategies. A Bayesian alternative has also been proposed by Witzany, underscoring that PBO is not the only possible formalization of overfitting uncertainty. citeturn28search1

### White's Reality Check

For candidate strategy \(k\), define performance differential against benchmark

\[
d_{k,t}=L_{0,t}-L_{k,t},
\]

where positive \(d\) means candidate \(k\) has lower loss or better performance.

White's family null is

\[
H_0:
\max_k E[d_{k,t}]\le0.
\]

A simplified statistic is

\[
T_{RC}
=
\max_k \sqrt T\,\bar d_k,
\]

with its null distribution obtained through an appropriate dependence-preserving bootstrap. White developed the Reality Check specifically to address data snooping when many models have been tried. citeturn24search2

Its practical drawback is conservatism when the model universe contains many irrelevant or poor alternatives.

### Hansen's SPA test

Hansen's Superior Predictive Ability test addresses the same broad null but studentizes performance differentials and uses a sample-dependent null treatment intended to reduce the influence of poor alternatives. Hansen's simulations show improved power and lower sensitivity to irrelevant alternatives relative to the original Reality Check. citeturn24search3

SPA remains a test of a defined family against a benchmark. It does not repair data leakage, unrealistic fills, or an undisclosed strategy universe.

### Bootstrap and confidence intervals

When returns are dependent, bootstrap blocks rather than individual rows. Politis and Romano's stationary bootstrap was developed to construct inference under weakly dependent stationary observations and is the resampling mechanism used in important data-snooping procedures. citeturn21search1turn24search2

For multi-asset portfolios, temporal blocks should normally be resampled **jointly across assets**, preserving contemporaneous cross-sectional dependence. Block length is itself a sensitivity parameter and should be reported.

Confidence intervals should be reported for the primary estimand and preferably for important risk-adjusted measures. Studentized time-series-bootstrap confidence intervals are especially suitable for Sharpe comparisons under non-normal, time-series returns. citeturn22search2

Drawdown confidence intervals are more difficult because drawdown is a nonlinear path functional; block-resampled path distributions should be treated as scenario uncertainty rather than as if maximum drawdown were normally distributed.

### Multiple-comparison corrections

Multiplicity control must match the scientific question.

- **Holm stepdown** controls familywise error and is suitable when a relatively small confirmatory family must avoid even one false rejection. Holm's original procedure is sequentially rejective and does not rely on an arbitrary fixed Sharpe cutoff. citeturn21search4turn21search21
- **Benjamini–Hochberg** controls the false discovery rate under its stated dependence conditions and is more natural for exploratory families where some false discoveries are tolerable. citeturn21search0turn21search6
- **Romano–Wolf stepdown** uses the joint distribution of test statistics and can improve power while controlling familywise error in correlated strategy comparisons. citeturn20search3
- **White RC / Hansen SPA** answer the family-level question of whether any searched alternative beats a benchmark. citeturn24search2turn24search3
- **DSR** adjusts a selected Sharpe for the expected winner effect of repeated trials and non-normality. citeturn27search0

No one method dominates every research design. The multiplicity family and correction method must be frozen before confirmatory analysis.

## Performance measurement, robustness, and worked examples

### Return and growth definitions

Let \(W_t\) be net strategy wealth after all modeled costs and financing.

Simple return:

\[
r_t=\frac{W_t}{W_{t-1}}-1.
\]

Log return:

\[
\ell_t=\log\frac{W_t}{W_{t-1}}.
\]

If elapsed calendar time is \(Y\) years,

\[
CAGR
=
\left(
\frac{W_T}{W_0}
\right)^{1/Y}-1
=
\exp
\left(
\frac{\sum_t\ell_t}{Y}
\right)-1.
\]

For cryptocurrency markets, annualization should use declared actual elapsed calendar time rather than mechanically assuming 252 trading days. The exact year-count convention must be documented.

### Volatility

For equally spaced returns under an assumption adequate for descriptive scaling,

\[
\hat\sigma_A
=
\sqrt A\,s_r.
\]

When dependence matters for inference, use long-run variance rather than treating \(\sqrt A\) scaling as exact. The need to adjust Sharpe-related statistics for serial correlation follows directly from Lo's analysis and from HAC/bootstrap econometrics. citeturn0search5turn21search3

### Drawdown and duration

Running peak:

\[
H_t=\max_{u\le t}W_u.
\]

Drawdown:

\[
DD_t=1-\frac{W_t}{H_t}.
\]

Maximum drawdown:

\[
MDD=\max_t DD_t.
\]

Drawdown duration is actual elapsed time from a peak until wealth equals or exceeds the previous peak. An unrecovered drawdown at the sample end is right-censored and must be reported as such rather than assigned an artificial recovery date.

### Calmar ratio

\[
Calmar
=
\frac{CAGR}{MDD}.
\]

The measurement interval must be stated. Calmar is undefined or unstable when the denominator is zero or extremely small and has no simple IID-normal sampling theory.

### Turnover

A transparent gross-notional definition is

\[
Turnover
=
\frac{
\sum_i |\text{trade notional}_i|
}{
\text{average NAV over period}
}.
\]

If a different convention—such as one-half buys plus sells—is used, it must be named explicitly. Turnover is central to crypto backtests because execution costs can dominate weak high-frequency signals; Pindza's peer-reviewed 2026 experiment found that leakage-controlled predictive information in the studied microstructure features did not survive the fees used in its economic evaluation. That is one empirical case, not a universal claim that short-horizon crypto strategies cannot work. citeturn25search0

### Profit factor

With trades defined ex ante,

\[
ProfitFactor
=
\frac{
\sum_{i:P_i>0}P_i
}{
\left|
\sum_{i:P_i<0}P_i
\right|
}.
\]

Trade segmentation must be frozen because splitting or combining executions can alter this statistic without changing portfolio wealth.

### Tail losses

For loss \(L=-r\), Value at Risk at level \(\alpha\) is the relevant loss quantile,

\[
VaR_\alpha
=
Q_\alpha(L),
\]

and Expected Shortfall is

\[
ES_\alpha
=
E[L\mid L\ge VaR_\alpha],
\]

under a continuous-distribution interpretation.

For trading strategies, also report worst realized period, worst gap/slippage event, liquidation loss where applicable, and drawdown tails. Normality should not be presumed; liquidation research finds that normal-tail assumptions can materially understate derivative margin requirements. citeturn20search0

### Benchmark-relative performance

For active return

\[
a_t=r^S_t-r^B_t,
\]

report cumulative active wealth, mean active return, tracking error, and where useful

\[
InformationRatio
=
\frac{\bar a}{s_a},
\]

with serial-dependence-aware inference.

Risk attribution can use a predeclared regression

\[
r^S_t-r_{f,t}
=
\alpha+
\beta^\top F_t+
\epsilon_t,
\]

with HAC or bootstrap uncertainty. Factor selection itself must not become an unreported post-hoc search; the factor-discovery literature shows why hundreds of candidate explanations require multiplicity awareness. citeturn24search4

### P&L attribution

Every backtest intended for serious review should reconcile:

\[
\text{net P\&L}
=
\text{gross signal P\&L}
-
\text{bid/ask}
-
\text{fees}
-
\text{slippage}
-
\text{impact}
+
\text{maker rebates}
+
\text{funding}
-
\text{borrow}
-
\text{liquidation/forced-exit loss}
+
\text{asset-event cash flows}.
\]

This attribution is more informative than net Sharpe alone. It identifies whether apparent alpha is actually fee-tier dependence, funding carry, passive beta, a favorable fill model, or a small gross signal overwhelmed by realistic execution.

The importance of explicit funding, timing, fees, and slippage is also supported by recent crypto work. AutoQuant's 2026 journal pre-proof reports substantial differences between zero/fee-only and more fully costed perpetual simulations, while explicitly acknowledging that its own experiments omit institutional-scale market impact and capacity. It should therefore be treated as useful provisional implementation evidence, not a final authority on costs. citeturn25search1turn25search2

### Forecast-to-order economic validity gate

A predictive metric (accuracy, F1, AUC, cross-sectional rank correlation, directional hit rate) is not an economic estimand. Freeze the transform from forecast to order before validation: threshold, calibration, abstention/no-trade decision, turnover, target sizing, rebalance frequency, and estimated round-trip friction **using only pre-decision information**. Compare the same forecast under a neutral no-trade policy and a simple cost-aware threshold policy, with any searched thresholds included in the trial family. The economic null is assessed on after-cost wealth, not merely predictive skill. Do not train on realized future spreads or select expensive-to-trade observations after seeing outcomes.

Bysik and Ślepaczuk (2026, **preprint**) find that selected hourly BTC prediction configurations with positive gross results fail under an assumed 10-basis-point trading cost; a cost-aware threshold materially changes evaluated economics, but their reported strategy results are not transferable universal parameters. [Preprint](https://arxiv.org/abs/2606.00060). Kim (2026, **SSRN working paper**) similarly distinguishes statistical test success from economic implementation validity. [Working paper](https://doi.org/10.2139/ssrn.6508779).

### Robustness program

Robustness should test whether the conclusion depends on a narrow favorable configuration rather than asking whether every perturbed backtest remains profitable.

| Test | Required design | Warning signal |
|---|---|---|
| **Parameter sensitivity** | Evaluate a predeclared neighborhood/surface around selected values. | Performance exists only at an isolated optimum. |
| **Sampling interval** | Recompute with defensible alternative bars/event aggregation. | Edge disappears after a minor timestamp/bar convention change. |
| **Transaction-cost shocks** | Use baseline historical costs plus empirically plausible stress schedules. | Conclusion reverses under modest cost uncertainty. |
| **Missing-data shocks** | Insert historical-like outage/gap blocks; suppress trading during unavailable observations. | Strategy relies on seamless data during stressed markets. |
| **Delayed signals** | Add one or more realistic event/bar delays and latency distributions. | Edge requires near-zero delay. |
| **Reduced liquidity** | Haircut executable depth and worsen queue/impact assumptions. | Performance requires all displayed liquidity to be available. |
| **Venue holdout** | Re-estimate/replay on separate eligible venues without retuning where possible. | Result is exchange-specific without economic justification. |
| **Regime segmentation** | Predefine regimes independently of strategy P&L. | All evidence comes from one market state. |
| **Crisis periods** | Report behavior during major volatility/liquidity episodes present in the sample. | Tail losses dominate the historical edge. |
| **Randomized trade timing** | Perturb entry timing while preserving approximate exposure/holding rules. | Exact timestamps appear suspiciously indispensable. |
| **Block bootstrap** | Preserve dependence using stationary/moving blocks. | Estimated edge changes sign in much of the resampled distribution. |
| **Capacity** | Increase size through observable depth plus impact assumptions. | Small-account result does not scale beyond negligible size. |

Regime segmentation must not be invented after looking at the strategy equity curve. “Bull,” “bear,” “crisis,” or volatility regimes require an external/predeclared rule.

### Hypothetical example: same-close look-ahead

Assume a one-hour strategy computes

\[
s_t=\mathbf 1(P_t^{close}>MA_t)
\]

from the bar ending 12:00:00 and the original vectorized code enters at \(P_t^{close}\).

That fill is invalid because the complete close-dependent signal does not exist until the closing observation has arrived. A corrected simulation might be:

```text
12:00:00.000  bar closes
12:00:00.080  final source update received
12:00:00.083  feature calculation completes
12:00:00.095  order leaves strategy
12:00:00.110  order eligible at venue
12:00:00.112  first executable ask after arrival
```

The research result must use the post-arrival executable price, not the 12:00 close. These timings are **illustrative only** and are not observations from any exchange.

### Hypothetical example: order-book execution

Suppose the first eligible asks after latency are:

| Ask price | Quantity |
|---:|---:|
| 100.00 | 2 |
| 100.10 | 5 |
| 100.25 | 10 |

A hypothetical five-unit market buy consumes two units at 100.00 and three at 100.10:

\[
VWAP
=
\frac{2(100)+3(100.10)}5
=
100.06.
\]

The simulator then adds the historical/modelled taker fee. Filling all five units at 100.00 because it was the best ask would overstate execution quality.

### Hypothetical example: overlapping labels

Suppose hourly observations predict the next 24-hour return:

\[
y_t=\frac{P_{t+24h}}{P_t}-1.
\]

Labels at 10:00 and 11:00 overlap for 23 hours. A random k-fold split can therefore place almost the same future price path into both training and testing.

The validation dataset should encode

\[
I_t=[t,t+24h],
\]

and purge training labels whose intervals overlap the test interval. An embargo may additionally be necessary where features or model state carry information across the boundary. Purging prevents direct overlap; it does not make the remaining samples fully independent.

### Hypothetical example: DSR and track-record uncertainty

Assume, purely for illustration:

```text
selected daily Sharpe                 = 0.080
number of observations               = 730
sample skewness                      = -0.60
raw kurtosis                         = 5.0
searched strategy variants           = 64
estimated SD of trial Sharpes        = 0.040
```

Using the DSR expected-maximum approximation for 64 **independent** trials gives approximately

\[
SR_0\approx0.0948.
\]

The selected Sharpe of 0.080 is below that multiple-trial benchmark. Applying the DSR formula yields approximately

\[
DSR\approx0.35.
\]

The point is not that 0.35 is a universal rejection threshold. The point is that the same observed Sharpe conveys very different evidence after acknowledging how many opportunities existed to select a winner. The actual DSR analysis must account for correlation among strategy trials. The formulas derive from Bailey and López de Prado. citeturn20view0turn27view0

If the same hypothetical record were tested against \(SR^*=0.02\) at 95% confidence using the MinTRL approximation, the required nominal record would be about 793 observations—longer than the hypothetical 730-observation record. Again, dependence or structural change could make effective evidence even smaller. citeturn17view1

## Reproducibility, experiment schema, and acceptance framework

### Reproducibility contract

A backtest is not reproducible merely because source code exists.

Every reported experiment must retain:

**Data snapshot.** Raw and normalized dataset identifiers; immutable hashes; source/vendor; retrieval timestamp; date coverage; schema; time zone; missing-data report; revision/backfill version; instrument-master version; funding/specification history; and universe snapshot.

**Code version.** Git commit or equivalent immutable source archive for signal code, simulator, preprocessing, portfolio logic, analytics, and report generation.

**Environment.** Language/runtime, operating/container image digest where applicable, exact dependencies, compiler/runtime flags relevant to numerical behavior, database engine/version where query semantics matter, and hardware/GPU details when numerical nondeterminism can affect training.

**Randomness.** Master seed plus component-specific random streams for model initialization, bootstraps, hyperparameter search, queue simulations, latency draws, and Monte Carlo scenarios.

**Execution specification.** Engine version; latency model; fee history source; slippage/impact parameters; queue assumptions; funding rules; margin configuration; order rounding; minimum sizes; event ordering; and forced-exit policy.

**Experiment lineage.** Parent experiment, hypothesis identifier, researcher, creation time, code hash, data hash, parameter set, optimization budget, strategy-family/trial identifier, validation split, and whether the final test was accessed.

**Outputs.** Raw fills, orders, positions, funding transactions, ledger state, equity series, diagnostics, statistical results, generated tables/figures, and output hashes.

Deterministic replay is claimed only if a third party can recreate the normalized data and event sequence from the frozen inputs and obtain the same results within a declared numerical tolerance. AutoQuant's 2026 pre-proof is notable for emphasizing auditable configuration rules and deterministic artifacts in crypto-perpetual research, although its empirical conclusions remain subject to its stated modeling limits. citeturn25search1turn25search2

### Research experiment manifest

A recommended machine-readable schema is:

```yaml
experiment:
  experiment_id: "immutable-uuid"
  protocol_version: "1.0.0"
  created_utc: "YYYY-MM-DDTHH:MM:SSZ"
  preregistration_hash: "sha256:..."
  parent_experiment_id: null
  phase: "discovery|validation|final_test"

hypothesis:
  hypothesis_id: "H-..."
  null: "Delta <= delta_0"
  alternative: "Delta > delta_0"
  estimand: "predeclared net performance difference"
  delta_0: "declared economically relevant boundary"
  primary_metric: "..."
  secondary_metrics: ["..."]
  benchmark: "..."

universe:
  asset_class: "digital_currency_spot|perpetual|future|dex_pool|outcome"
  venues: ["..."]
  membership_rule: "point-in-time rule"
  listing_rule: "..."
  delisting_rule: "..."
  liquidity_rule: "..."
  identity_map_version: "..."
  venue_qualification_report_hash: "sha256:..."
  qualified_data_intervals: ["..."]
  entitlement_and_coverage_status: "..."

data:
  raw_snapshot_hash: "sha256:..."
  normalized_snapshot_hash: "sha256:..."
  instrument_master_hash: "sha256:..."
  start: "..."
  end: "..."
  timezone: "UTC"
  timestamp_precision: "..."
  revisions_version: "..."
  missing_data_policy: "..."
  anomaly_policy: "..."
  source_tool_contracts_hash: "sha256:..."
  pagination_exhausted: false
  orderbook_replay_integrity: "verified|partial|not_applicable|untested"

information_set:
  feature_availability_rules: "..."
  as_of_join_policy: "strict"
  max_feature_lookback: "..."
  label_horizon: "..."
  publication_lag_rules: "..."

strategy:
  source_commit: "..."
  model_class: "..."
  feature_set: ["..."]
  parameter_space: "..."
  holding_period: "..."
  rebalance_rule: "..."
  risk_limits: "..."

execution:
  engine: "vectorized|bar|event"
  engine_version: "..."
  latency_model: "..."
  fee_schedule_snapshot: "..."
  spread_model: "..."
  slippage_model: "..."
  impact_model: "..."
  queue_model: "..."
  partial_fill_policy: "..."
  minimum_order_policy: "..."
  tick_rounding_policy: "..."
  borrow_policy: "..."
  funding_policy: "..."
  margin_model: "..."
  liquidation_model: "..."
  outage_policy: "..."
  forced_exit_policy: "..."
  dex_chain_pool_router_state: "not_applicable|..."
  gas_inclusion_mev_finality_policy: "not_applicable|..."

validation:
  method: "..."
  training_intervals: ["..."]
  validation_intervals: ["..."]
  purge_rule: "..."
  embargo_rule: "..."
  inner_optimization: "..."
  outer_evaluation: "..."
  final_holdout: ["start", "end"]
  final_holdout_access_count: 0

multiplicity:
  trial_family_id: "..."
  total_logged_trials: 0
  correction: "SPA|RC|Holm|Romano-Wolf|DSR|..."
  alpha_or_confidence: "predeclared"
  effective_trial_method: "..."

robustness:
  parameter_sensitivity: "..."
  cost_shocks: "..."
  liquidity_shocks: "..."
  latency_shocks: "..."
  missing_data_shocks: "..."
  venue_holdout: "..."
  regime_tests: "..."
  bootstrap: "..."
  capacity: "..."

reproducibility:
  runtime: "..."
  dependency_lock_hash: "sha256:..."
  container_digest: "..."
  master_seed: "..."
  deterministic_flags: "..."
  output_hash: "sha256:..."
```

### Accounting invariants

Every event-driven backtest should automatically test invariants such as:

\[
\text{ending equity}
=
\text{starting equity}
+
\text{all reconciled P\&L components},
\]

subject to declared rounding tolerance.

Additional invariants should verify that:

- position changes equal signed fills;
- fills never exceed order quantity;
- cancelled quantities cannot subsequently fill unless a race is explicitly modeled;
- prices and quantities respect historical tick/lot rules;
- funding is applied only to eligible position notional at eligible settlements;
- no order executes before its arrival timestamp;
- no feature value is available before `known_at`;
- margin and liquidation transitions reconcile to equity;
- all asset/universe membership is point-in-time;
- raw and normalized input hashes match the manifest.

### Acceptance states

Validation is a structured evidence classification, not a single Sharpe hurdle.

| Status | Scientific meaning |
|---|---|
| **REJECTED** | A decisive methodological defect invalidates the claimed experiment; the frozen hypothesis is materially contradicted by valid confirmatory evidence; realistic execution makes the stated strategy infeasible under its declared use case; or a required integrity gate fails in a way that cannot be repaired without redefining the experiment. |
| **INCONCLUSIVE** | Data or effective sample size is insufficient; confidence intervals include both economically useful and no-value outcomes; key execution assumptions dominate the result; final evidence conflicts across regimes/tests; important historical data are unavailable; or validation cannot distinguish signal from uncertainty. |
| **PROVISIONAL** | Discovery and internal OOS evidence are coherent after major controls, but the final confirmatory period is still untouched, a material execution component remains modeled rather than adequately observed, evidence depends on a narrow environment, or independent/paper validation is not yet available. |
| **VALIDATED_FOR_PAPER_TESTING** | The strategy specification was frozen before an untouched chronological final test; the final result is directionally and economically consistent with the preregistered estimand; multiplicity and dependence were addressed appropriately; plausible execution/cost stresses do not reveal a hidden infeasibility; no material leakage/data-integrity defect remains; and the complete experiment is reproducible. |

**VALIDATED_FOR_PAPER_TESTING does not mean statistically certain, profitable in the future, or qualified for production capital.**

A scientifically defensible decision should consider the joint evidence:

\[
\text{data integrity}
+
\text{protocol integrity}
+
\text{execution feasibility}
+
\text{statistical uncertainty}
+
\text{multiplicity}
+
\text{robustness}
+
\text{reproducibility}
+
\text{untouched evidence}.
\]

### Rejection conditions

The experiment should be **REJECTED without interpreting headline profitability** when any of the following materially affects the primary result:

1. future or revised information enters the signal;
2. historical universe membership cannot be reconstructed and survivorship materially affects the estimand;
3. the winning strategy cannot be tied to the full searched trial family;
4. final-test data were used to change the specification;
5. execution precedes signal availability;
6. the strategy assumes impossible shorting, leverage, order size, tick, lot, margin, or venue access;
7. purported fills cannot be supported by a defensible execution model;
8. funding or liquidation accounting is materially wrong for a derivatives strategy;
9. the ledger does not reconcile;
10. the data snapshot or code cannot be identified sufficiently to reproduce the claimed test.

The appropriate response to a defective backtest is not to add a statistical penalty to its Sharpe. Statistical corrections operate on valid experiments; they do not sanitize invalid chronology or fictitious execution.

### Inconclusive conditions

A strategy should generally remain **INCONCLUSIVE** rather than be forced into pass/fail when:

\[
CI(\Delta)
\]

contains both the predeclared no-value region and economically meaningful positive outcomes; the effective track record is too short; higher-moment estimates used by PSR/DSR are unstable; PBO/DSR/SPA and chronological evidence materially disagree; plausible cost assumptions span profitable and unprofitable outcomes; or the required historical fill/liquidity information is too incomplete to choose between those cases.

This treatment is preferable to inventing a universal Sharpe requirement. PSR/MinTRL explicitly demonstrate how the evidentiary meaning of a Sharpe estimate varies with record length, skewness, kurtosis, and benchmark; DSR adds the number/effective number of trials. citeturn27search12turn27search0

### Statistical validation versus production execution qualification

Statistical validation asks whether historical evidence supports the preregistered estimand after reasonable controls.

Production qualification is a different problem. It additionally requires evidence about actual order-routing behavior, live/paper fill discrepancies, current venue connectivity, monitoring, stale-data detection, operational limits, kill/disable mechanisms, counterparty/custody constraints, capacity calibration, and failure recovery.

Therefore:

\[
\text{historically validated}
\not\Rightarrow
\text{production qualified}.
\]

The required terminal state of this methodology is deliberately **VALIDATED_FOR_PAPER_TESTING**, not “approved to trade.”

## Evidence traceability, bibliography, and version policy

### Evidence-to-rule traceability matrix

| Rule ID | Methodological rule | Principal evidence | Evidence status |
|---|---|---|---|
| **RD-01** | Separate discovery from untouched confirmation. | White; Sullivan–Timmermann–White; Harvey–Liu–Zhu. citeturn24search0turn24search2turn24search4 | Peer reviewed |
| **RD-02** | Log the complete searched strategy family. | White; DSR; PBO. citeturn24search2turn27search0turn27search9 | Peer reviewed |
| **DATA-01** | Use strict point-in-time availability rather than latest revised data. | Data-snooping logic plus crypto timestamp-quality evidence. citeturn24search2turn20search1 | Peer reviewed + operational control |
| **DATA-02** | Reconstruct historical listings, delistings, and inactive assets. | Będowska-Sójka et al.; Yang–Kwon; Ammann et al. citeturn26search1turn26search6turn26search8 | Peer reviewed + working paper |
| **DATA-03** | Do not assume reported volume equals executable liquidity. | Cong et al.; Aloosh–Li; Amiram–Lyandres–Rabetti. citeturn29search1turn29search2turn29search3 | Peer reviewed |
| **TIME-01** | Preserve native timestamp precision and latency. | Foley et al.; Shynkevich. citeturn20search1turn20search6 | Peer reviewed |
| **BIAS-01** | Correct family-level data snooping/multiple testing. | White; Hansen; Romano–Wolf. citeturn24search2turn24search3turn20search3 | Peer reviewed |
| **BIAS-02** | Do not use conventional single-test significance after broad factor search. | Harvey–Liu–Zhu. citeturn24search4 | Peer reviewed |
| **SIM-01** | Match simulator fidelity to order/execution complexity. | Market-impact and crypto-microstructure evidence. citeturn22search3turn22search5turn20search1 | Peer reviewed + operational control |
| **EXEC-01** | Marketable fills consume executable spread/depth after latency. | Cont–Kukanov–Stoikov; crypto fragmentation studies. citeturn22search5turn23search3 | Peer reviewed |
| **EXEC-02** | Touching a limit price is not automatic full execution. | Order-book/impact/adverse-selection evidence. citeturn22search5turn3search4 | Peer reviewed + operational control |
| **EXEC-03** | Funding is point-in-time and settlement-specific. | Inan. citeturn29search0 | Peer reviewed/advance online as of cutoff |
| **EXEC-04** | Margin and liquidation mechanics must be stateful. | Cheng et al.; Alexander–Deng–Zou. citeturn20search0turn13search8 | Peer reviewed |
| **VAL-01** | Purge overlapping label intervals. | López de Prado; later CPCV comparison. citeturn28search3turn28search0 | Monograph + peer reviewed |
| **VAL-02** | CPCV is a robustness/inference tool, not automatically a literal chronological path. | López de Prado CPCV construction; comparative evidence. citeturn28search3turn28search0 | Monograph + operational interpretation |
| **STAT-01** | Adjust Sharpe inference for serial dependence. | Lo; Newey–West; Ledoit–Wolf. citeturn0search5turn21search3turn22search2 | Peer reviewed |
| **STAT-02** | Use PSR/MinTRL to quantify Sharpe uncertainty when assumptions are suitable. | Bailey–López de Prado. citeturn27search12turn17view0turn17view1 | Peer reviewed |
| **STAT-03** | Deflate selected Sharpe for strategy-search multiplicity. | Bailey–López de Prado DSR. citeturn27search0turn27view0 | Peer reviewed |
| **STAT-04** | Diagnose selection overfitting with PBO where trial matrix supports it. | Bailey et al. citeturn27search9turn27search31 | Peer reviewed |
| **STAT-05** | Preserve time dependence in bootstrap inference. | Politis–Romano. citeturn21search1 | Peer reviewed |
| **ROB-01** | Stress fees, slippage, timing, and evaluation-window reuse in crypto derivatives. | Pindza; AutoQuant. citeturn25search0turn25search2 | Peer reviewed + in press |
| **REPRO-01** | Freeze data, code, configuration, and deterministic artifacts. | AutoQuant plus proposed governance. citeturn25search1 | In press + operational control |
| **ACC-01** | Do not use a universal Sharpe cutoff as scientific acceptance. | Lo; PSR/MinTRL; DSR. citeturn0search5turn27search12turn27search0 | Peer reviewed |

### Research synthesis through October 20, 2026

The foundational literature reaches a consistent high-level conclusion despite methodological differences: the apparent best strategy selected from a large research universe should not be evaluated as though it had been proposed in isolation. Sullivan, Timmermann, and White operationalized this problem for technical trading rules; White formalized a family-level Reality Check; Hansen increased power with SPA; Harvey, Liu, and Zhu showed why conventional significance becomes inappropriate after broad factor searches; Romano and Wolf developed dependence-aware stepwise multiple testing; and Bailey and collaborators developed PSR, DSR, and PBO as complementary diagnostics focused on Sharpe uncertainty and backtest selection. citeturn24search0turn24search2turn24search3turn24search4turn20search3turn27search0turn27search9

These tools are **competing and complementary rather than interchangeable**. White RC/SPA test a family relative to a benchmark; Holm/Romano–Wolf control hypothesis-testing errors; PSR asks how probable it is that a Sharpe exceeds a benchmark under its approximation; DSR shifts that benchmark to reflect winner selection; PBO evaluates how often the selection rule chooses strategies that subsequently rank poorly; nested chronological validation estimates tuning performance; and purging/embargo address information overlap. None repairs an invalid historical information set or fictional execution. citeturn24search2turn24search3turn20search3turn27search0turn27search9turn28search3

Cryptocurrency evidence adds reasons to be stricter rather than looser. Prices and information are fragmented across exchanges; liquidity measurement is venue- and measure-sensitive; timestamps and matching-engine behavior can be problematic; reported volume can be manipulated; delistings and temporary non-tradability matter; perpetual contracts add recurring funding; and leveraged derivatives introduce state-dependent liquidation. citeturn23search3turn23search0turn20search1turn29search1turn26search1turn29search0turn20search0

The newest literature as of the cutoff is informative but must be weighted by publication status. Pindza's June 2026 peer-reviewed crypto-microstructure experiment reports that leakage-aware validation and realistic fees overturned stronger naïve machine-learning impressions in its sample. citeturn25search0 In contrast, Kim's VALID framework and Nefedov's crypto-factor audit are SSRN working papers and remain provisional despite findings strongly aligned with the older overfitting literature. citeturn25search3turn25search4 Wang, Zeng, Li, and Wang's “Training Set Delusion” is likewise a working paper, so its conclusion that strict OOS testing substantially weakens apparent Bitcoin ML predictability should be treated as provisional. citeturn26search0turn26search3 AutoQuant was a journal pre-proof available online in August 2026 and is useful for execution-aware auditability, while Inan's funding-rate study was available online only three days before this document's cutoff. citeturn25search2turn29search0

### Additional evidence and technical source audit (October 22, 2026)

- Ranaldo, A., Viswanath-Natraj, G., & Wang, J. (2026). “Blockchain Currency Markets.” *Journal of Financial and Quantitative Analysis*, published online April 13, 2026. **Peer reviewed.** https://www.cambridge.org/core/journals/journal-of-financial-and-quantitative-analysis/article/blockchain-currency-markets/31C8A865840FCC2EE51CC667381F9FE1
- “Linking MEV attacks to further maximise attackers’ gains: evidence from the Ethereum blockchain.” (2026). *Blockchain: Research and Applications*, 7(3), 100340. **Peer reviewed.** https://doi.org/10.1016/j.bcra.2025.100340
- Bysik, A., & Ślepaczuk, R. (2026). “Machine Learning-Based Bitcoin Trading Under Transaction Costs: Evidence From Walk-Forward Forecasting.” arXiv:2606.00060. **Preprint; provisional.** https://arxiv.org/abs/2606.00060
- Kim, J. (2026). “Beyond Accuracy: A Validation Framework for Machine Learning in Cryptocurrency Trading.” SSRN, revised August 3, 2026. **Working paper; provisional.** https://doi.org/10.2139/ssrn.6508779
- 0xArchiveIO. “0xarchive-mcp,” official repository and read-only tool descriptions, consulted October 22, 2026. **Provider documentation, not academic validation or evidence of subscription entitlement.** https://github.com/0xArchiveIO/0xarchive-mcp

### Verified bibliography

**Arian, H., Norouzi Mobarekeh, D., & Seco, L.** “Backtest overfitting in the machine learning era: A comparison of out-of-sample testing methods in a synthetic controlled environment.” *Knowledge-Based Systems* (2024), DOI 10.1016/j.knosys.2024.112477. **Peer reviewed.** citeturn28search0

**Aloosh, A., & Li, J.** “Direct Evidence of Bitcoin Wash Trading.” *Management Science* 70(12), 8875–8921 (2024), DOI 10.1287/mnsc.2021.01448. **Peer reviewed.** citeturn29search2

**Almgren, R., & Chriss, N.** “Optimal Execution of Portfolio Transactions.” *Journal of Risk* (2001), DOI 10.21314/JOR.2001.041. **Peer reviewed.** citeturn22search3

**Alexander, C., Deng, Y., & Zou, B.** “Hedging with automatic liquidation and leverage selection on bitcoin futures.” *European Journal of Operational Research* 306(1), 478–493 (2023), DOI 10.1016/j.ejor.2022.07.037. **Peer reviewed.** citeturn13search8

**Amiram, D., Lyandres, E., & Rabetti, D.** “Trading Volume Manipulation and Competition Among Centralized Crypto Exchanges.” *Management Science* 71(10), 8604–8622 (2025), DOI 10.1287/mnsc.2021.02903. **Peer reviewed.** citeturn29search3

**Ammann, M., Burdorf, T., Liebi, L., & Stöckl, S.** “Survivorship and Delisting Bias in Cryptocurrency Markets.” SSRN working paper (2022). **Working paper; non-refereed evidence.** citeturn26search8

**Bailey, D. H., Borwein, J. M., López de Prado, M., & Zhu, Q. J.** “The Probability of Backtest Overfitting.” *Journal of Computational Finance* 20(4), 39–69 (2017), DOI 10.21314/JCF.2016.322. **Peer reviewed.** citeturn27search9turn27search31

**Bailey, D. H., & López de Prado, M.** “The Sharpe Ratio Efficient Frontier.” *Journal of Risk* 15(2), 3–44 (2012). **Peer reviewed; source of PSR and MinTRL.** citeturn27search12turn27search24

**Bailey, D. H., & López de Prado, M.** “The Deflated Sharpe Ratio: Correcting for Selection Bias, Backtest Overfitting, and Non-Normality.” *Journal of Portfolio Management* 40(5), 94–107 (2014), DOI 10.3905/jpm.2014.40.5.094. **Peer reviewed.** citeturn27search0

**Będowska-Sójka, B., Wójcik, P., & Pele, D. T.** “Early warning systems for cryptocurrency markets: Predicting ‘zombie’ assets using machine learning.” *North American Journal of Economics and Finance* 81, 102543 (2026), DOI 10.1016/j.najef.2025.102543. **Peer reviewed.** citeturn26search1turn26search14

**Benjamini, Y., & Hochberg, Y.** “Controlling the False Discovery Rate: A Practical and Powerful Approach to Multiple Testing.” *Journal of the Royal Statistical Society: Series B* 57(1), 289–300 (1995), DOI 10.1111/j.2517-6161.1995.tb02031.x. **Peer reviewed.** citeturn21search0turn21search6

**Brandvold, M., Molnár, P., Vagstad, K., & Valstad, O. C. A.** “Price discovery on Bitcoin exchanges.” *Journal of International Financial Markets, Institutions & Money* 36, 18–35 (2015), DOI 10.1016/j.intfin.2015.02.010. **Peer reviewed.** citeturn23search1

**Brauneis, A., Mestel, R., Riordan, R., & Theissen, E.** “How to measure the liquidity of cryptocurrency markets?” *Journal of Banking & Finance* 124, 106041 (2021), DOI 10.1016/j.jbankfin.2020.106041. **Peer reviewed.** citeturn23search0

**Cheng, Z., Deng, J., Wang, T., & Yu, M.** “Liquidation, leverage and optimal margin in bitcoin futures markets.” *Applied Economics* 53, 5415–5428 (2021), DOI 10.1080/00036846.2021.1922597. **Peer reviewed.** citeturn20search0

**Cong, L. W., Li, X., Tang, K., & Yang, Y.** “Crypto Wash Trading.” *Management Science* 69(11), 6427–6454 (2023), DOI 10.1287/mnsc.2021.02709. **Peer reviewed.** citeturn29search1

**Cont, R., Kukanov, A., & Stoikov, S.** “The Price Impact of Order Book Events.” *Journal of Financial Econometrics* 12(1), 47–88 (2014), DOI 10.1093/jjfinec/nbt003. **Peer reviewed.** citeturn22search5

**Deng, K.** “AutoQuant: An auditable expert-system framework for execution-constrained auto-tuning in cryptocurrency perpetual futures.” *Expert Systems with Applications*, article 133924, available online August 5, 2026, DOI 10.1016/j.eswa.2026.133924. **Journal pre-proof/in press at the evidence cutoff.** citeturn25search1turn25search2

**Foley, S., Krekel, W., Mollica, V., & Svec, J.** “Not so fast: Identifying and remediating slow and imprecise cryptocurrency exchange data.” *Finance Research Letters* 51, 103401 (2023), DOI 10.1016/j.frl.2022.103401. **Peer reviewed.** citeturn20search1turn20search5

**Hansen, P. R.** “A Test for Superior Predictive Ability.” *Journal of Business & Economic Statistics* 23(4), 365–380 (2005), DOI 10.1198/073500105000000063. **Peer reviewed.** citeturn24search3

**Hansen, P. R., Lunde, A., & Nason, J. M.** “The Model Confidence Set.” *Econometrica* 79(2), 453–497 (2011), DOI 10.3982/ECTA5771. **Peer reviewed.** citeturn27search1turn27search3

**Harvey, C. R., Liu, Y., & Zhu, H.** “… and the Cross-Section of Expected Returns.” *Review of Financial Studies* 29(1), 5–68 (2016), DOI 10.1093/rfs/hhv059. **Peer reviewed.** citeturn24search4

**Holm, S.** “A Simple Sequentially Rejective Multiple Test Procedure.” *Scandinavian Journal of Statistics* 6(2), 65–70 (1979). **Peer reviewed.** citeturn21search4turn21search21

**Inan, E.** “Predictability of funding rates.” *International Review of Financial Analysis*, article 105464, available online October 17, 2026, DOI 10.1016/j.irfa.2026.105464. **Peer-reviewed journal article available online at the evidence cutoff; very recent and therefore treated cautiously.** citeturn29search0

**Kim, J.** “Beyond Accuracy: A Validation Framework for Machine Learning in Cryptocurrency Trading.” SSRN, posted April 28, 2026; revised August 3, 2026. **Working paper; provisional.** citeturn25search3

**Ledoit, O., & Wolf, M.** “Robust performance hypothesis testing with the Sharpe ratio.” *Journal of Empirical Finance* 15(5), 850–859 (2008), DOI 10.1016/j.jempfin.2008.03.002. **Peer reviewed.** citeturn22search2turn22search7

**Lo, A. W.** “The Statistics of Sharpe Ratios.” *Financial Analysts Journal* 58(4) (2002), DOI 10.2469/faj.v58.n4.2453. **Peer reviewed.** citeturn0search5

**López de Prado, M.** *Advances in Financial Machine Learning*. Wiley, 2018. Chapters on purged k-fold cross-validation and combinatorial purged cross-validation. **Scholarly monograph; methodology source, not a peer-reviewed journal test of universal superiority.** citeturn28search3turn28search11

**Makarov, I., & Schoar, A.** “Trading and Arbitrage in Cryptocurrency Markets.” *Journal of Financial Economics* 135(2), 293–319 (2020), DOI 10.1016/j.jfineco.2019.07.001. **Peer reviewed.** citeturn23search3turn23search6

**Nefedov, S.** “How Much Sharpe is Illusory? Quantifying Backtest Overfitting in Crypto Factor Strategies.” SSRN, posted August 27, 2026. **Working paper; provisional.** citeturn25search4

**Newey, W. K., & West, K. D.** “A Simple, Positive Semi-Definite, Heteroskedasticity and Autocorrelation Consistent Covariance Matrix.” *Econometrica* 55(3), 703–708 (1987). **Peer reviewed.** citeturn21search3turn21search17

**Pindza, E.** “Microstructure alpha: hierarchical learning and cross-asset transfer in cryptocurrency markets.” *Frontiers in Blockchain* 9 (2026), DOI 10.3389/fbloc.2026.1811716. **Peer reviewed.** citeturn25search0

**Politis, D. N., & Romano, J. P.** “The Stationary Bootstrap.” *Journal of the American Statistical Association* 89(428), 1303–1313 (1994), DOI 10.1080/01621459.1994.10476870. **Peer reviewed.** citeturn21search1

**Romano, J. P., & Wolf, M.** “Stepwise Multiple Testing as Formalized Data Snooping.” *Econometrica* 73(4), 1237–1282 (2005), DOI 10.1111/j.1468-0262.2005.00615.x. **Peer reviewed.** citeturn20search3

**Shynkevich, A.** “Price discovery in cryptocurrency markets: sub-second evidence.” *Economics Letters* 266, 113026 (2026), DOI 10.1016/j.econlet.2026.113026. **Peer reviewed.** citeturn20search6

**Sortino, F. A., & van der Meer, R.** “Downside Risk: Capturing What's at Stake in Investment Situations.” *Journal of Portfolio Management* 17(4), 27–31 (1991), DOI 10.3905/jpm.1991.409343. **Peer reviewed.** citeturn22search0

**Sullivan, R., Timmermann, A., & White, H.** “Data-Snooping, Technical Trading Rule Performance, and the Bootstrap.” *Journal of Finance* 54(5), 1647–1691 (1999), DOI 10.1111/0022-1082.00163. **Peer reviewed.** citeturn24search0

**Tiniç, M.** “Adverse selection in cryptocurrency markets.” *Journal of Financial Research* 46(2), 497–546 (2023), DOI 10.1111/jfir.12317. **Peer reviewed.** citeturn3search4

**Wang, J., Zeng, C., Li, N., & Wang, Q.** “The Training Set Delusion: Machine Learning Overfitting in Bitcoin Return and Volatility Prediction.” SSRN 5797242, dated November 24, 2025 and circulating through 2026. **Working paper; provisional.** citeturn26search0turn26search3

**White, H.** “A Reality Check for Data Snooping.” *Econometrica* 68(5), 1097–1126 (2000), DOI 10.1111/1468-0262.00152. **Peer reviewed.** citeturn24search2

**Witzany, J.** “A Bayesian Approach to Measurement of Backtest Overfitting.” *Risks* 9(1), 18 (2021), DOI 10.3390/risks9010018. **Peer reviewed; alternative formulation of overfitting uncertainty.** citeturn28search1

**Yang, S., & Kwon, H.** “Developing Predictive and Explainable Models for Cryptocurrency Delistings: A Case Study of Binance Exchange.” *Asia-Pacific Journal of Financial Studies* (2026), DOI 10.1111/ajfs.70045. **Peer reviewed.** citeturn26search6turn26search11

### Version policy and update triggers

This file follows semantic methodology versioning:

```text
MAJOR.MINOR.PATCH

MAJOR
  Changes the scientific interpretation of prior results:
  inference framework, validation architecture, chronology rule,
  execution semantics, acceptance state, or core accounting.

MINOR
  Adds a new control, simulator capability, robustness test,
  evidence class, market type, or reporting requirement without
  invalidating correctly produced prior results.

PATCH
  Corrects wording, citations, examples, metadata, or other
  non-analytic defects.
```

A review is mandatory when any of the following occurs:

- new peer-reviewed evidence materially challenges PSR, DSR, PBO, CPCV, SPA, bootstrap, or other core validation logic;
- an exchange changes funding, fee tiers, tick/lot constraints, margin, liquidation, order priority, contract multipliers, or matching-engine semantics relevant to a maintained strategy;
- a data vendor announces historical revisions or the project detects previously unknown timestamp/backfill errors;
- the simulator changes event ordering, fill logic, collateral accounting, liquidation handling, or cost decomposition;
- live/paper execution materially disagrees with simulated spread, latency, queue, impact, or funding assumptions;
- the strategy expands from centralized venues to DEX execution, where gas, block ordering, MEV, reorgs, failed transactions, bridge risk, and smart-contract state require additional methodology;
- a material class of assets, derivatives, or collateral is added;
- a previously untouched final period is opened and subsequently used to modify the strategy;
- a reproducibility replay fails;
- a significant accounting invariant fails;
- a severe market event exposes an unmodeled operational state.

The update process must preserve prior versions and state whether the change would have altered historical strategy acceptance. A methodological revision must never be silently applied retroactively to make a previously failed strategy appear to have passed.

The governing scientific rule is therefore:

\[
\boxed{
\text{Credible backtest evidence}
\neq
\text{best historical equity curve}
}
\]

but rather

\[
\boxed{
\text{credible evidence}
=
\text{point-in-time data}
+
\text{valid chronology}
+
\text{realistic execution}
+
\text{controlled model search}
+
\text{dependence-aware inference}
+
\text{robustness}
+
\text{reproducibility}
+
\text{untouched confirmation}.
}
\]

That standard is deliberately conservative. The financial-econometrics literature shows why repeated search inflates apparent discoveries, while the cryptocurrency literature adds venue fragmentation, data-quality problems, manipulated volume, funding, liquidation, and delisting as concrete channels through which historically attractive results can fail to correspond to executable evidence. citeturn24search2turn24search4turn27search0turn23search3turn20search1turn29search1turn29search0turn20search0