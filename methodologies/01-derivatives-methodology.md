# 01-derivatives-methodology.md — Crypto Derivatives Analysis Methodology (v1.1.0, research cutoff 2026-10-22)

Crypto derivatives data can support a defensible directional assessment only when venue mechanics are normalized, known measurement limits are respected, and each signal has passed walk-forward validation with multiple-testing correction. On their own, the commonly cited "signals" (raw funding, aggregate OI, liquidation heatmaps, max pain) describe market state; none has been shown to predict returns. This file is a reusable standard for quantitative research agents. It covers instruments, formulas, data checks, signal specifications, statistical tests, and a decision protocol that outputs BULLISH, BEARISH, NEUTRAL, or INCONCLUSIVE.

## TL;DR

- **Treat derivatives metrics as state descriptors first.** The best-supported findings are about pricing and limits to arbitrage:
  - Perp–spot deviations are large but have been shrinking (He, Manela, Ross & von Wachter).
  - Crypto carry averages above 10% p.a., and high carry predicts crashes (Schmeling, Schrimpf & Todorov, BIS).
  - Order-flow imbalance scaled by depth moves short-horizon prices (Cont, Kukanov & Stoikov, plus crypto replications).
  - Direct evidence that funding or OI predicts returns is weak, unstable, or vendor-sourced.
- **Measurement error is a first-order problem.**
  - Binance's public liquidation stream pushes at most one order per symbol per second, so its totals are lower bounds.
  - Aggregated OI and volume suffer from double counting, unit mismatches, and wash trading. Cong, Li, Tang & Yang (Management Science 69(11)) estimate that wash trading "on average is as high as 77.5% of the total trading volume on the unregulated exchanges, with a median of 79.1%."
  - Funding intervals differ by venue and can change dynamically (Binance 1h for capped contracts; Hyperliquid hourly).
- **Default to INCONCLUSIVE.** Issue a directional call only when all three hold: (a) data pass the quality gates; (b) at least one locally calibrated signal survives out-of-sample and multiple-testing checks; (c) spot, cross-venue, and macro context do not contradict it. This file supplies no universal weights or thresholds. Every numeric trigger must come from your own walk-forward calibration.

---

## 1. Scope and scientific assumptions

**Scope.** Digital currencies and their spot, perpetual, dated-futures, and options markets **only where an installed connector can retrieve the specified observations at run time**. Venue eligibility is dynamic and data-family-specific, not a static whitelist. Hyperliquid, Lighter, HIP-3, and OKX are currently discoverable through named tools; Binance, Bybit, Deribit, BitMEX, CME, dYdX, and others are comparison venues only when an installed connector actually returns the required direct or clearly attributed data. HIP-4 prediction markets and synthetic equity/index contracts are outside digital-currency derivatives scope. Outputs are evidence-graded market-state assessments for a stated horizon, not trade recommendations.

**Assumptions (explicit, falsifiable):**
1. **A1 – Zero-sum positioning.** Every open long has a matching short. Aggregate OI measures gross exposure, not net direction.
2. **A2 – Mechanism ≠ prediction.** Funding exists to anchor perps to an index. Observing it does not validate a forecast.
3. **A3 – Venue heterogeneity.** Formulas, caps, intervals, index constituents, and liquidation engines differ across venues and change over time. Read specifications *as of each timestamp*.
4. **A4 – Non-stationarity.** Do not assume parameters carry across structural breaks. Examples: Binance portfolio margin (Apr 2022), US spot ETFs (Jan 2024), dynamic funding intervals (2025), the October 2025 ADL episode.
5. **A5 – Evidence hierarchy.** Peer-reviewed/central bank > working papers > exchange documentation (authoritative for mechanics only) > vendor research > media.
6. **A6 – UNVERIFIED.** A claim with no identifiable source is tagged UNVERIFIED and must not be used as a signal input until validated independently.

**Grades:** **E1** peer-reviewed/central bank; **E2** working paper; **E3** exchange documentation; **E4** vendor/industry; **E5** media/secondary; **U** UNVERIFIED.

---

## 2. Literature synthesis (with conflicts reconciled)

### 2.1 Perpetual pricing theory
- **Ackerer, Hugonnier & Jermann (AHJ)** [E1, *Mathematical Finance*; NBER WP 32936].
  - Derive no-arbitrage prices for linear, inverse, and quanto perpetuals.\[1\]
  - The perp price is "the risk-neutral expectation of the spot sampled at a random time that reflects the intensity of the price anchoring."\[2\]
  - Identify funding specifications under which perp and spot prices coincide.\[2\]
- **He, Manela, Ross & von Wachter (HMRV)** [E2, arXiv:2212.06888v7, dated 2026-09-17; the abstract states deviations "are larger than in traditional currency markets, comove across currencies, and diminish over time"]. Derive random-maturity no-arbitrage bounds under trading costs, including Binance's clamp. Empirical findings:
  - Mean absolute deviation of about 52%–90% per year, declining about 22 pp per year.\[3\]
  - BTC arbitrage Sharpe ratios of 3.35 (retail fees) to 11.65 (zero-fee market makers), or 3.27 and 10.46 after effective spreads.\[3\]
  - Deviations compressed after Binance introduced portfolio margining in April 2022.\[3\]
  - Order-flow impact is larger when initial deviations are large.\[3\]
  - Past returns positively predict deviations.\[3\]
  - Price convergence, not funding, dominates arbitrage returns.\[3\]
  - Binance–Bybit BTC funding correlation is 0.74; Bybit's effective spread was 2–10× Binance's on every sampled day.\[3\]
  - Hyperliquid's specification "mirrors that of Binance, including the clamp feature."\[3\]
- **Implication:** read the perp–spot deviation relative to a cost-adjusted no-arbitrage band, as a function of arbitrage capacity, not as raw sentiment.

### 2.2 Carry and basis
- **Schmeling, Schrimpf & Todorov (SST)** [E1/E2; BIS WP 1087, published 2023-04-04; *Management Science* 2026].
  - Carry averages above 10% annually. Per BIS WP 1087 it "can become very large (up to 60% p.a.) and varies strongly over time," driven by "trend-chasing and attention by smaller investors" and "the relative scarcity of arbitrage capital."
  - Interest-rate differentials explain very little of it.\[4\]
  - Futures show "excess volatility" relative to spot.\[4\]
  - **High carry predicts future crashes**, alongside a rising price of crash insurance.\[4\]
  - The journal abstract says carry is "sometimes exceeding 40% per annum."\[5\] Treat both the 60% and 40% figures as sample-specific maxima, not thresholds.
- **Christin, Routledge, Soska & Zetlin-Jones** [E2]. Short-perp/long-spot shows high in-sample Sharpe, which they attribute to differences of opinion and leverage constraints. HMRV report that their dynamic strategy outperforms this directional carry.\[3\]
- **arXiv 2510.14435** [E2]. Reports a carry Sharpe of 6.45 over 2020–2025 (funding mean ≈8%, volatility 0.8%), with profitability "compressed sharply since 2024."\[6\] **Reconciliation:** carry is real but time-varying and capacity-limited. Never extrapolate historical carry Sharpe ratios.

### 2.3 Price discovery (sample-dependent; unresolved)
| Study | Sample | Finding |
|---|---|---|
| Alexander, Choi, Park & Sohn (2020, JFM) [E1] | BitMEX minute data, 2018-era | BitMEX derivatives lead major spot exchanges\[7\] |
| Cosenza & Stalder (SSRN) [E2] | HF spot + perps, fiat/stablecoin | Binance spot *and* perps are primary; lower costs and higher volume help\[8\] |
| Kia et al. (2026, Financial Review) [E1] | Minute FCVAR from Oct 2021 | After spot-ETF approval, spot dominates (e.g., 89% vs 11% futures in one pair)\[9\] |
| J. Int'l Money & Finance (2025) [E1] | 20 spot / 26 futures; Hayashi–Yoshida | CME futures lead; transaction size matters\[10\] |
| Time-varying study (PubMed 38620702) [E1] | Daily | Futures Granger-cause spot and dominate IS\[11\] |

**Reconciliation:** which market leads depends on sampling frequency, venue set, period (before or after ETFs), and metric (IS/CS/ILS). Estimate leadership locally on rolling windows (§5.8).

### 2.4 Microstructure
- **Cont, Kukanov & Stoikov (2014)** [E1]. Short-interval price changes are driven mainly by OFI.\[12\]\[13\] The relation is linear, with slope inversely proportional to depth. Volume–price relations are noisier.\[14\]
- **Crypto replications:**
  - Binance Futures 1s data, Jan 2022–Oct 2025 (arXiv 2602.00776) [E2]: a largely monotone OFI effect, concave at the extremes; wider spreads reduce predictability.\[15\]
  - "Quarter-hour effect" (arXiv 2607.09426) [E2, single study, fragile]: boundary order imbalance predicts 4–12h returns; baseline imbalance does not.\[16\]
  - Charles University thesis on 2025 BTC perp data at 100 ms: martingale-beating OFI/TFI predictability under purged evaluation.\[17\]
- **Theory:** Stoikov (2018) micro-price;\[18\] Kyle (1985) and Glosten–Milgrom (1985) on adverse selection.

### 2.5 Funding as a return predictor (weak or contested)
- Inan (*International Review of Financial Analysis*, online 2026-10-17, journal pre-proof) [E1, subject to final publication]: BTC/USDT Binance and Bybit next-period **funding rates**, not BTC returns, are forecastable with double-autoregressive models against a no-change baseline; stability changes through time. This is a stronger provenance grade than the earlier SSRN-only version.\[19\]
- Yang (SSRN) [E2]: positive funding is informative in a volatility-measurement context. The author explicitly rejects reading this as a trading rule.\[20\]
- Vendor evidence [E4]:
  - Fulgur Ventures blog: slight negative relation between BitMEX funding and the next 8h BTC return, R² ≈ 0.003.\[21\]
  - Presto Labs: R² = 12.5% for 7-day funding changes vs *contemporaneous* price changes.\[22\] That is coincident, not predictive.
