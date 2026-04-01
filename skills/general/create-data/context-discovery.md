# Context Discovery

> **Shared resource.** This skill uses the same discovery logic as create-ruleset. See [../create-ruleset/context-discovery.md](../create-ruleset/context-discovery.md) for the full discovery procedure.

## create-data Specific Notes

When running discovery for create-data (vs create-ruleset), the subagent should also look for:

- **Existing generated data** — `dataset/**/augmented/*/index.json` — previously generated samples for this domain
- **Gold standards** — `dataset/**/augmented/*/gold-standards/` — approved reference samples
- **Coverage reports** — `dataset/**/augmented/*/coverage-report.md` — previous gap analysis
- **Feedback files** — `dataset/**/rulesets/*_feedback.md` — post-generation feedback from prior runs (check for `acknowledged` block per [interface contract](../shared/interface-contract.md))

These additional scan targets inform Phase 0 decisions (reuse gold standards, run coverage analysis, pre-apply feedback).
