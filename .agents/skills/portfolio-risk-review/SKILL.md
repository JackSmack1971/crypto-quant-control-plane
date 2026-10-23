---
name: portfolio-risk-review
description: Challenge crypto portfolio exposures or proposed paper allocations for tail risk, concentration, liquidity, leverage and scenario robustness; personal-account reads require explicit request.
---
# Portfolio risk challenge
Read `methodologies/05-portfolio-risk-methodology.md` and relevant execution/microstructure guidance.
1. Confirm whether the question is hypothetical or explicitly authorizes account reads. Otherwise use only user-provided hypothetical positions.
2. Normalize net/gross notionals, delta, margin, funding, counterparty, bridge, collateral and concentration exposures; do not aggregate incompatible units.
3. Stress liquidity gaps, wrong-way collateral moves, correlation breaks, liquidation cascades, depegs, venues and adverse exits.
4. Compare risk budget, maximum drawdown assumptions, stop-fill feasibility and fat-tail assumptions; flag unavailable evidence.
5. Return critical vetoes and falsifiable mitigation tests without altering any account or orders.
