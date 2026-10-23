# 07 — On-Chain Intelligence Methodology

**Version:** 1.0  
**Research cutoff:** 2026-10-22 (America/Detroit); external material and tool metadata consulted on this date.  
**Domain:** Digital currencies, tokenized protocol claims, stablecoins, wrapped assets, crypto-native spot markets and derivatives **only**.  
**Status:** Research methodology and proposed internal controls—not a guarantee of data coverage, an empirical performance claim, financial advice, or authority to transact.  
**Companion files:** `01-derivatives-methodology.md`, `03-factor-research-methodology.md`, `04-backtesting-methodology.md`, `05-portfolio-risk-methodology.md`, `06-source-provenance-methodology.md`. A proposed `02-spot-market-microstructure-methodology.md` may own more detailed execution-book analysis.

## 0. Mandate and decision principles

The mission of on-chain intelligence is to derive **falsifiable, time-correct, uncertainty-aware descriptions** of digital-currency supply, custody, movement, economic use, leverage and protocol risk from observable ledger records, supplemented by explicitly labeled off-chain observations. It does not convert pseudonymous addresses into verified people, raw transfer amounts into capital inflows, TVL into organic demand, DEX volume into genuine trading, or market correlation into causation.

**Rules:**

1. **Observed transaction ≠ economic actor ≠ intent.** A hash establishes an included state transition under the selected canonical chain; it does not establish beneficial ownership, human identity, motivation, or the accounting treatment of a transfer.
2. **Consensus state outranks dashboards for ledger facts.** Prefer independently verifiable blocks, logs, receipts and contract state for canonical transaction facts. An indexer is an important convenience layer, not a different consensus authority. Treat verified explorer source code as code evidence, not a security audit.
3. **Venue eligibility is dynamic.** An accessible connector must be callable in this session; its supported chain, venue, market, metric, history, pagination, terms and timestamp freshness must also be qualified. A tool listed in the environment is a *candidate*, not proof of usable records.
4. **Separate three analytical layers:** (a) chain-native observations; (b) derived entity/contract/flow interpretations; (c) off-chain venue, derivatives and market observations. Never silently replace one with another.
5. **As-of integrity matters.** Record event time, chain observation/finality time, provider publish time, retrieval time and revision time. A backfilled historical address label or contract decoder is not automatically knowable at historical decision time.
6. **Disclose uncertainty and abstain.** Unknown entity, unavailable archive state, ambiguous bridging, cross-chain duplicates, opaque custodial internals or unresolved reorganization are valid outcomes.
7. **Read-only by default.** No signatures, approvals, swaps, token transfers, custody operations, webhooks, alerts or orders without a separate explicit authorization. For methodology research, do not need write operations at all.

### Evidence status vocabulary

Use `VERIFIED_ON_CHAIN`, `CORROBORATED`, `DERIVED`, `PROVISIONAL`, `CONFLICTED`, `STALE`, `UNAVAILABLE`, and `UNVERIFIABLE`. These are proposed internal classifications, not normative labels provided by any protocol. For reporting into the seven-state framework of Document 06, map `VERIFIED_ON_CHAIN` to `VERIFIED`, `DERIVED`/`PROVISIONAL` to `PROVISIONAL` unless independently corroborated, and `UNVERIFIABLE` to `UNVERIFIED`. **Do not** claim `VERIFIED_ON_CHAIN` for an entity label or economic explanation merely because its underlying transactions are canonical.

## 1. Research questions, claims and measurement units

Every investigation starts with a claim register:

| Field | Requirement |
|---|---|
| Question / claim ID | One testable assertion, with explicit null or alternative explanation |
| Asset and identity | Chain/network, native coin or token contract/mint, token version, wrapped/bridged distinction, decimals and issuer if applicable |
| Unit of analysis | Transaction, output, address, wallet cluster, entity, contract, pool, bridge message, block, chain-day or protocol-day |
| Universe | Exact chain(s), finalized height range, asset/protocol/venue filters, inclusion/exclusion and survivorship treatment |
| Outcome and estimator | Operational definition, numerator, denominator, unit, horizon and expected direction |
| Information cutoff | Decision timestamp plus as-of knowledge rule and chain-finality standard |
| Baseline | Naïve activity, fee, asset, peer and market benchmarks; alternate methodology |
| Confounders | Price, volatility, fee regime, incentives, seasonality, bot activity, bridge/custody changes and chain outages |
| Validation | Reconciliations, independent observation paths, labeled uncertainty and falsification tests |
| Operational decision | Report / conditional monitor / no conclusion / reject claim; not an automatic order instruction |

Specify whether an analysis is **descriptive**, **predictive**, **causal**, **risk surveillance** or **forensic attribution**. Each has different evidence requirements. Use exploratory findings to frame subsequent, independently tested hypotheses rather than promoting inspected patterns into confirmed alpha.

### Canonical analytical objects

