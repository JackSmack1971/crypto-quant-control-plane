# 05-portfolio-risk-methodology.md

## Portfolio Risk Methodology: Quantitative Foundations and Empirical Framework for Digital Currencies

**Revision:** 2026-10-22  
**Scope:** Spot digital currencies, stablecoins, wrapped and bridged tokens, tokenized claims, lending and liquidity-provider positions, perpetual and dated futures, and options **only where the connected data venue and account/instrument support are demonstrated**.  
**Status:** Research methodology and paper-risk governance; **not** an assertion of a deployed risk engine, approved investment mandate, live account access, or authority to trade.

### Methodological principles and evidence grades

Cryptocurrency returns frequently exhibit heavy tails, volatility clustering, regime dependence and episodic liquidity loss. These characteristics motivate **comparative forecasting, conservative scenario analysis and independent validation**, not the claim that any one model is universally reliable. The purpose of portfolio risk analysis is to estimate losses that may arise under a specific portfolio state, horizon, market path and executable venue set; to expose model uncertainty; and to define explicit escalation when inputs are missing or contradictory.

- **Empirical finding [E]:** independently published and dated evidence about observed market behavior; generalization beyond the study sample must be justified.
- **Research candidate [R]:** estimator or construction rule requiring a pre-registered, point-in-time, cost-inclusive out-of-sample comparison.
- **Operational policy [P]:** proposed portfolio control; thresholds are *not* empirical laws, are inactive until approved and calibrated, and do not authorize execution.
- **Verified capability [V]:** tool operation and asset/venue/date range actually queried in the current investigation; a listed tool is not equivalent to demonstrated coverage.
- **Unverified [U]:** missing observations, undocumented venue features, estimated historical depth, extrapolated parameters or unsupported execution capability. Do not silently promote U to V.

Risk estimates must state: `as_of_utc`, `portfolio_snapshot_id`, quote/base currency, instrument and venue identifiers, lookback period, sampling frequency, holding/liquidation horizon, marks and their freshness, model version, parameter calibration period, missing-data fraction, confidence/uncertainty interval if estimable, and stress assumptions. Separate **observed data, model estimates, hypothetical shocks, and policy decisions** in every report.

### 1. Portfolio Accounting Foundations

Risk begins with a reconciled **position-and-collateral ledger** at an exact timestamp, not a stitched together collection of current prices. For instrument *i* record signed contract units `q_i`, contract multiplier `m_i`, settlement asset, mark and index price, executable bid/ask, entry basis, realized/unrealized P&L, funding accrual, fees, borrow liability, collateral encumbrance, venue, margin mode and close-out rules. The reporting currency and FX/stablecoin conversion path must be explicit.

For a linear USD-quoted position, directional notional is `N_i = q_i × m_i × P_i`; **inverse and quanto contracts need their own payoff and sensitivity functions**. A canonical NAV identity is:

`NAV_t = Σ_j [asset_balance_j × executable_or_valuation_FX_j] + Σ_k [derivative_fair_value_k] − Σ_l [liability_value_l] − unpaid_fees − accrued_borrow_costs`

Avoid double-counting collateral and derivative account balances. Maintain **two parallel views**: (a) accounting/fair-value NAV and (b) conservative realizable or stressed liquidation NAV incorporating exit cost, haircuts, restricted withdrawals and disputed recoverability. Pending orders and reserved margin count toward forward-looking exposure even though they are not yet filled. Closed, pending, failed, canceled and partially filled instructions must be reconciled separately.

**Mark hierarchy [P]:** (1) verified venue-specific risk mark for liquidation calculations; (2) validated reference market prices for valuation; (3) executable depth-aware bid/ask for unwind scenarios; (4) independent oracle observations only where their heartbeat, deviation bounds, staleness and manipulation risks can be assessed. A CEX midpoint is not automatically a consolidated or executable fair value. A median across oracles is not sufficient if they share upstream venues. Record source divergence and stale-price flags. **Stablecoins are marked at observed convertibility/market value, never automatically at $1.**

