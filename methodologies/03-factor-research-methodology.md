# 03-factor-research-methodology.md

As of October 22, 2026, the strongest replicated core of cryptocurrency factor research holds up: a market factor, a size effect, and short-horizon (1–4 week) momentum, all of which survive into post-2020 data. A network-adoption "value" proxy is promising but less replicated. Derivatives carry is a real premium that is shrinking, not a durable cross-sectional alpha. Treat every other candidate signal as a statistical anomaly until it passes point-in-time universe construction, multiple-testing deflation, spanning tests, and net-of-cost out-of-sample validation.

## TL;DR

- **Established:** market, size and momentum span the crypto cross-section (Liu, Tsyvinski & Wu, JF 2022). Size, two-week momentum and price-to-new-address value stay significant after 2020. Longer-horizon momentum, volatility, volume and beta sorts do not (Borri, Liu, Tsyvinski & Wu, ARFE 2026).
- **Fragile:**
  - Results swing with researcher design choices; across 20,736 designs, non-standard errors exceed standard errors (Fieberg et al. 2024).
  - Size and volume anomalies come from micro-caps. Large-cap momentum is costly and earns its alpha mostly on the short side (Fieberg, Liedtke & Zaremba 2024).
  - The BTC cash-and-carry Sharpe ratio was 6.45 over 2020–2025, fell to 4.06 from 2024 and turned negative in 2025 (Borri et al. 2026, Binance BTC perpetuals at 8-hour frequency, Aug 2020–May 2025).
- **Mandatory for agents:**
  - Use a survivorship-free, point-in-time universe with wash-trade-screened volume.
  - Apply HAC / dependence-robust inference, family-aware multiplicity control, and DSR/PBO as complementary diagnostics. The numerical promotion thresholds below are conservative policy choices, not universal statistical laws; report uncertainty and feasibility when a diagnostic is undefined.
  - Call nothing exploitable alpha until it survives market–size–momentum and latent-factor sensitivity analyses, realistic venue-specific costs, sealed out-of-sample testing, and paper monitoring.

```yaml
---
document_id: 03-factor-research-methodology
audience: ChatGPT quantitative research agents
research_cutoff: 2026-10-22
evidence_labels:
  "[E]": finding from a verified peer-reviewed paper or primary source
  "[W]": finding from a working paper/preprint (not peer-reviewed at cutoff)
  "[P]": procedure or default proposed by this document (not an empirical claim)
  "[U]": unverified or weakly sourced; re-check before use
---
```

## Key Findings

1. **Three different objects.**
   - A *risk premium* compensates for exposure to priced bad-state risk. Crypto market beta, and plausibly network-adoption value, are the main candidates.
   - An *anomaly* is unexplained average return. It may reflect risk, mispricing, data artefacts or mining.
   - *Alpha* is net-of-cost, capacity-feasible, out-of-sample excess return over the agent's benchmark.
   - Most published crypto "factors" are evidence of the second kind only.