- **Chain**: protocol/network identity, chain ID when applicable, genesis/network context, fork and rollup/L2 settlement relationship.
- **Asset**: `(chain_id, contract_address_or_native_id, token_standard, deployment_version)` plus symbolic aliases; symbol alone is not an identifier. For UTXO assets, use a network and native-asset key; DTI if independently established.
- **Transaction**: `(chain_id, transaction_hash)` together with block hash/height, transaction index, execution status, value, fees, sender and chain-specific context.
- **Event/log**: `(chain_id, block_hash, transaction_hash, log_index)` or chain-appropriate event index; store contract address, topics, encoded data, ABI/decoder version and removed/reorg status.
- **UTXO**: `(chain_id, transaction_id, output_index)` with creation and spending linkage.
- **Token transfer**: a decoder-produced interpretation of an event or state delta; mark mint, burn, ordinary movement, internal account adjustment and rebasing distinctly.
- **Economic exposure**: asset-denominated beneficial claim or liability; may differ from token balances due to collateral, lending, vault shares or rehypothecation.
- **Entity label**: `entity_id, labeled_addresses, label_type, evidence, confidence, valid_from, known_from, revision`—a hypothesis unless authenticated first-party evidence establishes control.

## 2. Connected-tool and venue capability architecture

**Point-in-time inventory checked 2026-10-22.** Tool registration and a metadata response were checked for 0xArchive. Other rows reflect exposed callable tool descriptions; **not every endpoint or supported chain was live-tested**. Refresh before every major study.

| Tool family | Useful on-chain or adjacent surface | Major limitation / routing rule |
|---|---|---|
| **Blockscout Blockchain Data** | EVM-chain discovery; blocks, transaction details, address transaction and token transfer histories; token balances; ABI, verified code, contract reads | Chain-specific, indexed, potentially partial; chain discovery requires a valid session authorization handshake; explorer labels are not owner attestations. Check chain and pagination per query. |
| **0xArchive** | Venue-specific Hyperliquid core, HIP-3, HIP-4, spot, Lighter, RH-Lighter market records; selected wallet/account positions, position changes, wallet classifications, transfers and market aggregation where listed | **Market archive ≠ general-purpose canonical chain indexer.** Histories, wallet classifications and exposure are provider observations. Check exact `get_capabilities`, `get_data_coverage`, `get_symbol_coverage`, `get_data_quality_status` and incidents. |
| **CoinGecko MCP** | Searchable asset identifiers, pricing, market data, relevant on-chain/DEX endpoints when found through `search_docs` | Entitlements and plan limits must be verified by specific method call. Aggregator identity is not proof of token authenticity. |
| **CoinPaprika Keyless Latest** | Asset metadata, tickers and market context as cross-checks | Mostly market aggregation, not first-party address/transaction provenance; avoid claiming wallet coverage. |
| **CoinMarketCap Public MCP** | Token discovery and metric/quote context; optional classification | Market aggregator; do not present as independent chain receipt evidence. |
| **Massive** | Crypto market pricing/aggregate comparators through supported API endpoints | Data availability and product scope depend on resolved endpoint and access; not proof of on-chain custody. |
| **fin-data crypto tools** | OKX spot/swap instruments, recent trades, candles, order book, funding and OI when supported | Exchange microstructure; not chain-native transfers or wallet-ownership proof. |
| **Co-Invest/Liquid** | Hyperliquid-linked market/positioning and authenticated account context | Proprietary cohort and trader analytics; methodology/coverage may be opaque. Distinguish simulated vs live account data and no implied authority to execute. |
| **Other discovered providers** | May include on-chain analytics, chain-specific RPC or event indexers if actually installed and callable | Do not assume past mentions of Dune, Helius, Alchemy, DexPaprika, CCXT, Bitquery, Blockscout PRO, etc. mean those connectors are mounted in this session. Re-discover and test. |

**0xArchive verified metadata observation:** `get_capabilities` reports the separate venue keys `hyperliquid`, `hip3`, `hip4`, `spot`, `lighter`, and `rh-lighter`, with datatype-specific read routes, first-served timestamps, live/replay flags, page limits and accepted intervals. The coverage endpoint reports archive-level counts and ranges. These are **provider-declared**, not independently audited completeness. For core Hyperliquid it declared trades served from 2023-04-15, and L4 checkpoint/diff order-book reconstruction beginning around 2026-03-11. Lighter L3 and Hyperliquid spot L4 differ in their coverage. Never generalize an exchange-wide start date to every symbol or to entire historical depth. A coverage response may contain different earliest *stored* versus earliest *served* dates; use the stricter endpoint policy and test actual pages.

**0xArchive usage ladder:** `get_capabilities` → `get_exchange_coverage` / `get_data_coverage` → `get_symbol_coverage` → `get_data_quality_status` / `get_data_incidents` → specific `get_*` read call → pagination/fullness audit → independent venue or canonical-chain check where possible. For chain-custody hypotheses, prefer blockchain indexers/RPC over L2/L4 order books, aggregated trader PnL or venue wallet classification. A fill and an account position are not equivalent to an on-chain deposit or withdrawal.

**Qualification record (required):** `tool_name`, `tool_version_or_description_snapshot`, `provider`, `native_vs_derived`, `chain`, `venue`, `instrument`, `dataset`, `requested_window`, `served_window`, `earliest/latest`, `cadence`, `max_page`, `cursor_behavior`, `record_count`, `freshness`, `completeness_evidence`, `error_mode`, `license`, `query_hash`, `timestamp_utc`, `outcome`. If a field cannot be observed, write `UNKNOWN`; do not infer `COMPLETE` from a success response.

A venue enters research scope **only** for the verified instrument and metric at the requested horizon. A HIP-3 token referencing an equity or index, or noncrypto prediction-market outcome, is outside the core asset universe (it may be included only as an explicitly labeled external explanatory variable).

