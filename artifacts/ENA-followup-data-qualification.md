# ENA Follow-up: Same-Venue Prices and USDe Supply Recovery

Run: ENA-PIT-DQ-20261023-02. Public read-only sources only. Retrieval occurred 2026-10-23 UTC; exact per-call timestamps were not returned by the tools.

## Qualification matrix

| Series/source | Instrument and metric | Verified range | Availability/revision evidence | Missingness and disposition |
|---|---|---|---|---|
| ENA, Kraken spot | ENA/USD, market ID ENAUSD; daily OHLCV close in USD per ENA | 720 consecutive candles, 2024-11-02 00:00 UTC to 2026-10-22 00:00 UTC | Candle event timestamp is UTC Unix milliseconds. Original publication time and historical revision/vintage log unavailable. | 0 missing dates in retrieved span. Kraken documented OHLC history cap is 720 latest entries; earlier history cannot be recovered through this endpoint. Qualified for same-venue descriptive returns within this window only. |
| BTC, Kraken spot | BTC/USD, market ID XXBTZUSD; same daily OHLCV fields | Same 720 dates as ENA | Same limitations | 0 missing dates in common returned span. Qualified benchmark for this venue/window. |
| ETH, Kraken spot | ETH/USD, market ID XETHZUSD; same daily OHLCV fields | Same 720 dates as ENA | Same limitations | 0 missing dates in common returned span. Qualified benchmark for this venue/window. |
| USDe, HT Digital / Ethena Proof-of-Reserves feed | Weekly reported Total Token Supply in millions | Rendered rows include 2026-08-21 through 2026-10-23; examples: Oct 16 4,732.82m; Oct 9 4,821.55m; Oct 2 4,903.84m | Page showed last updated 2026-10-23 00:08 UTC. Per-row first publication times, preserved vintages, and amendments are not supplied. | Historical candidate, not point-in-time qualified. Only limited rows could be verified from the rendered page; missingness rate not measurable. Oct 23 observation excluded from any pre-holdout use. |
| USDe, Ethena attestation archive | Monthly custodian attestations | Official index lists 2024-04 through 2026-01 | Individual linked reports and their publication/revision timestamps were not acquired in this run. | Recovery lead; no values entered until report-level extraction and scope verification. |
| USDe, DefiLlama | Historical daily UTC TVL, distinct from verified token supply | Public page reports history from 2023-12-14 through 2026-10-22 | Current history extract; no vintage or first-publication log verified | Context only. TVL was not substituted for USDe total supply. |

## Price source checks

Kraken active spot instruments were resolved before fetching candles. Two pages were requested per pair (500 then 221 rows). Each pair returned 721 rows including the 2026-10-23 00:00 UTC boundary candle; after excluding that row there are 720 common dates, no duplicate timestamps, and no calendar gaps. The candle dated 2026-10-22 is the latest included observation.

Binance candidate check failed with HTTP 451 restricted-location response from its public markets endpoint. Coinbase resolved active ENA/USD, BTC/USD and ETH/USD spot pairs, but the queried history returned no ENA candles and only 300 BTC/ETH candles ending 2025-01-25. These are source-access/coverage failures, not evidence the pairs did not trade. Kraken therefore provides the qualified common venue panel, though its older-history cap leaves the April-November 2024 period uncovered.

## Historical supply recovery finding

Three routes have different evidential status. First, the Ethereum USDe contract totalSupply at a finalized historical block is a reconstructible on-chain state observation, but a daily finalized-block series has not yet been built and provider first-indexing times remain unknown. Second, Ethena's monthly attestation index appears to reach back to April 2024, but the source documents must be individually acquired and their dates, scope, and revisions checked. Third, HT Digital shows weekly supply observations in 2026, but a current page is not an archived contemporaneous tape. DefiLlama's cited daily history is TVL and cannot stand in for supply.

## Frozen holdout and exposure

The frozen confirmatory design and holdout dates remain unchanged: 2026-10-23 through 2028-10-22. No regression was fit. This run did not use boundary observations in any pre-holdout analysis. However, the existing CoinGecko archive already included a 2026-10-23 00:00 UTC ENA/BTC/ETH point; the Kraken retrieval also returned its 2026-10-23 00:00 UTC candle; and the reviewed live HT Digital page displayed a supply point at 2026-10-23 00:08 UTC. These were accessed and are retained only in provenance records. The first holdout date has therefore been accessed, so the whole holdout cannot be represented as untouched. The remaining future interval has not been analyzed; retain the original frozen dates and disclose this boundary exposure in any confirmatory evaluation.

This stage does not report BTC/ETH-adjusted return statistics because its scope was data acquisition and qualification. It establishes a descriptive price panel from 2024-11-02 through 2026-10-22, but does not establish daily point-in-time supply, revenue, executed buyback, or effective-float series. No complete fundamental predictive test is available.

## Tool and source ledger

| Source/tool | Execution and evidence |
|---|---|
| CCXT MCP 0.1.3 / CCXT 4.5.88 | Safety status returned no accounts; public market tier true; private read, trading, funds, and implicit writes false. Public markets search and OHLCV only. |
| Kraken OHLCV | Exact resolved symbols ENA/USD, BTC/USD, ETH/USD; daily spot candles. Retrieved tool payload pages archived in artifacts/ena-same-venue-spot-kraken-2026-10-23.json. That archive includes the boundary row, explicitly excluded from pre-holdout calculations. |
| Binance | Public candidate query executed; HTTP 451 restricted-location error. |
| Coinbase | Public active market search and OHLCV executed; inadequate common historical range. |
| HT Digital / Ethena PoR | Public current page reviewed; it states that weekly or more frequent publications reflect outputs from the PoR application and checks, and do not automatically constitute continuous assurance or a full audit opinion. |
| Ethena attestation docs and DefiLlama | Public pages reviewed; individual reports/API payload were not acquired. |

## Sources

- [Kraken OHLC API reference](https://docs.kraken.com/api-reference/market-data/get-ohlc-data) — says only the 720 most recent entries are returned.
- [HT Digital / Ethena Proof-of-Reserves feed](https://data.ht.digital/por/ethena).
- [Ethena custodian attestation index](https://docs.ethena.fi/resources/custodian-attestations).
- [DefiLlama Ethena USDe history](https://enterprise.defillama.com/protocol/ethena-usde).
- [Binance Spot API documentation](https://developers.binance.com/en/docs/catalog/core-trading-spot-trading/api/rest-api/market).
- [Previous coverage matrix](ENA-PIT-data-coverage-matrix.md), including original source and methodology manifest.
