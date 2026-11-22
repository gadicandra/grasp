# grasp: understand what you ship

A Claude Code plugin that makes you **learn while you vibe-code**. You keep the speed of agentic coding.
grasp adds a few small, research-backed moments of friction at the points where learning actually happens.

> In a randomized trial, developers who used AI while learning a new library scored 17 points lower on a
> comprehension quiz. The ones who used AI to *ask why* kept their understanding.
> ([Anthropic, 2026](https://www.anthropic.com/research/AI-assistance-coding-skills)). grasp enforces that second pattern.

## Install

```
/plugin marketplace add gadicandra/grasp
/plugin install grasp@grasp
/grasp:init
```

Requires Python 3.10+ (stdlib only) and git. No telemetry, no network calls.

## How it works: episodes

One **episode** = one feature, bug, or task. Not weeks or sprints. Switch projects whenever you want.

| Phase | Command | What happens (≈2 min each) |
|---|---|---|
| ENTRY | `/grasp:start <title>` | Re-entry quiz if you've been away ≥3 days, then up to 3 due cards for this project's stack |
| PLAN | `/grasp:next` | You write `PLAN:` (files, data flow, risk). Claude critiques it and never rewrites it |
| BUILD | `/grasp:next` | You predict the diff before reading it. You write the `TODO(human)` core-logic parts |
| VERIFY | `/grasp:next` | You name 2 failure cases before Claude writes tests |
| CLOSE | `/grasp:done` | 3 questions (why / what-if / trace), self-score then graded, handoff note, adaptation check |

- `--rush` for deadlines: minimal friction, but what you skipped becomes **learning debt** that resurfaces in this project later.
- `!quick <prompt>` skips the plan gate for trivial changes. It's counted, not forbidden.
- `/grasp:review` drills due cards any time. `/grasp:status` shows your learner model.

## Adaptive by design

| Level | You | Claude |
|---|---|---|
| L0 Observer | answer questions | writes everything |
| L1 Co-pilot | write the plan + 1 core section (hard plan gate) | the rest |
| L2 Pilot | plan + 2 core sections, Socratic hints | boilerplate, tests |
| L3 Architect | plan, spec, first review | hints only on request |

Levels are **per domain** (auto-detected from `package.json` / `pyproject.toml`), so you can be L3 in Next.js and L0 in PyTorch.
After each episode, deterministic rules look at your last 3 episodes in that domain and may propose **one** small step.
You accept, reject, or dispute it. Changes need ≥3 episodes between them, and a rejected proposal isn't re-offered for 5 episodes.
Every decision is logged.

## Your data

| Where | What |
|---|---|
| `~/.grasp/` (git repo) | Portable knowledge: levels, concept mastery, concept cards. Survives plugin uninstall. |
| `<project>/.grasp/` | This project: episodes, handoff notes, architecture cards, learning debt. Commit it or gitignore it. |

All data is plain JSON + Markdown. Set `GRASP_HOME` to move the global journal.

## Develop

```
python3 tests/test_core.py
claude plugin validate .
claude --plugin-dir .      # try it locally
```

## Research basis

Generation effect (Slamecka & Graf 1978) · desirable difficulties (Bjork & Bjork 2011) · retrieval practice
(Roediger & Karpicke 2006) · self-explanation (Chi et al. 1994) · expertise reversal (Kalyuga et al. 2003) ·
open/negotiated learner models (Bull & Kay) · GenAI and learning (Bastani et al., PNAS 2025; Lee et al., CHI 2025).

## License

MIT
