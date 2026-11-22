---
name: start
description: Start a grasp learning episode for one feature, bug, or task. Use when the user begins new work.
argument-hint: "<feature title> [--rush]"
disable-model-invocation: true
allowed-tools: Bash(grasp:*)
---
Run `grasp start $ARGUMENTS` and follow its output exactly.

- Warm-up / re-entry: ask ONE question at a time. Wait for the user's answer. Ask them to self-score 0-2 first,
  then give your grade 0-2 with a one-line reason, then run `grasp grade <id> <score>` with YOUR grade.
- Never reveal an answer key before the user answers. If they say "I don't know", grade 0 and teach it briefly.
- Re-entry: ask the questions before showing the handoff note, then show the note.
- When the warm-up is done, run `grasp next` and follow the phase instructions it prints.
