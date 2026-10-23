# Agent coordination contract (project workflow, not a runtime capability)

## Roles and boundaries
Primary agent owns triage, scope, tool gating, methodology conflicts, synthesis and final verdict. Specialists assess bounded questions independently; none approves actions, validates its own thesis as independent review, owns overlapping edits, or spawns descendants. The `verifier` only attests observed checks. All repository workers here are read-only domain agents; edits, when requested, remain with the primary/single designated implementation owner.

## Dispatch
1. Primary records `task_id`, baseline Git status if available, input digest, question, venue/instrument/horizon, evidence budget, permitted tools, privacy scope and expected artifact.
2. Route by distinct concern: source-validator -> provenance/quality; derivatives-analyst -> derivative/book; factor-researcher -> hypothesis; backtest-auditor -> evaluation; risk-validator -> independent adversarial review; onchain-analyst -> chain evidence; verifier -> artifact/test evidence.
3. Parallelize independent read-only work only; start with no more than three relevant workers and `max_depth=1`. If an exposed native subagent mechanism is absent, use sequential single-agent analysis and disclose limitation. Do not assume prompts trigger automatic dispatch.
4. Wait for source and domain investigators, reconcile conflicts at a **synthesis barrier**, then assign adversarial review of the consolidated thesis with the same evidence pointers, without prejudging the answer.
5. Before final report, verifier checks only actual run outputs and schema compliance when applicable. The primary records disagreeing conclusions and abstains where evidence is inadequate.

## Handoff envelope (Markdown or JSON; normative for replies, not enforced by Codex)
```
task_id:
role:
scope:
input_refs: [source+version/hash/time]
methodologies: [path+hash where possible]
tools_checked: [canonical source/tool, arguments scope, outcome]
findings: [{claim, label, support, severity, confidence}]
contradictions: []
unknowns: []
checks: [{command_or_test, status: PASS|FAIL|NOT_RUN, evidence}]
recommended_next_test:
```
`confidence` is epistemic quality, not an expected return or likelihood of profit. No worker claims approval or runtime enforcement.

## Evidence and state transfer
Pass immutable artifact paths/hashes and concise citations through native subagent messaging; no claim of shared agent-only memory. Avoid a shared mutable scratchpad. If persistent handoff files are explicitly permitted, use non-overlapping owner-written files and register their hashes. Research manifest captures local source bytes only, not external tool executions or effective managed settings.

## Failure modes
Timeout, absent tool, stale source, uncheckable PIT clock, insufficient book sequence, invalid schema, and contradictory independent reviewers each remain visible. No majority vote resolves factual conflict. Do not paper over agent errors with a fabricated successful handoff.