Perpetual funding is a **cash flow or accrual**, not a retroactive change in trade entry price by default; maintain accounting convention explicitly. Dated futures require basis and expiry/settlement treatment. Vanilla options require contract-specific volatility surfaces, Greeks and expiry. Power perpetuals, exotic claims and concentrated-liquidity positions require instrument-specific payoff/rebalancing and oracle assumptions; absent these, set risk status to **UNMODELED** rather than approximate by spot notional. LP valuation must model fees, price ranges, adverse selection, gas and inventory composition. Track staking lockups, withdrawal queues, validator/slashing exposure, lending health factors, liquidation penalties and cross-chain settlement delays.

**Reconciliation gate [P]:** fail closed for risk-increasing decisions when assets, liabilities, fills, collateral, or position signs are unreconciled. Produce a discrepancy ledger with amount, source, time and severity; never infer a zero balance merely because a connector returned no records.

### 2. Exposure Measurement

Report exposure simultaneously on **economic, risk-factor, liquidation and legal-claim bases**. At minimum calculate signed delta-equivalent USD exposure, absolute gross delta, signed net delta, gross notional, gross/notional-to-NAV leverage, derivative gamma/vega/theta where relevant, margin utilization, borrow/liquidation liabilities, and liquidatable collateral. Delta equivalents require coherent contract multipliers and FX units. Gross notional and delta-exposure are complementary, not interchangeable.

A BTC beta is a useful diagnostic but not a sufficient factor model. Estimate rolling sensitivity to BTC, ETH, a broad crypto index (if point-in-time reproducible), liquidity/size, momentum, market-wide funding/basis and stablecoin stress where measured. Candidate robust regression and state-dependent beta estimators are **compared** with OLS; outlier robustness alone does not make a beta stable. Distinguish market delta from **basis, carry, funding, collateral and venue-default risks** in ostensibly delta-neutral portfolios.

Produce overlapping, non-additive concentration reports by: individual economic issuer/token; chain and rollup; smart contract/upgrade authority; stablecoin issuer and reserve/collateral dependency; bridge and wrapper; lending protocol; validator/custodian; exchange and settlement venue; common oracle; liquidation engine; token unlock cohort; and strategy/correlated trade cluster. Token ticker is **not** a durable asset identity: use chain ID, contract address, instrument ID, underlying, wrapper, expiry and venue-specific identifier. Flag duplicate exposure from staked assets, LP claims, collateral reuse and synthetic replicas.

Concentration measures include maximum issuer weight, Herfindahl-Hirschman index `HHI = Σ_i w_i²` on weights summing to one (multiply by 10,000 only for that convention), and concentration of **stressed loss**, not only market value. Negative or leveraged weights make naïve HHI misleading; report the chosen positive exposure denominator. Record correlated failure domains and estimate their full-loss scenarios.

### 3. Return and Covariance Estimation

Use UTC-synchronized, corporate-action/token-event-adjusted **point-in-time** data with explicit venue and bar-building logic. Cryptocurrency markets operate continuously, but outages, instrument creation, delistings, suspensions and unavailable history create irregular samples. Do not backfill zero returns for nonexistent trading; never use today's survivors to construct a historical universe. Benchmark daily risk at 24-hour intervals, and intraday liquidation risk at intervals justified by the actual observation frequency and horizon. One-hour observations are **not** a universal substitute for tick data or for independent daily tail samples.

Candidate estimators [R] are sample covariance, exponentially weighted covariance, Ledoit–Wolf or other positive-semidefinite shrinkage, factor covariance, realized covariance with asynchronous-observation controls, and DCC/ADCC-type conditional correlation when sample length and diagnostics permit. Choose **by rolling out-of-sample forecasting loss and risk consequences**, accounting for estimation cost and parameter instability. Ledoit–Wolf shrinkage addresses estimation error but does not ensure stable regimes or correct tail predictions. ADCC-GARCH can be valuable; it is **not mandatory** and must beat parsimonious baselines out of sample before operational use.

