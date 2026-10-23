# Control plane optimization — 2026-10-22

## Scope and evidence
This revision is based on the supplied `crypto-quant.zip`, the project control-plane reference guides and OpenAI's published guidance on skill modularity and subagent separation. No Git repository existed inside the archive; original files serve as baseline. No Codex CLI runtime or crypto-provider connection was exercised.

## Findings and disposition
1. **FAIL (fixed):** `scripts/verify_scaffold.py` required precisely five methodology names despite the archive containing nine. The validator now requires all nine.
2. **FRAGMENTED (improved):** one broadly triggered skill absorbed seven distinguishable workflows. Refocused as orchestration plus six domain-specific skills with disjoint goals and lazy methodology routing.
3. **FRAGMENTED (improved):** five custom agent roles lacked a shared task/handoff schema. Two roles added and a common mandatory behavioral handoff established in `docs/orchestration-contract.md`.
4. **PARTIAL (improved):** primary instruction routing excluded methodologies 02, 07, 08, 09. All nine are now referenced with domain triggers.
5. **PARTIAL (improved):** offline regression checks lacked missing-domain/skill and agent-write-negation cases. Three negative tests added.
6. **UNVERIFIED (unchanged):** effective sandbox, managed requirements, per-method MCP authorization, network enforcement, tool schema, provider connectivity, native agent dispatch, on-chain data retention and audit coverage require a live controlled environment.

## Decisions
- No financial/exchange MCP servers were added: upstream identity, auth, actual method-level read restrictions and user/runtime access are unverified.
- No order execution is supported; even paper-order modification requires a different expressly authorized environment, not a research skill.
- Keep `sandbox_mode` legacy network-off settings, without mixing with newer permission-profile semantics, pending exact CLI version and managed-policy qualification.
- Do not add custom automation or a shared mutable subagent memory service. Coordinator-mediated handoffs preserve causal ownership.
- Do not edit nine extensive research methodologies; changes here address control-plane coupling and tests.
- No historical provider data, backtests or market quotes were verified during this revision.

## Verification
`python scripts/verify_scaffold.py`: PASS, 28 manifest inputs.
`python -m unittest discover -s tests -v`: PASS, nine tests.
Not executed: `codex --version`, effective config inspection, MCP initiation, tool schema/risk checks, simulated native agent runs, empirical skill-trigger evals, market-data checks.

## Next live acceptance gates
1. In a clean, trusted Codex CLI installation inspect effective project, system, managed and user config, as well as sandbox and permissions behavior.
2. Validate skill discovery/trigger precision with positive and negative prompts. Confirm seven agents are parsed and boundaries honored.
3. Exercise two independent read-only source calls; record method args, timestamps and errors. Reject speculative permissions.
4. Rehearse a full source + domain + adversarial + verifier chain; verify task IDs, pointer-based handoffs and degraded verdicts.
5. Extend tests with schema-validating real report fixtures and track activation precision, evidence completeness, reviewer defect yield, unsupported claims and cost per validated result.