2. **Horizons are compressed.** Crypto momentum lives at roughly 1–4 weeks. 12- and 24-week momentum sorts are insignificant in 2014–2025 [E]. Dobrynskaya (2023) finds momentum up to 2–4 weeks and reversal beyond about one month [E]. [arxiv](https://arxiv.org/pdf/2510.14435)
3. **Contradictions are mostly design.** Grobys & Sapkota (2019) find no momentum, using monthly data on 143 coins. [hse](https://conference.hse.ru/files/download_file_ex?hash=FAE0AB2DC7A67656E89A0B1CB27D8C7D&id=3B5EE9A5-0B18-458A-9458-B4ED0F6C6664) Shen, Urquhart & Wang (2020) use reversal as the third factor. [repec](https://ideas.repec.org/a/eee/finlet/v34y2020ics1544612319304519.html) Cong, Karolyi, Tang & Zhao find momentum only in the largest coins and reversal elsewhere. [finexpert](https://www.finexpert.info/newsletter/newsletter-april822) Horizon, size segment and weighting reconcile most of these results [E].
4. **Frictions and data quality are first-order.**
   - Across 29 exchanges, wash trading averaged 77.5% of total volume on unregulated venues, with a median of 79.1% (Cong, Li, Tang & Yang, Management Science 2023) [E].
   - Naive cross-exchange "arbitrage" across 510 BTC–fiat pairs on 165 exchanges in 49 currencies earns about 68.5% per week (Borri et al. 2026). Restricted to implementable pairs, that falls to about 3.8% per week [E].
5. **Decay is the base rate.**
   - Across 97 equity predictors, average monthly long-short returns fall from 0.58% in-sample to 0.402% out-of-sample (−26%) and 0.264% post-publication (−58%) (McLean & Pontiff 2016) [E].
   - Crypto anomaly returns occur mainly in bull markets and fade [E]. [repec](https://ideas.repec.org/a/eee/finana/v94y2024ics1057521924001509.html)
   - The BTC carry Sharpe ratio was 6.45 over 2020–2025, fell to 4.06 from 2024 and turned negative in 2025 (Borri et al. 2026) [E].
6. **Complexity must earn its place.** In crypto, the C-4 model plus three higher-order terms (adjusted R² ≈ 0.70) nearly matches a single nonlinear Kolmogorov–Arnold factor (≈ 0.72) [E/W]. [arxiv](https://arxiv.org/pdf/2510.14435) ML must beat a regularized linear baseline on identical purged folds, net of costs.

---

## 1. Scientific Foundations and Literature Review

### 1.1 Definitions

| Term | Definition | Notation |
|---|---|---|
| Characteristic | Point-in-time attribute of asset $i$ at $t$ | $c_{i,t}$ |
| Signal | Transformation hypothesized to forecast $r_{i,t+h}$ | $s_{i,t}=f(c_{i,t})$ |
| Traded factor | Return of a zero-cost portfolio built from a signal | $f_{k,t}$ |
| Exposure (beta) | Time-series sensitivity to a factor | $\beta_{i,k}$ |
| Risk premium | $\lambda_k=\mathbb{E}[f_{k,t}]$ (traded) or cross-sectional price of beta | $\lambda_k$ |
| Alpha | $r^e_{i,t}=\alpha_i+\sum_k\beta_{i,k}f_{k,t}+\varepsilon_{i,t}$ | $\alpha_i$ |
| Cross-sectional prediction | Ranks assets at $t$; target is relative return | IC, sorts, Fama–MacBeth |
| Time-series prediction | Forecasts one asset/market over time | predictive regression, TSMOM |

### 1.2 How crypto differs from equity factor research

1. **No accounting cash flows.** Value is proxied by price-to-new-addresses, network adoption, or protocol fees [E/W].
2. **Faster "metabolism."** Momentum turns into reversal after about one month [E]. [ssrn](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=3913263)
3. **Jumps are the rule.** Bitcoin shows significant jumps on about 28% of days, vs about 5.3% for Dow stocks (2015–2025) [E]. [arxiv](https://arxiv.org/pdf/2510.14435)
4. **Adoption fundamentals.** On-chain user adoption explains about 8% of return variation [E/W]. [arxiv](https://arxiv.org/pdf/2510.14435)
5. **Market structure.**
   - Trading is 24/7, fragmented across venues and quote currencies.
   - Perpetuals account for more than 98% of BTC futures volume in the Schmeling–Schrimpf–Todorov sample (as reported by Borri et al. 2026).
   - Law-of-one-price deviations persist across venues [E]. [arxiv](https://arxiv.org/pdf/2510.14435)
6. **Data integrity.** Wash trading, manipulation and 2013 Mt. Gox-era data issues [E]. [reading](https://centaur.reading.ac.uk/113166/1/Crypto%20Wash%20Trading_final.pdf)
7. **Regime change.** Correlation with global equities rose from 1% before 2020 to 39% after [E]. [arxiv](https://arxiv.org/pdf/2510.14435)
8. **Universe churn.** The CoinGecko sample has 18,622 active and 29,230 inactive coins [E]. [arxiv](https://arxiv.org/pdf/2510.14435)

### 1.3 Crypto asset-pricing literature

| Study | Venue | Key finding | Label |
|---|---|---|---|
| Liu & Tsyvinski, "Risks and Returns of Cryptocurrency" | RFS 34(6), 2021 | Returns are driven by crypto-specific (network) factors, with strong time-series momentum. Attention proxies forecast returns. [oup](https://academic.oup.com/rfs/article-abstract/34/6/2689/5912024) WP version: a one-SD rise in "Bitcoin" Google searches predicts +2.3% two-week-ahead returns. [nber](https://www.nber.org/system/files/working_papers/w24877/w24877.pdf) | [E]; WP magnitudes [W] |
| Liu, Tsyvinski & Wu, "Common Risk Factors in Cryptocurrency" | JF 77(2), 1133–1177, 2022 | Market, size and momentum (C-3) span the cross-section. 10 significant characteristic strategies are explained by C-3. [yale](https://economics.yale.edu/research/common-risk-factors-cryptocurrency) | [E] |
| Borri, Liu, Tsyvinski & Wu, "Coming of Age" | ARFE 18, 2026; arXiv 2510.14435 | Sample: CoinGecko, Dec 31 2013–Sep 6 2025. Starting from 18,622 active and 29,230 inactive coins, filters leave 16,468 unique coins and about 9.5 million records. CSIZE, 2-week CMOM and CVALUE are significant both full-sample and post-2020. C-4 adjusted R² is 0.473, vs 0.046 for C-1. | [E] |
| Cong, Karolyi, Tang & Zhao, "Value Premium, Network Adoption…" | SSRN 3985631 | Momentum in the largest coins, reversal elsewhere. Value and adoption premia. C-5 model; token-category segmentation. [finexpert](https://www.finexpert.info/newsletter/newsletter-april822) | [W] |
| Bianchi & Babiak, "A Factor Model for Cryptocurrency Returns" | CERGE-EI WP 710 | 3-factor IPCA reaches total R² of 17.2%, vs 9.6% for a static 6-factor model. [cerge-ei](https://www.cerge-ei.cz/pdf/wp/Wp710.pdf) | [W] |
| Shen, Urquhart & Wang | FRL 34, 2020 | Market + size + reversal beats crypto-CAPM (more than 1,700 coins). [repec](https://ideas.repec.org/a/eee/finlet/v34y2020ics1544612319304519.html) | [E] |
| Dobrynskaya, "Cryptocurrency Momentum and Reversal" | JAI 26(1), 2023 | Momentum at 2–4 weeks, reversal beyond 1 month, driven by losers. [pm-research](https://www.pm-research.com/content/iijpracapp/early/2023/07/28/pa2023jaipa073) | [E] |
| Grobys & Sapkota, "Cryptocurrencies and momentum" | Econ. Letters 180, 2019 | No significant momentum (monthly). [sciencedirect](https://www.sciencedirect.com/science/article/pii/S0165176519301077) | [E] |
| Borri, "Conditional tail-risk in cryptocurrency markets" | JEF 50, 2019 | High CoVaR exposure within crypto; none to US equities or gold. [semanticscholar](https://www.semanticscholar.org/paper/Conditional-Tail-Risk-in-Cryptocurrency-Markets-Borri/a93a2dadfe7a04212ec141a18208e4fb9144106b) | [E] |
| Fieberg, Günther, Poddig & Zaremba | IRFA 92, 2024 | Non-standard errors exceed standard errors. [repec](https://ideas.repec.org/a/eee/finana/v92y2024ics1057521924000383.html) Size and momentum are the most robust. [arxiv](https://arxiv.org/pdf/2510.14435) | [E] |
| Fieberg, Liedtke & Zaremba | IRFA 94, 2024 | Size and volume anomalies are micro-cap effects. Momentum is costly and short-driven. [uni-bremen](https://media.suub.uni-bremen.de/handle/elib/8606) Returns concentrate in bull markets and fade. [repec](https://ideas.repec.org/a/eee/finana/v94y2024ics1057521924001509.html) | [E] |
| Fieberg, Liedtke, Poddig, Walker & Zaremba | JFQA 60, 2025 | Trend factor in the crypto cross-section. [ssrn](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=4601972) | [E] |
| Schwenkler & Zheng | JCF 93, 2025 | News-co-mentioned peers move opposite to shocks, then reverse over weeks. | [E] |
| Schmeling, Schrimpf & Todorov, "Crypto Carry" | Mgmt Sci 2026; BIS WP 1087 | BIS WP 1087: carry averages above 10% annually and "can become very large (up to 60% p.a.)". The Management Science version says "sometimes exceeding 40% per annum." High carry predicts crashes. | [E] |
| He, Manela, Ross & von Wachter, "Fundamentals of Perpetual Futures" | arXiv 2212.06888 | Mean absolute perp deviations of 52–90% p.a., declining by about 22 pp per year. [arxiv](https://arxiv.org/html/2212.06888v7) | [W] |
| Cong, Li, Tang & Yang, "Crypto Wash Trading" | Mgmt Sci 69(11), 2023 | Wash trading averages 77.5% of total volume on unregulated exchanges (median 79.1%), across 29 exchanges. | [E] |
| Cong, He & Tang, "The Tokenomics of Staking" | NBER WP 33640 | Staking ratio predicts returns; staking-carry Sharpe of 1.60. [nber](https://www.nber.org/system/files/working_papers/w33640/w33640.pdf) | [W] |

### 1.4 Factor zoo, replication, overfitting

| Study | Venue | Lesson for crypto agents |
|---|---|---|
| Harvey, Liu & Zhu | RFS 29(1), 2016 | New factors need t > 3.0. "Most claimed research findings… are likely false." [researchgate](https://www.researchgate.net/publication/333799453_Shrinking_the_Cross-Section) | [oup](https://academic.oup.com/rfs/article/29/1/5/1843824)
| Hou, Xue & Zhang, "Replicating Anomalies" | RFS 33(5), 2020 | With microcaps mitigated, 65% of 452 anomalies fail at \|t\| ≥ 1.96 and 82% fail at 2.78. | [researchgate](https://www.researchgate.net/publication/345507035_Replicating_Anomalies)
| Jensen, Kelly & Pedersen | JF 78(5), 2023 | Bayesian replication rate of 82.4%; factors cluster into 13 themes; evidence spans 93 countries. | [aqr](https://www.aqr.com/Insights/Research/Working-Paper/Is-There-a-Replication-Crisis-in-Finance) [wiley](https://onlinelibrary.wiley.com/doi/pdfdirect/10.1111/jofi.13249)
| McLean & Pontiff | JF 71(1), 2016 | Across 97 predictors, average monthly returns are 0.58% in-sample, 0.402% out-of-sample (−26%) and 0.264% post-publication (−58%). |
| Kozak, Nagel & Santosh | JFE 135(2), 2020 | Sparse-characteristic SDFs are inadequate; shrink low-variance PCs instead. [ssrn](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2945663) |
| Gu, Kelly & Xiu | RFS 33(5), 2020 | Trees and neural nets win through interactions; shallow nets beat deep ones. [ssrn](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=3159577) [researchgate](https://www.researchgate.net/publication/345352337_Empirical_Asset_Pricing_via_Machine_Learning) |
| Bailey & López de Prado | JPM 40(5), 2014 | Deflated Sharpe Ratio. | [ssrn](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2460551)
| Bailey, Borwein, López de Prado & Zhu | J. Comp. Finance 20(4), 2017 | PBO estimated via CSCV. | [ssrn](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2326253) [arxiv](https://arxiv.org/pdf/2605.04004)
| Novy-Marx & Velikov | RFS 29(1), 2016 | Strategies with under 50% monthly turnover mostly survive costs; buy/hold spreads are the best mitigation. | [ssrn](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2535173) [nber](https://www.nber.org/papers/w20721)

The disagreement between Hou–Xue–Zhang and Jensen–Kelly–Pedersen shows that replication rates depend on weighting, microcap treatment and priors. [Substack](https://systematicallybiased.substack.com/p/pockets-of-replicability-post5) Crypto has micro-cap-dominated coin counts and large non-standard errors, so a conservative, HXZ-style protocol is the default [P].

---

## 2. Formal Factor Taxonomy

Evidence tiers:
- **T1:** replicated in peer-reviewed crypto work, including post-2020 data.
- **T2:** some evidence, but limited or contradictory.
- **T3:** theory plus time-series or industry evidence only.
- **T4:** hypothesis.

| # | Family | Mechanism | Prior class | Tier | Caveats |
|---|---|---|---|---|---|
| F1 | Market | Aggregate crypto risk | Risk premium | T1 | Equity-correlation regime shift |
| F2 | Size | Illiquidity/attention | Risk + friction | T1 gross / T2 net | Micro-cap driven; post-2020 t = −1.69 |
| F3 | Momentum (1–4 wk) | Under-reaction; retail extrapolation | Anomaly | T1 (large caps) | Null at monthly horizon; short-leg/cost heavy |
| F4 | Reversal (1 wk / >1 mo) | Liquidity provision; overreaction | Anomaly / liquidity | T2 | Confined to small, illiquid coins [W] |
| F5 | Value / network adoption | Price vs network fundamentals | Candidate premium | T2 | Address gaming; limited chain coverage |
| F6 | Liquidity | Illiquidity premium | Risk / friction | T2 | Volume sorts insignificant; wash trading |
| F7 | Volatility / downside / tail | Lottery vs crash compensation | Ambiguous | T2/T3 | 24-wk vol sort insignificant |
| F8 | Market beta | CAPM / BAB | Risk (theory) | T3 | Beta sorts insignificant |
| F9 | Funding carry / basis | Convenience yield; scarce arbitrage capital | Crash-risk premium + limits to arbitrage | T2 (TS) / T3 (XS) | Sharpe compressing; predicts crashes |
| F10 | Open interest / positioning | Crowded leverage → liquidations | Anomaly / risk | T3 | No verified cross-sectional study |
| F11 | On-chain activity | Usage demand | Fundamental | T2 | Bots/spam; chain-specific definitions |
| F12 | Tokenomics / dilution / unlocks / staking | Supply shocks; issuance analog | Anomaly | T3 (unlocks), T2 (staking) | Unlock evidence preliminary [U] |
| F13 | Attention / sentiment | Limited attention; retail flow | Behavioral | T2 (TS) / T3 (XS) | Google Trends rescaling look-ahead |
| F14 | Quality / protocol fees / TVL | Cash-flow analog | Candidate premium | T3/T4 | Incentive-inflated fees; TVL double-counting |
| F15 | Macro / cross-asset betas | Financialization; monetary policy | Systematic exposure | T2 (TS) | Regime-dependent; pre-2018 null |
| F16 | Higher moments / nonlinear terms | Jump risk, skewness | Risk (theory) | T2 | In-sample selection |

---

## 3. Point-in-Time Universe Rules [P unless noted]

**Principle:** at every rebalance $t$, both the universe and every input must be reconstructible from data with `available_ts` < $t$.

| Rule | Specification |
|---|---|
| U1 Identity | Permanent `asset_id` for the economic asset. `contract_id` = (chain, address, decimals). Ticker history carries validity intervals. Never join on ticker alone. |
| U2 Wrapped/bridged | Map to the underlying asset as a representation and exclude from the cross-section (Borri et al. 2026 practice [E]). |
| U3 Migrations/redenominations/rebrands/forks | Keep a `corporate_actions` table with ratios; adjust prices and supply for continuity. Treat fork coins as distributions. |
| U4 Stablecoins | Exclude from factor cross-sections [E practice]. Keep them as quote/funding inputs and as depeg state variables. Classify point-in-time from launch. |
| U5 Other exclusions | Exchange, LP, rebasing and leveraged tokens and RWAs, except in a pre-registered robustness universe. |
| U6 Listing date | At least 30 daily observations before $t$ [E: Borri et al. 2026], and at least the signal's lookback. |
| U7 Size floor | Replication: MCAP ≥ US$1M [E]. Production: top-N (100/200) by trailing 30-day median MCAP. |
| U8 Liquidity | Trailing 30-day median clean volume of at least US$1M/day, or at least k× position size. |
| U9 Supply | Circulating supply as snapshotted at $t$ (vintage-stamped); compute FDV separately. |
| U10 Venue | Tradable at $t$ on an approved venue; record a `shortable` flag (spot borrow or perp). |
| U11 Delistings | Keep dead coins. Delisting return runs to realizable recovery value, or −100% if none. Never drop coins ex post. |
| U12 Volume cleaning | Approved-venue volume only. Flag Benford and trade-size-rounding violations (Cong et al. 2023 method [E]). | [nber](https://www.nber.org/system/files/working_papers/w30783/w30783.pdf)
| U13 Prices | VWAP across approved venues with outlier filters at a fixed UTC close; store the venue list per $t$. |
| U14 Winsorization | Winsorize estimation returns at extreme tails (Borri et al. use 0.0025% [E]). Never winsorize evaluation P&L. |

**Leakage controls.**
- **L1 Timestamps.** Every field carries `event_ts`, `observed_ts`, `ingested_ts` and an independently justified `available_ts`; missing historical first-availability evidence is never retrospectively inferred from a present-day download.
  - On-chain data: confirmation plus vendor lag.
  - Google Trends: the vintage as downloaded.
  - Unlock schedules: as published before $t$.
- **L2 Vintages.** Immutable vintages; no overwriting.
- **L3 Execution.** Signal observed at $t$ may first be acted upon at the next feasible venue timestamp after data availability and computation latency. Next-hour TWAP is a benchmark scenario, not a guaranteed fill; execution prices must reflect contemporaneous executable depth or a conservative bounded model.
- **L4 Universe snapshots.** Persisted `universe_t`; the backtester reads only from these.

---

## 4. Factor Formulas and Data Schemas

**Conventions [P].**
- Rank normalization: $z_{i,t}=\Phi^{-1}((\text{rank}(s_{i,t})-0.5)/N_t)$.
- Robust alternative: $(s-\text{med})/(1.4826\,\text{MAD})$, clipped at ±3.
- Characteristic winsorization: 1st/99th percentile.
- Missing data: excluded from single-factor sorts; set to zero after normalization in composites, with coverage logged; no forward-fill beyond staleness limits.
- Portfolios: quintiles, value-weighted with a 10% cap as the primary specification. Equal-weighted is diagnostic only, because EW overweights micro-caps [E]. [Substack](https://systematicallybiased.substack.com/p/pockets-of-replicability-post5)

| ID | Formula | Data / freq. | Lookback / lag | Hold | Rationale | Support | Contradict |
|---|---|---|---|---|---|---|---|
| CMKT | $\sum_i w_{i,t-1}r_{i,t}-r^f_t$, $w\propto$ MCAP | Prices, supply, T-bill / wk | — / 0 | — | Aggregate risk | LTW 2022 | — |
| CSIZE | $\ln\text{MCAP}_{i,t}$; Q1 − Q5 | Price × circ. supply / wk | point / 0 | 1 wk | Illiquidity | LTW 2022; Shen 2020 | Micro-cap driven |
| CMOM | $\prod_{k=0}^{1}(1+r^w_{i,t-k})-1$ (variants 1–4 wk) | Returns / wk | 2 wk / 0 | 1 wk | Under-reaction | LTW 2022; Dobrynskaya 2023 | Grobys & Sapkota 2019 |
| STREV | $-r_{i,t}$ (1 d–1 wk), ranked within size bucket | Returns / d–wk | 1 d–1 wk / 0 | 1 d–1 wk | Liquidity provision | Shen 2020 | Large-cap momentum |
| LTREV | $-(\prod_{k=5}^{K}(1+r^w_{i,t-k})-1)$, $K\in\{12,24,52\}$ | Returns / wk | 1–12 mo / 0 | 4–12 wk | Overreaction | Dobrynskaya 2023 | MOM12/24 insignificant |
| TREND | FM-weighted combination of $P/\text{MA}(L)$, $L\in\{5,…,200\}$ d | Prices / d | ≤200 d / 0 | 1 wk | Trend | Fieberg et al. 2025 | — |
| CVALUE | $\ln(\text{MCAP}/\text{NewAddr})$; Q1 − Q5 | MCAP, new addresses / wk | 1–4 wk / ≥1 d | 1 wk | Network value | LTW; Borri 2026 | Address gaming |
| ADOPT | $\Delta\ln\text{ActiveAddr}$ (4 wk vs prior 4 wk) | On-chain / wk | 8 wk / ≥1 d | 1–4 wk | Network effects | Cong et al.; L&T 2021 | Bots |
| ILLIQ | $\frac1D\sum_d \lvert r_{i,d}\rvert/\text{DVol}^{clean}_{i,d}$ | Returns, clean volume / d | 30 d / 0 | 1–4 wk | Illiquidity | Bianchi, Babiak & Dickerson 2022 | Volume sorts insignificant |
| VOL | $\text{sd}(r_{i,d})$ | Returns / d | 30 d–24 wk / 0 | 1–4 wk | Lottery vs risk | — | Insignificant (Borri 2026) |
| DOWNBETA | $\text{cov}(r_i,r_m\mid r_m<\mu_m)/\text{var}(r_m\mid r_m<\mu_m)$ | Returns / d | 180 d / 0 | 4 wk | Downside risk | Dobrynskaya [U] | — |
| TAIL | $\Delta$CoVaR at $q=0.05$ | Returns / d | 1 yr / 0 | 4 wk | Tail premium | Borri 2019 | — |
| BETA | Dimson beta (1 lag) on CMKT | Returns / d | 24 wk / 0 | 4 wk | CAPM/BAB | — | Insignificant (Borri 2026) |
| FUND | $\sum_{7d}\text{fr}_{i,k}$, OI-weighted across venues, annualized; low − high | Perp funding / 8 h | 7 d / 0 | 1 d–1 wk | Crowded leverage | Schmeling et al. (TS) | No XS peer-review [T3] |
| BASIS | $\frac{F-S}{S}\cdot\frac{365}{T-t}$ or perp premium | Futures, index / d | point–5 d / 0 | 1 d–1 wk | Convenience yield | Schmeling et al.; Chi et al. 2023 [U] | Crash predictability |
| OICHG | $\Delta\ln\text{OI}^{USD}_{7d}-\beta\,\Delta\ln\text{MCAP}$ | OI / d | 7 d / 0 | 1 d–1 wk | Leverage build-up | [U] | — |
| INFL | $\ln(\text{Supply}_t/\text{Supply}_{t-52w})$; low − high | Supply vintages / wk | 52 wk / snapshot | 4–12 wk | Dilution | [T3] | — |
| UNLOCK | $\sum_{(t,t+30d]}\text{Unlock}/\text{CircSupply}_t$ from schedules published before $t$ | Vesting vintages / d | fwd 30 d / pub. date | Event | Supply overhang | Preliminary [U] | — |
| STAKE | Staking ratio or $y^{stake}-\text{INFL}$ | Staking / wk | point / ≥1 d | 1 wk | Staking carry | Cong, He & Tang [W] | — |
| ATTN | $\ln\text{SVI}_t-\text{med}(\ln\text{SVI}_{t-8w:t-1})$ | Trends vintages / wk | 8 wk / vintage | 1–2 wk | Limited attention | Liu & Tsyvinski 2021 (TS) | XS thin |
| NEWSPEER | $-\text{sign}(\epsilon_{j,t})$ after peer shock >2σ | News co-mentions / d | event / news ts | Weeks | Overreaction | Schwenkler & Zheng 2025 | — | [berkeley](https://cdar.berkeley.edu/sem217-gustavo-schwenkler-santa-clara-university-news-driven-peer-co-movement-crypto-markets)
| FEES | $\ln(\text{MCAP}/\text{Fees}^{ann})$ | Protocol fees / wk | 30–90 d / vendor | 4–12 wk | Cash-flow value | [T4] | Incentive fees |
| MACROβ | $\beta^X$ from $r_i=a+\beta^M r_m+\beta^X\Delta X+e$, $X\in${equity, DXY, real yield, breakevens} | Weekly | 52–104 wk / release lag | 4 wk | Macro exposure | Borri 2026 correlations | Pre-2018 null |

**Schemas [P]** (all tables carry `vintage_id` and `available_ts`):
- `asset_master(asset_id, asset_class, class_valid_from/to)`
- `contract_map(asset_id, chain, address, decimals, valid_from/to)`
- `ticker_history(asset_id, venue, ticker, valid_from/to)`
- `corporate_actions(asset_id, event_type, effective_ts, ratio, successor_id)`
- `market_bar(asset_id, venue, quote_ccy, bar_ts, OHLC, volume_usd, n_trades, venue_integrity_flag)`
- `supply_snapshot(asset_id, snapshot_ts, circulating, total, max)`
- `derivatives_bar(asset_id, venue, type, expiry, bar_ts, mark, index, funding_rate, funding_interval_h, oi_usd)`
- `onchain_metric(asset_id, chain, metric, ts, value, methodology_version)`
- `unlock_schedule(asset_id, unlock_ts, amount, published_ts)`
- `attention(asset_id, source, period_ts, value, download_ts)`
- `universe_snapshot(rebalance_ts, asset_id, eligible, exclusion_reason, mcap, clean_adv, shortable)`
- `signal_value(signal_id, version, asset_id, formation_ts, raw, normalized, coverage_flag)`

---

## 5. Statistical Evaluation Procedures

| Test | Procedure | Assumptions | Crypto limitations |
|---|---|---|---|
| Portfolio sorts | Quintiles at $t$, hold $h$; report means, t-stats, monotonicity | Enough names per bucket | Thin early cross-sections; EW micro-cap bias; breakpoint sensitivity |
| Long-short | $f_t=r_{Q5}-r_{Q1}$, gross and net | Short leg implementable | Borrow/perp availability; short-leg alpha |
| IC / rank IC | $\text{IC}_t=\rho_S(s_{i,t},r_{i,t+h})$; mean, ICIR, HAC t | Stationary IC | EW across coins; add a cap-weighted IC |
| Fama–MacBeth | Per-$t$ cross-sectional regression; $\bar\gamma$ with Newey–West SE | Weakly dependent $\gamma_t$ | Errors-in-variables with estimated betas (Shanken); outliers → WLS/ranks |
| Factor-mimicking portfolios | Cross-sectional WLS coefficients as portfolios | Linear mapping | High turnover |
| Time-series regressions | $f^{new}_t=\alpha+\beta'F_t+e_t$ vs C-1/C-3/C-4 | Same construction across benchmarks | Benchmark choices change α |
| GRS | Joint α = 0, $F_{N,T-N-K}$ | Normal i.i.d. errors | Jumps → use bootstrap GRS |
| HAC / Newey–West | Bartlett kernel; $L=\lceil4(T/100)^{2/9}\rceil$ or $h-1$ for overlapping returns | Finite 4th moments | Heavy tails → pair with bootstrap |
| Bootstrap CIs | Stationary/block bootstrap, block length ≈ $T^{1/3}$; percentile-t | Stationarity within blocks | Regime shifts → by-regime bootstrap |
| Reality check / SPA | White (2000), Hansen (2005) over all logged specifications | Complete trial log | Invalid if trials are missing |
| DSR, PBO | §6 | §6 | Effective trial count; non-exchangeable regimes |

**Mandatory report [P]** (gross and net; full, pre-2020 and post-2020 samples):
- mean, HAC t, bootstrap CI;
- Sharpe, skewness, kurtosis, maximum drawdown;
- quintile means; IC and ICIR (EW and cap-weighted);
- alphas vs C-1, C-3 and C-4;
- turnover; names per leg; short-leg share of returns;
- breakeven cost $c^*=\bar r^{gross}_{LS}/(2\,\overline{\text{TO}})$.

**Economic significance [P]:** all of the following must hold.
- Net mean > 0 with uncertainty bounds reported; a HAC t ≥ 2.0 is a proposed screening threshold, not evidence of confirmed investment performance.
- Net Sharpe ≥ 0.5 standalone, or incremental Sharpe ≥ 0.2.
- Capacity ≥ the intended allocation.
- Returns not concentrated in fewer than 5 assets or fewer than 10% of periods.

---

## 6. Multiple-Testing Safeguards

**Trial log [P]**
- Log every specification, including failures, before viewing results: `trial_id, hypothesis_id, spec_hash, data_vintage, metrics`.
- Without a log, no factor can be promoted.

| Control | Rule | Source |
|---|---|---|
| Single-test hurdle | HAC \|t\| ≥ 3.0 for new factors | Harvey, Liu & Zhu 2016 [E] | [repec](https://ideas.repec.org/a/oup/rfinst/v29y2016i1p5-68..html)
| FWER | Holm when any false positive is costly | [P] |
| FDR | BH or BY at q = 0.05 per research batch; BHY-implied cutoff ≈ 2.78 | HLZ 2016; HXZ 2020 [E] | [duke](https://people.duke.edu/~charvey/Research/Published_Papers/P118_and_the_cross.PDF) [ssrn](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=3275496)
| Bayesian shrinkage | Shrink alphas toward theme means before ranking | JKP 2023 [E] | [wiley](https://onlinelibrary.wiley.com/doi/full/10.1111/jofi.13249)
| Non-standard error | Design multiverse: ≥3 weightings × ≥3 universes × ≥2 breakpoints × ≥2 rebalance frequencies. Promote only if >80% keep the sign and >50% are significant. | Fieberg et al. 2024 [E]; thresholds [P] | [sciencedirect](https://www.sciencedirect.com/science/article/pii/S1057521922003696)

**Deflated Sharpe Ratio** (Bailey & López de Prado 2014):
$$\text{PSR}(SR^*)=\Phi\!\left(\frac{(\widehat{SR}-SR^*)\sqrt{T-1}}{\sqrt{1-\hat\gamma_3\widehat{SR}+\frac{\hat\gamma_4-1}{4}\widehat{SR}^2}}\right),\quad SR^*_0=\sqrt{\mathbb{V}[\widehat{SR}_n]}\Big((1-\gamma)\Phi^{-1}(1-\tfrac1N)+\gamma\Phi^{-1}(1-\tfrac{1}{Ne})\Big)$$
- DSR = PSR($SR^*_0$), with $\gamma\approx0.5772$.
- Rule [P]: net DSR ≥ 0.95.
- $N$ is the effective number of independent trials, estimated by clustering trial-return correlations. It is never 1.

**PBO via CSCV** (Bailey, Borwein, López de Prado & Zhu 2017):
- Split the $T\times N$ trial matrix into $S$ (e.g., 16) blocks.
- For each of the $\binom{S}{S/2}$ train/test splits, take the in-sample winner's out-of-sample relative rank $\bar\omega$.
- Compute $\lambda=\ln(\bar\omega/(1-\bar\omega))$; PBO = Pr(λ ≤ 0).
- Rule [P]: PBO ≤ 0.20 → promote; 0.20–0.50 → quarantine; > 0.50 → reject the specification family.

**Holdout discipline [P]**
- Reserve the most recent 12 months when history is sufficient, otherwise pre-register a shorter chronological holdout and downgrade evidence; never claim an independent test if the holdout has already influenced specifications.
- Report pre-2020 and post-2020 results separately.
- For published factors, use McLean–Pontiff decay as an equity-derived prior, not a crypto estimate.

---

## 7. Factor Independence and Robustness Tests

**Independence [P]**
1. **Correlation.** Factor-return correlations (full sample, rolling 52-week, down-markets) and average rank correlations; flag \|ρ\| > 0.7.
2. **Multicollinearity.** Median per-date VIF; if > 5, orthogonalize or drop.
3. **Residualization.** $s_{i,t}=a_t+b_t^\top[\ln\text{MCAP},\text{CMOM},\text{ILLIQ},\hat\beta]_{i,t}+\eta_{i,t}$; sort on $\eta$. A signal that works only in raw form is a repackaged known factor.
4. **Double sorts.** Size first, then the candidate; report the spread within each size tercile.
5. **Spanning.** $f^{new}_t=\alpha+\beta_M\text{CMKT}+\beta_S\text{CSIZE}+\beta_{Mo}\text{CMOM}+\beta_L\text{CLIQ}+e_t$; require α HAC t ≥ 3.0. Use GRS for several new factors jointly.
6. **Incremental power.** Change in Fama–MacBeth adjusted R² on 25 or more test portfolios (benchmarks: C-1 = 0.046, C-4 = 0.473 [E]), plus the change in maximum Sharpe of the tangency portfolio.
7. **Conditional exposures.** Characteristic-instrumented loadings (IPCA-style [W]); the candidate's alpha must survive.

| Stability test [P] | Procedure | Fail condition |
|---|---|---|
| Rolling performance | 52-wk mean, Sharpe, IC with HAC bands | Sharpe < 0 in > 40% of windows |
| Regimes | BTC 200-day trend; volatility median split; funding regime; equity-correlation regime; stablecoin growth | Significant in one regime only, with no ex-ante rationale |
| Market cycles | Halving cycles; Mar 2020, May 2021, Terra-Luna (May 2022), FTX (Nov 2022) | Sign flip across cycles |
| Size segments | Top 20 / 21–100 / 101–500 | Works only in 101–500 |
| Exchange dependence | Regulated-only vs largest venue vs aggregator | Lost on regulated-only data |
| Sessions | Asia / Europe / Americas UTC blocks; weekends | Driven by one illiquid session |
| Structural breaks | Bai–Perron / sup-Wald; CUSUM on IC | Post-break mean ≈ 0 |
| Crowding | Correlation with published factors; valuation spread; OI and funding concentration in legs | Rising comovement with a compressing spread |
| Capacity | AUM ladder $1M–$500M; impact = spread/2 + $k\sigma\sqrt{q/\text{ADV}}$ | Net Sharpe < 0.5 at target AUM |
| Cost sensitivity | 1×, 2×, 3× costs; $c^*$; with/without buy-hold buffer | Fails at 2× |
| OOS decay | In-sample vs expanding-window vs holdout | Holdout < 50% of in-sample, or holdout t < 1.0 |
| Short-leg dependence | Long-only alpha vs CMKT | All alpha from an unimplementable short leg |

**Cost model [P]**
- Spot: fee + half-spread + impact.
- Perps: actual funding at each venue's interval.
- Shorts: borrow cost or funding.
- Untradable assets are skipped, not filled.
- Fee levels are calibration placeholders [U] until fitted to actual fills.

---

## 8. Predictive Modeling

**Model ladder [P].** Each rung must beat the previous one on identical purged out-of-sample folds, net of costs.

| Rung | Model |
|---|---|
| 0 | Zero/mean forecast; equal-weight C-3 composite |
| 1 | OLS / Fama–MacBeth on ranks |
| 2 | Ridge, LASSO, elastic net; KNS-style PC shrinkage [E] |
| 3 | Higher-order terms with forward selection (FS-FMB [E/W]); GAMs |
| 4 | Random forest or gradient-boosted trees (depth ≤ 4) |
| 5 | Shallow neural nets (1–3 layers); shallow beat deep in Gu–Kelly–Xiu [E] |
| 6 | IPCA / latent factors [W] |

**Evidence.**
- In equities, Gu–Kelly–Xiu find ML "in some cases" doubles regression-based strategies [E]. [oup](https://academic.oup.com/rfs/article-pdf/33/5/2223/33209812/hhaa009.pdf)
- In crypto, transparent higher-order terms capture most of the nonlinear factor's fit (0.70 vs 0.72) [E/W]. [arxiv](https://arxiv.org/pdf/2510.14435)
- An IRFA (2024) ML crypto study exists, but its authors and results were not verified [U].

**Validation [P]**
- **Nested walk-forward.** Outer loop: e.g., 3-year train / 6-month test. Hyperparameters are tuned only inside the outer training window.
- **Purging.** Drop training labels whose $[t,t+h]$ window overlaps test labels (López de Prado 2018).
- **Embargo.** $e=\max(h,1\,\text{wk})$ after each test fold.
- **CPCV.** Provides dependence-aware sensitivity paths only when its block structure respects chronological availability; it does not replace a genuinely forward chronological holdout, and is not identical to CSCV-based PBO.
- **Targets.** Cross-sectionally ranked returns, or time-series excess returns; never mixed.
- **Metrics.** OOS $R^2$ against a zero forecast, rank IC, net long-short Sharpe, and a Diebold–Mariano test vs baseline.
- **Interpretability.** OOS permutation importance and SHAP, partial dependence for the top 5 features, and feature-rank stability (Kendall τ ≥ 0.5 across folds). Unstable or uninterpretable models are quarantined.

---

## 9. Composite Signals

| Method | Weights | Strength | Risk |
|---|---|---|---|
| Equal weight | $1/K$ on ranks | No estimation error | Ignores quality and correlation |
| Inverse-volatility | $\propto1/\sigma(f_k)$ | Balanced risk | Ignores expected return |
| IC-weighted | $\propto\widetilde{\text{IC}}_k$ (shrunk) | Uses predictive evidence | Noisy; weights chase recent IC |
| IC-covariance | $\propto(\Sigma^{shr}_{IC})^{-1}\overline{\text{IC}}$ | Handles correlated signals | Inversion amplifies error |
| Mean–variance on factors | $\propto\hat\Sigma_f^{-1}\hat\mu_f$, $w\ge0$, $w_k\le0.4$ | In-sample max Sharpe | Overfits without shrinkage (KNS) |
| Constrained portfolio optimization | $\max\ \alpha'x-\frac\lambda2x'\Sigma x-\text{TC}(\Delta x)$ with neutrality and liquidity caps | Integrates costs | Depends on the cost model |

**Rules [P]**
1. Only VALIDATED signals may enter a composite.
2. Equal weight is the default. Estimated weights must beat it out-of-sample after DSR, and every weighting scheme tried counts as a trial.
3. Shrink ICs: $\widetilde{\text{IC}}_k=\kappa\overline{\text{IC}}_k+(1-\kappa)\overline{\text{IC}}_{all}$, with $\kappa=T_k/(T_k+104)$.
4. Merge signals with \|ρ\| > 0.7 into a theme first (JKP-style).
5. Control turnover with separate rebalance clocks for fast and slow signals, signal smoothing ($\tilde s_t=\phi\tilde s_{t-1}+(1-\phi)s_t$), and buy/hold buffers (enter in the top 20%, exit below the top 40%; Novy-Marx & Velikov [E]). [alphaarchitect](https://alphaarchitect.com/wp-content/uploads/2021/08/Factor_Investing_and_Trading_Costs.pdf)
6. No universal weights are given. Weights are specific to universe, horizon, cost model and vintage.

---

## 10. Factor Lifecycle and Acceptance/Rejection Decision Protocol

HYPOTHESIS → SPECIFICATION → DATA AUDIT → REPLICATION → VALIDATION → OUT-OF-SAMPLE TEST → PAPER MONITORING → RETIREMENT. QUARANTINE and REJECTED are reachable from any stage.

| Stage | Promote if [P] | Quarantine if | Reject if |
|---|---|---|---|
| HYPOTHESIS | Mechanism, sign, horizon and risk-vs-mispricing stated; literature checked | — | No mechanism |
| SPECIFICATION | Formula, lag, universe and hold frozen and hashed; trial log opened | — | Spec changed after viewing results without logging |
| DATA AUDIT | U1–U14 and L1–L4 pass; coverage ≥ 70%; vintages reproducible; wash screen applied | Coverage 50–70% | Look-ahead found; coverage < 50% |
| REPLICATION | Published factor: same sign and within ±50% of the original mean. New factor: a second agent matches signals to 1e-6. | Sign right, magnitude < 50% | Sign mismatch |
| VALIDATION | Gross t ≥ 3.0; FDR q ≤ 0.05; C-3 alpha t ≥ 2.5; gross DSR ≥ 0.95; works in ≥ 2 of 3 non-micro size segments; ≥ 80% multiverse sign stability | t in [2, 3), or one regime with ex-ante rationale | t < 2; spanned (alpha t < 1); micro-cap only |
| OUT-OF-SAMPLE TEST | ≥ 12-month sealed holdout: net mean > 0, t ≥ 1.5, ≥ 50% of in-sample; PBO ≤ 0.20; net DSR ≥ 0.95; survives 2× costs | Holdout at 25–50% of in-sample, or PBO 0.2–0.5 | Holdout ≤ 0, or PBO > 0.5 |
| PAPER MONITORING | ≥ 26 weekly rebalances; tracking within 2σ; realized costs ≤ 1.5× model | 26-week net Sharpe < 0; cost overrun | Drawdown > 2× backtest max DD; data source lost |
| RETIREMENT | — | — | 52-week net t < 0 at two consecutive reviews; structural break with mean ≈ 0; crowding breach; mechanism invalidated |

**Classification rules [P]**
- **Risk premium** requires all of:
  - a bad-state mechanism;
  - either negative factor returns in crypto drawdowns, liquidity crunches or depegs, or a positive Fama–MacBeth λ with an insignificant intercept;
  - persistence across regimes.
- **Anomaly:** significant alpha without risk evidence.
- **Exploitable alpha:** only after net out-of-sample and paper monitoring at capacity.
- Labels can overlap. Carry, for example, is plausibly both a crash-risk premium and a limits-to-arbitrage anomaly.

**Operational checklist.** Every item must be YES:
1. Ex-ante mechanism.
2. Bad-state classification evidence.
3. Point-in-time universe including dead coins.
4. All inputs `available_ts`-compliant.
5. Volume cleaned.
6. HAC t ≥ 3.0 and bootstrap CI excludes 0.
7. FDR control.
8. DSR ≥ 0.95.
9. PBO ≤ 0.20.
10. Multiverse stability.
11. C-3/C-4 alpha t ≥ 2.5.
12. Survives residualization.
13. Significant outside micro-caps.
14. Net > 0 at 1× and 2× costs.
15. Short leg implementable, or a viable long-only version.
16. Capacity sufficient.
17. Holdout criteria met.
18. Paper period passed.

Outcomes:
- All YES → **PROMOTE**.
- NO on item 3, 4, 11 or 14 → **REJECT**.
- Otherwise, one or two NOs → **QUARANTINE**, re-tested within 90 days.

---

## 11. Worked Research Examples

These show how to apply the procedures to cited results. They report no new empirical findings.

**A — Replicating CMOM.**
1. **Hypothesis.** Past-2-week winners outperform next week. Mechanism: retail trend-chasing in crypto, versus contrarian behavior in stocks (Kogan et al. 2024 [E]). [arxiv](https://arxiv.org/pdf/2510.14435)
2. **Target.** Q5 − Q1 = 2.6%/wk (NW t = 3.89) full-sample; 2.1%/wk (t = 3.70) post-2020 [E]. [arxiv](https://arxiv.org/pdf/2510.14435)
3. **Contradiction.** Rerun with monthly holding and 12-month formation (as in Grobys & Sapkota). Expect a null or reversal, consistent with Dobrynskaya's horizon result.
4. **Segmentation.** Expect momentum in large caps and reversal in small ones.
5. **Costs.** Fieberg, Liedtke & Zaremba report heavy costs and short-leg alpha [E]. Compute $c^*$; test long-only Q5 vs CMKT and a buffered variant.
6. **Expected label.** Anomaly, partially exploitable in large caps.

**B — Funding rate: new factor or disguised momentum?**
1. **Hypothesis.** High funding marks crowded longs, which underperform over 1–7 days. The time-series mechanism is from Schmeling et al. [E]; the cross-sectional version is T3.
2. **Audit.** Normalize venue funding intervals. Treat the Binance clamp mass point (He et al. [W]). Perp listing biases the universe toward large coins; document it.
3. **Tests.** Residualize FUND on CMOM, size and ILLIQ, because past returns predict deviations [W]. Then require spanning alpha t ≥ 3.0.
4. **Regime.** Test 2024–2026 separately, since the carry Sharpe turned negative in 2025 [E]. [arxiv](https://arxiv.org/pdf/2510.14435) If the effect is confined to 2020–23, quarantine it as a decayed premium.
5. **Separate hypothesis.** Test FUND as a crash-timing variable for CMKT, logged as its own trial.

**C — Token-unlock event study.**
1. **Hypothesis.** Unlocks of at least 2% of circulating supply within 30 days produce negative abnormal returns. Evidence is preliminary only [U].
2. **Data.** Use only schedule vintages published before $t$; back-filled schedules leak.
3. **Design.**
   - Benchmark: CMKT plus size-matched portfolios.
   - Windows: [−30,−1], [0,+5], [+6,+30].
   - Standard errors clustered by calendar week; placebo pseudo-events.
   - Controls for age, FDV/MCAP and size.
4. **Multiple testing.** FDR, DSR and costs apply across all thresholds and windows tried.

**D — Arbitrage mirage.**
- Naive BTC cross-exchange sorts over 510 BTC–fiat pairs on 165 exchanges in 49 currencies (CryptoCompare, Dec 2013–Jan 2025) earn about 68.5%/wk. Implementable pairs earn about 3.8%/wk, consistent with risk compensation [E].
- **Rule [P]:** an implausibly high gross return means untradable states until implementability is proven.

---

## 12. Candidate Factor Registry Template

| Field | Content | Example (CMOM) |
|---|---|---|
| `factor_id` / `version` | Unique ID; a spec change creates a new version | `CMOM_2W_VW_Q5` / 1.0.0 |
| `family` / `evidence_tier` | §2 | F3 / T1 |
| `hypothesis` / `prior_class` | Mechanism, sign, horizon | Under-reaction, +, 1 wk / anomaly |
| `formula_latex` | Exact formula | $\prod_{k=0}^{1}(1+r^w_{i,t-k})-1$ |
| `data_sources` | Tables, vendors, vintages | `market_bar` (vintage id) |
| `freq` / `lookback` / `hold` / `lag` | — | wk / 2 wk / 1 wk / 0 |
| `universe_rule` | §3 rules and parameters | U6–U14; MCAP ≥ $1M |
| `normalization` / `winsor` / `missing` | — | rank / returns 0.0025% / exclude |
| `portfolio` / `cost_model_id` | — | quintile VW, 10% cap / `TC_v3` |
| `trial_log_ref` | Path, raw N, effective N | `trials/CMOM`, 48 (eff. 11) |
| `results_gross` / `results_net` | Mean, HAC t, Sharpe, DSR, PBO, IC | — |
| `spanning` / `robustness` | α vs C-1/3/4; §7 pass map | — |
| `supporting_lit` / `contradicting_lit` | Citations | LTW 2022; Dobrynskaya / Grobys & Sapkota; Fieberg et al. |
| `status` / `history` / `next_review` | Lifecycle stage | VALIDATION / … / 2027-01-20 |
| `owner_agent` / `reviewer_agent` | Separation of duties | — |

---

## 13. Research Reproducibility Checklist [P]

- [ ] Commit hash in every result file; environment pinned (lockfile or container digest); seeds logged.
- [ ] Raw data immutable with `vintage_id`; derived tables rebuilt by script.
- [ ] Universe snapshots persisted for each rebalance.
- [ ] Complete trial log, with effective N computed.
- [ ] Spec hash recorded before results; holdout access logged.
- [ ] All tables and figures generated by code with a single command.
- [ ] Second-agent re-implementation at VALIDATION.
- [ ] Cost model versioned; historical fee schedules stored.
- [ ] Every literature claim mapped in the claim-to-source matrix with a label.
- [ ] Limitations and [U] items listed.

---

## 14. Bibliography (verified references)

Verification marks:
- **V:** confirmed on a publisher, NBER, SSRN, RePEc or arXiv page.
- **V\*:** confirmed via a reference list in a verified paper.
- **S:** standard reference, not re-fetched.

**Crypto**
- Bianchi & Babiak (2021), A Factor Model for Cryptocurrency Returns, CERGE-EI WP 710. [V]
- Bianchi, Babiak & Dickerson (2022), *J. Banking & Finance* 142, 106547. [V\*]
- Borri (2019), Conditional tail-risk in cryptocurrency markets, *J. Empirical Finance* 50, 1–19. [V]
- Borri, Liu, Tsyvinski & Wu (2026), Cryptocurrency as an Investable Asset Class: Coming of Age, *Annual Review of Financial Economics* 18; arXiv 2510.14435. [V]
- Borri & Shakhnov (2022), The Cross-Section of Cryptocurrency Returns, *RAPS* 12(3), 667–705. [V\*]
- Cong, He & Tang, The Tokenomics of Staking, NBER WP 33640. [V]
- Cong, Karolyi, Tang & Zhao, Value Premium, Network Adoption, and Factor Pricing of Crypto Assets, SSRN 3985631. [V]
- Cong, Li, Tang & Yang (2023), Crypto Wash Trading, *Management Science* 69(11), 6427–6454. [V] [bris](https://research-information.bris.ac.uk/en/publications/crypto-wash-trading/)
- Dobrynskaya (2023), Cryptocurrency Momentum and Reversal, *J. Alternative Investments* 26(1), 65–76. [V]
- Fieberg, Günther, Poddig & Zaremba (2024), Non-standard errors in the cryptocurrency world, *IRFA* 92, 103106. [V] [repec](https://ideas.repec.org/r/oup/rfinst/v33y2020i5p2019-2133..html)
- Fieberg, Liedtke, Metko & Zaremba (2023), Cryptocurrency factor momentum, *Quantitative Finance* 23(12), 1853–1869. [V] [repec](https://ideas.repec.org/a/eee/finana/v78y2021ics1057521921002349.html)
- Fieberg, Liedtke, Poddig, Walker & Zaremba (2025), A Trend Factor for the Cross Section of Cryptocurrency Returns, *JFQA* 60(7), 3116–3153. [V]
- Fieberg, Liedtke & Zaremba (2024), Cryptocurrency anomalies and economic constraints, *IRFA* 94, 103218. [V] [sciencedirect](https://www.sciencedirect.com/science/article/pii/S1057521922003696)
- Griffin & Shams (2020), Is Bitcoin really untethered?, *JF* 75(4). [V\*]
- Grobys & Sapkota (2019), Cryptocurrencies and momentum, *Economics Letters* 180, 6–10. [V]
- He, Manela, Ross & von Wachter, Fundamentals of Perpetual Futures, arXiv 2212.06888. [V]
- Kogan, Makarov, Niessner & Schoar (2024), Are cryptos different?, *JFE* 159, 103897. [V\*]
- Liu & Tsyvinski (2021), Risks and Returns of Cryptocurrency, *RFS* 34(6), 2689–2727. [V]
- Liu, Tsyvinski & Wu (2022), Common Risk Factors in Cryptocurrency, *JF* 77(2), 1133–1177. [V]
- Liu, Tsyvinski & Wu (2021), Accounting for Cryptocurrency Value, SSRN 3951514. [V\*]
- Makarov & Schoar (2020), Trading and arbitrage in cryptocurrency markets, *JFE* 135(2), 293–319. [V\*]
- Schmeling, Schrimpf & Todorov, Crypto Carry, *Management Science* (2026, DOI 10.1287/mnsc.2024.05069); BIS WP 1087. [V]
- Schwenkler & Zheng (2025), News-driven peer co-movement in crypto markets, *J. Corporate Finance* 93, 102772. [V] [scu](https://scholarcommons.scu.edu/finance/10/)
- Shen, Urquhart & Wang (2020), A three-factor pricing model for cryptocurrencies, *FRL* 34, 101248. [V]

**Methods / factor zoo**
- Bailey & López de Prado (2014), The Deflated Sharpe Ratio, *JPM* 40(5), 94–107. [V] [sharperat](http://www.sharperat.io/do-not-deflate-I.html)
- Bailey, Borwein, López de Prado & Zhu (2017), The Probability of Backtest Overfitting, *J. Computational Finance* 20(4), 39–69. [V] [arxiv](https://arxiv.org/pdf/2512.12924)
- Feng, Giglio & Xiu (2020), Taming the Factor Zoo, *JF* 75, 1327–1370. [V\*]
- Gu, Kelly & Xiu (2020), Empirical Asset Pricing via Machine Learning, *RFS* 33(5), 2223–2273. [V]
- Hansen (2005), A Test for Superior Predictive Ability, *JBES* 23(4). [V\*] [arxiv](https://arxiv.org/pdf/2607.06117)
- Harvey, Liu & Zhu (2016), …and the Cross-Section of Expected Returns, *RFS* 29(1), 5–68. [V] [repec](https://ideas.repec.org/a/oup/rfinst/v29y2016i1p5-68..html)
- Hou, Xue & Zhang (2020), Replicating Anomalies, *RFS* 33(5), 2019–2133. [V] [oup](https://academic.oup.com/rfs/article-abstract/33/5/2019/5236964)
- Jensen, Kelly & Pedersen (2023), Is There a Replication Crisis in Finance?, *JF* 78(5), 2465–2518. [V] [github](https://github.com/bkelly-lab/ReplicationCrisis)
- Kozak, Nagel & Santosh (2020), Shrinking the Cross-Section, *JFE* 135(2), 271–292. [V] [arxiv](https://arxiv.org/pdf/2508.14986)
- López de Prado (2018), *Advances in Financial Machine Learning*, Wiley. [V\*] [arxiv](https://arxiv.org/pdf/2505.14050)
- McLean & Pontiff (2016), Does Academic Research Destroy Stock Return Predictability?, *JF* 71(1), 5–32. [V] [signaltrace](https://www.signaltrace.wiki/markov-model/Papers/McLean-and-Pontiff-2016)
- Newey & West (1987), *Econometrica* 55(3). [V\*]
- Novy-Marx & Velikov (2016), A Taxonomy of Anomalies and Their Trading Costs, *RFS* 29(1), 104–147. [V] [nber](https://www.nber.org/papers/w20721)
- White (2000), A Reality Check for Data Snooping, *Econometrica* 68(5). [V\*] [arxiv](https://arxiv.org/pdf/2606.09025)
- Amihud (2002), *J. Financial Markets* 5. [V\*]
- Fama & MacBeth (1973), *JPE* 81. [V\*]
- Benjamini–Hochberg (1995); Benjamini–Yekutieli (2001); Gibbons–Ross–Shanken (1989). [S]

**Unverified [U]**
- Chi et al. (2023), *J. Futures Markets*, DOI 10.1002/fut.22425: basis as the strongest cross-sectional futures signal. Snippet only; authors and pages unverified.
- Dobrynskaya, downside risk, *IRFA* 91 (2024).
- Token-unlock working papers and industry reports.
- SSRN 6725492 (BTC funding/OI).
- IRFA 94 (2024) crypto ML study.

---

## 15. Claim-to-Source Matrix

| # | Claim | Source | Label |
|---|---|---|---|
| 1 | Market, size and momentum span the crypto cross-section | Liu, Tsyvinski & Wu 2022 | [E] |
| 2 | CMOM 5–1 = 0.026/wk (t 3.89); post-2020 0.021 (t 3.70); CSIZE and CVALUE significant | Borri et al. 2026, Table 2 | [E] |
| 3 | MOM12/24, VOL, VOLUME and beta sorts insignificant | Borri et al. 2026, Table 3 | [E] |
| 4 | C-4 adjusted R² 0.473 vs C-1 0.046; FS-FMB ≈ 0.70; KA ≈ 0.72 | Borri et al. 2026, Table 5 | [E/W] |
| 5 | Equity correlation 1% → 39% after 2020 | Borri et al. 2026, Table 1 | [E] |
| 6 | BTC jump days ≈ 28% vs 5.3% for stocks | Borri et al. 2026, Table 4 | [E] |
| 7 | Carry averages above 10% annually and reaches up to 60% p.a. (BIS WP 1087); "sometimes exceeding 40% per annum" (Mgmt Sci 2026); predicts crashes | Schmeling, Schrimpf & Todorov | [E] |
| 8 | Carry Sharpe 6.45 (2020–2025) → 4.06 (from 2024) → negative (2025); funding mean ≈ 8% with 0.8% volatility | Borri et al. 2026 (Binance BTC, Aug 2020–May 2025) | [E] |
| 9 | Perps above 98% of BTC futures volume in the Schmeling–Schrimpf–Todorov sample | Schmeling et al., via Borri et al. | [E] |
| 10 | Perp deviations 52–90% p.a., declining ~22 pp/yr [arxiv](https://arxiv.org/html/2212.06888v7) | He et al. | [W] |
| 11 | Wash trading averages 77.5% of total volume on unregulated exchanges (median 79.1%; 29 exchanges) | Cong, Li, Tang & Yang 2023 | [E] |
| 12 | Momentum at 2–4 wk, reversal beyond 1 mo | Dobrynskaya 2023 | [E] |
| 13 | No momentum (143 coins, monthly) | Grobys & Sapkota 2019 | [E] |
| 14 | Market + size + reversal model | Shen, Urquhart & Wang 2020 | [E] |
| 15 | Large-cap momentum, small-cap reversal; value and adoption premia | Cong, Karolyi, Tang & Zhao | [W] |
| 16 | Non-standard errors exceed standard errors | Fieberg et al. 2024 (IRFA 92) | [E] |
| 17 | Micro-cap size/volume anomalies; costly, short-driven momentum; bull-market concentration | Fieberg, Liedtke & Zaremba 2024 | [E] |
| 18 | IPCA R² 17.2% vs 9.6% | Bianchi & Babiak | [W] |
| 19 | Google searches → +2.3% 2-week-ahead returns | Liu & Tsyvinski NBER WP 24877 | [W] |
| 20 | News-peer reversal | Schwenkler & Zheng 2025 | [E] | [ssrn](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=3572471)
| 21 | Arbitrage over 510 pairs / 165 exchanges / 49 currencies: 68.5%/wk → 3.8%/wk when implementable | Borri et al. 2026; Borri & Shakhnov 2022 | [E] |
| 22 | t > 3.0 hurdle | Harvey, Liu & Zhu 2016 | [E] | [nber](https://www.nber.org/system/files/working_papers/w20592/w20592.pdf)
| 23 | 65% / 82% replication failure | Hou, Xue & Zhang 2020 | [E] | [cxoadvisory](https://www.cxoadvisory.com/big-ideas/most-stock-anomalies-fake-news/)
| 24 | 82.4% Bayesian replication rate | Jensen, Kelly & Pedersen 2023 | [E] | [wiley](https://onlinelibrary.wiley.com/doi/full/10.1111/jofi.13249)
| 25 | 0.58% → 0.402% (−26% OOS) → 0.264% (−58% post-publication) monthly | McLean & Pontiff 2016 | [E] |
| 26 | Under 50% turnover survives costs | Novy-Marx & Velikov 2016 | [E] | [alphaarchitect](https://alphaarchitect.com/trading-costs-destroy-factor-investing/)
| 27 | Trees/NNs gain via interactions; shallow beats deep | Gu, Kelly & Xiu 2020 | [E] |
| 28 | Sparse SDFs inadequate | Kozak, Nagel & Santosh 2020 | [E] |
| 29 | Staking-carry Sharpe 1.60 | Cong, He & Tang | [W] |
| 30 | Retail trend-chasing in crypto | Kogan et al. 2024 | [E] |
| 31 | Unlocks cause negative returns | Preliminary only | [U] |
| 32 | Funding/OI predict the cross-section | None verified | [U] |
| 33 | DSR/PBO/holdout/promotion thresholds | This document | [P] |

---

## 16. Caveats

- **Thin samples.** Evidence spans 2014–2025, only 1.5–3 cycles, so regime tests have limited power.
- **Author overlap.** Key post-2020 estimates come from a review by the C-3/C-4 authors. Independent work (Fieberg et al.) agrees on robustness but stresses costs and micro-caps.
- **Working papers.** C-5, IPCA, perp fundamentals, staking, and all cross-sectional funding/OI/unlock evidence were not peer-reviewed at cutoff.
- **Equity priors.** HXZ, JKP, McLean–Pontiff and Novy-Marx–Velikov are equity studies, used here as priors and procedures.
- **Liu & Tsyvinski versions.** The 2018 NBER abstract reports no exposure to stock or macro factors; [nber](https://www.nber.org/system/files/working_papers/w24877/w24877.pdf) the RFS abstract stresses crypto-specific drivers. [oup](https://academic.oup.com/rfs/article-abstract/34/6/2689/5912024) Post-2020 correlations contradict the pre-2018 null in any case.
- **Cost figures.** Cost levels are placeholders to calibrate.

---

## 17. Research Cutoff and Update Triggers

**Cutoff:** October 22, 2026.

**Re-review triggers [P]:**
1. A peer-reviewed cross-sectional study on funding, OI, unlocks or protocol fundamentals → re-tier F9–F14.
2. Journal publication of Cong et al., Bianchi & Babiak, He et al., or Borri et al. FS-FMB/KA → update [W] to [E].
3. Market-structure shocks:
   - closure of a top-5 derivatives venue;
   - changes to funding intervals or margining (He et al. link portfolio margin to compressed deviations [W]); [arxiv](https://arxiv.org/html/2212.06888v7)
   - a stablecoin depeg > 5% lasting > 24 h.
4. Regulatory change, e.g., implementation of the US GENIUS Act (enacted July 2025, per Borri et al. 2026) [arxiv](https://arxiv.org/pdf/2510.14435) or EU MiCA phases → re-run U4 and U10.
5. Decay alarm: a promoted factor's 52-week net t < 0, or two quarters of negative carry Sharpe.
6. Vendor methodology changes → re-run DATA AUDIT.
7. Quarterly literature scan; full revision by 2027-10-22.

---

## 18. October 2026 Evidence Amendments and Corrections

**Scope.** All investable assets in this document are *digital currencies / cryptoassets*. Price-linked HIP-3 equity, commodity or index instruments and binary HIP-4 outcome contracts may be used as explanatory state variables or market-structure controls, but must **not** silently enter the digital-currency factor return universe. Venue eligibility is determined by currently accessible read-only connectors, not by a universal exchange whitelist. A tool listing implies a callable interface, **not** complete or cost-free historical coverage.

### 18.1 Newly verified peer-reviewed evidence

- **Brigida (2026), _Crypto pricing with hidden factors_, Finance Research Letters 109, 110488**, https://doi.org/10.1016/j.frl.2026.110488 : a Giglio–Xiu-style latent-factor approach finds both crypto-specific and equity-industry risk exposure; TVL is not independently priced after latent-factor adjustment. **[E]**. Add a latent-factor robustness benchmark to §§5, 7, 8. This does **not** invalidate C-3; it makes a C-3-only alpha claim incomplete.
- **Schmeling, Schrimpf & Todorov (2026), _Crypto Carry_, Management Science**, https://doi.org/10.1287/mnsc.2024.05069 : the published paper confirms substantial and varying crypto futures basis and limits-to-arbitrage effects. **[E]**. Avoid extrapolating historical carry levels or assuming every perp funding signal is a cross-sectional premium.
- **Borri, Liu, Tsyvinski & Wu (2026), _Cryptocurrency as an Investable Asset Class: Coming of Age_, Annual Review of Financial Economics 18**, https://doi.org/10.1146/annurev-financial-111524-010949 : published review-in-advance on August 10, 2026; the journal abstract describes **seven** stylized facts, while earlier preprint descriptions differ. **[E] journal-level conclusions; manuscript-version-specific statistics must retain exact version/table references**.
- **Fieberg et al. (2024)**, https://doi.org/10.1016/j.irfa.2024.103106; **Fieberg, Liedtke & Zaremba (2024)**, https://doi.org/10.1016/j.irfa.2024.103218 : design variation and tradeability materially alter factor results. **[E]**. Consequently apply venue, liquidity and weighting sensitivity as first-order identification tests, not cosmetic appendices.

**Correction [P].** The original's fixed criteria (`t ≥ 3`, `DSR ≥ .95`, `PBO ≤ .20`, twelve-month holdout, 26 paper weeks, 80% multiverse sign stability) are an intentionally conservative *research governance policy*. None is a universally sufficient scientific theorem. A strong t-statistic cannot rescue leaked samples; DSR and PBO cannot be reliably computed from an incomplete or biased search-history matrix. Report *not estimable* rather than forcing pass/fail. Avoid interpreting a risk premium solely from positive historical average returns: evidence of priced bad-state covariance, exposure prices, and robustness is required.

### 18.2 Formal evidence and claim ledger amendment [P]

Every quoted effect size must include `study_version`, `table_or_figure`, `sample_start`, `sample_end`, `asset_filter`, `weighting`, `gross_or_net`, `statistic`, `unit` and `publication_status_asof`. Distinguish published journal estimates from older draft estimates. If the source was not independently inspected to the claimed table, mark the *numeric estimate* **[U: table verification pending]**, even if the publication itself is verified. Recheck the document's pre-existing numerical claims (including unusually high Sharpe ratios, jump frequencies, the 20,736-spec multiverse, and source-linked bibliography) before using them as replication acceptance targets. Do not infer that being mentioned in a review independently replicates the underlying finding.

## 19. Connector-Aware Venue and Data Access Protocol [P]

### 19.1 Capability registry (observed interfaces on 2026-10-22)

| Connector / provider | Observed data-access surface | Research role | Non-negotiable limitation |
|---|---|---|---|
| **0xArchive** | Hyperliquid core perpetuals, HIP-3, HIP-4, Hyperliquid spot, Lighter, Lighter on Robinhood Chain; trades, funding, OI, order books and selected L3/L4 histories | Primary venue-native historical microstructure and derivatives research | Query *symbol-specific* coverage, data incidents, entitlement, pagination and reconstruction before declaring a historical panel complete |
| **Co-Invest / Liquid** | Market discovery, quotes, technical indicators, current depth, positioning and cohort signals, market news | Cross-check and potential predictive descriptors | Current snapshots and proprietary derived positioning are not automatically historically reproducible; no user/account write operations in research mode |
| **fin-data MCP** | Crypto instrument discovery, spot/swap candles, current books, recent trades, funding, OI, mark and sentiment (via supported backend) | Independent spot/derivatives cross-check | Endpoint pagination and exchange coverage depend on the particular operation; current snapshot is not historical L2 |
| **Massive** | Searchable market-data endpoints and historical APIs | Cross-asset reference / asset-level coverage, conditional upon endpoint entitlement | Verify supported crypto venue, resolution, period and plan per endpoint; do not infer historical tick availability |
| **CoinGecko, CoinPaprika, CMC** | Asset discovery / identifiers / listings / quoted aggregates through available actions | Independent identity, circulating-supply and market-cap verification | Aggregated historical market cap and supply may reflect revised information rather than archived point-in-time vintages |
| **Blockscout** | EVM chain / address / contract / transaction information | Verify token contract, issuance, activity and on-chain supply where supported | Chain coverage and block finality vary; tokens/addresses do not directly equal economic users |
| **Other active crypto tools** | Discover per session rather than assume installed capabilities (for example, market explorers or crypto docs search) | Specialized validation | Never treat a named provider or endpoint as qualified until a read-only probe succeeds |

Read-only capability discovery does not authorize trading, order placement, paper-account mutation, webhook registration, wallet watchlist writes, or account-specific data retrieval unrelated to a factor hypothesis.

### 19.2 0xArchive capability audit (service reports observed 2026-10-23 00:15 UTC)

The service advertised the following **venue-level** coverage, not instrument-level completeness:

| Venue/data | Earliest in service-wide coverage report | Important qualification |
|---|---|---|
| Hyperliquid perpetual trades | 2023-04-15 03:31 UTC | Historical fills/trades; reporting of about one-hour lag for fills |
| Hyperliquid funding and OI | 2023-05-20 02:50 UTC | Current status **degraded** for both; reported 24h completeness 98.8% |
| Hyperliquid standard L2 book snapshots | 2023-04-15 00:00 UTC | ~1.2-second snapshot resolution is **not** historical tick-by-tick order-level reconstruction |
| Hyperliquid L4 diffs and order events | 2026-03-10 ~22:00 UTC | Event-level ~100ms batches; checkpoint-based reconstruction available beginning March 2026 |
| Hyperliquid L4 full checkpoints | 2026-03-11 01:03 UTC | Start from valid checkpoint and apply every ordered diff without gaps |
| Hyperliquid liquidation events | 2025-12-22 00:00 UTC | Older events may exist internally but are not served; lag may apply |
| Lighter fills | 2025-01-17 08:43 UTC | Market-specific coverage must still be checked |
| Lighter L2 historical book | 2026-01-29 02:13 UTC | Provider describes tick-level snapshot coverage, not necessarily complete order-event history |
| Lighter L3 order-level books | 2026-03-05 03:33 UTC | Check whether snapshots are continuous enough for chosen estimand |
| HIP-3 market histories | Varies by datatype (fills from 2025-10-13; L4 from 2026-03) | Include only HIP-3 crypto-underlying instruments in asset factors |
| Hyperliquid spot trades | 2025-03-22 10:50 UTC | Separate orderbook and trade availability |
| HIP-4 outcome markets | Available from 2026-05 for select types | **Excluded** from cryptoasset factor universe; contextual risk signals only |
| Lighter on Robinhood Chain | Mid-2026 onward, datatype-dependent | Crypto-only membership requires contract classification |

The reported `historicalCoverage: 0.4` for some datasets must **not** be reinterpreted as 40% completeness without a provider definition. **Coverage reports and capability policy floors can differ**: use the later valid bound where they conflict, and inspect the actual requested market. The overall service health was `degraded` when queried, despite several individual venues reporting `operational`. Do not convert headline 99.9% completeness to a guarantee for an arbitrary coin, interval or research date.

### 19.3 Per-study probe [P]

For every (`venue`, `instrument`, `datatype`, `analysis_window`) tuple:

1. Discover the instrument's canonical venue identifier and trading history; resolve symbol aliases, HIP prefixes, spot pairs and contract terms.
2. Run 0xArchive `get_capabilities`, `get_symbol_coverage`, `get_freshness`, relevant market read operations and `get_data_incidents`; inspect data quality/latency. Where no equivalent read exists, mark unavailable.
3. Record actual earliest and latest **returned** timestamps, limits, paging cursor behavior, interval availability, returned/expected event counts, clock quality, and observed outages.
4. Page until the requested range is complete or a hard limit/error is reached. Deduplicate by a native event identifier plus venue/instrument and keep raw response digests.
5. Confirm cross-page ordering, timestamps, monotonic sequence identifiers where available, and no duplicated or omitted boundaries.
6. For L4/L3 replay, validate checkpoint + diff continuity by comparing reconstructed subsequent checkpoints. Quantify divergence and gap durations. A missing diff means reconstruction is invalid **after that gap** until re-anchored.
7. Match trade-derived OHLCV to independently retrieved candles only as a **consistency check**; candles never substitute for missing trades or order-book events.
8. Label each feature `native_event`, `checkpoint_reconstructed`, `sampled_snapshot`, `aggregated`, or `model_estimate` and attach an observed `coverage_ratio`, not an unsupported completeness claim.

Reject event-driven factor tests if complete historical event sequencing is necessary and cannot be established. For slower weekly factors, aggregated funding/OI with defensible gaps may still be usable after uncertainty and missing-data sensitivity tests.

## 20. Venue-Native Factor Extensions [P; exploratory until validated]

The existing F1–F16 taxonomy remains the primary model. Register the following as **nested F6/F7/F9/F10 subfamilies**, not independent established anomalies:

| Candidate ID | Ex-ante signal definition | Required granularity | Sign hypothesis (test both only as separate logged trials) | Main threat |
|---|---|---|---|---|
| `OFI_L2` | Cont–Kukanov–Stoikov-style best-quote queue change, standardized by contemporaneous depth | Time-ordered L2 updates | Short-horizon price pressure | Snapshot sampling misses intervening events |
| `DEPTH_IMB` | `(bid_depth - ask_depth)/(bid_depth + ask_depth)` inside fixed basis-point bands | Contemporaneous L2 book | Microstructure pressure | Stale book, spoofing, ambiguous quote conversions |
| `FLOW_TOX` | Signed aggressor volume / total volume, with trade-sign reliability documented | Native trades | Continuation vs adverse selection | Maker/taker-side confusion |
| `CVD_DIVERGENCE` | Signed cumulative trade flow minus estimated flow expected under contemporaneous returns | Native trades | Pressure exhaustion | Inferred CVD is not a native aggressor series |
| `CANCEL_INTENSITY` | Cancelled resting depth / displayed depth per interval, by side and queue band | L4 order lifecycle | Fragile displayed liquidity | Partial cancellation or modification semantics |
| `LIQ_PRESSURE` | Realized liquidations / trailing trade volume with sign and concentration | Liquidation events | Forced flow and reversal | Ex-post contemporaneous identification leakage |
| `FUND_OI_INTERACTION` | Within-venue standardized funding surprise × OI change | Timestamped funding/OI | Crowded leverage unwind | Endogenous funding, nonmatching sampling clocks |
| `VENUE_DISLOCATION` | Executable cross-venue spread after latency, inventory and transfer frictions | Synchronized bid/ask, fees and inventory | Dislocation mean reversion | Non-synchronous books; infeasible cross-venue hedges |
| `QUEUE_COST` | Estimated executable participation cost conditioned on queue location / simulated depth | Validated L3/L4 reconstruction | Execution cost conditional on signal | Cannot infer queue priority from L2 alone |

Anchor microstructure research in **Cont, Kukanov & Stoikov (2014), _The Price Impact of Order Book Events_, Journal of Financial Econometrics**, and **Kyle (1985), _Continuous Auctions and Insider Trading_, Econometrica**, as *market-microstructure methodological priors*, not as direct crypto out-of-sample validation. Claims of crypto-specific return predictability must be tested anew.

**Sampling and alignment rules:** use UTC exchange event timestamps where possible; preserve ingest time; lag all factors until actually available; prohibit a funding print from entering a pre-settlement prediction; allow missing book snapshots to remain missing; standardize by venue and liquidity bucket *within the training fold*; distinguish venue-local prediction from pooled cross-sectional cryptoasset prediction. Use heteroskedasticity- and cross-sectional-dependence-aware uncertainty, including clustering by asset and calendar period or date-level block bootstrap where appropriate. A 100ms feature is not meaningfully validated by a weekly Sharpe alone.

## 21. Statistical and Implementation Corrections [P]

1. **Portfolio direction.** The primary high-minus-low sort is only compatible with factors whose score is defined so that high means long. CSIZE's small-minus-large return requires explicit orientation. Store `signal_direction`; report low–high and high–low consistently. Avoid inferring universal signs from a table label.
2. **Risk-free rate.** A dollar T-bill proxy is not interchangeable with actual USDC/USDT lending or margin financing. Report excess USD benchmark returns separately from venue-executable funding economics; stablecoin depegs and borrowing constraints belong in the cost and risk models.
3. **Funding calculations.** Reconstruct cash transfers from the venue's actual funding convention, timestamps, mark notional and direction. Annualized rates are display transformations, not realized cashflows. Do not OI-weight rates across venues as though the agent can trade the synthetic consolidated rate.
4. **Spot versus perpetual assets.** Maintain separate `asset_id` (economic cryptoasset), `instrument_id` (spot/perp contract), `venue_id`, `collateral_id`, and contract terms. A perp's realized total return includes price, funding, trading costs, collateral and liquidation risk; it must not be pooled with spot price return.
5. **Returns and price discontinuities.** Specify simple vs log returns, compounding convention, delisting cash recovery, migrations, denomination changes, forks, stablecoin quote conversions and negative/zero-price filtering. Do not manufacture prices across data gaps.
6. **Multiple testing.** BH at q=.05 and BY at q=.05 are distinct procedures; a fixed `t≈2.78` is **not** a generic BH/BY cutoff. Compute adjusted p-values from the actual hypothesis family and dependence assumptions. Use a bootstrap reality check or SPA when strategy returns are jointly dependent. DSR requires the correct return-period Sharpe and effective *predeclared* trial count, and does not substitute for family-level p-value correction.
7. **PBO.** CSCV assumes sufficient comparable partitions; under regime non-exchangeability PBO is descriptive at best. Estimate it only with enough candidate strategies and credible train/test partitions. Distinguish CSCV from purged CPCV; do not report a PBO for a single candidate selected without a recoverable experiment log.
8. **Statistical power.** If histories are shorter than the mandated holdout, indicators lack enough observations, or the number of independent market regimes is small, label `UNDERPOWERED`. Do not interpret a nonsignificant result as proof of no effect.
9. **Cost calibration.** Prefer measured spread, depth, partial fills, missed trades, fee schedules, funding, liquidation and adverse-selection paths from the **same accessible instrument and date**. If only snapshots exist, use conservative bounds and label `COST_MODEL_UNCALIBRATED`. Stress 1×/2×/3× costs and capacity by *actual* target notional rather than the legacy illustrative $1M–$500M ladder.
10. **Economic classification.** A peer-reviewed association is not a causal risk premium. Use exposure prices plus documented bad-state covariance and risk-model robustness before `RISK_PREMIUM`; reserve `ANOMALY` for statistically replicable association and `EXPLOITABLE_ALPHA` only for net implementable OOS and paper evidence.
11. **Cross-sectional dependence.** Weekly cryptocurrency returns share market shocks and exchange failures. Supplement HAC across time with date/asset clustered or block-bootstrapped cross-sectional regressions, and assess effective independent observations. Avoid using individual asset-weeks as independent samples.
12. **Sealed evaluation.** Report an immutable timestamped model freeze, train/validation/OOS date boundaries, archive query manifest, source vintages, trial counts and outcome of all prior attempts. Adding a post-hoc feature version after viewing a holdout requires a **new** future holdout.

### New metadata schema [P]

```yaml
factor_research_run:
  asset_scope: digital_currencies_only
  venue_scope: connector_accessible_and_read_only
  cutoff_utc: 2026-10-22T23:59:59Z
  research_mode: paper_only
  tool_discovery_ts: null
  connector_capability_manifest_hash: null
  literature_claim_ledger_ref: null
  factor_spec_hash: null
  train_window: null
  validation_window: null
  sealed_holdout_window: null
  units_and_return_convention: null
  trials_raw: null
  trials_effective_estimate: null
  data_quality_status: unverified
  cost_model_status: uncalibrated
  result_status: hypothesis

observations_required:
  - asset_id
  - instrument_id
  - venue_id
  - native_symbol
  - quote_asset_id
  - collateral_asset_id
  - event_ts
  - observed_ts
  - ingested_ts
  - available_ts
  - vintage_id
  - data_granularity
  - source_tool
  - request_parameters_digest
  - raw_payload_digest
  - quality_flags

venue_coverage_required:
  - datatype
  - scope_start_ts
  - scope_end_ts
  - first_returned_ts
  - last_returned_ts
  - native_interval_or_event_cadence
  - page_limit
  - pagination_complete
  - reconstruction_validated
  - gaps_and_incidents
  - latency_distribution
  - entitlement_verified
```

**Acceptance override:** `DATA_AUDIT` cannot pass while a decision-driving venue/instrument/date tuple is `unverified`, a required event sequence is discontinuous, availability chronology is missing, or a modeled cost lacks a conservative validated bound. Underpowered, limited-coverage work can still be published as exploratory research, but may not be promoted to exploitable alpha.

## 22. Targeted Claim-to-Source Addendum

| Claim | Evidence/source | Status at cutoff |
|---|---|---|
| Crypto returns expose latent crypto and equity-industry factors; TVL not independently priced after adjustment | Brigida (2026), https://doi.org/10.1016/j.frl.2026.110488 | [E] |
| Crypto basis/carry varies and reflects leverage demand and arbitrage frictions | Schmeling, Schrimpf & Todorov (2026), https://doi.org/10.1287/mnsc.2024.05069 | [E] |
| Researcher design variation materially affects crypto anomaly significance | Fieberg et al. (2024), https://doi.org/10.1016/j.irfa.2024.103106 | [E] |
| Microcap effects and trading frictions weaken naive anomaly results | Fieberg, Liedtke & Zaremba (2024), https://doi.org/10.1016/j.irfa.2024.103218 | [E] |
| Published August 2026 ARFE version of _Coming of Age_ describes seven stylized facts | Borri et al. (2026), https://doi.org/10.1146/annurev-financial-111524-010949 | [E] |
| 0xArchive historical L4 diffs / checkpoints available for specified Hyperliquid scopes from March 2026 | Live `get_capabilities` and `get_data_coverage` service metadata queried October 22, 2026 | [TOOL; not peer-reviewed] |
| Funding/OI service currently degraded, reported completeness 98.8% in 24h | Live `get_data_quality_status` queried October 22, 2026 | [TOOL; transient] |
| OFI / depth imbalance / liquidation pressure earn post-cost crypto factor premia | Hypotheses proposed here, not replicated evidence | [P/U] |

**Operational use:** Preserve §§1–17 as the baseline specification and treat §§18–22 as controlling amendments wherever older assumptions conflict. Future complete-document consolidation should preserve the study-specific formulas, taxonomy, replication examples and full bibliography, while replacing any superseded instructions explicitly noted here.