## 3. Collection protocol and chain finality

### 3.1 Collection order

1. Resolve token/market identity without trusting a ticker; enumerate token redeployments, proxies, wrappers, forks, L2 representations and pool variants.
2. Resolve chain and indexer capability. For EVM via Blockscout, acquire any session prerequisite before chain discovery/chain-specific queries; select the verified chain ID instead of guessing.
3. Identify exact finalized, safe/confirmed or latest chain state as separately named categories. Record finality policy, consensus type, height, hash and retrieval time.
4. Capture raw block/transaction/receipt/log/trace or UTXO observations; request full cursor sequences. Capture errors and truncations.
5. Cross-check indexer data against chain-native reads or a second independent node/indexer for a **risk-weighted sample**; use all records if practicable for decision-critical large flows.
6. Decode protocol events with ABI/code versions effective at the event height; recompute arithmetic and supply invariants.
7. Create an append-only event table and an independently derived labeled metric table with explicit `known_at` and versioned transforms.
8. Publish coverage gaps, reversions, conflicts and the minimum qualifying observation time alongside every result.

### 3.2 Finality is protocol-specific

- **Bitcoin/PoW:** confirmation depth confers probabilistic—not absolute—finality. Record depth and choose the acceptance threshold based on exposure, reorg observations and study purpose. A constant six-confirmation rule is a conventional practice, not a universal mathematical guarantee.
- **Ethereum PoS:** differentiate `latest`, `safe` and `finalized` tags and record consensus checkpoint/fork context; Ethereum documentation describes economic finality rather than an arbitrary confirmation count. Verify which tag a given RPC/indexer actually used.
- **Rollups/L2s:** distinguish sequencer inclusion, L2 protocol finality, data availability, parent-chain settlement and any fraud/challenge or validity-proof state. Do not treat a fast sequencer confirmation as identical to irrevocable L1 settlement.
- **Solana and other chains:** use native commitment/finality semantics and account for failed or reverted instructions, inner instructions and address-table resolution as relevant. EVM log heuristics cannot be transplanted unchanged.
- **Bridges:** the source lock/burn and destination mint/release are separate observations with possibly different finality. Chain reorgs, proof delays, relayer failure and manual recovery can leave a message pending.

Maintain `(observed_block_hash, canonical_block_hash_at_check, removed, reorg_depth, finality_status, last_checked)`; reorg correction must **append**, not silently overwrite. Results based on unfinalized records should be labeled provisional.

### 3.3 Time and as-of admissibility

Retain at minimum `block_time`, `observed_at`, `finalized_at_or_unknown`, `provider_published_at_or_unknown`, `retrieved_at`, `label_known_at`, `transform_created_at`, `revision_at`. Block timestamps may not equal wall-clock inclusion times. `first_available_for_decision` must reflect the **latest relevant availability constraint** (including finality, indexing, labeling and ingestion). For a historical backtest, a label added in 2026 cannot support an alleged 2024 ex-ante whale predictor unless the 2024 label state is verifiably reconstructed. The provenance rules of Document 06 govern immutable raw artifacts and bitemporal revisions.

## 4. Address labeling, clustering and counterparty inference

### 4.1 Evidence tiers

| Tier | Example | Permissible statement |
|---|---|---|
| A: Direct attestation | Cryptographically signed control claim, documented first-party verified deployment, authenticated exchange disclosure | Specific documented control, subject to scope and date |
| B: Strong corroboration | Consistent authenticated contract role plus independent institutional disclosure | Probable role/control with supporting records |
| C: Heuristic | Co-spend, common funding, interaction timing, change-output detection, gas sponsorship, transaction graphs | Hypothesized association, error-prone |
| D: Vendor/community label | Explorer tag, dashboard label, analyst-provided cluster | Attributed label of that provider, not verified identity |
| E: Unknown | No credible corroboration | `UNKNOWN`—exclude from named-entity conclusions |

Explicitly distinguish **key control**, **service usage**, **custodial beneficiary**, **smart-contract role**, **economic ownership**, and **human identity**. A deposit address administered by an exchange, an omnibus hot wallet, a smart contract called by many users and a whale-controlled wallet are categorically different objects.

Bitcoin multi-input clustering can be false under CoinJoin/PayJoin or collaborative spend designs; change heuristics misclassify wallets and scripts. Account-based chains present entirely different failure modes: relayers, smart contract accounts, multisigs, account abstraction, delegatecalls, routers, bridges and gas sponsorship. Do not automatically treat shared funders or identical trade timing as common ownership. A 2026 evaluation of the multi-input heuristic found that full-cluster precision and recall could be much lower than results restricted to disclosed service addresses, demonstrating why clusters should remain probabilistic [R3].

**Clustering quality audit:** report labeled ground-truth source/coverage, pairwise precision and recall, entity-weighted measures, false merges, false splits, leakage across train/test, stability across periods and chains, and uncertainty in aggregates induced by ambiguous membership. At minimum provide a sensitivity analysis with conservative/high-confidence-only labels versus wider clusters. Never silently apply a new clustering algorithm to old backtests.

**Privacy and safety:** analyze public activity only for legitimate research objectives; do not assert criminality from heuristics, de-anonymize private persons, publish sensitive off-chain personal data, or operationalize an uncertain identity label as if proven. Restrict storage of personally identifiable labels and provide review/correction paths.