Quantify regime variation using rolling volatility, down/up-market correlations, factor co-movement and structural-break diagnostics. Test joint downside exceedances and conditional co-crashes; estimate lower-tail dependence with appropriate copulas or multivariate EVT **only if effective tail counts support the fit**. Clayton-type copulas model lower-tail dependence under some conventions; Gumbel models upper-tail dependence; rotated/survival constructions may change this. Never assert correlations universally become exactly 1 during crashes.

Validation [P]: rolling-origin training windows; locked holdout; positive-semidefinite checks; forecast-versus-realized variance loss; sensitivity to 24/7 horizon and stale sampling; block-bootstrap confidence intervals; and cost-inclusive portfolio consequences. If confidence is weak or the covariance condition number is extreme, fall back to a conservative diagonal/shrunk/factor model, larger buffers, or reduced allowable risk rather than fabricating precision.

### 4. Portfolio Construction

No portfolio-construction algorithm is presumptively superior. Compare **cash/stablecoin or no-position baseline, 1/N, capped market-cap weighting, inverse volatility, constrained minimum variance, constrained risk parity, hierarchical risk parity (HRP), mean–variance with robust return assumptions, and scenario/ES-constrained optimization** on the same point-in-time universe and execution rules. Use an asset-specific risk-free/collateral treatment; stablecoin balances carry issuer and liquidity risk.

| Candidate [R] | Principal benefit | Critical limitation and required test |
|---|---|---|
| 1/N | transparent low-estimation baseline | equal dollars do not equal risk; turnover/universe choice matters |
| Inverse volatility | parsimonious dispersion | ignores covariance, jump and funding risks |
| Shrinkage minimum variance | leverages diversified covariance | low-volatility concentration, regime change, estimation error |
| Constrained MVO | explicit risk/return tradeoff | return forecast error, turnover and unstable allocations |
| Risk parity | spreads modeled volatility contributions | does not eliminate common shocks; leverage/covariance sensitive |
| HRP | clustering avoids explicit full covariance inversion | linkage instability, implicit cluster choices, no guaranteed crypto superiority |
| ES/scenario constrained | targets downside and non-linear risk | finite tail samples, scenario misspecification, computational sensitivity |

For HRP, specify distance/linkage, clustering window, quasi-diagonalization and recursive bisection; test cluster stability by resampling and compare **after costs** against simpler alternatives. A 2026 cryptocurrency HRP working-paper comparison of multiple variants reports modest differences within its HRP family, underlining the danger of promoting a single method as a universal winner [S8]. Do not transport equity-only RL-HRP findings to crypto without independent replication.

Constraints [P] must cover minimum executable size, maximum single name, issuer/chain/venue/failure-domain exposure, financing availability, funding/basis carry, margin headroom, position-level stress, portfolio ES, turnover and worst-case time-to-exit. Include no-trade bands, transaction costs and **infeasibility diagnostics**. Use purged/embargoed time-series validation where labels/horizons overlap; compare results across market regimes, asset survivorship and rebalance frequencies. No optimizer can manufacture diversification when the investable universe has one dominant failure mode.

### 5. Position Sizing

Size from a **joint risk budget**, not merely an estimated edge. A candidate stop-based maximum quantity for linear instruments is:

`Q_max = min[(NAV × approved_loss_budget)/(stressed_stop_distance × multiplier + adverse_gap_cost_per_unit + fees_per_unit), liquidity_cap, margin_cap, issuer_cap, scenario_loss_cap]`.

The loss budget and gap allowance are policy assumptions requiring approval. Stops are not loss guarantees; market gaps, outages, ADL and liquidation can make realized losses exceed planned stop losses. Inverse/quanto instruments require a correct nonlinear payoff expression. ATR and realized volatility can inform distance, but must not be used mechanically for thin-liquidity tokens with discontinuous paths.

The classical quadratic approximation `f* ≈ μ/σ²` is only a **local approximation** to growth-optimal risky allocation under restrictive assumptions; it does not incorporate bankruptcy, jump tails, funding or model uncertainty. Even fractional Kelly can be dangerously large after estimation error. Treat Kelly as a **research diagnostic**, capped by scenario survival and portfolio-wide risk constraints, not a default sizing rule. Claims of fixed half-Kelly growth/drawdown benefits must not be carried over without testing the return-generating assumptions.

