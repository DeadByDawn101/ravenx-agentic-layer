# RavenX Agentic Layer

A minimal runtime scaffold for a practical agent orchestration layer in the RavenX workspace.

## Goals
- define a clean boundary between contracts, routing, skills, verification, and execution
- keep the first iteration small, typed, and easy to replace
- ground the design in patterns observed across adjacent agentic repos

## Current layout
- `docs/comparative-intake.md` captures the best reusable ideas from the reviewed repos
- `docs/implementation-spec-v0.md` defines the first runtime contract and milestones
- `docs/behavior-autoresearch-loop.md` defines the first behavior mutation and evaluation loop
- `src/ravenx_agentic_layer/` contains the Python scaffold for routing, handoff generation, and behavior evals
- `tests/` covers route behavior, runtime behavior, and baseline autoresearch evals

## Quick start
```bash
python -m pytest
```

## Current runtime surface
The v0 scaffold accepts a normalized request with:
- `task`
- `scope`
- `constraints`
- `verification`
- `deliverable`

It returns:
- a route decision (`direct_edit`, `one_shot`, or `delegated_loop`)
- an optional matched skill
- a deterministic event trace
- a verification plan

## Runtime additions
- route decisions now resolve to explicit execution profiles
- each profile carries an execution rhythm with named checkpoints
- `OpenClawAdapter` converts runtime results into a behavior payload that can drive OpenClaw-facing instruction injection
- coding tasks now emit a built-in `handoff` artifact for cross-session and cross-agent continuation
- a minimal behavior autoresearch harness can score candidate mutations against route, skill, handoff, and checkpoint expectations

## Built-in coding handoff artifact
When the runtime matches the `repo-coding-loop` skill, it now produces a typed handoff payload with:
- a continuation summary tied to the active execution profile
- ordered next actions for the next session or delegate agent
- carried-forward verification commands
- watchouts derived from task constraints and scope size

This makes coding-task continuation inspectable instead of burying session handoff instructions in prompt text.

## Behavior autoresearch scaffold
- `BehaviorEvalHarness` runs inspectable task fixtures against the current runtime
- `CandidateMutation` lets the repo trial small behavior changes like new route terms or skill triggers
- `BehaviorLoopPlan` turns misses into the next concrete mutation ideas instead of vague tuning notes
- `DEFAULT_BEHAVIOR_EVALS` gives the repo a baseline suite for bounded edits, synthesis, and delegated multi-file work

## Next steps
- move behavior eval cases into fixture files for larger coverage
- add verification-plan and handoff-content scoring
- add a CLI or service wrapper once the core behavior is stable
- extend the adapter payload into a concrete bootstrap entrypoint
