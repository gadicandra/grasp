---
name: done
description: Close the active grasp episode with explain-back questions, grading, handoff note, and adaptation.
disable-model-invocation: true
allowed-tools: Bash(grasp:*), Bash(git diff:*), Bash(git log:*)
---
Close the active episode. Use the conversation and `git diff` to see what was built.

1. Ask exactly 3 questions about THIS episode's code, one at a time:
   - WHY: why this approach over a concrete alternative?
   - WHAT-IF: which input or condition breaks it, and what happens?
   - TRACE: walk the path from user action to storage/output through the actual files and functions.
   If the episode was RUSH, ask only the TRACE question.
2. For each: user answers from memory (no peeking at code), user self-scores 0-2, then you grade 0-2 with a
   one-line reason. Note any misconception in one sentence.
3. Ask the user to write a 3-5 line handoff note (what was built, key decision, what is still unclear).
   You may suggest edits; do not write it for them.
4. If RUSH: list files or concepts the user touched without understanding as learning-debt questions.
5. Pipe JSON to `grasp close` with a heredoc:
   {"answers":[{"q":"...","concept":"domain/concept","scope":"project|concept","a_hint":"key points",
     "self":0,"ai":0,"misconception":"optional"}],
    "handoff":"...","debt":[{"q":"...","concept":"...","a_hint":"..."}],"plan_fix":"none|minor|major"}
6. If the output contains an ADAPTATION PROPOSAL, explain it in plain words and ask: accept, reject, or dispute.
   - Dispute: ask 2 harder verification questions on that domain. If both are scored 2, treat as accept for a
     level-up dispute (or reject for a level-down one). Otherwise keep the proposal as it stands.
   - Run `grasp adapt accept` or `grasp adapt reject`.
