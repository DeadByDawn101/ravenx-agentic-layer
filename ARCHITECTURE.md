# Architecture

## Intent
RavenX Agentic Layer is a thin coordination layer for agent workflows in the RavenX workspace.

## Current core pieces
- **Contracts**: normalize task, scope, constraints, verification, and deliverable into a typed request
- **Routing**: choose `direct_edit`, `one_shot`, or `delegated_loop`
- **Skills**: match reusable guidance cards without hiding the decision path
- **Verification**: turn request verification into an explicit plan with risk notes
- **Runtime**: emit a deterministic event trace around the selected route
- **Behavior autoresearch**: run fixture-like eval cases against baseline or mutated routing and skill behavior

## Principles
- prefer small scoped actions over broad autonomous behavior
- keep repo-local patterns as the source of truth
- make verification explicit for each change
- separate route policy from model and provider choice
- keep the runtime transport-agnostic so CLI or service wrappers can be added later

## Event model
The first event surface is intentionally small:
1. `task.accepted`
2. `route.selected`
3. `skill.matched`
4. `verification.planned`
5. `execution.ready`
6. `task.completed`

## First implementation target
The current scaffold accepts:
1. task
2. scope
3. constraints
4. verification commands
5. expected deliverable

And returns:
1. route decision
2. matched skill, if any
3. verification plan
4. event trace