- **Conclusion:** funding is persistent and forecastable as a series. Its power to predict returns is unproven and must be shown locally.

### 2.6 Liquidations, ADL, and the October 10–11, 2025 cascade
- **Reported totals** [E5, CoinGlass via media]:
  - $19.13B liquidated and more than 1.6 million traders liquidated in 24h (CoinGlass data reported by Coinpedia, Oct 11, 2025; CNN had an earlier $18.28B "as of 3:47 p.m. ET"). CoinGlass called it "the largest liquidation event in crypto history." Of the total, $16.7B were longs and $2.46B shorts.
  - By venue: Hyperliquid ≈ $10.3B, Bybit $4.6B, Binance $2.4B.\[23\]\[24\]
- **Open interest** [E4, CoinDesk Research]: perp OI fell 43% ($217B → $123B); Hyperliquid OI fell 57% ($14B → $6B).\[25\]
- **Under-reporting claims:**
  - Hyperliquid co-founder/CEO Jeff Yan (X post, Oct 13, 2025, via The Block): "Because liquidations happen in bursts, this could easily be 100x under-reporting under some conditions."
  - CoinGlass on X (Oct 10, 2025): "The actual total is likely much higher — #Binance only reports one liquidation order per second."
  - CoinShares says losses "could exceed $50 billion"\[26\] (an estimate, not verifiable).
- **ADL research** [E2]:
  - Chitra (arXiv 2512.01112): 34,983 ADL executions across 19,337 wallets; $2.1B closed in 12 minutes; the queue overshot by about $653M.\[27\]\[28\]\[29\]
  - Chitra & Thogiti (arXiv 2602.15182): an explicit replay model puts the overshoot at only $45.0M–$51.7M.\[30\] **The estimate is model-dependent; always cite the model with the number.**
  - arXiv 2603.15963: $2.047B realized ADL notional.\[31\]
- **Early warning** (arXiv 2607.27070, seven cascades) [E2]:
  - No early-warning variable holds across events. An in-sample October 2025 pattern inverted for August 2024.\[32\]
  - Binance's historical liquidation-snapshot dumps were discontinued, so the study had to use OI and taker flow as proxies.\[33\]
- **Implication:** liquidation indicators are conditional state measures. No universal crash predictor is supported.

### 2.7 Data integrity
- Cong, Li, Tang & Yang (*Management Science* 69(11), 6427–6454; NBER WP 30783) [E1] examine 29 centralized exchanges. "The wash trading volume on average is as high as 77.5% of the total trading volume on the unregulated exchanges, with a median of 79.1%."
- HMRV exclude exchanges known to misreport.\[3\]
- Volume-based ratios therefore require venue filtering.

### 2.8 Options and volatility
- **DVOL** [E3]:
  - Uses the two expiries bracketing 30 days, a variance-swap methodology, and interpolation.\[34\]
  - Excludes options with delta below 5%.\[35\]
  - Smoothed as an EMA of the last 240 one-second values.\[34\]
  - Expected daily move ≈ DVOL/√365.\[34\]
- **Volatility risk premium:**
  - Almeida, Grith & Miftachov (arXiv 2410.15195) [E2]: BTC VRP of 0.14, "much higher than that of the S&P 500."\[36\]
  - Winkel & Härdle (*Risks* 2023) [E1]: U-shaped pricing kernels and time-varying premia.\[37\]
  - Alexander & Imeraj [E1]: Bitcoin VIX and VRP from 15-minute Deribit data.\[38\]
  - Delta-hedged backtests [E2]: option risk premia are significantly negative.\[39\]
- **Max pain:** no peer-reviewed crypto support was found → **UNVERIFIED** (§6.3).

---

## 3. Mathematical definitions and formulas

Notation: $S_t$ index/spot; $F_t$ perp/futures; $M_t$ mark; $Q$ contracts; $m$ multiplier; $\tau$ years to expiry; $f^{(k)}$ funding per settlement for interval $k$ hours.

### 3.1 Payoffs
- **Linear:** $\text{PnL}_{quote}=Q\,m\,(F_1-F_0)$.
- **Inverse** (USD face $N$): $\text{PnL}_{coin}=N(1/F_0-1/F_1)$. This is non-linear in USD. Collateral falls exactly when longs lose (wrong-way margin).
- **Quanto:** $Q\,m\,(F_1-F_0)$ paid in a third currency at a fixed multiplier. USD PnL depends on underlying/settlement-currency covariance (AHJ price this explicitly).

### 3.2 Funding
$$\text{Payment}_{long\to short}=Q\,m\,M_{t_s}\,f^{(k)}_{t_s}\quad(f>0:\text{ longs pay})$$

**Binance** [E3]:
- $f=\bar P+\text{clamp}(I-\bar P,-0.05\%,+0.05\%)$, with $I$ = 0.01%/8h (0% for some pairs, e.g., ETHBTC).\[40\]\[41\]
- The premium index is sampled every 5s and time-weighted. If $\bar P\in[-0.04\%,0.06\%]$, then $f=I$.\[41\]
- A per-symbol cap/floor applies. For non-8h intervals the rate is scaled by $(8/N)$, as summarized from the FAQ by PANews/Futu.\[42\]

**Binance interval rules:**
- Selected contracts moved to 4h effective 2023-10-12.\[43\]
- From 2025-05-02 08:00 UTC, a contract whose previous settlement hit the cap/floor switches to **1h**.\[44\]
- From 2026-01-02, per a mirror of Binance's announcement corroborated by PANews (not fetched from Binance directly), 1h contracts revert to 4h after 16 consecutive cycles with |f| ≤ 0.025%.\[45\]\[46\]

**Hyperliquid** [E3]:
- An 8h-equivalent rate $F=\bar P+\text{clamp}(I-\bar P,-0.0005,0.0005)$ is **paid hourly at 1/8**.\[47\]
- Premium $=0.5(\text{impact bid}+\text{impact ask})/\text{oracle}-1$, sampled every 5s.\[47\]
- Cap is 4%/hour for all assets. $I$ = 0.01%/8h ("11.6% APR paid to short").\[47\]
- The API value is already hourly.\[48\]

### 3.3 Normalization and annualization
- 8h-equivalent: $f^{(8)}_{eq}=f^{(k)}\cdot 8/k$.
- APR (default, no reinvestment): $\sum_{s\in yr}f_s\approx\bar f^{(k)}\cdot 8760/k$.
- APY: $\prod(1+f_s)-1$. Use only if PnL is actually re-margined.
- **Rule:** report APR, and record the interval *per observation*, because Binance intervals can change mid-sample. Never compare raw hourly and raw 8h prints.

### 3.4 Basis
- Dated: $b_t=(F_t/S_t-1)/\tau$, or $\ln(F_t/S_t)/\tau$. Perp premium: $p_t=M_t/S_t-1$.
- Cost of carry: $F=Se^{(r-y)\tau}$. SST show that $r$ explains little, so the convenience yield $y$ dominates.
- **Perp no-arbitrage (derived, constant parameters, continuous funding $\kappa(F-S)$; consistent with AHJ/HMRV):** $F=\frac{\kappa}{\kappa-(r-r^*)}S$ for $\kappa>r-r^*$. For empirical work, use HMRV's clamp-specific bounds.

### 3.5 OI and leverage proxies
- Notional OI: $OI^{\$}=OI^{c}\,m\,M_t$ (linear). For inverse contracts, contracts × USD face.
- $\Delta OI^{\$}=m\,M_{t-1}\Delta OI^c$ (position change) $+\,m\,OI^c_t\Delta M$ (revaluation). **Infer opening or closing only from contract counts.**
- Estimated leverage ratio: $ELR=OI^{\$}/\text{ExchangeReserves}^{\$}$. This relies on vendor wallet labels (E4) and is a noisy proxy.
- Turnover $V/\overline{OI}$, after filtering out wash-trade venues.

### 3.6 Liquidation measures
- Isolated linear long, approximate (ignores fees and tiers): $P_{liq}\approx P_0(1-1/L+mmr)$. Venue tier tables override this.
- Observed intensity $LI_t=\sum\text{liq}_{(t-h,t]}/OI^{\$}_{t-h}$. Set `lower_bound=true` for snapshot feeds.

