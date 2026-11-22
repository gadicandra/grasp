---
name: init
description: Set up grasp in the current project (register project, global journal, optional commit hook).
disable-model-invocation: true
allowed-tools: Bash(grasp:*)
---
Ask the user two yes/no questions:
1. Commit `.grasp/` with the project (recommended: it documents decisions and learning), or gitignore it?
2. Install a git commit-msg hook that requires a `WHY:` section (>= 15 words in their own words)?

Then run `grasp init` with `--gitignore` and/or `--commit-hook` as chosen, and show the output.
Finish by telling them: start work with `/grasp:start <feature>`; use `--rush` near deadlines;
prefix trivial prompts with `!quick`.
