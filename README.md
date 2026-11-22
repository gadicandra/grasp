<h1 align="center">grasp</h1>

<p align="center">
  <em>Learn while you vibe-code. Let AI write the code, and still understand what you ship.</em>
</p>

<p align="center">
  <a href="#quick-start">Quick start</a> | <a href="#how-it-works">How it works</a> | <a href="#faq">FAQ</a> | <a href="https://github.com/gadicandra/grasp/releases">Releases</a>
</p>

<p align="center">
<a href="https://github.com/gadicandra/grasp/actions/workflows/ci.yml"><img src="https://github.com/gadicandra/grasp/actions/workflows/ci.yml/badge.svg" alt="CI" /></a>
<a href="https://github.com/gadicandra/grasp/releases"><img src="https://img.shields.io/github/v/release/gadicandra/grasp?label=release" alt="Release" /></a>
<a href="https://code.claude.com/docs/en/plugins"><img src="https://img.shields.io/badge/Claude_Code-plugin-D97757" alt="Claude Code plugin" /></a>
<img src="https://img.shields.io/badge/python-3.10%2B-blue" alt="Python 3.10+" />
<a href="LICENSE"><img src="https://img.shields.io/badge/License-MIT-green.svg" alt="MIT License" /></a>
</p>

## Overview

AI coding tools are great at writing code. The catch is that when the AI does the planning, the coding,
**and** the reviewing, you finish the project without really knowing how it works.

