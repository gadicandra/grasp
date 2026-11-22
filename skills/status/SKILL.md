---
name: status
description: Show the grasp learner model (levels, weakest concepts, learning debt, adaptation history).
disable-model-invocation: true
allowed-tools: Bash(grasp:*)
---
Run `grasp status` and show its output. Then add at most 3 short observations (e.g., biggest calibration gap,
oldest debt). If the user disagrees with their level, offer the dispute flow from /grasp:done.
