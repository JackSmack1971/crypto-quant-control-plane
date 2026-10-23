---
name: derivatives-microstructure
description: Investigate crypto perpetuals, funding, basis, order books, liquidations and spot execution costs without conflating modeled depth with actual fills.
---
# Derivatives and market microstructure
Read `methodologies/01-derivatives-methodology.md` for derivatives, `methodologies/02-spot-market-microstructure-methodology.md` for spot books, and `methodologies/09-strategy-execution-methodology.md` only for fill/execution simulation.
1. Determine venue and product, symbol/contract, collateral, multiplier, quote, tick/lot sizes and temporal granularity.
2. Distinguish order-book snapshots vs ordered deltas; check sequence continuity, dropped updates, latency and timestamps before claiming reconstructed history.
3. Distinguish settled from predicted funding, mark/index/last prices, gross/net OI and liquidation model forecasts from observed events.
4. Evaluate spread, depth, participation, maker/taker fees, adverse selection and impact at stated sizes. Refrain from claiming size is executable merely because displayed.
5. Report evidence and failure cases; do not place, cancel or amend orders.