## 5. Fund flow accounting: from token movements to economic exposures

### 5.1 Gross flows are not net capital

Define token-level gross inflow and outflow across a **documented entity boundary** `B` for period `t`:

`inflow_B,t = Σ amount(asset) for finalized transfers with source ∉ B and destination ∈ B`  
`outflow_B,t = Σ amount(asset) for finalized transfers with source ∈ B and destination ∉ B`  
`netflow_B,t = inflow_B,t − outflow_B,t`

For UTXO protocols, calculate economic outputs net of change with confidence intervals where ownership is uncertain. For EVM, de-duplicate overlapping traces, ERC-20 `Transfer` logs and event abstractions; neither logging alone nor native transaction value is a complete balance reconciliation for every token. **Internal movements** between addresses in `B` must not create boundary inflows. Clearly separate token quantities, native chain fees and USD valuations.

Net balance identity (nonrebase, no hidden state changes):

`closing_balance − opening_balance = external_inflows − external_outflows + minted − burned + protocol_accounting_adjustments`.

Adjust explicitly for rebases, yield-bearing vault share exchange rates, fee-on-transfer tokens, blacklisting, confiscation, proxy upgrade changes, token migrations, forks, slashing, lending collateral and bridge liabilities. If balance identity fails, do not publish a reliable netflow metric.

### 5.2 Exchange and custody flows

A transfer to a labeled exchange deposit address is **not** a confirmed market sell; it can represent custody, collateral, market making, internal recycling or an unreconciled bridge movement. A transfer out is not necessarily customer accumulation. Label metrics as `gross_transfers_to_labeled_exchange_addresses` or `net_boundary_flow`, **not** automatic spot buy/sell volume. Maintain hot/cold/omnibus/multisig mappings with versioned coverage and explicit unknown address share.

For any asserted supply held by exchanges, report estimated address coverage, proof/source, liability-side observability and whether addresses are shared across services. On-chain reserve holdings alone cannot establish complete solvency without liabilities, encumbrances and audit scope.

### 5.3 Bridges and wrappers

Build a bridge-message ledger with source chain, destination chain, bridge protocol/version, source lock/burn, destination release/mint, message ID, transaction/receipt proofs, pending/delayed/failed status, fees, finality and decimal conversion. Deduplicate paired source/destination events when measuring economic cross-chain capital movement. Token supply across wrapped representations must not be double-counted as original economic supply. Investigate unmatched bridge obligations and contract upgrade/admin privileges.

For issuer-backed stablecoins, separate issuer mint/redemption, circulating ledger tokens, custodial reserves, bridge-wrapped claims and pool-held balances. A redemption event is not a bank reserve verification; reserve attestations have separate dates and methodological limitations.

## 6. Token supply, ownership and concentration

Compute separately:

- `total_supply_on_chain` via canonical token state as of height (or native protocol issuance state).
- `free_float_estimate` under a declared inclusion definition; not interchangeable with supply reported by aggregators.
- `effective_circulating_supply` excluding contract-locked, vesting, treasury, lost/unspendable, custodied and wrapped representations **only when definitions and evidence justify** each exclusion.
- `mint_rate`, `burn_rate`, `emissions`, `unlock_schedule`, `staking_rate`, `liquid_stake_exposure` and `net_new_liquid_supply`, with units and source of lock/unlock assumptions.
- Concentration measured by address and, separately, by **high-confidence entity**; exclude or stratify exchanges, bridges, vaults, burn addresses and pool contracts as appropriate.

For entity distribution shares `s_i`, report `HHI = Σ s_i²` and top-k share, but do not equate one contract address with one ultimate owner. Address concentration is mechanically distorted by staking pools, bridge custody, exchange omnibus wallets and protocol treasuries. Document denominator (issued, circulating, free float), unlabeled fraction, uncertainty intervals and observed evolution rather than a single marketing figure.

Token control/security checklist: owner/minter/burner/upgrader roles; proxy implementations and admin keys; transfer restrictions and allowlists; fee/tax switches; pausable/freeze/seize functions; timelock and governance execution delay; emergency powers; concentrated vesting; mint authority; supply rebase; external call and oracle dependencies. Source-code verification is a prerequisite for some controls but **not** a substitute for testing actual runtime bytecode, inherited roles, upgrade paths, delegatecalls or externally controlled dependencies.

## 7. DeFi accounting and protocol state

### 7.1 Protocol activity matrix

| Domain | Primary observations | Necessary interpretation/control |
|---|---|---|
| AMMs/DEX | Swap events, liquidity mint/burn, reserves, fee-growth state, router paths | Identify multi-hop swaps, aggregator reuse, MEV, wash-trading candidates, pool migrations and token-specific transfer fees |
| Lending | Supply/borrow/repay/liquidation, scaled balances, indexes, oracle collateral prices | Distinguish gross deposits from outstanding deposits, debt from utilization, recursive leverage and rehypothecation |
| Staking/restaking | Validator/delegation state, deposits, withdrawals, slash events, receipt tokens | Separate underlying capital from liquid staking derivative claims; monitor exit queues and correlated slash risk |
| Stablecoins | Mint/burn/redemption, pool liquidity, peg deviations, collateral and reserve attestation | Differentiate on-chain supply from issuer claims, redemption access and reserve quality |
| Governance | Proposal, vote snapshot, quorum, execution, timelock, admin changes | Weight voting power, delegation concentration, veto controls and executed—rather than merely proposed—changes |
| Bridges | Escrow/burn/mint/release, relayer messages, challenge windows | Match economic claim across chains and detect stranded or duplicated representation |
| Liquidations | Health factor, liquidation receipt, collateral seized, auction proceeds | Distinguish on-chain DeFi liquidation from exchange-reported derivative forced trades |

