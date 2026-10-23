# Twelve-axis control-plane audit — 2026-10-22

**Baseline:** uploaded `crypto-quant-codex-control-plane.zip`. **Scope:** offline scaffold. **Assessment vocabulary:** PASS = evidence supports local contract; PARTIAL = useful mechanism but gaps; BLOCKED = cannot confirm in this environment. **No Codex CLI binary, live MCP access, Git checkout, effective managed requirements or network enforcement was available during this audit.** No financial action was taken.

| Axis | Baseline | Finding / change | Residual verification |
|---|---|---|---|
| 1. Project identity & trust | PARTIAL | Trust onboarding text exists; added explicit distinction between desired repo state and resolved runtime trust | Verify user/workspace trust in target Codex |
| 2. Config resolution | PARTIAL | Replaced unrecognized `max_concurrent_threads_per_session` with documented `agents.max_threads`; added `max_depth = 1`; offline verifier now checks unknown keys | Run installed `codex` against trusted project and inspect effective config |
| 3. Instructions | PARTIAL | Strengthened provenance, instruction/permission separation, conflicting-methodology handling and truncation-conscious checks | Inspect actual AGENTS selection and budget |
| 4. Model policy | PARTIAL | No project model hard-pinning: avoids unsupported or inaccessible model assumptions; verifier rejects speculative model IDs | Document resolved model/effort per run |
| 5. Sandbox & permissions | PARTIAL | Retains existing conservative legacy workspace-write/network-off policy; checks no mixed permission-profile mode | User/admin policy and host sandbox may differ |
| 6. Approvals | PARTIAL | Retains `on-request`; audit highlights no approval is an enforcement substitute for explicit no-trade server restrictions | Test live approval behavior/managed requirements |
| 7. Tool capability registry | PARTIAL | Existing inventory already distinguishes chat tools from Codex and denylisted 0xArchive management; added invocation-level evidence; no unverified financial servers registered | Qualify schemas, exact allowlists and data coverage individually |
| 8. Execution environment | BLOCKED | No frozen runtime or dependencies implied; portable stdlib-only checks and manifests | Verify target OS/CLI/Python versions, credentials and network policy |
| 9. Network policy | PARTIAL | Retained `sandbox_workspace_write.network_access = false`; explicit test guards | Confirm CLI effective network state; hosted MCP access is a different surface |
| 10. Agent orchestration | PARTIAL | Five bounded roles kept; depth 1; optional validation and single-writer discipline documented | Spawn/review only if supported and authorized |
| 11. Source control | PARTIAL | Archive has no `.git`; baseline/diff discipline clarified; content manifest supports comparisons | Establish Git baseline after installation, then test dirty-state handling |
| 12. Governance & telemetry | PARTIAL | Added offline manifest with file digests and reproducibility metadata, evidence-limit statements and JSON-schema validation tests | Correlate CLI/OTel, Git and provider evidence externally if needed |

## Correctness and safety boundaries

**Fixed:** invalid agent concurrency configuration and superficial offline verifier. **Strengthened:** visible audit coverage, structural negative tests, a deterministic file-digest manifest for local inputs, no-trade and no-secret checks, schema-shape checks and invocation/snapshot evidence instructions.

**Preserved byte-for-byte:** five extensive domain methodologies and the original VVV artifact. No speculative Codex components, finance endpoints, webhooks or server registrations were introduced. The `research_manifest.py` output is a user-generated artifact; it is **not** an immutable runtime authorization snapshot, off-host audit ledger, or proof that live data was retrieved.

### Evidence & source hierarchy

- Project engineering references: `12-logical-subsystems.md`, `Engineering-Guide-Codex-Instruction-Behavioral-Policy-Plane.txt`, `Engineering-Guide-Skills-Subsystem(1).txt`, `Engineering-Guide-Codex-Tool-Capability-Registry.md`, `Codex-CLI-Agent-Orchestration.md`, `codex-cli-governance-audit-telemetry.md`, `Source-Control-Change-Management(1).md` (supplied project references).
- Codex official [config reference](https://developers.openai.com/codex/config-reference), [subagents](https://developers.openai.com/codex/subagents), [AGENTS.md guide](https://developers.openai.com/codex/guides/agents-md), [security](https://developers.openai.com/codex/agent-approvals-security), [skills](https://developers.openai.com/codex/skills). Checked web reference availability 2026-10-22; do not construe this audit as an empirical compatibility test of the installed CLI.

### Acceptance before operational adoption

1. Run `python3 scripts/verify_scaffold.py` and `python3 -m unittest discover -s tests -v` offline.
2. Check `codex --version`, effective trusted-project config, agent availability and configured MCP registration.
3. Attempt only explicitly authorized harmless metadata reads; validate allowlist and refusal of external-write tool classes via actual server/host policy, not prompt language.
4. Record source timestamps and independent comparisons before any claim of live evidence.
5. Review Git status/diff and inspect manifest before publishing any modified repository.
