# RavenX Agentic Layer

A minimal runtime scaffold for a practical agent orchestration layer in the RavenX workspace.

## Goals
- define a clean boundary between contracts, routing, skills, verification, and execution
- keep the first iteration small, typed, and easy to replace
- ground the design in patterns observed across adjacent agentic repos

## Current layout
- `docs/comparative-intake.md` captures the best reusable ideas from the reviewed repos
- `docs/implementation-spec-v0.md` defines the first runtime contract and milestones
- `src/ravenx_agentic_layer/` contains the first Python scaffold for routing and event emission
- `tests/` covers basic route and runtime behavior

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

## Built-in coding handoff artifact
When the runtime matches the `repo-coding-loop` skill, it now produces a typed handoff payload with:
- a continuation summary tied to the active execution profile
- ordered next actions for the next session or delegate agent
- carried-forward verification commands
- watchouts derived from task constraints and scope size

This makes coding-task continuation inspectable instead of burying session handoff instructions in prompt text.

## Next steps
- move routing heuristics into fixture-backed policy tests
- add a CLI or service wrapper once the core behavior is stable
- extend the adapter payload into a concrete bootstrap entrypoint