Drawdown-adaptive sizing [P] should use approved NAV high-watermark conventions, hysteresis, and separate treatment of market losses versus deposits/withdrawals. Restrict new risk during data uncertainty or risk-budget breaches; do not mechanically force a fire sale into zero liquidity.

### 6. Tail Risk

Measure **VaR and expected shortfall together** over stated horizons (for example, 24 hours and the realistic stressed exit horizon), with loss `L = −portfolio_P&L` in the reporting currency. At confidence `α`, `VaR_α` is the α-quantile of loss; `ES_α` is the average of the worst `1−α` fraction of loss under a continuous distribution, with an appropriate generalized definition for atoms. ES is coherent under the standard loss framework; **neither VaR nor ES captures unmodeled insolvency, terminal liquidity freezes or unobserved protocol loss without scenarios**.

Candidate forecast methods [R]: historical and filtered historical simulation, EWMA or GARCH with heavy-tailed innovations, joint VaR–ES specifications, regime-dependent models, and peaks-over-threshold EVT where thresholds/tail sample counts are defensible. Cornish–Fisher expansions are an **optional diagnostic** only when resulting quantiles remain admissible and monotone; high skew/kurtosis can make them unreliable. This is a correction to the source's preferred analytical method. A 2025 crypto-portfolio ES comparison found GARCH-based methods strong in its tested sample [S1]; this is evidence to test GARCH, **not** a general ranking. A 2026 peer-reviewed regime-dependent digital-asset model provides an additional candidate, not a mandatory upgrade [S2].

Backtest VaR exceptions (frequency and clustering) and **joint VaR–ES performance** using consistent scoring functions, comparative predictive-ability tests and Acerbi–Székely-type diagnostics as appropriate [S9]. Define significance level, dependence adjustment and minimum effective tail observations in advance. Do not interpret three consecutive weekly rejections as a universal statistical law: multiple testing and overlapping windows may produce false alarms. Report interval estimates, calibration failures and model-versus-baseline comparisons; flag **INSUFFICIENT_TAIL_SAMPLE** when warranted.

For liquidity-sensitive portfolios, maintain **two distinct tails**: mark-to-market P&L and conservative liquidation/realization P&L. Estimate multi-horizon path-dependent liquidation risk via scenario replay including margin calls, collateral haircuts, venue halts and intraperiod extremes; square-root-of-time scaling is not assumed valid through jump regimes.

### 7. Liquidity and Execution Risk

Liquidity risk is **venue-, side-, size-, time- and path-specific**. Do not treat quoted volume, pooled global volume or 24-hour turnover as executable exit capacity. Keep independently verified instruments and venues; exclude unsupported venues from executable risk reduction assumptions. For each venue/pair and trade size, calculate best bid/ask, depth-at-basis-point bands, spread, book imbalance, observed fill/slippage (when available), cancellation/replenishment behavior, order-book age, quote availability and executed trade distribution.

**Order-book reconstruction standard [P]:** snapshots alone do not establish historical tick-level depth or queue dynamics. For exact historical reconstruction, require documented incremental events, snapshot synchronization, sequence continuity, update semantics, timestamps and checksums; verify gaps and replay results. If only sampled historical books are supplied, calculate **sampled snapshot depth** and report reconstruction **NOT_ESTABLISHED**. Trades are not depth, candles are not trades, and current books are not historical books. An order-book history endpoint does not imply full level-3 reconstruction.

For DEX automated market makers, estimate exact pool route/fees, marginal price impact from reserves or concentrated-liquidity ticks, active liquidity by range, gas, MEV/sandwich exposure, failed-transaction cost, block/reorg/finality risk, sequencer dependency and bridge/withdrawal delay. Traditional square-root impact and Almgren–Chriss models are optional candidates for appropriate order-driven venues, **not** default truth for AMMs. Recent peer-reviewed research finds that AMM/CEX market quality depends materially on gas costs, trade size and venue design [S5, S6, S7].