**grasp** is a plugin for [Claude Code](https://code.claude.com) that fixes this. Think of it as a tutor
sitting next to you and the AI. The AI still does most of the typing. grasp just makes sure you do the
**thinking** at the few moments where learning actually happens.

> [!NOTE]
> This isn't a guess. In a [2026 study by Anthropic](https://www.anthropic.com/research/AI-assistance-coding-skills),
> developers who used AI to learn a new library scored **17 points lower** on a comprehension quiz.
> The developers who used AI to *ask why* didn't lose any understanding. grasp builds that habit into your workflow.

### What it looks like

```text
> /grasp:start login form

  Welcome back. It's been 10 days since "checkout page".
  Quick question first: why did you store the cart in a cookie instead of the database?

> /grasp:next                                   ← you write your plan, the AI critiques it
> PLAN: form posts to a server action, check password, risk = leaking which emails exist

  One thing you got right: ...   One risk you missed: no rate limiting ...

> /grasp:next                                   ← the AI builds, and leaves one key part for you
  I left one TODO(human) in actions.ts. Before you open the file:
  what do you think I changed, and why?

> /grasp:done                                   ← 3 short questions, then a note for future you
  Q1 (why): ...   Q2 (what if): ...   Q3 (trace): ...
  Score 0.67. You rated yourself 0.83, so you were a little overconfident on Q3.
```

## At a glance

<table>
<tr>
<td width="50%" valign="top">
<h3>🧭 Think first, then build</h3>
You write a short plan before the AI writes code. The AI critiques your plan and never replaces it.
</td>
<td width="50%" valign="top">
<h3>✍️ You write the important part</h3>
The AI writes the boring parts (setup, styling) and leaves the core logic as <code>TODO(human)</code> for you.
</td>
</tr>
<tr>
<td width="50%" valign="top">
<h3>🃏 Automatic flashcards</h3>
Useful things you learn become flashcards on their own. They come back after 1, 3, 7, 21, and 60 days, so you don't forget them.
</td>
<td width="50%" valign="top">
<h3>📈 Help that adjusts to you</h3>
As you get better, the AI helps less. If you struggle, it helps more. It always asks before changing anything.
</td>
</tr>
</table>

## Quick start

Requirements: [Claude Code](https://code.claude.com), Python 3.10+, and git. Nothing else to install.

**1. Install the plugin** (inside Claude Code):

```text
/plugin marketplace add gadicandra/grasp
/plugin install grasp@grasp
```

**2. Set it up in your project:**

```text
/grasp:init
```

**3. Start your first feature:**

```text
/grasp:start add a login form
```

That's it. grasp guides you from there.

## Why use grasp

- **Keeps the speed.** Each step takes about 2 minutes. You still ship with AI, you just understand what you shipped.
- **Fits messy schedules.** grasp works per feature, not per week. Switch between projects as often as you want.
- **Honest about deadlines.** In a hurry? Rush mode cuts the extra steps and remembers what you skipped, so you can catch up later.
- **Your data stays with you.** Everything is plain text files on your computer. No account, no tracking, no network calls.

## How it works

### One feature = one episode

Every feature, bug fix, or task you work on is one **episode**. Each episode has 5 short steps:

| Step | Command | What happens | Why it helps |
|---|---|---|---|
| **1. Warm up** | `/grasp:start <name>` | A few quick questions about older work | Remembering something makes it stick |
| **2. Plan** | `/grasp:next` | You write a 3–5 line plan. The AI points out what's good and what's missing | Coming up with ideas yourself beats reading someone else's |
| **3. Build** | `/grasp:next` | The AI writes code and leaves the key part for you. You guess what changed before you look | Guessing first shows you what you got wrong |
| **4. Check** | `/grasp:next` | You name 2 ways it could break, then the AI writes tests | You learn to spot problems yourself |
| **5. Wrap up** | `/grasp:done` | 3 questions (why, what if, trace the flow), then you write a short note for future you | Explaining something is the best test of understanding |

> [!TIP]
> **On a deadline?** Use `/grasp:start fix the bug --rush`. The extra steps are skipped, and anything you didn't
> understand is saved as **learning debt**. It comes back as a question the next time you work on that project.
>
> **Tiny change?** Start your message with `!quick` to skip the plan step. grasp counts how often you do this
> but never blocks it.

### Four levels of help

| Level | You do | The AI does |
|---|---|---|
| **L0 · Observer** | Answer questions | Writes everything |
| **L1 · Co-pilot** | Write the plan + 1 key part of the code | Everything else (you can't skip the plan) |
| **L2 · Pilot** | Write the plan + 2 key parts | Setup and tests. Asks you a guiding question before explaining |
| **L3 · Architect** | Plan, design, and review first | Gives hints only when you ask |

Levels are tracked **per technology**, detected from your `package.json` or `pyproject.toml`. You can be
an Architect in Next.js and an Observer in PyTorch at the same time.

<details>
<summary><b>How grasp decides to change your level</b></summary>

After each episode, grasp looks at your last 3 episodes in that technology:

- Average score **0.80 or higher** → it suggests moving **up** one level.
- Average score **below 0.55** → it suggests moving **down** one level.
- You often rate yourself higher than your actual score → it asks you to guess your score first, to train your self-awareness.
- Your plans often need big fixes → the plan step becomes required again.

The rules:

- It changes **one small thing at a time**, with at least 3 episodes between changes.
- You can **accept**, **reject**, or **dispute** each suggestion. If you dispute, you answer 2 harder questions to prove your case.
- If you reject a suggestion, it isn't offered again for 5 episodes.
- Rush episodes don't count toward your level.
- Every decision is saved, so you can see how you've grown over time.

</details>

### Coming back to an old project

If you haven't touched a project for 3 or more days, grasp first asks you what you remember about the
last feature you built. **Then** it shows you your own notes. Trying to remember before reading is much
better for memory than reading first.

### Commands

| Command | What it does |
|---|---|
| `/grasp:init` | Set up grasp in the current project |
| `/grasp:start <name>` | Start an episode (add `--rush` for deadline mode) |
| `/grasp:next` | Go to the next step (add `--skip` to skip one; skips are recorded) |
| `/grasp:done` | Finish the episode: questions, score, notes |
| `/grasp:review` | Practice your due flashcards any time |
| `/grasp:status` | See your levels, weakest topics, and learning debt |

## Your data

| Where | What's inside |
|---|---|
| `~/.grasp/` | Things you know in general: your levels and general flashcards (e.g. "how do server actions work?"). Shared across all your projects. |
| `<your-project>/.grasp/` | Things about this project: episode notes and project flashcards (e.g. "why is the cart stored in a cookie?"). |

Everything is plain JSON and Markdown that you can open and read. Your data is **kept even if you uninstall
grasp**. You can commit the project folder to show your learning process, or add it to `.gitignore`.

<details>
<summary><b>Under the hood (for developers)</b></summary>

grasp has three layers:

```
Hooks (run automatically)     Session start → load your level and rules into the AI
                              Each message  → block code requests that skip the plan step
                              Each reply    → save flashcards the AI suggested
Skills (you run them)         /grasp:start, :next, :done, :review, :status, :init
Core (bin/grasp)              One Python file, standard library only. All logic and data live here.
```

At the end of each reply during an episode, the AI adds a small `grasp` block with the concepts it
touched and suggested flashcards. A hook reads that block and saves it. No extra AI call is needed.

Strict rules (enforced by code): the plan gate at L1 and the optional `WHY:` commit check.
Soft rules (followed by the AI): leaving `TODO(human)` parts and not answering quiz questions for you.

</details>

## FAQ

<details>
<summary><b>Will this slow me down?</b></summary>
A little, by design. Most steps take about 2 minutes. When time is tight, use <code>--rush</code> or <code>!quick</code>.
</details>

<details>
<summary><b>Can I cheat?</b></summary>
Yes. You can ask the AI to just answer, or skip steps. grasp doesn't try to be a prison. It records what you skip
and shows it back to you. The real test is whether you can explain your code without the AI.
</details>

<details>
<summary><b>Does it work with languages other than English?</b></summary>
Questions are in English by default. You can answer in any language. To change the question language, run
<code>/plugin configure grasp@grasp</code>.
</details>

<details>
<summary><b>Does it send my code or data anywhere?</b></summary>
No. grasp makes no network calls and has no tracking. It only talks to Claude Code, which you are already using.
</details>

<details>
<summary><b>How do I remove it?</b></summary>
Run <code>claude plugin uninstall grasp@grasp</code>. Your notes in <code>~/.grasp</code> and <code>.grasp/</code> stay on your computer.
</details>

## The research behind it

grasp is built on well-tested learning science:

| Idea | In plain words | Source |
|---|---|---|
| Generation effect | You remember what you create better than what you read | Slamecka & Graf, 1978 |
| Retrieval practice | Testing yourself beats re-reading | Roediger & Karpicke, 2006 |
| Spaced repetition | Reviewing over growing gaps stops forgetting | Leitner, 1972 |
| Self-explanation | Explaining something shows whether you really get it | Chi et al., 1994 |
| Desirable difficulty | A bit of struggle leads to deeper learning | Bjork & Bjork, 2011 |
| Expertise reversal | Help that's good for beginners can hold experts back | Kalyuga et al., 2003 |
| AI and learning | AI without guardrails can hurt learning | Bastani et al., *PNAS* 2025 · Lee et al., *CHI* 2025 |

## Contributing

Ideas, bug reports, and pull requests are welcome. Please [open an issue](https://github.com/gadicandra/grasp/issues)
first for bigger changes. If a level change felt too fast or too slow, tell us. That feedback helps tune the rules.

Run the tests:

```bash
python3 tests/test_core.py
claude plugin validate .
claude --plugin-dir .     # try your changes locally
```

## License

[MIT](LICENSE)
