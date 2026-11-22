# Changelog

Bump `version` in `.claude-plugin/plugin.json` with every release. Users stay pinned to the old version until you do.

## 0.1.0 (2026-11-22)

- Episode loop: `/grasp:start` (with `--rush`), `/grasp:next`, `/grasp:done`
- Hooks: session context injection, PLAN gate (hard at L1, soft at L2+), automatic card capture
- Two-layer cards (portable concepts in `~/.grasp`, project cards in `<project>/.grasp`) with Leitner spacing
- Per-domain levels L0-L3 with deterministic, negotiable adaptation proposals
- Re-entry quiz after 3+ days away; learning debt from rush episodes
- Optional `WHY:` commit-msg hook