Run liquidation exercises at proposed size and at smaller/larger sizes, as well as in dislocated markets, reporting a **range** of exit cost and time. Include path feasibility: pre-positioned collateral, transfer restrictions, cross-venue latency, gas and network congestion. If real executable history is unavailable, report scenario bounds rather than a fitted market-impact coefficient. A price-only tool response cannot justify precise slippage, queue fill or liquidation time.

### 8. Derivatives-Specific Risk

For each perpetual, dated future or option, record exchange-defined margin tiers, contract payoff, mark-index-fair-price distinction, funding accrual and schedule, maker/taker costs, maintenance margin, funding currency, liquidation-price semantics, fee/penalty regime and insurance-fund/ADL rules **as published for that venue and date**. Never assume a uniform ADL ranking formula or universal API availability of liquidation levels. Funding rates can change sign, scale, settlement frequency or methodology; treat prolonged funding as a scenario and cash flow, not deterministic exponential decay.

Compute **account-level and position-level liquidation buffers** by replaying the venue's risk engine where documented, including correlated losses, margin tier jumps, collateral depegs, basis blowouts and pending orders. Model stop execution as contingent on venue availability and priority: liquidation may happen before the stop can execute. For options, reprice under joint spot/volatility/skew/term-structure stress; Greeks alone are local approximations. For correlated hedges across venues, model one-sided ADL, close-only changes and inability to transfer margin. Prefer isolated margin for exposures with standalone tail failure only after comparing venue rules and capital efficiency; it is a **conditional policy**, not a universal mandate.

### 9. Counterparty and Operational Risk

Quantify distinct **loss-given-failure and time-to-recovery** distributions for exchanges, custodians, issuers, bridges, oracles, multisigs, validators, lending protocols and data/API providers. Loss of venue access is not necessarily immediate zero recovery; use zero-recovery as a severe case alongside delayed and partial recovery. Proof-of-reserves cannot alone establish complete liabilities, solvency or legal recoverability.

Stablecoin risks include reserve composition, issuer redemption rights, banking concentration, liquidity, exchange-premium fragmentation, depeg contagion and collateral haircuts. A 2025 study using high-frequency observations from 70 non-stable assets found sharply elevated jumps/co-jumps after Tether depegs [S3]; a 2026 study distinguishes mechanisms across stablecoin designs [S10, **working paper**]. Do not assign a single corporate-debt default-probability model to every stablecoin.

Track smart-contract upgrade/admin keys, oracle provenance, chain halts, rollup sequencers, bridge dependencies, withdrawal gates, token supply/unlocks, validator centralization, key custody, API permissions and connector compromise. Disallow new risk on stale/contradictory high-priority inputs; preserve a read-only/manual risk review path. Network unavailability tests must use stress durations calibrated to available margin runway, not an untested universal 6–12-hour survival claim.

### 10. Stress Testing

Use **historical-event replay, coherent factor shocks, mechanism-driven scenario trees and reverse stress tests**. Every scenario specifies price paths, timing, collateral marks, venue status, oracle/index behavior, funding, fees, depth, recovery assumptions, margin rules, and whether hedges remain executable. Published historical moves are descriptive anchors; no invented exact shock is presented as a historical observation.

| Scenario | Required model interactions | Evidence status |
|---|---|---|
| March 2020-type broad crash | gap moves, intraday path, correlation shifts, liquidation and slippage | historical template; shocks calibrated from chosen data |
| 2022 stablecoin/exchange-type crisis | peg discount, issuer/venue failure, withdrawal freezes, contagion | historical template; venue effects conditional |
| Stablecoin depeg and co-jump | collateral haircut, FX translation, cross-asset jumps, funding/margin feedback | supported contagion mechanism [S3] |
| Venue halt or ADL | partial/zero fills, asymmetric hedge closure, recovery/transfer delay | scenario; needs actual venue rules |
| Order-book collapse | depth removal, adverse selection, spread widening, exit infeasibility | stress bounds; requires L2/L3 where available |
| Funding/basis dislocation | nonlinear margin drains, basis widening, negative carry | hypothetical parameters labeled |
| Chain/bridge/protocol exploit | chain halt, frozen claims, forced correlation, partial/zero recovery | failure-domain scenario |
| Liquidity and credit spiral | sell pressure → price move → collateral haircut → further liquidation | model scenario, validate dependencies |
| Oracle/mark divergence | reference price conflict, false margin trigger, stale marking | data integrity stress |

