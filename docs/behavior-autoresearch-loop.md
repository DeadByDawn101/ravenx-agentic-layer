# Behavior Autoresearch Loop

## Goal
Add a concrete evaluation layer for RavenX behavior tuning without jumping straight to model training. The unit of improvement here is agent behavior: routing, skill choice, execution rhythm, and handoff quality.

## Loop shape
1. Define representative behavior eval cases.
2. Run the baseline runtime against those cases.
3. Apply a candidate mutation.
4. Re-run evals and compare misses.
5. Generate the next mutation plan from observed failures.

## Current mutation surface
The first scaffold intentionally mutates only a few high-leverage behavior controls:
- extra summary routing terms
- extra implementation routing terms
- extra skill cards and triggers

This keeps the loop small and inspectable before adding heavier prompt or provider-level mutation.

## Eval schema
Each case records:
- normalized `TaskRequest`
- expected route
- expected skill, if any
- whether a coding handoff should be produced
- expected execution checkpoints

Each outcome scores four checks:
- route correctness
- skill correctness
- handoff correctness
- checkpoint correctness

## Why this matters
This gives RavenX a practical bridge between static runtime logic and future automated behavior research. Instead of saying "the agent got better," the repo can now say exactly which policy mutation improved which task class.

## Near-term extension ideas
- add YAML-backed eval fixtures for larger scenario sets
- score verification plan quality and risk-note quality
- add handoff artifact content assertions, not just presence
- compare multiple candidate mutations in a small tournament
- add tool-call expectations for shell-heavy or delegation-heavy tasks