### 7.2 TVL and economic usage

**TVL is a conditional accounting measurement, not an unambiguous measure of unique value creation.** Define `TVL_protocol = Σ units_of_eligible_claims × reference_price`, under a published eligible-claim registry; exclude or separately report recursive deposits, nested vaults, synthetic claims, LP tokens and bridged wrappers to avoid double-counting. Publish both gross TVL and estimated unique external collateral, with wide uncertainty where liabilities and beneficial ownership are hidden.

Volume, users and fees also require semantic care:

- **Active address ≠ unique person**; sybils, bots, AA smart wallets and relayers distort counts.
- **Transaction count ≠ meaningful adoption**; incentives, batching and bots change transaction technology.
- **DEX trading volume ≠ authentic economic turnover**; wash/self-trading and circular routing require detection controls.
- **Protocol fee revenue ≠ token-holder cash flow**; allocate fees to validators, LPs, keepers, treasury, token burn and holders according to actual mechanism and governance state.
- **Rewards emissions ≠ sustainable yield**; separate external fee revenue from inflationary incentives and valuation gains.

Avoid claiming that any one on-chain adoption metric causally predicts returns without an independently specified design and holdout.

## 8. MEV, manipulative trading and suspicious flow classification

Build transaction-level bundles or adjacency analyses to identify **candidate** sandwich attacks, backruns, JIT liquidity, circular swaps and repeated in-group trading. Document contract/router calls, event order, pool state before/after and profit after gas, priority fees, bribes and inventory mark-to-market. Distinguish legitimate arbitrage and market making from abusive activity; algorithmic flags are neither court findings nor proof of ownership.

**Suggested diagnostic features:** near-symmetric buy/sell cycles, rapid round trips with little net position change, repeated synchronized wallets, fee-adjusted negative profits, concentration of reciprocal counterparties, abnormal volume relative to unique external liquidity, low long-run inventory risk, correlated deployer/LP/market maker control and reactions around campaigns or listing events. Stress test innocent explanations: inventory recycling, arbitrage, aggregators, routing quirks and legitimate LP rebalancing.

Use graph-based wash-trading detection as a **screen**. A 2025 working paper proposes a network method detecting relatively closed counterparty clusters; a September 2026 peer-reviewed study reports wash-trading-related patterns and determinants on major cryptoexchanges. Neither authorizes a universal DEX fraud threshold or supports labeling a specific pool without its underlying records [R4, R5].

**Market impact / MEV distinction:** an observed transfer may be followed by price change because of broader information or simultaneous activity. For suspected causal effects, use event windows with matched controls, pretrends, congestion/gas controls, liquidity stratification and placebo event times; report endogenous transaction timing and inference limitations.

## 9. On-chain intelligence features and falsifiable hypotheses

Feature families may include:

| Family | Example feature | Principal leakage / confounding risk |
|---|---|---|
| Holder activity | New funded wallets, retention cohorts, realized dormant-spend volume | Wallet churn, sybils, exchange sweeping, vendor future labels |
| Exchange-boundary flow | High-confidence net token flow into labeled exchanges / free float | Incomplete labels, custody reclassification, unsold deposits |
| Supply pressure | Scheduled unlocks, liquid treasury transfers, mint/burn and net newly liquid tokens | Announcements priced in, insider allocation unknown, inaccurate vesting schedule |
| Stablecoin liquidity | Verifiable mint/redemption and bridge-net stablecoin changes | Cross-chain duplication and issuer reserve interpretation |
| DeFi stress | Borrow utilization, collateralization, liquidations, oracle deviation, redemption queues | Recursive positions, stale or manipulated oracles |
| On-chain liquidity | Pool depth at defined slippage, reserves, concentration, LP withdrawal rate | JIT liquidity, MEV, concentrated liquidity price ranges |
| Contract control | Privileged-role changes, implementation upgrades, admin transfers | Decoder/ABI version drift, unobserved timelock execution |
| Token distribution | Entity-stratified top-k, Gini/HHI and treasury supply | Custodial false aggregation and unknown beneficiary share |
| Economic traction | Net protocol fees from external users, repeat usage cohorts | Incentives, wash volume, internal subsidy accounting |

Every feature requires: formal equation, release latency, observability boundary, time-aware normalization, missingness code, outlier policy, calibration set, admissible use and minimally one adversarial falsification test. Avoid arbitrary z-score windows chosen after inspecting returns. Recompute results using high-confidence-only versus broad labels, different finality choices, native units versus dollar conversion and aggregate versus per-chain reporting.

**No free causal inference:** correlation between exchange inflows and future returns is a predictive association at best. Market-wide news, price impact, market maker rebalancing and token-specific events can create common causes or reverse causation. Only call an effect causal with defensible identification assumptions, counterfactual design and sensitivity analysis.

## 10. Statistical validation and backtesting interface

Follow Document 03 for preregistration, factor specification, controls, multiplicity and robustness; Document 04 for temporal cross-validation, train/test separation, fees, slippage, market impact and portfolio simulation. On-chain additions:

1. Use **block-time / known-time as-of joins**, not a retrospective perfect-labeled panel.
2. Make the sample universe survivorship-aware, including failed tokens, migrated contracts, hacked protocols, delistings and chains whose data disappeared.
3. Partition observations by token, entity, chain, venue, deployment vintage and regime; cluster/heteroskedasticity-robust inference must fit actual dependency structure. Cross-sectional token-day rows are rarely independent.
4. Account for highly persistent, overlapping horizons, zero-inflated events and heavy-tailed flow sizes; compare robust methods and preregister treatment of price spikes.
5. Run placebo assets, randomly permuted event times, lag/lead tests, ex-ante label-free benchmarks and sensitivity to threshold/feature selection.
6. Audit prior analyst inspection and candidate mining; quantify multiple testing and avoid claiming a universal `t > 3` pass rule.
7. Report net economic value after chain gas, bridge fees, DEX price impact, adverse selection, funding, liquidation and any exchange execution costs—not merely gross price movement.
8. **Separate the research signal from tradable venue access**. On-chain market evidence does not imply a Liquid, Hyperliquid or other connector permits executing the intended instrument.

For predictive features, preserve `feature_event_time`, `feature_known_at`, `feature_computed_at`, `prediction_time`, `earliest_executable_time`, and realized-label horizon. Reject any example where feature availability is after prediction or execution decision time.

## 11. Security, oracle and failure-mode surveillance

Screen protocol-specific exposures to contract upgradeability, oracle manipulation, price feed delay, sequencer outages, bridge validator compromises, multisig concentration, governance takeover, liquidation feedback loops, validator censorship, consensus reorgs, contract pause/freeze powers and asset redemption risk. Distinguish **observed state** (e.g., actual admin, timelock delay) from **hypothetical exploitability** (which requires separate security analysis).

**Risk scenarios** (proposed, not empirical laws):

- **Bridge halt:** destination claims outstanding while source escrow persists; estimate redemption queue, secondary-market haircut and delayed settlement.
- **Stablecoin depeg:** simulate collateral and borrow health under nonlinear oracle/lending responses; avoid assuming continuous liquidity.
- **Admin compromise:** quantify maximum mint/freezable balance under current permissions; document whether actions require quorum, delay or multiple signatures.
- **Protocol upgrade:** recalculate ABI/state semantics by historical implementation; flag incompatible event interpretation.
- **DEX liquidity withdrawal:** recompute executable exit with reserve/CL position changes and MEV uncertainty.
- **Chain congestion/reorg:** widen data and settlement delays; suspend event-dependent decisions if the finality predicate fails.

Escalate to Documents 01/05 for derivatives liquidation, concentration, scenario loss and portfolio limits. Do not introduce independent risk limits without reconciliation to Document 05.

## 12. Confidence, coverage and abstention rules

Report separately:

- **Canonicality:** accepted fork, finality state and height/hash evidence.
- **Completeness:** sampled versus complete, first/last, cursor exhaustion, chain/contract coverage, excluded events and missing fraction.
- **Identity quality:** provenance, confidence and unknown fraction of labeled address/flow coverage.
- **Metric validity:** units, contract ABI/version, replay/reconciliation and material assumptions.
- **Timeliness:** observation, publication, retrieval and revision clocks.
- **Economic interpretation:** transfer versus sale, contract balance versus beneficial holding, TVL versus capital and attribution certainty.
- **Independence:** truly independent RPC observations versus two dashboards querying the same upstream indexer.

**Hard abstentions (proposed internal governance controls):** unresolved token identity; no usable canonicality evidence for decision-critical flows; unsupported chain/metric; irreconcilable balance arithmetic; absent history for historical claim; materially incomplete pagination; off-chain market aggregate substituted as on-chain record; entity identification not supported by confidence evidence; future labels in historical features; provider-unresolved conflicting data; rights/terms prohibit needed processing. `UNKNOWN` and conditional conclusions are acceptable outputs.

Numeric tolerances, minimum coverage, staleness limits, address-label confidence and reconciliation error budgets must be **study-specific and prespecified** by accountable reviewer; do not import arbitrary percentages from an unrelated chain, protocol or strategy. Exceptions must preserve uncertainty in the final output.

## 13. Operational workflow and gates

| Gate | Required evidence | Failure disposition |
|---|---|---|
| G0 — Scope | Digital-currency identity, chain/venue/metric and research question | Out of scope or clarify asset mapping |
| G1 — Capability | Callable route, chain/market, actual history/pagination and permissions | `UNAVAILABLE`—do not synthesize imaginary coverage |
| G2 — Canonicality | Block/hash, finality/reorg policy or correctly identified off-chain market source | `PROVISIONAL` or abstain |
| G3 — Parsing | ABI/decoder version, decimal/unit normalization and zero silent failures | Reject affected rows |
| G4 — Reconciliation | Flow conservation, ledger balances, deduplication and independent spot checks | `CONFLICTED`; quantify unresolved gap |
| G5 — Attribution | Address/entity label evidence and known-time version | Anonymous or probabilistic only |
| G6 — PIT integrity | Publication/finality/retrieval availability ≤ historical decision time | Research-only retrospective, not backtest-admissible |
| G7 — Analysis | Hypothesis, benchmark, confounders, appropriate uncertainty | Exploratory or no conclusion |
| G8 — Publication | Raw references, versioned transform, query coverage, caveats, reviewer and no trade-action claim | Withhold conclusion until fixed |