Compute for each: instantaneous and pathwise NAV, peak margin usage, first failure or liquidation time, stressed exit proceeds, unfunded collateral requirement, tail P&L, unavailable hedge portion and recovery time. **Reverse stress** solves for the smallest coherent price/liquidity/venue shock that breaches each hard risk budget. Explicitly include scenarios outside historical support and treat their probabilities as unknown, not 99.9%-precise.

### 11. Risk Budgeting

Risk budgets are governance decisions that must be **approved, calibrated, versioned and tested**. Allocate across overlapping single-asset, factor, issuer, venue, chain, liquidity, leverage and scenario-loss constraints. For a differentiable, positively homogeneous portfolio risk measure `ρ`, Euler contribution can be written `RC_i = w_i × ∂ρ(w)/∂w_i`, with `Σ RC_i = ρ(w)` under regularity assumptions. For ES, contributions may be expressed using conditional losses in the portfolio tail; with atoms, discontinuities, nonlinear options or unstable tail samples, report approximation and uncertainty rather than asserting a unique exact decomposition.

Define proposal fields instead of unsupported universal percentages:

| Control | Required calibration record |
|---|---|
| Per-position and per-issuer maximum loss | NAV basis, exit horizon, stress and gap allowances |
| Maximum factor/chain/venue exposure | overlapping-failure scenario and concentration tolerance |
| Maximum margin and leverage | maintenance margin, adverse marks, funding drain and ADL rules |
| Maximum stressed liquidation cost/time | venue-level L2/AMM evidence, confidence and data gaps |
| Daily/weekly ES and scenario loss | forecasting backtests, coverage and scenario design |
| Drawdown response | high-watermark method, hysteresis, permissions and liquidity costs |
| Data-quality and model risk | source availability, latency, disagreement, missingness and fallback |

If policy limits conflict, choose the more conservative **non-execution** interpretation until an authorized human resolves the tradeoff. No unapproved percentage, time limit, portfolio NAV, position or order is implicitly supplied by this document.

### 12. Monitoring and Escalation

Use auditable **research states**, not autonomous trade instructions:

| State | Illustrative trigger [P, calibrate] | Required response |
|---|---|---|
| `GREEN` | reconciled and timely inputs; approved budgets not breached | standard paper-risk evaluation; no implied trading authority |
| `WATCH` | risk forecast deterioration, source divergence, rising funding, worsening venue depth | shorten monitoring interval, widen scenarios, review new-risk proposals |
| `REDUCE_RISK_REVIEW` | approved limit breach, margin runway erosion, significant venue/issuer uncertainty | prohibit risk increases; present manually reviewed reduction alternatives with executable bounds |
| `HALT_NEW_RISK` | unresolved ledger, stale essential data, disallowed venue, unmodeled payoff or broken risk calculation | stop proposed new risk; preserve audit trail; do not force liquidation via broken data |
| `EMERGENCY_HUMAN_REVIEW` | imminent venue liquidation, exploitable key compromise, custody/withdrawal failure | surface exposure, feasible risk mitigations, tradeoffs and recovery options to authorized operator |

**No state authorizes order placement, cancellation, wallet transfer or custody movement.** Actual execution requires a separately proven, authorized control plane and explicit permissions. A venue outage does not justify an automatic global liquidation that the venue cannot support.

At each snapshot record: NAV and data reconciliation, long/short beta and derivatives Greeks, ES/VaR calibration, stress-budget usage, margin headroom by venue, capital trapped in withdrawal/settlement, source age/conflicts, depth and liquidation capacity, collateral issuer risks, and open/pending orders. Trigger out-of-cycle reviews for model backtest deterioration, structural venue changes, peg events, new correlated exposures and critical provider outages. Compare policies quarterly **or sooner when material risk changes**; retain immutable previous versions and decision logs.