### 3.7 Microstructure
- Spread $(a-b)/mid$; depth $D_k$ within $k$ bps; book imbalance $(q^b-q^a)/(q^b+q^a)$.
- Micro-price, first-order (Stoikov's estimator adds a Markov correction): $b+(a-b)\,q^b/(q^b+q^a)$.
- OFI (CKS): $e_n=q^b_n\mathbb 1\{b_n\ge b_{n-1}\}-q^b_{n-1}\mathbb 1\{b_n\le b_{n-1}\}-q^a_n\mathbb 1\{a_n\le a_{n-1}\}+q^a_{n-1}\mathbb 1\{a_n\ge a_{n-1}\}$.\[13\] $OFI=\sum e_n$, with $\Delta mid=\beta\,OFI+\epsilon$ and $\beta\propto 1/\text{depth}$.
- Taker imbalance (HMRV eq. 27): $(V^{buy}_{taker}-V^{sell}_{taker})/(V^{buy}_{taker}+V^{sell}_{taker})$.\[49\]
- Kyle's λ: rolling slope of $\Delta p$ on signed volume.

### 3.8 Volatility
- $RV=\sum r_i^2$; $BV=\frac{\pi}{2}\sum|r_i||r_{i-1}|$; jump component $\max(RV-BV,0)$.
- HAR-RV: $RV_{t+1}=\beta_0+\beta_dRV_t+\beta_wRV^{(5)}_t+\beta_mRV^{(22)}_t+\epsilon$. Because crypto trades 24/7, setting 7/30-day windows is a design choice that must be tested.
- $VRP=IV^2_{30d}-E_t[RV_{t\to t+30d}]$, in variance units.
- $RR_{25}=IV_{25C}-IV_{25P}$; $BF_{25}=\tfrac12(IV_{25C}+IV_{25P})-IV_{ATM}$.
- For inverse options, coin-settled "net delta" includes a premium adjustment. State the convention used.

---

## 3.9 Research estimands and non-directional endpoints (v1.1)

Every hypothesis must specify **one target** before inspecting returns: (a) funding forecast error, (b) perp–spot deviation convergence time, (c) next-horizon signed return, (d) next-horizon realized variance / tail exceedance, (e) market impact or execution shortfall, or (f) liquidation / ADL event probability. An observed relationship with one target is **not evidence for a different target**. In particular, funding forecastability does not imply return forecastability; volatility forecastability does not imply directional predictability; and liquidation-level density does not measure realized liquidations.

Use rolling-origin baselines appropriate to each target: persistence/no-change for funding; random walk/martingale for returns; HAR-RV or historical variance for volatility; simple spread/depth baselines for impact; base-rate and calibrated logistic/hazard benchmarks for stress. Evaluate conditional calibration (reliability diagrams, Brier score and log loss for event probabilities; MAE/QLIKE for funding and variance where appropriate) before economic utility.

**New evidence, held as hypotheses rather than universal triggers:** Inan (online 2026-10-17) reports next-period BTC funding forecasts outperform a no-change baseline, with instability across windows (E1, journal pre-proof). A September 2026 SSRN study of extreme negative funding reports different forward price behavior on up-days and down-days; the observational sample and independent-author working-paper status require independent replication before promotion (E2). A 2026 *Studies in Economics and Finance* study models leverage-driven systemic risk in ten Binance perpetuals in 2023–2024; transportability to Hyperliquid or small-cap tokens is unestablished (E1). See §15 additions.

---

## 4. Data requirements and validation

### 4.1 Minimum inputs
| Field | Timestamp | Notes |
|---|---|---|
| Trades (price, size, aggressor, id) | Exchange event + receipt | Prefer aggressor flag over tick rule |
| L2 book snapshots + diffs with sequence ids | Event + receipt | Binance WS lacks initial snapshots; vendors fetch REST snapshots\[50\] |
| Mark, index, premium index | 1s/native | Record index constituents/weights |
| Funding realized + predicted | Settlement time | Store interval per print |
| OI (contracts and notional) | Snapshot time | Record cadence |
| Liquidations | Event time | Coverage flag |
| Options chain (bid/ask IV, OI) | Snapshot time | Never mix snapshots |
| Multi-venue spot | Event | Index replication, discovery tests |
| ETF flows, stablecoin supply, on-chain | Daily/block | Record publication lag |

### 4.2 Known data defects
- **Binance liquidation stream** [E3]:
  - Since 2021-04-27, it pushes snapshots "at a maximum frequency of 1 order push per second."\[51\]
  - The 2026-04-10 changelog changed the documented rule from "the latest" to "**the largest** one liquidation order within 1000ms."\[51\]
  - Since 2026-04-06, REST `forceOrders` covers only the past 90 days, and `allForceOrders` is no longer maintained.\[51\]
  - → Totals are lower bounds, counts are censored, and the sampling rule changed. Use a regime dummy at 2026-04-10.
- **Historical snapshots:** Binance's public liquidation-snapshot dumps were discontinued (arXiv 2607.27070), so backfills depend on whoever recorded the live stream.\[33\]
- **Aggregated OI:** coin- and USD-margined units get mixed, cross-listed products get double counted, snapshot times differ, and vendor coverage changes. Rebuild aggregates per contract.
- **Volume:** wash trading (Cong et al.). Apply a venue whitelist plus trade-size clustering and volume–volatility screens.
- **Clocks:** exchange and receipt times differ, and collector location matters (Tardis records Binance from GCP Tokyo; Binance runs on AWS Tokyo).\[50\] Use event time for causality tests and receipt time for latency-realistic backtests.
- **Outages:** on Oct 10, 2025, Binance cited "systems under heavy load" (CoinShares).\[26\] Flag feed gaps longer than a documented limit.

### 4.3 Gate G1 – data quality
1. Where complete premium observations and contemporaneous contract specifications exist, recompute funding and compare within documented rounding; otherwise mark `funding_recomputation_unavailable` and prohibit claims of verified reconstruction (do not fail unrelated descriptive analysis).
2. Each funding print carries its interval; test for interval switches.
3. OI has no negatives, units are harmonized, and contract changes are consistent with flow (soft check). Separate contract-count change from mark-price revaluation and instrument rebases.
4. For sequence-bearing L2 deltas, rebuild books with snapshot anchoring and verify continuity; for periodic L2 snapshots, check crossed/stale books but **do not claim missing event-by-event reconstruction**. Record gaps and resyncs.
5. Each venue index is within tolerance of the cross-venue median. Breaches flag outage or depeg, e.g., collateral issues reported on Oct 10, 2025 [E5].
6. Liquidation coverage is `verified_complete` **only with a reconciled event universe and known capture rules**, `observed_partial`, `sampled_lower_bound`, or `vendor_modelled`. Public on-chain fills alone do not establish that every liquidation, ADL, or backstop event has been identified.

---

## 4.4 Connector-defined venue eligibility and live capability audit (v1.1)

**A venue is eligible only for the data family successfully queried.** Installed tool descriptions show possible APIs, not an active entitlement, complete historical coverage, or continuous collector. At each run, record connector, endpoint, venue, canonical instrument, instrument type, quote/collateral token, dataset family, requested/returned window, first/last exchange timestamps, sampling resolution, actual row count, pagination/cursor exhaustion, server-side coverage flags, tier/auth restriction, receipt time, and independent spot/index comparator. Do not infer that accessible venues constitute the total market.

| Connector reachable in this environment | Data and venue scope evidenced by tool discovery | Research role and hard limitation |
|---|---|---|
| **0xArchive** | Hyperliquid native perps; separate Hyperliquid spot, HIP-3, HIP-4, Lighter mainnet and Robinhood Chain Lighter families. Historical Hyperliquid trades/fills, L2 snapshots, funding, OI, liquidations, mark/oracle; some Lighter order-book endpoints support checkpoint, 30s, 10s, 1s and `tick` frames | **Primary observed historical derivatives archive** when a family+symbol+dataset resolver and a paginated raw query both succeed. Do not merge spot/perp/HIP-3/Lighter or mistake periodic L2 snapshots for L2 diffs/L3 queue reconstruction. Tier-limited history remains limited. |
| **fin-data-mcp-http-v2** | OKX spot/swap/futures/options instrument lists; current book, public recent trades, OI, funding and bounded funding history | Independent cross-venue snapshot/short-lookback comparison, not presumed full tick archive. Return actual `instId` and timestamps. |
| **Massive** | Crypto historic trade tick endpoint and crypto aggregated bars; current L2 book endpoint discovered | Independent spot/crypto print and price corroboration where provider entitlement permits. No assumption that current L2 can backfill historical L2, or that spot ticks substitute for perpetual trades. |
| **Co-Invest / Liquid** | Symbol-level Hyperliquid/Liquid market intelligence (price, funding, OI, proprietary trader cohorts); current book viewing; limited wallet position history | Contemporary positioning context; provider-derived cohorts are non-exhaustive proxies, not independent OI census. Derived smart-money scores never bypass calibration. |
| **CoinPaprika, CoinGecko, CMC Public** | Token identity, price/market-cap metadata or market reference workflows | Canonical asset and comparator validation, **not** substitutes for derivative venue microstructure. |
| **Blockscout** | EVM contract/transaction/chain exploration | Collateral/token-event contextual evidence only. Wallet or chain observations do not automatically identify leveraged positions or complete liquidations. |
| **Other installed crypto market-data connectors** | Discover on each run; qualify response independently | Eligible only after confirming actual source venue, native time resolution and contract identity. |

**0xArchive BTC audit observation (2026-10-22T23:55Z; metadata, not a downloaded/backtested dataset):** `resolve_market_data(family=hyperliquid,symbol=BTC,dataset=orderbook)` returned an active BTC perp and an orderbook metadata window 2023-04-15T00:00:07.400Z–2026-10-22T23:55:56.500Z, with approximately 1-second sampled cadence. The same metadata lists fills from 2023-04-19 and OI/funding from 2023-05-20. These are **archive coverage claims**, not evidence that the current user tier can read all years or that every event is reconstructable. Tool documentation describes a free rolling 30-day window and up to 1,000 records/page for key historical calls; check actual server responses and entitlement. Historical L2 *snapshots* at ~1-second cadence cannot recover unseen adds/cancels, order priority, or complete sequence dynamics between snapshots. Lighter `tick` checkpoint/delta frames require both cursor and cursor sequence and independent continuity validation.

**Audit procedure:** (1) discover instruments and source market families; (2) resolve exact family/symbol/dataset, checking `selected|partial|denied|unavailable`; (3) request narrow historical slices including a nontrivial active window; (4) page to terminal cursor while deduplicating stable event IDs, and persist gap metrics; (5) test index-vs-mark and cross-venue sanity; (6) assign quality tier `T0_verified_replay`, `T1_observed_snapshots_or_trades`, `T2_aggregated_history`, `T3_current_only`, or `T4_unavailable`; (7) suppress features needing a higher tier. A server reporting `completeness:100` does not prove completeness without denominator, collection methodology and independent gap checks.

**Information-set guard:** distinguish event time, exchange publish time, connector availability time and local receive time. For every backtest feature, require `available_at <= decision_time`; a retrieved historical series is not inherently point-in-time faithful. Include fee tiers, oracle/mark revisions, funding rule versions, market launches/delistings and venue outages. Reject simulated order-book queue priority without L3/order IDs and true event deltas.

---

## 5. Detailed analytical procedures

### 5.1 Market-structure map (per run)
1. For each contract, record: venue, type, multiplier, margin asset, index constituents, mark method, funding formula, interval, cap/floor, maintenance-margin tiers, liquidation engine, insurance fund, ADL rule.
2. Record available margin modes (cross, isolated, portfolio). Portfolio margin is structural: HMRV show it compressed deviations.
3. Record settlement rules.
   - Dated futures settle to index averages.
   - CME specifications were not verified in this session (UNVERIFIED).
   - Deribit DVOL futures settle on the time-weighted DVOL between 07:00 and 08:00 UTC [E3].\[52\]
4. Hyperliquid liquidation waterfall (secondary summary [E5]; confirm in primary docs):
   - Book liquidation, in 20% clips for positions above 100,000 USDC.\[53\]
   - Backstop liquidation below 2/3 of maintenance margin.\[53\]
   - ADL at the previous mark price for negative-equity accounts.\[53\]

### 5.2 Funding analysis
1. Normalize to 8h-equivalent and APR per observation interval.
2. Use realized funding only after its settlement/publication time. Archived predicted funding is eligible solely when an authentic point-in-time prediction timestamp precedes the decision; backfilled current predictions leak information.
3. Describe the distribution:
   - quantiles;
   - share of prints at baseline $I$ (clamp region);
   - share at cap/floor;
   - skew and Hill tail index;
   - same-sign runs.
4. Measure persistence with ACF/PACF, AR(1) half-life $\ln0.5/\ln\phi$, and DAR/GARCH (Inan).
5. Compute cross-venue dispersion $\sigma_{venue}(f^{(8)}_{eq})$. HMRV attribute it to segmentation and liquidity.
6. Test lead/lag:
   - Granger causality on returns vs Δfunding;
   - local projections with HAC errors;
   - out-of-sample $R^2_{OS}$ against the historical mean.
7. **Carry P&L net of costs:**
$$\Pi=\sum \text{signed funding received}_s-c_{entry}-c_{exit}-\text{slippage}-\text{financing}-\text{hedge mismatch}-\text{margin opportunity cost}-\text{venue-risk haircut}$$
   - Hedge mismatch: index vs spot venue, inverse convexity, stablecoin basis.
   - Venue risk: FTX funding diverged on the insolvent venue (HMRV) [E2];\[3\] October 2025 ADL left spot legs naked [E5].\[54\]
8. A funding observation remains a *state descriptor* until it passes §8 for that specific asset, venue set, and horizon.

### 5.3 Open interest and positioning
1. Work in contract counts and decompose notional changes (§3.5).
2. Use the quadrant table below for description only:

| ΔP | ΔOI (contracts) | Consistent with | NOT sufficient to conclude |
|---|---|---|---|
| + | + | Net new positions while price rose | "Longs aggressive" (every new long has a new short) |
| + | − | Net closing while price rose | Which side initiated |
| − | + | Net new positions while price fell | "Shorts piling in" |
| − | − | Net closing / forced deleveraging | That liquidations caused the move |

3. Pair ΔOI with taker imbalance to describe *who demanded liquidity*. Do not claim intent: taker sells can be hedges, liquidations, or arbitrage legs.
4. Vendor long/short ratios are venue-specific account samples, not zero-sum notional. Treat them as venue-local proxies, and only after validation.
5. For ELR, interpret changes within a single venue, not levels.

### 5.4 Liquidation analytics
1. Build the observed series per venue, with coverage flags.
2. Model the mechanics: maintenance-margin tiers, mark-price triggers (not last trade), partial-liquidation rules.
3. **Modelled heatmaps** (OI × assumed leverage distribution) are hypotheses. Label them `vendor_modelled`, record their assumptions, and never backtest them as if observed.
4. Cascade diagnostics (conditional):
   - depth in a band vs modelled liquidation notional in that band;
   - OI concentration by venue (on Oct 10, 2025, Hyperliquid accounted for over half of reported liquidations);\[24\]
   - share of collateral that is non-USD or synthetic.
5. Run event studies across several cascades (§8). The evidence shows precursors differ from event to event.

### 5.5 Microstructure
1. Compute spread, depth at {5, 10, 25, 50} bps, imbalance, micro-price, OFI, and Kyle's λ.
2. Resiliency: half-life of depth recovery after large trades.
3. Adverse selection: realized vs effective spread at 1s, 5s, and 60s.
4. Multi-venue books:
   - normalize ticks and units before consolidating;
   - drop stale venues;
   - test robustness to ±latency shifts.
5. Screen for manipulation: rapid-cancel spoofing proxies and self-match/round-lot wash patterns.

### 5.6 Basis, options, volatility
1. Term structure: annualized basis by expiry, slope, and roll-down. Calibrate any thresholds locally.
2. Fit the surface (e.g., SVI) per expiry from bid/ask mid IV. Reject expiries with too few valid strikes. Track ATM term structure, RR25, BF25, and ΔDVOL.
3. VRP: $IV^2$ vs subsequent RV at the matched horizon, using 5-minute RV and a bipower jump check.
4. Dealer-gamma estimates need an assumption about who holds which side. Unless positioning is observed, label them **UNVERIFIED-model**.
5. **If reliable options data are unavailable:** do not impute IV from perps. Use RV-only measures, set `options_unavailable`, and ABSTAIN on VRP and skew signals.

### 5.7 Volatility modelling
- Models: GARCH(1,1), GJR, and EGARCH with Student-t errors; HAR-RV(-J).
- Comparison: QLIKE/MSE losses with Diebold–Mariano tests, plus a Model Confidence Set when many models are compared.
- A cascade preprint reports α+β ≈ 0.92 around October 2025 [E4-quality].\[55\] Treat it as illustrative only.

### 5.8 Cross-venue price discovery
1. Run Johansen cointegration only on synchronized, currency-comparable digital-currency spot/perp/futures series with sufficient observations; exclude ETF NAV and equity/index synthetics from the core universe.
2. Fit a VECM and compute Hasbrouck IS bounds (across orderings), Gonzalo–Granger CS, and ILS.
3. For asynchronous ticks, use Hayashi–Yoshida cross-correlation over a lag grid.
4. Re-estimate on rolling windows and report leadership as a distribution over time.

---

## 5.9 Coverage-aware workflows by data tier (v1.1)

- **T0 — verified event replay:** aggressor-side trades and ordered L2 deltas with sequence continuity plus known fees/latency; OFI and execution simulations may be tested, but L3 priority remains unavailable without order-level events.
- **T1 — observed historical trades and/or periodic book snapshots:** trade-imbalance, quoted depth/spread and snapshot-conditioned price-impact studies are eligible. Snapshot-difference proxies may be defined separately; they **are not CKS event OFI** unless all underlying add/cancel/execute updates are observed.
- **T2 — candle/aggregate funding/OI only:** carry, basis, medium-frequency volatility and lagged OI hypotheses. No tick-by-tick impact, spoofing classifications or liquidation print reconstruction.
- **T3 — current-only:** descriptive current-state monitoring; no historic signal promotion without independently retained point-in-time data.
- **T4 — absent/unusable:** mark each unavailable modality, preserve the others; do not fabricate substitutes.

Disallow any feature that combines current-position cohort membership with historic features unless cohort membership was archived as of the decision date. Align changing token decimals, contract specifications, funding regimes and index basket compositions as-of-time. Analyze BTC/ETH/SOL separately before pooling; for illiquid digital currencies demand token-age and listing/delisting survivorship controls and a minimum effective sample size determined before testing.

**Microstructure verification:** define depth either in native size or common USD notional, specify fixed-bps versus fixed-level band, record book age, and measure sensitivity to 1/5/10-second sampling plus observed delivery latency. For Lighter tick frames, require documented delta semantics, checkpoint recovery and gap-free sequence; do not assume Hyperliquid 1-second snapshots are comparable to Lighter tick frames.

**Liquidity-adjusted economic validation:** propagate venue maker/taker fees, rebate eligibility, queue-position uncertainty, nonlinear market impact, funding timing, cross-venue transfer time, inventory/margin funding costs, liquidation probability and ADL haircut scenarios. Stress spot/perp leg disconnect, stablecoin depeg, API outage and insufficient withdrawability. Report capacity and worst-case execution failure separately from expected net returns.

---

## 6. Signal specification tables

All thresholds are **placeholders θ, to be calibrated walk-forward**. The literature endorses no universal numeric threshold.

### 6.1 Signal catalog

| ID | Definition (units) | Inputs + timestamps | Hypothesis | Horizon | Supporting | Contradicting / limits | Confounders | Validation | Abstain when |
|---|---|---|---|---|---|---|---|---|---|
| S1 Funding extreme | $z=(APR-\text{med}_W)/\text{MAD}_W$, realized prints | Funding, interval, settlement time | Crowded leveraged demand → higher reversal/crash risk | 1–30d | SST carry→crashes [E1]; HMRV extrapolative demand [E2] | Fulgur R²≈0.003 [E4]; Yang disclaimer [E2]; Inan: funding forecastable ≠ returns | Interval switches; caps; clamp mass; stablecoin rates | Walk-forward local projections; SPA; DSR | Cap/floor binding; interval change in window; too few episodes |
| S2 Basis dislocation | $p_t-\text{band}^{no\text{-}arb}_t$ (APR %), HMRV cost band; dated basis z | Mark, index, fee tier, rates | Beyond-band deviation = constrained arbitrage → basis mean-reverts (not necessarily price) | hours–weeks | HMRV Sharpe 3.27–10.46 after spreads [E2]; SST [E1] | Compression since 2024 [E2] | Index composition; depeg; venue solvency | OOS convergence rate; net P&L | Solvency doubt; withdrawal halt; index outage |
| S3 OI-conditioned move | $\Delta OI^c_{h}/OI^c$ × sign($r_h$) × taker OIB | OI contracts, trades | New leverage alongside price moves → fragility | 1–7d | Cascade OI −43% [E4] | Precursors not event-invariant [E2] | Revaluation; listings; ETF basis trades | Conditional event study; regime splits | Only notional OI; low venue coverage |
| S4 Liquidation stress | $LI_t$ (% OI/h) and $(L_{long}-L_{short})/(L_{long}+L_{short})$ | Liq feed + coverage flag, OI | Price-insensitive forced flow → overshoot/reversal, or continuation if thin | min–2d | Oct 2025 $16.7B vs $2.46B [E5]; ADL papers [E2] | Lower-bound feeds; no invariant precursor [E2] | ADL vs liquidation; 2026-04-10 rule change | Event study, matched controls | Only `vendor_modelled`; no regime dummy |
| S5 Vol expansion | $\ln(RV_{1d}/\widehat{RV}^{HAR})$; ΔDVOL; VRP | 5-min returns, DVOL, chain | Volatility clusters; compressed VRP precedes stress | 1–30d | HAR/GARCH [E1]; BTC VRP 0.14 [E2] | Predicts magnitude, not sign | Jumps; weekends | DM/MCS; sign tests | Options unavailable → VRP leg off |
| S6 Order-flow imbalance | $OFI_h/\bar D$ (unitless) | L2 diffs, sequence ids, event time | Net aggressive demand moves price ∝ 1/depth | sec–min | CKS [E1]; arXiv 2602.00776 [E2] | Fast decay; concavity; spreads | Spoofing; latency; tick size | Purged CV vs martingale; latency shifts | Book gaps; resync; stale venue |
| S7 Funding dispersion | $\sigma_{venue}(f^{(8)}_{eq})$ (bps/8h) | Funding, all venues | Segmentation/stress | 1–7d | HMRV (FTX dispersion) [E2] | Small-venue noise | Interval mismatch | Event study vs stress dates | Fewer than 3 valid venues |
| S8 Carry crash-risk | Standardized carry z (SST definition) | Basis, spot | High carry predicts crashes | 1–3m | SST [E1] | Post-ETF compression [E5] | Rates; ETF basis capacity | Rolling OOS logit for drawdown > θ | Fewer than 2 boom-bust cycles |

### 6.2 Units and timestamp discipline
Funding is stored as a decimal per settlement plus interval hours, then converted to APR. OI is stored in both contracts and USD, with snapshot times. Liquidations are stored in USD with event time and coverage flag. Every feature must be timestamped at or before decision time minus its publication lag (e.g., ETF flows are published after the US close).

### 6.3 Max pain (critical evaluation)
Max pain is the strike that minimizes aggregate option-holder payoff at expiry. Its pinning story assumes dealers are net short options and hedge in a way that pulls price toward that strike. Public OI data cannot observe either assumption, and no peer-reviewed crypto evidence was found → **UNVERIFIED**. It is excluded from decisions by default. If tested, use an expiry-window event study with random-strike placebos.

---

## 7. Worked hypothetical examples (ALL NUMBERS HYPOTHETICAL)

**H1 – Normalization.**
- Venue A (8h) prints 0.0300%. Venue B (hourly) prints 0.0050%.
- 8h-equivalents: A = 0.0300%; B = 0.0400%.
- APR: A = 0.03% × 1095 = 32.85%; B = 0.005% × 8760 = 43.8%.
- Comparing the raw prints would have reversed the ranking.

**H2 – Cash-and-carry.**
- $1,000,000 notional at 20% APR for 30 days → gross ≈ $16,438.
- Costs:
  - fees (4 legs × 4 bps) $1,600;
  - slippage (4 legs × 3 bps) $1,200;
  - 5% opportunity cost on 50% margin ≈ $2,055;
  - 2% venue haircut ≈ $822.
- Net ≈ $10,761 (≈13.1% APR), *if funding persists*.
- A sign flip, or a mark spike that liquidates the short leg, leaves an unhedged long.

**H3 – OI interpretation.**
- Price +4%, notional OI +6%, contracts +1.9%, taker OIB +0.08.
- Most of the notional rise is revaluation.
- Correct: "net new contracts opened while takers bought." Incorrect: "longs are piling in."

**H4 – Liquidation feed bias.**
- Over 60s, Binance's stream yields 60 messages totalling $12M. An on-chain venue reports $30M from complete fills.
- This does not show Binance liquidated less. Its figure is a lower bound (at most one order per symbol per second, the largest since 2026-04-10).

**H5 – Protocol run.**
- G1 passes.
- S1 funding z = +2.8 vs calibrated θ = 2.5 (2021–2025 walk-forward; Holm-adjusted p = 0.03 for 7-day drawdown probability).
- S8 elevated; S3 contracts rising with price; VRP compressed.
- Spot IS midpoint = 0.6; ETF flows positive.
- Output: **INCONCLUSIVE (directional)**, with `elevated_downside_tail_risk=true`. S1 and S8 predict crash probability, not drift sign, and spot demand contradicts them.

---

## 8. Statistical tests and rejection criteria

Significance levels are conventions and must be pre-registered (default α = 0.05 after correction).

| Method | Assumptions | Specification | Window | Diagnostics | Inappropriate when |
|---|---|---|---|---|---|
| ADF/KPSS, Zivot–Andrews | Linear AR; ZA allows a break | Unit-root tests | Several hundred obs | AIC/BIC lags | Unmodelled breaks (ETF, interval changes) |
| VAR + Granger | Stationarity; correct lags | $y_t=\sum A_iy_{t-i}+u_t$; Wald on cross-lags | Rolling 30–180d | Ljung–Box; stability roots | Levels; asynchronous data; omitted common driver |
| Johansen VECM | I(1); Gaussian errors | $\Delta y_t=\alpha\beta'y_{t-1}+\sum\Gamma_i\Delta y_{t-i}+\epsilon$ | Rolling | Trace/max-eig; α significance | Unadjusted rolls; USD vs USDT mismatch |
| Hasbrouck IS / GG CS / ILS | Valid VECM | IS via Cholesky (bounds); CS via $\alpha_\perp$ | Intraday | IS bound width | Wide bounds → report CS/ILS |
| Hayashi–Yoshida | Asynchronous diffusions | $\sum\Delta X_i\Delta Y_j\mathbb 1\{I_i\cap J_j\neq\emptyset\}$ over lags | Tick | Bootstrap CI | Heavy noise without pre-averaging |
| GARCH/GJR/EGARCH | Conditional variance; t errors | $\sigma^2_t=\omega+\alpha\epsilon^2_{t-1}+\gamma\epsilon^2_{t-1}\mathbb 1_{<0}+\beta\sigma^2_{t-1}$ | ≥2–3y daily | ARCH-LM; sign bias | Jump-dominated; unstable parameters |
| RV / HAR | Semimartingale | §3.8 | 5-min default | Signature plot; jump tests | Ultra-HF without noise-robust estimator |
| Markov switching | Finite Markov regimes | $y_t\mid s_t\sim N(\mu_s,\sigma^2_s)$ | Multiple episodes | Label stability | Smoothed (look-ahead) probabilities in backtests |
| Event study | Clean, non-overlapping dates | CAR vs matched controls | ≥10 events (convention) | Placebos | Single event → descriptive only |
| Local projections | HAC | $r_{t\to t+h}=a_h+b_hx_t+\Gamma Z_t+e$ | Rolling OOS | Newey–West lags ≥ h | Overlap without HAC |
| White RC / Hansen SPA | Stationary loss differentials | Bootstrap max vs benchmark | All variants tried | Report all variants | Hidden variants |
| Harvey–Liu–Zhu; Holm/BHY | Multiple testing | t ≈ 3.0 hurdle (equity-factor recommendation; floor, not crypto calibration) | — | Test count | — |
| Deflated Sharpe; PBO | Non-normal; N trials known | DSR adjusts for N, skew, kurtosis; PBO via CSCV | — | Report N | Unknown N → assume large |
| Purged/embargoed walk-forward | Overlapping labels | Purge overlaps; embargo after test | Fold ≥ several × horizon | Leakage audit | Random K-fold |
| Diebold–Mariano / MCS | Stationary $d_t$ | DM HAC t-stat | OOS | HAC | Nested models → Clark–West |

**Promotion rule (descriptive → validated).** All of the following must hold:
1. The pre-specified target and out-of-sample effect sign are consistent in at least two non-overlapping regimes **if two independent regimes exist**; otherwise label preliminary, not validated.
2. The adjusted p-value is below α across the recorded family of tried variations (or a preregistered confidence-sequence/e-value design applies); report effect-size confidence intervals and effective episode/sample counts.
3. For trading rules, DSR probability > 0.95 (convention).
4. For economic strategies, net-of-cost performance stays positive under adverse (not just median) fees, latency, funding sign flips and capacity assumptions; a purely predictive, non-tradable forecast is evaluated on its proper loss and calibration instead.
5. The effect survives known confounders, asset/venue clusters, point-in-time leakage tests, delisted-token inclusion and a genuinely untouched forward holdout. The final model/threshold is frozen before holdout evaluation.

---

## 9. Failure modes and research limitations

1. **Regime breaks.** Portfolio margin (2022) compressed deviations. Spot ETFs (2024) moved price discovery to spot. Binance funding-interval rules changed in 2023, 2025, and 2026. The liquidation-stream wording changed on 2026-04-10.
2. **Censoring.** Caps and clamps truncate funding; snapshots truncate liquidations. Use censored or indicator models.
3. **Survivorship.** FTX data end abruptly, and delisted contracts are often missing.
4. **Single-event overfitting.** October 2025 dominates recent tails, and its patterns inverted on other events (arXiv 2607.27070).\[32\]
5. **Model-dependent ADL conclusions.** Overshoot estimates range from $653M down to $45–52M depending on the model.
6. **Vendor opacity.** Heatmaps, long/short ratios, ELR, and a "5% liquidation-intensity threshold" (Amberdata blog [E4])\[56\] are UNVERIFIED as thresholds.
7. **Wash volume** inflates turnover and liquidity proxies.
8. **Asynchronous clocks** can create spurious lead–lag.
9. **External validity.** Evidence is mostly BTC/ETH on Binance, BitMEX, Deribit, and CME. Generalization to altcoins and DEXs is weak.
10. **Capacity decay.** Published profits attract capital: HMRV find deviations shrinking about 22 pp per year, and carry has compressed since 2024.\[3\]\[6\]

---

## 10. Operational checklist

- [ ] **G0** Record scope: asset, venues, horizon, decision time (UTC).
- [ ] **G1** Data quality (§4.3): coverage flags set, interval audit done, clock offset logged.
- [ ] **G2** Archive contract specs, funding formula, cap, and interval as of each timestamp.
- [ ] **G3** Normalize: funding to 8h-equivalent and APR; OI in contracts and USD.
- [ ] **G4** State description: funding, basis term structure, OI decomposition, observed liquidations, liquidity, vol/VRP/skew.
- [ ] **G5** Only `validated` signals vote; the rest are reported as context.
- [ ] **G6** Cross-market confirmation (§11).
- [ ] **G7** Decision (§12), with evidence table and abstention reasons.
- [ ] **G8** Log input hash, model versions, and number of variants tried (for DSR/SPA).

---

## 11. Cross-market confirmation

1. **Spot vs perp leadership.** Use rolling IS/CS/ILS **only where synchronized eligible venue prices exist**. Post-ETF Bitcoin results are period- and instrument-specific; do not impose spot leadership on other currencies.
2. **Alignment.** Confirm the perp premium against each venue’s index and another **independently observed eligible venue when available**. Fewer than two independent venues means `single_venue_limitation`, not invented confirmation.
3. **ETF flows (optional BTC/ETH macro context).** Use lagged, timestamp-available observations only, if the connected source exposes them. ETF/CME positioning may reflect basis hedging; do not infer directional investor intent.
4. **Stablecoin supply.** Slow-moving liquidity context only. No validated short-horizon threshold was found (UNVERIFIED as a signal).
5. **On-chain flows.** Depend on vendor wallet labels (E4); context only.
6. **Macro risk.** The October 2025 cascade followed President Trump's Oct 10, 2025 announcement of an additional 100% tariff on Chinese imports (CNN; CoinShares). Per CoinShares (Oct 20, 2025), Bitcoin "plunged as low as $104,782.88… down more than 14% from its Friday high of $122,574.46," and Ether fell 12.2% to $3,436.29. Exogenous shocks can override derivatives signals, so report a risk flag.
7. **Liquidity state.** Wide spreads or collapsed depth reduce the reliability of microstructure signals (arXiv 2602.00776).\[15\]

---

## 12. Operational decision protocol

**Inputs:** the set $\mathcal V$ of validated signals for this asset and horizon. Each has a sign $d_i\in\{-1,0,+1\}$, a calibrated strength $s_i$, and reliability flags. Also the context set $\mathcal C$ (§11).

1. If G1 fails or $|\mathcal V|=0$ → **INCONCLUSIVE** (`data_quality` / `no_validated_signal`).
2. Drop any signal whose abstention condition is triggered.
3. If every remaining signal sits in its calibrated neutral zone → **NEUTRAL**.
4. Compute $A=\sum_i d_i$ with **equal votes**, unless locally calibrated weights have been validated out-of-sample under §8. This file provides no universal weights.
5. Signals of opposite sign with comparable strength → **INCONCLUSIVE** (`signal_conflict`). Correlated signals sharing inputs or construction count as one cluster unless joint weighting is externally validated.
6. If $A>0$ ($<0$), **at least one independent OOS-calibrated return-direction signal is present**, and no validated context item contradicts → **BULLISH** (**BEARISH**). Otherwise → **INCONCLUSIVE** (`cross_market_conflict` or `non_directional_evidence_only`).
7. Tail-risk signals (S1, S4, S5, S8) validated only for magnitude or crash probability set flags (`elevated_downside_tail_risk`, `elevated_vol`). They do not set direction.
8. The output reports horizon, an evidence table (value, calibration window, OOS statistics), contradicting evidence, and abstention reasons. Avoid claims about trader intent.

---

## 13. Machine-readable indicator specifications

```yaml
id: S1_funding_extreme
version: 1.0.0
status: descriptive   # 'validated' only after Section 8 promotion rule
inputs:
  - {name: funding_realized, unit: decimal_per_settlement, timestamp: settlement_time_utc,
     required_fields: [venue, symbol, interval_hours, rate, cap, floor]}
transform:
  normalize_8h_eq: "rate * 8 / interval_hours"
  apr_simple: "rate * 8760 / interval_hours"
  zscore: "(apr - rolling_median(apr, W)) / rolling_mad(apr, W)"
params:
  W: {value: null, calibrate: walk_forward}
  theta_high: {value: null, calibrate: walk_forward}
hypothesis: "Crowded leveraged demand raises crash/reversal probability (SST)"
horizon_days: [1, 7, 30]
evidence: {supporting: [SST_BIS1087, HMRV_v7], contradicting: [Fulgur_R2_0.003, Yang_SSRN_7397158]}
confounders: [interval_switch, cap_binding, clamp_mass, stablecoin_rate_shift]
validation: {cv: purged_walk_forward, embargo: "max(horizon)", multiple_testing: [hansen_spa, holm], sharpe: deflated}
abstain_if: ["share_at_cap_or_floor > limit", "interval_regime_change == true", "episodes < min_episodes"]
output_semantics: "tail-risk flag unless direction validated"
```

```json
{
  "id": "S4_liquidation_stress",
  "version": "1.0.0",
  "status": "descriptive",
  "inputs": [
    {"name": "liquidations", "unit": "usd_notional", "timestamp": "exchange_event_time",
     "coverage_flag": ["complete", "sampled", "vendor_modelled"]},
    {"name": "open_interest", "unit": "usd_and_contracts", "timestamp": "snapshot_time"}
  ],
  "definition": {"LI": "sum(liq_usd over (t-h,t]) / OI_usd(t-h)",
                 "one_sidedness": "(L_long - L_short) / (L_long + L_short)"},
  "data_rules": {"binance_usdm": "max 1 order/symbol/1000ms since 2021-04-27; 'largest' since 2026-04-10",
                 "lower_bound_if": "sampled", "exclude_if": "vendor_modelled", "regime_dummy": "2026-04-10"},
  "params": {"h_minutes": null, "theta": null, "calibration": "walk_forward_event_study"},
  "abstain_if": ["only_vendor_modelled", "feed_gap_seconds > limit"]
}
```

```yaml
id: S6_ofi_depth_normalized
definition: "sum(e_n over [t,t+h]) / mean_depth_k_bps"
inputs: [l2_diffs_with_sequence_ids, exchange_timestamp, receipt_timestamp]
params: {h_seconds: null, k_bps: null}
benchmark: martingale_midprice
validation: {cv: purged_walk_forward, latency_shift_ms: [0, 50, 200], multiple_testing: holm}
abstain_if: [sequence_gap, book_resync_in_window, venue_stale]
```

---

## 14. Evidence-to-methodology traceability matrix

| # | Claim | Source | Grade | Used in |
|---|---|---|---|---|
| 1 | Perp = risk-neutral spot at random time; linear/inverse/quanto | AHJ | E1 | §3.1, §3.4 |
| 2 | Deviations 52–90%/yr, −22 pp/yr; Sharpe 3.35–11.65; portfolio margin compresses | HMRV v7 | E2 | §2.1, S2, §9 |
| 3 | Funding corr 0.74; Bybit spreads 2–10× | HMRV v7 | E2 | S7 |
| 4 | Taker flow leans against deviation | HMRV App. D.6 | E2 | §3.7 |
| 5 | Carry >10%, up to 60%; predicts crashes | SST | E1/E2 | S1, S8 |
| 6 | Carry Sharpe 6.45; compressed since 2024 | arXiv 2510.14435 | E2 | §2.2 |
| 7 | Binance formula, clamp, 5s premium | Binance FAQ | E3 | §3.2 |
| 8 | Binance 4h/1h/revert rules | Binance FAQ / mirror | E3/E5 | §3.2 |
| 9 | Hyperliquid hourly, 4%/h cap | Hyperliquid docs | E3 | §3.2 |
| 10 | Liquidation stream 1/s; "largest" since 2026-04-10; 90-day REST | Binance docs/changelog | E3 | §4.2, S4 |
| 11 | Oct 2025 $19.13B, >1.6M traders; $16.7B/$2.46B; venue split | CoinGlass via Coinpedia/media | E5 | §2.6 |
| 12 | OI −43%; Hyperliquid −57% | CoinDesk Research | E4 | S3 |
| 13 | 34,983 ADL; $2.1B/12 min; ~$653M | arXiv 2512.01112 | E2 | §2.6 |
| 14 | Overshoot $45.0–51.7M | arXiv 2602.15182 | E2 | §2.6 |
| 15 | Event-heterogeneous precursors; dumps discontinued | arXiv 2607.27070 | E2 | §5.4 |
| 16 | Wash trading avg 77.5% (median 79.1%) on unregulated exchanges | Cong et al. 2023 | E1 | §4.2 |
| 17 | OFI linear ∝ 1/depth | CKS 2014 | E1 | S6\[13\] |
| 18 | Crypto OFI monotone/concave | arXiv 2602.00776 | E2 | S6, §11 |
| 19 | BitMEX leads spot | Alexander et al. 2020 | E1 | §2.3 |
| 20 | Spot dominant post-ETF | Kia et al. 2026 | E1 | §2.3, §11 |
| 21 | Binance spot+perps lead | Cosenza & Stalder | E2 | §2.3 |
| 22 | CME leads (Hayashi–Yoshida) | JIMF 2025 | E1 | §5.8 |
| 23 | DVOL construction | Deribit | E3 | §2.8 |
| 24 | BTC VRP 0.14 | arXiv 2410.15195 | E2 | S5 |
| 25 | Funding predictable (DAR) | Inan SSRN | E2 | §2.5 |
| 26 | Max pain pinning | none | U | §6.3 |
| 27 | 5% liquidation-intensity threshold | Amberdata blog | E4/U | §9 |

---

## 14.1 Version 1.1 evidence and connector change log

| Change | Evidence level | Operational consequence |
|---|---|---|
| Inan (2026-10-17) now an online *IRFA* journal pre-proof rather than only an SSRN manuscript | E1 provisional publication status | Upgrade bibliographic provenance; retain funding-versus-return distinction. |
| Shek (2026-09-26), conditional negative-funding reversals, BTC/ETH/SOL | E2 single independent-author working paper | Pre-register regime interaction and replicate; no fixed reversal rule. |
| Shek (2026-09-29), funding-drag and volatility-conditioned time to parity | E2 working paper | Optional survival-analysis hypothesis for basis correction; independently replicate. |
| 2026 *Studies in Economics and Finance* leverage/systemic-risk research | E1 | Add portfolio/tail-risk endpoint and examine transfer outside Binance. |
| 0xArchive Hyperliquid BTC metadata returned in this run | Tool observation, not academic validation | Source-specific historical modality gates, rolling-tier/access and event-vs-snapshot distinctions. |
| OKX/Massive/Co-Invest/CoinPaprika connector tool discovery | Tool specification, not successful end-to-end archive validation | Venue selection by successful family-specific retrieval, not static venue list. |

## 15. Bibliography

*† = standard citation whose DOI was not re-verified against the publisher in this session; confirm before external use.*

**Newly verified / supplemental research (as of 2026-10-22)**
- Inan (2026), *Predictability of funding rates*, *International Review of Financial Analysis*, online 2026-10-17, article 105464. https://doi.org/10.1016/j.irfa.2026.105464
- Shek (2026), *Conditional Arbitrage Capacity: Evidence from Crypto Perpetual Funding Rates* [SSRN working paper]. https://papers.ssrn.com/sol3/papers.cfm?abstract_id=7520320
- Shek (2026), *Limits to Coordination: Funding Drag in Crypto Perpetual Funding Rates* [SSRN working paper]. https://papers.ssrn.com/sol3/papers.cfm?abstract_id=7529458
- *Systemic risk from financial leverage in digital asset markets: evidence from cryptocurrency derivatives* (2026), *Studies in Economics and Finance*. https://doi.org/10.1108/SEF-04-2026-0367
- Garcia Seuma (2026), *Where does the criticality live?* [arXiv working paper]. https://arxiv.org/abs/2607.27070
- 0xArchive MCP, Hyperliquid historical L2 snapshots/trades/coverage: tool metadata audited 2026-10-22; revalidate each session. (No academic citation implied.)

**Perpetuals, carry, basis**
- Ackerer, Hugonnier & Jermann (2026). Perpetual Futures Pricing. *Mathematical Finance* 36(3).\[1\] https://doi.org/10.1111/mafi.70018 ; NBER w32936 https://doi.org/10.3386/w32936
- He, Manela, Ross & von Wachter. Fundamentals of Perpetual Futures. arXiv:2212.06888v7. https://doi.org/10.48550/arXiv.2212.06888
- Schmeling, Schrimpf & Todorov. Crypto Carry. BIS WP 1087 https://www.bis.org/publications/working-paper-1087-crypto-carry ; *Management Science* (2026) https://doi.org/10.1287/mnsc.2024.05069 \[5\]
- Christin, Routledge, Soska & Zetlin-Jones. The Crypto Carry Trade. https://gerbil.life/papers/CarryTrade.v1.2.pdf
- Hugonnier & Jermann. Perpetual Futures Pricing with Stochastic Rates and Clamp (WP).\[57\] https://finance.wharton.upenn.edu/~jermann/research.html
- Cryptocurrency as an Investable Asset Class: Coming of Age. https://arxiv.org/abs/2510.14435
- Inan, E. (2026). Predictability of funding rates. *International Review of Financial Analysis*, article 105464, available online 2026-10-17 (journal pre-proof). https://doi.org/10.1016/j.irfa.2026.105464 ; earlier SSRN https://papers.ssrn.com/sol3/papers.cfm?abstract_id=5576424
- Yang. Apparent Roughness and Funding-Rate Asymmetry. https://papers.ssrn.com/sol3/papers.cfm?abstract_id=7397158

**Price discovery**
- Alexander, Choi, Park & Sohn (2020). *J. Futures Markets* 40(1), 23–43. https://doi.org/10.1002/fut.22050 \[7\]
- Cosenza & Stalder. Where is the Price of Bitcoin Determined? https://papers.ssrn.com/sol3/papers.cfm?abstract_id=4983566
- Kia et al. (2026). Price Discovery in Bitcoin ETF Market. *Financial Review*. https://doi.org/10.1111/fire.70026
- Price discovery in bitcoin spot and futures markets (2025). *JIMF*. https://www.sciencedirect.com/science/article/abs/pii/S0261560625001500
- Time-varying futures role in Bitcoin pricing. https://pubmed.ncbi.nlm.nih.gov/38620702
- Makarov & Schoar (2020). *JFE* 135(2), 293–319. https://doi.org/10.1016/j.jfineco.2019.07.001 \[5\]
- Hasbrouck (1995). *J. Finance* 50(4). https://doi.org/10.1111/j.1540-6261.1995.tb04054.x †
- Gonzalo & Granger (1995). *JBES* 13(1). https://doi.org/10.1080/07350015.1995.10524576 †
- Hayashi & Yoshida (2005). *Bernoulli* 11(2). https://doi.org/10.3150/bj/1116340299 †
- Johansen (1991). *Econometrica* 59(6). https://doi.org/10.2307/2938278 †

**Microstructure and integrity**
- Cont, Kukanov & Stoikov (2014). *J. Financial Econometrics* 12(1), 47–88. https://doi.org/10.1093/jjfinec/nbt003 \[13\]\[14\]
- Stoikov (2018). The micro-price. *Quantitative Finance* 18(12). https://doi.org/10.1080/14697688.2018.1489139 \[18\]
- Kyle (1985). *Econometrica* 53(6). https://doi.org/10.2307/1913210 †
- Glosten & Milgrom (1985). *JFE* 14(1). https://doi.org/10.1016/0304-405X(85)90044-3 †
- Cong, Li, Tang & Yang (2023). Crypto Wash Trading. *Management Science* 69(11). https://doi.org/10.1287/mnsc.2021.02709 \[58\]
- Explainable Patterns in Cryptocurrency Microstructure. https://arxiv.org/abs/2602.00776
- The Quarter-Hour Effect. https://arxiv.org/abs/2607.09426
- When Does Order Flow Matter? https://arxiv.org/abs/2607.09230

**Liquidations, ADL, cascades**
- Chitra. Autodeleveraging: Impossibilities and Optimization. https://arxiv.org/abs/2512.01112
- Chitra & Thogiti. Autodeleveraging as Online Learning. https://arxiv.org/abs/2602.15182
- Risk-Based Auto-Deleveraging. https://arxiv.org/abs/2603.15963
- Where does the criticality live? https://arxiv.org/abs/2607.27070
- Liquidation, Leverage and Optimal Margin in Bitcoin Futures Markets. https://arxiv.org/abs/2102.04591
- CoinDesk Research, $19B liquidation. https://www.coindesk.com/research/market-spotlight-the-19-billion-liquidation-that-shook-crypto
- CoinShares, Billions in liquidations. https://coinshares.com/us/insights/knowledge/billions-in-liquidations-what-happened/

**Volatility and options**
- Andersen, Bollerslev, Diebold & Labys (2003). *Econometrica* 71(2). https://doi.org/10.1111/1468-0262.00418 †
- Corsi (2009). *JFEc* 7(2). https://doi.org/10.1093/jjfinec/nbp001 †
- Barndorff-Nielsen & Shephard (2004). *JFEc* 2(1). https://doi.org/10.1093/jjfinec/nbh001 †
- Bollerslev (1986). *J. Econometrics* 31(3). https://doi.org/10.1016/0304-4076(86)90063-1 †
- Glosten, Jagannathan & Runkle (1993). *J. Finance* 48(5). https://doi.org/10.1111/j.1540-6261.1993.tb05128.x †
- Hamilton (1989). *Econometrica* 57(2). https://doi.org/10.2307/1912559 †
- Almeida, Grith & Miftachov. Risk Premia in the Bitcoin Market. https://arxiv.org/abs/2410.15195
- Winkel & Härdle (2023). *Risks* 11(5), 85. https://doi.org/10.3390/risks11050085
- Alexander & Imeraj. The Bitcoin VIX and Its Variance Risk Premium. https://www.pm-research.com/content/iijaltinv/23/4/84
- Deribit. DVOL methodology. https://insights.deribit.com/exchange-updates/dvol-deribit-implied-volatility-index/

**Multiple testing and validation**
- White (2000). *Econometrica* 68(5). https://doi.org/10.1111/1468-0262.00152 †
- Hansen (2005). *JBES* 23(4). https://doi.org/10.1198/073500105000000063 †
- Harvey, Liu & Zhu (2016). *RFS* 29(1). https://doi.org/10.1093/rfs/hhv059 †
- Bailey & López de Prado (2014). Deflated Sharpe Ratio. *JPM* 40(5). https://doi.org/10.3905/jpm.2014.40.5.094 †
- Bailey, Borwein, López de Prado & Zhu. Probability of Backtest Overfitting. *J. Computational Finance*. https://doi.org/10.21314/JCF.2016.322

**Exchange documentation**
- Binance funding FAQ. https://www.binance.com/en/support/faq/introduction-to-binance-futures-funding-rates-360033525031
- Binance derivatives changelog. https://developers.binance.com/docs/derivatives/change-log
- Binance liquidation streams. https://developers.binance.com/docs/derivatives/usds-margined-futures/websocket-market-streams/Liquidation-Order-Streams
- Hyperliquid funding. https://hyperliquid.gitbook.io/hyperliquid-docs/trading/funding
- Tardis.dev Binance futures details. https://docs.tardis.dev/historical-data-details/binance-futures
- Bybit, OKX, BitMEX, dYdX, CME specifications: not re-fetched in this session; retrieve current versions before use (UNVERIFIED here).

---

## 16. Version, research cutoff, update triggers

- **Version:** 1.1.0 · **Research cutoff:** 2026-10-22 · Signal statuses default to `descriptive`; all connector access is re-audited on each run.
- **Review when any of these occur:**
  1. A venue changes its funding formula, interval rule, cap, or liquidation/ADL engine.
  2. A liquidation feed changes its sampling or retention rules (cf. Binance 2026-04-10 / 2026-04-06).
  3. A new top-tier liquidation cascade, or any ADL activation on a major venue.
  4. New peer-reviewed or central-bank work on perp pricing, funding predictability, price discovery, or cascade early warning, or a new HMRV/SST version.
  5. A structural change: new ETF types, regulated perpetuals, or collateral rules (e.g., the CFTC's December 2025 crypto-collateral pilot reported by TokenPost [E5]).
  6. A validated signal fails its promotion rule on the latest fold → demote it to `descriptive`.
  7. An annual review in any case.

## Sources

1. [EconPapers: Perpetual Futures Pricing](https://econpapers.repec.org/paper/nbrnberwo/32936.htm)
2. [Fundamentals of Perpetual Futures](https://ouci.dntb.gov.ua/en/works/lmagXvBl/)
3. [Fundamentals of Perpetual Futures](https://arxiv.org/html/2212.06888v7)
4. [Crypto carry](https://www.bis.org/publications/working-paper-1087-crypto-carry)
5. <https://api.crossref.org/works?filter=doi:10.1016/j.jfineco.2019.07.001,doi:10.1287/mnsc.2024.05069&select=DOI,title,container-title,volume,issue,page,published,abstract>
6. [Cryptocurrency as an Investable Asset Class: Coming of Age](https://arxiv.org/pdf/2510.14435)
7. <https://api.crossref.org/works/10.1002/fut.22050>
8. [Where is the Price of Bitcoin Determined? Price Discovery in a Fragmented Market by Riccardo Cosenza, Simon Stalder :: SSRN](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=4983566)
9. [Price Discovery in Bitcoin ETF Market - Kia - 2026 - Financial Review - Wiley Online Library](https://onlinelibrary.wiley.com/doi/10.1111/fire.70026)
10. [Price discovery in bitcoin spot and futures markets - ScienceDirect](https://www.sciencedirect.com/science/article/abs/pii/S0261560625001500)
11. [What role do futures markets play in Bitcoin pricing? Causality, cointegration and price discovery from a time-varying perspective? - PubMed](https://pubmed.ncbi.nlm.nih.gov/38620702)
12. [The Price Impact of Order Book Events](https://oamonitor.ireland.openaire.eu/rpo/rcsi/search/publication?pid=10.2139%2Fssrn.1712822)
13. [The price impact of order book events - Archive ouverte HAL](https://hal.science/hal-00937055)
14. [Price Impact of Order Book Events](https://academic.oup.com/jfec/article-abstract/12/1/47/816163)
15. [Explainable Patterns in Cryptocurrency Microstructure](https://arxiv.org/html/2602.00776v1)
16. [The Quarter-Hour Effect: Periodic Algorithmic Trading and Return Predictability in Cryptocurrency Futures](https://arxiv.org/html/2607.09426v2)
17. [CHARLES UNIVERSITY FACULTY OF SOCIAL SCIENCES Institute of Economic Studies](https://dspace.cuni.cz/bitstream/handle/20.500.11956/213492/130479083.pdf?sequence=1&isAllowed=y)
18. <https://api.crossref.org/works/10.1080/14697688.2018.1489139>
19. [Predictability of Funding Rates by Emre Inan :: SSRN](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=5576424)
20. [Apparent Roughness and Funding-Rate Asymmetry: Evidence from Bitcoin and Ether Perpetuals by Fuli Yang :: SSRN](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=7397158)
21. [Bitcoin funding rates and price predictability](https://medium.com/@fulgur.ventures/bitcoin-funding-rates-and-price-predictability-27ce95535af1)
22. [Can Funding Rate Predict Price Change?](https://www.prestolabs.io/research/can-funding-rate-predict-price-change)
23. [October 10 Crypto Crash Explained: Causes & Statistics](https://www.datawallet.com/crypto/october-10-crypto-crash-explained)
24. [Oct. 10 Crypto Flash Crash: Exchanges, Whales & Traders Who Lost the Most](https://www.ccn.com/education/crypto/oct-10-crypto-flash-crash-exchanges-whales-traders-who-lost/)
25. [Market Spotlight: Inside Crypto’s \$19 Billion Liquidation Event](https://www.coindesk.com/research/market-spotlight-the-19-billion-liquidation-that-shook-crypto)
26. [Billions in Crypto Liquidations: Inside October’s \$19B Crash](https://coinshares.com/us/insights/knowledge/billions-in-liquidations-what-happened/)
27. [\[2512.01112\] Autodeleveraging: Impossibilities and Optimization](https://arxiv.org/abs/2512.01112)
28. [(PDF) Autodeleveraging: Impossibilities and Optimization](https://www.researchgate.net/publication/398224690_Autodeleveraging_Impossibilities_and_Optimization)
29. [Tarun Chitra on X: "https://t.co/Dn9915MUK3" / X](https://x.com/tarunchitra/status/1998451653154906236)
30. [Autodeleveraging as Online Learning](https://arxiv.org/html/2602.15182)
31. [Risk-Based Auto-Deleveraging](https://arxiv.org/pdf/2603.15963)
32. [Where does the criticality live? Early-warning signals are event-heterogeneous across seven crypto-perpetual liquidation cascades · Pith](https://pith.science/paper/2607.27070)
33. [Where does the criticality live? Early-warning signals are event-heterogeneous across seven crypto-perpetual liquidation cascades](https://arxiv.org/pdf/2607.27070)
34. [DVOL - Deribit Implied Volatility Index - Deribit Insights](https://insights.deribit.com/exchange-updates/dvol-deribit-implied-volatility-index/)
35. [Implied Volatility vs Historical Volatility in Bitcoin](https://financefeeds.com/implied-volatility-vs-historical-volatility/)
36. [Risk Premia in the Bitcoin Market Caio Almeida\* Maria Grith† Ratmir Miftachov‡](https://arxiv.org/pdf/2410.15195)
37. [(PDF) Pricing Kernels and Risk Premia implied in Bitcoin Options](https://www.researchgate.net/publication/370461386_Pricing_Kernels_and_Risk_Premia_implied_in_Bitcoin_Options)
38. [The Bitcoin VIX and Its Variance Risk Premium](https://www.pm-research.com/content/iijaltinv/23/4/84)
39. [(PDF) Valuation and hedging of cryptocurrency inverse options](https://www.researchgate.net/publication/382233254_Valuation_and_hedging_of_cryptocurrency_inverse_options)
40. [Binance Funding Rate Explained: When It's Charged, How to Calculate It, Long or Short, Arbitrage (2026)](https://coinvado.com/en/posts/binance-futures-funding-rate-guide-2026/)
41. [Introduction to Binance Futures Funding Rates](https://www.binance.com/en/support/faq/introduction-to-binance-futures-funding-rates-360033525031)
42. [How Does Binance's Algorithm Update Cut Off the 'Fee Leverage' of Speculative Coins?](https://news.futunn.com/en/post/62346087/how-does-binance-s-algorithm-update-cut-off-the-fee)
43. [Important Updates on Funding Rates of USDⓈ-M Perpetual Contracts](https://www.binance.com/en/support/announcement/important-updates-on-funding-rates-of-usd%E2%93%A2-m-perpetual-contracts-98d6b24d3e5c4f84a8ed04087997d8d0)
44. [Introduction to Binance Futures Funding Rates](https://www.binance.info/en/support/faq/detail/360033525031)
45. [Binance updates funding rate and settlement frequency for USDT-based perpetual contracts.](https://www.panewslab.com/en/articles/13be25f4-ae90-4812-b940-840838c27305)
46. [Important Updates on Funding Rate Settlement Frequency of USDⓈ-M Perpetual Contracts (2026-01-02)](https://www.treeofalpha.com/preview_article?id=1767339193416)
47. [Funding - Hyperliquid Docs - GitBook](https://hyperliquid.gitbook.io/hyperliquid-docs/trading/funding)
48. [How Hyperliquid funding rates work](https://www.dwellir.com/guides/hyperliquid-funding-rates)
49. [Fundamentals of Perpetual Futures](https://arxiv.org/pdf/2212.06888)
50. [Binance USDS-M Futures](https://docs.tardis.dev/historical-data-details/binance-futures)
51. [Change Log](https://developers.binance.com/docs/derivatives/change-log)
52. [Deribit DVOL Futures A brief overview Deribit DVOL Futures, 2023](https://insights.deribit.com/downloads/DVOL-deck.pdf)
53. [Hyperliquid Insurance Fund & ADL Explained (vs Lighter, Aster)](https://cipher-intelligence.io/blog/hyperliquid-insurance-fund-explained/)
54. [Inside the \$19B Flash Crash - insights4vc](https://insights4vc.substack.com/p/inside-the-19b-flash-crash)
55. [(PDF) Anatomy of the Oct 10–11, 2025 Crypto Liquidation Cascade: Macroeconomic Triggers, Market Microstructure, and Systemic Risk Lessons](https://www.researchgate.net/publication/396645981_Anatomy_of_the_Oct_10-11_2025_Crypto_Liquidation_Cascade_Macroeconomic_Triggers_Market_Microstructure_and_Systemic_Risk_Lessons)
56. [Leverage & Liquidations: The \$31B Deleveraging](https://blog.amberdata.io/leverage-liquidations-the-31b-deleveraging)
57. [Urban Jermann - Papers](https://finance.wharton.upenn.edu/~jermann/research.html)
58. [Crypto Wash Trading](https://pubsonline.informs.org/doi/abs/10.1287/mnsc.2021.02709)