**Minimal read-only execution sequence:**

```text
Input: research_question, token/chain, intended time window, decision horizon
Resolve native coin or exact token/contract and chain version
Discover available connected tools and relevant endpoint/entitlement
Qualify chain + metric + market/symbol + retained history + pagination
Fetch immutable raw records, block references, cursor logs and source metadata
Check canonicality/finality and append reorg corrections
Decode with versioned ABI/schema; deduplicate transfers and bridge legs
Reconcile supply/flows/positions; compare genuinely independent records
Apply time-versioned entity labels with UNKNOWN state preserved
Construct study-specific features and sensitivity bands
Apply as-of and statistical tests; invoke companion methods where applicable
Publish claim register, results, sources, coverage, conflicts, confidence, limitations
Never initiate transactional operations as part of this workflow
```

## 14. Required reproducible evidence artifacts

One completed study should export or document the following logical artifacts (formats may be Markdown, CSV/Parquet, SQL, JSON and/or immutable stored payloads):

1. **Scope manifest:** asset/chain/deployment identifiers, protocol/venue inclusion, question/hypotheses, time window and exclusion logic.
2. **Connector capability manifest:** tool/endpoint names, access outcome, rate/pagination/retention, requested versus returned boundaries, terms and query time.
3. **Raw acquisition ledger:** request hashes, parameters and cursors, response hashes, UTC retrieval, provider response, retries, errors and any gaps.
4. **Canonical state table:** chain ID, block hash/height, finalized/safe/latest status, reorg revision and chain-specific proof notes.
5. **Decoded events ledger:** transaction/event IDs, implementation/ABI/decoder versions, raw-to-decoded value and unit transforms.
6. **Entity-label register:** assertion, evidence tier, validity dates, knowledge dates, confidence and conflict/unknown status.
7. **Reconciliation report:** supply/transfer/contract state identities, fee and bridge adjustments, difference analysis.
8. **Feature and analysis register:** equations, feature lags, samples, benchmarks, sensitivity, multiple-testing and leakage checks.
9. **Claim-to-evidence matrix:** every published numerical or identity assertion mapped to reproducible observations, transformations and admissibility.
10. **Publication record:** reviewer, limitations, future invalidation triggers, data-revision notice and reproduction instructions.

### Suggested compact claim-to-evidence schema

```yaml
claim_id: chainflow-001
asset:
  chain: <resolved network>
  contract_or_native_asset: <immutable identity>
metric: <explicit definition and units>
window_utc: [<start>, <end>]
consensus_state: <finalized/safe/probabilistic/unknown>
source:
  primary: <specific connected tool, endpoint, query hash>
  independent_check: <separately qualified source or null>
coverage:
  expected: <number or unknown>
  observed: <number>
  pagination_complete: <true/false/unknown>
  gaps: <description>
time:
  last_event_at: <timestamp>
  known_at: <timestamp or unknown>
  retrieved_at: <timestamp>
  revised_at: <timestamp or null>
entity_attribution:
  tier: <A/B/C/D/E>
  known_at: <timestamp or null>
transformation_version: <git hash or immutable version>
uncertainty: <confidence interval / bounded scenario / nonquantifiable>
interpretation: <observed / derived / speculative>
status: <VERIFIED_ON_CHAIN/CORROBORATED/DERIVED/PROVISIONAL/CONFLICTED/STALE/UNAVAILABLE/UNVERIFIABLE>
```

The template is illustrative. Do not literally publish angle-bracket placeholders as observations.

## 15. Escalation and falsification casebooks

**Case A — “Whales deposited $20m to exchanges.”** Require explicit entity boundary, token price timestamp, share of labeled exchange addresses, removal of internal custody transfers, bridges and duplicate event decoding. Report best-supported deposit **transfers**, not assumed sales. Falsify by checking subsequent flow recycling and venue fill/price data independently.

**Case B — “A protocol’s TVL doubled, therefore adoption doubled.”** Reconcile price appreciation, incentive emissions, recursive borrowing, LP receipt-token duplicates, bridges, token supply rebase and unique external collateral; report address cohorts and fee-paying external usage separately. Reject causal phrasing absent a design.

**Case C — “One wallet controls 35% of supply.”** Check if the wallet is a CEX omnibus account, burn address, staking contract, bridge escrow, multisig, vault, treasury or router. Report address-level concentration and separately identified beneficial entities; preserve unknown ownership.

**Case D — “Hyperliquid order-book behavior proves wallet outflow.”** It does not. 0xArchive trade/book/account position series can measure venue-market behavior and reported positions. A verified transfer requires the appropriate chain/deposit-withdrawal data and settlement semantics. Treat correlations as cross-layer evidence, not equivalence.

**Case E — “New address clustering improves predictive backtest.”** Run historical known-time labels (not current backfills), full-cluster ground-truth precision/recall, alternative heuristics and label-free benchmarks. If no historical label archive exists, classify the exercise as retrospective exploratory—not implementable out-of-sample evidence.

**Case F — “A bridge minted tokens before backing arrived.”** Align source and destination clocks, finality, proof/messaging latency, relayer retries and burn/mint pairing. Distinguish temporary pending bridge messages from economic undercollateralization and document unmatched liabilities.