### 13. Final Document Controls

#### Evidence-to-control traceability

| Finding / issue | Evidence | Conservative methodological implication |
|---|---|---|
| Crypto ES estimators differ materially | 2025 crypto ES comparison [S1]; 2025 joint VaR/ES paper [S11] | compare GARCH, historical and joint-tail models; use out-of-sample scoring |
| Regimes change tail-loss forecasts | 2026 digital asset regime study [S2] | test regime-aware models against parsimonious baseline, never require without gain |
| Stablecoin depegs transmit jump risk | 2025 high-frequency study [S3] | jointly stress collateral, price gaps and co-jumps |
| Model selection can be unstable | 2026 crypto HRP working paper [S8] | compare simple and complex allocation methods after costs |
| CEX and DEX liquidity are structurally different | 2025–26 peer-reviewed exchange studies [S5–S7] | venue-specific fees, gas, impact and execution feasibility |
| VaR and ES need joint validation | established statistical methodology [S9] | joint scoring, exception diagnostics and uncertainty reporting |
| Account insolvency is a path problem | venue margin rules + mechanism scenarios [P] | pathwise stress of marks, funding, fills, ADL and collateral |

#### Connected crypto tool and venue evidence protocol (2026-10-22)

This is a **tool inventory relevant to possible research**, not a statement that every operation was successfully queried for a requested instrument, period, or venue.

| Tool family present in environment | Research use | Critical limitation |
|---|---|---|
| **0xArchive** | Hyperliquid core perps and spot where exposed; HIP-3 markets; Lighter and RH Lighter market families; discoverable trades, current/historical books, candles, funding, OI, liquidations; Lighter L3 book operations where exposed | verify instrument mapping, earliest/latest actual record, granularity, pagination, retention, snapshot versus incremental fidelity and gaps **per endpoint**; L3 tool name alone proves no complete reconstruction |
| **Co-Invest / Liquid** | tradable-market discovery, market/positioning analysis, current order book views and account/paper context if authorized | current displays, trader positioning and paper records do not establish long-run historical fills or executable live order controls |
| **Massive** | market history, technicals and cross-asset validation subject to available exact operations | verify crypto instrument/venue coverage, licensing and timestamp alignment per query |
| **CoinGecko, CoinPaprika and CoinMarketCap public tools** | asset identity, spot reference series, market-cap/universe checks, cross-source comparisons | aggregate venues and sampled bars are not microstructure; circulating supply and timestamps require point-in-time verification |
| **DexPaprika / DEX-oriented feeds where accessible** | pool liquidity, chain/pool identification, DEX activity | pool snapshots do not prove attainable route, gas, MEV or historical active ticks |
| **Blockscout and other verified chain explorers** | contracts, tokens, transfers and chain history | on-chain balances are not complete off-chain liabilities, claim ownership or executable market liquidity |
| **fin-data, Massive, other market and on-chain MCP families** | independent historical and derivative cross-checks | tool registration does not guarantee data licensing, history, accuracy or particular venue support |

**Qualification sequence [P]:** discover exact operation and schema → resolve unique exchange/chain/market/contract → run a minimal read-only probe → record first/last *returned* observation (not advertised retention), page size and cursor, granularities and update types → perform time-range/pagination continuity tests → inspect timestamps, duplicates and missing spans → cross-check an independent source → record qualified scope or `UNVERIFIED`. For each historical book/trades request, specifically determine whether the feed contains time-consistent snapshots, deltas, L2 aggregated levels, L3 event/order IDs, sequence numbers and cancellation messages. If any element needed for full replay is absent, classify full reconstruction **NOT POSSIBLE FROM VERIFIED DATA** or **NOT ESTABLISHED**, not 'complete'.

Never substitute candles for historical trades, trade prints for quotes, or an inferred liquidation heat map for actual account liquidation thresholds. Default to **paper research only** and provide reproducible citations, query dates, source IDs, parameters and caveats.

#### Reproducible risk-report contract

Every produced risk artifact should include:

