---
name: review
description: Review due grasp cards (spaced retrieval) for the current project's domains.
argument-hint: "[max cards]"
disable-model-invocation: true
allowed-tools: Bash(grasp:*)
---
Run `grasp due $ARGUMENTS` (default 10). For each card, one at a time: ask the question, wait for the answer
from memory, user self-scores 0-2, you grade 0-2 against the answer key with a one-line reason, then run
`grasp grade <id> <your score>`. Never show the answer key before they answer. End with a one-line summary.
