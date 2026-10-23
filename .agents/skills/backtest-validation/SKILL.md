---
name: backtest-validation
description: Audit or design cryptocurrency backtests for chronological holdouts, PIT leakage, data snooping, fills, slippage, funding, margin and reproducibility.
---
# Backtest validation
Read `methodologies/04-backtesting-methodology.md`, `methodologies/09-strategy-execution-methodology.md` for simulation, and source provenance when needed.
1. Require immutable hypothesis/trial ledger, data vintages, asset universe, target strategy, split/embargo rules and untouched final holdout.
2. Check PIT feature release versus decision clock, survivorship, survivorship of venues, corporate/token events, and chronology.
3. Check fees, borrow/funding, spread, delay, queue/partial fills, impact, margin/liquidations, market closures or outages and volume capacity as applicable.
4. Report benchmark, sample size, uncertainty, selection correction and regime robustness. Run only available tests; unrun tests stay UNVERIFIED.
5. Audit actual commands, outputs and artifact hashes; never present a backtest plan as historical performance.