```yaml
methodology: 05-portfolio-risk-methodology.md
revision: 2026-10-22
run_utc: REQUIRED
portfolio_snapshot_id: REQUIRED
reporting_currency: REQUIRED
mode: read_only_or_paper
assets_and_venue_contracts: REQUIRED
verified_data_provenance: REQUIRED
pricing_and_margin_conventions: REQUIRED
risk_horizons: REQUIRED
model_and_baseline_versions: REQUIRED
out_of_sample_validation: REQUIRED_OR_EXPLICITLY_UNAVAILABLE
scenario_parameters_and_status: REQUIRED
missing_data_and_unmodeled_instruments: REQUIRED
risk_limit_approval_status: REQUIRED
recommendations: advisory_only
execution_authority: none
```

#### Reference bibliography (selected, checked as of 2026-10-22)

**Peer-reviewed research**

- **[S1]** *No shortfall of ES estimators: Insights from cryptocurrency portfolios*. *Finance Research Letters* 73 (2025), 106685. https://doi.org/10.1016/j.frl.2024.106685
- **[S2]** Saidane and Ben Mohamed, *Forecasting Regime-Dependent Tail Risk in Digital Asset Portfolios With a Mixture of Hidden Markov Factor Analyzers*. *Journal of Forecasting* (published April 16, 2026). https://doi.org/10.1002/for.70159
- **[S3]** *From depegs to jumps: The role of stablecoin instabilities in crypto market dynamics*. *Journal of International Money and Finance* 155 (May 2025), 103339. https://doi.org/10.1016/j.jimonfin.2025.103339
- **[S4]** Li, Liu and Yan, *Performance-based regularization for downside-risk cryptocurrency portfolios*. *Pacific-Basin Finance Journal* 97 (2026), 103084. https://doi.org/10.1016/j.pacfin.2026.103084
- **[S5]** *On the Quality of Cryptocurrency Markets: Centralized vs. Decentralized Exchanges*. *Management Science* (March 2026). https://doi.org/10.1287/mnsc.2024.07703
- **[S6]** Ranaldo, Viswanath-Natraj and Wang, *Blockchain Currency Markets*. *Journal of Financial and Quantitative Analysis* (April 2026). https://www.cambridge.org/core/journals/journal-of-financial-and-quantitative-analysis/article/blockchain-currency-markets/31C8A865840FCC2EE51CC667381F9FE1
- **[S7]** Schwertfeger and Vogt, *Arbitrage trading between decentral and central cryptocurrency exchanges*. *Journal of Banking & Finance* 188 (2026), 107721. https://doi.org/10.1016/j.jbankfin.2026.107721
- **[S11]** Chen, Chen and Hsu, *Bayesian Forecasting of Value-at-Risk and Expected Shortfall in Cryptocurrency Markets*. *Applied Stochastic Models in Business and Industry* 41 (2025), e2926. https://doi.org/10.1002/asmb.2926

**Working papers and methodological references (not automatically peer-reviewed crypto evidence)**

- **[S8]** Matys, Rodriguez and Delfau, *Hierarchical Risk Parity Variants for Cryptocurrency Portfolios: Denoising, Detoning, Tail Dependence, Embeddings, and Statistical Inference, 2020–2026*. UCEMA working paper, May/June 2026. https://ucema.edu.ar/sites/default/files/2026-06/dt928.pdf
- **[S9]** Fissler, Ziegel and Gneiting, *Expected Shortfall is jointly elicitable with Value at Risk—Implications for backtesting*. 2015 methodological preprint. https://arxiv.org/abs/1507.00244
- **[S10]** Wu and Liu, *Stability Anchors and Risk Amplifiers: Tail Spillovers Across Stablecoin Designs*. 2026 preprint. https://arxiv.org/abs/2602.18820

**Document change discipline:** revisions must log which claim, model, data provider, venue or policy changed and why; they must preserve failed experiments and uncertainty; and they must not silently recast hypothetical thresholds as statistically validated findings. Historical source citations are examples of general market evidence, not attestations about current portfolio values or connector availability.