## 16. Research basis, evidence grades and bibliography

The sources below establish **methods, limitations or protocol semantics**, not universal trading predictability. Peer-reviewed evidence is distinguished from preprints/working papers and operator documentation. On-chain network and vendor capabilities can change; requalify at execution time.

**[R1 — Official protocol documentation]** Ethereum Foundation / ethereum.org, *Proof-of-stake (PoS)* and *Frequently Asked Questions*; describes checkpoint justification and economic finality. https://ethereum.org/developers/docs/consensus-mechanisms/pos/ and https://ethereum.org/developers/docs/consensus-mechanisms/pos/faqs/

**[R2 — Official protocol engineering]** Ethereum Foundation, *How The Merge Impacts Ethereum’s Application Layer* (2021); distinguishes `safe`, `finalized` and head block concepts, subject to changes in client interfaces. https://blog.ethereum.org/2021/11/29/how-the-merge-impacts-app-layer

**[R3 — Provisional preprint, July 2026]** Müller, Elsner, Niedermayer, Haslhofer, Goger, Kühl & Rückert, *How Reliable Is the Multi-Input Heuristic for Bitcoin Address Clustering in Law Enforcement Contexts?* Reports full-cluster precision/recall of approximately 0.36/0.44 in its evaluation; **not** a portable performance estimate for other cohorts/chains. https://arxiv.org/abs/2607.07414

**[R4 — Academic working paper]** Sirolly, Ma, Kanoria & Sethi, *Network-Based Detection of Wash Trading*, Columbia Business School (2025). Applies network analysis to detection and documents false-inference challenges. https://business.columbia.edu/faculty/research/network-based-detection-wash-trading

**[R5 — Peer-reviewed, September 2026]** Sila, Kocenda, Kristoufek & Kukacka, *Determinants of wash trading in major cryptoexchanges*, *International Review of Financial Analysis*, vol. 117, article 105283 (2026). DOI: https://doi.org/10.1016/j.irfa.2026.105283 . Its exchange sample and proxies do not prove manipulation in any specific DEX pool.

**[R6 — Preprint, March 2024]** Schnoering, Porthaux & Vazirgiannis, *Assessing the Efficacy of Heuristic-Based Address Clustering for Bitcoin*. Examines clustering heuristics and time-varying clustering ratios. https://arxiv.org/abs/2403.00523

**[R7 — Provisional preprint, September 2026]** Schnoering, Bresson & Vazirgiannis, *Refining Heuristic-Based Bitcoin Address Clustering with Graph Neural Networks*. Motivates identifying suspicious heuristic cluster merges; validation/generalization remains a live question. https://arxiv.org/abs/2609.01942

**[R8 — Industry empirical surveillance; non-independent commercial analysis]** Solidus Labs, *Understanding Wash Trading in Crypto* (report series; 2025 webpage). Useful for adversarial hypotheses, not as a universal prevalence parameter or audit of every blockchain. https://www.soliduslabs.com/reports/crypto-wash-trading

**[R9 — Standards for evidence management]** W3C, *PROV-O* / *PROV-DM* (2013), https://www.w3.org/TR/prov-o/ ; Wilkinson et al. (2016), *The FAIR Guiding Principles for scientific data management and stewardship*, *Scientific Data*, DOI https://doi.org/10.1038/sdata.2016.18 . Apply Document 06 for detailed provenance governance.

**[R10 — General empirical-statistical framework]** Harvey, Liu & Zhu (2016), *... and the Cross-Section of Expected Returns*, *Review of Financial Studies*, https://doi.org/10.1093/rfs/hhv059 ; Bailey, Borwein, López de Prado & Zhu (2014/2017), *The Probability of Backtest Overfitting*, https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2326253 . Use as motivation for multiple-testing controls and realistic OOS validation, not as crypto-specific universal numeric gates.

**[R11 — Live connected metadata, observed 2026-10-22]** 0xArchive MCP `get_capabilities({})` and `get_data_coverage({})`. Provider-reported venue and datatype schemas, retained timestamps, page limits and record counts; not independently audited on-chain evidence and not an assertion that every history request will succeed. Preserve the actual tool response in a study-specific capability manifest.

**[R12 — Tool inventory, observed 2026-10-22]** Exposed Blockscout Blockchain Data, CoinGecko, CoinPaprika Keyless Latest, CMC Public, Massive, fin-data crypto, Co-Invest/Liquid and 0xArchive tools. Blockscout `get_chains_list` could not be tested independently because this session first requires a `session_id` from `__unlock_blockchain_analysis__`. No chain-support assertion is based on that unsuccessful query.

---

## Change and review policy

A revision requires an explicit changelog, owned methodological decision, retained old mapping/decoder/label versions and an assessment of retrospective research impact. Review on chain fork, hard fork, proxy upgrade, new token standard, venue API/schema change, archive outage/incident, material clustering-ground-truth challenge, bridge exploit or new empirical methodological evidence. Avoid calendar-based claims of continued validation without actual reruns.

**Version 1.0 — 2026-10-22:** Established scope, dynamic callable-tool qualification, 0xArchive market-versus-ledger separation, EVM/UTXO and cross-chain accounting, uncertainty-preserving entity attribution, PIT/finality controls, manipulation/adoption diagnostics, statistical interface and reproducible artifact contract.
