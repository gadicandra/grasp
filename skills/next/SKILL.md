---
name: next
description: Move the active grasp episode to its next phase (plan, build, verify, close).
argument-hint: "[--skip]"
disable-model-invocation: true
allowed-tools: Bash(grasp:*)
---
Run `grasp next $ARGUMENTS`. Follow the phase instructions it prints for the rest of this phase.
If the new phase is CLOSE, run the /grasp:done procedure.
