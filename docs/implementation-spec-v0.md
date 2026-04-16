# RavenX Agentic Layer v0 Implementation Spec

## Goal
Ship a minimal, original, testable agentic core that can accept normalized work, choose an execution mode, emit runtime events, and return a verification-aware plan.

## Non-goals
- full provider integration
- full CLI chat UX
- remote task execution
- live MCP serving
- autonomous background loops

## Contract

### TaskRequest
```json
{
  "task": "add retry handling to the sender",
  "scope": ["src/sender.ts", "tests/sender.test.ts"],
  "constraints": ["preserve API", "no new deps"],
  "verification": ["bun test tests/sender.test.ts"],
  "deliverable": "passing tests and summary"
}
```

### Route kinds
- `direct_edit`
- `one_shot`
- `delegated_loop`

### RuntimeEvent kinds
- `task.accepted`
- `route.selected`
- `skill.matched`
- `verification.planned`
- `execution.ready`
- `task.completed`

## Routing policy

### direct_edit
Choose when all are true:
- scope is small and explicit
- ambiguity is low
- task is implementation or edit oriented
- verification is narrow

### one_shot
Choose when any are true:
- user mainly wants synthesis, intake, summarization, or planning
- no file mutation is required yet
- response can be produced in one model call

### delegated_loop
Choose when any are true:
- scope spans multiple modules or is open-ended
- task likely needs iterative exploration
- verification burden is medium to high
- multiple tools or sub-steps are expected

## Skill matching
Skills are simple structured cards with:
- `name`
- `triggers`
- `preferred_route`
- `required_tools`
- `verification_style`

v0 matcher can be keyword and scope based. The important thing is that skill selection becomes inspectable.

## Model and execution profiles
Profiles should be separate from route choice.

Example profile families:
- `local_reasoner`
- `local_tool_caller`
- `cloud_general`
- `cloud_fallback`

v0 only needs metadata, not live adapters.

## Verification plan
A verification plan is a list of checks plus risk notes.

Example:
```json
{
  "commands": ["pytest tests/unit/test_router.py"],
  "artifacts": ["git diff -- src/router.py"],
  "risk_notes": ["broader integration not yet exercised"]
}
```

## Proposed file layout
```text
src/ravenx_agentic_layer/
  __init__.py
  contracts.py
  router.py
  runtime.py
  skills.py
  profiles.py
  verification.py
tests/
  test_router.py
  test_runtime.py
```

## First milestone
Implement a pure-Python local scaffold that:
1. accepts a `TaskRequest`
2. chooses a `RouteDecision`
3. matches zero or one `SkillCard`
4. emits a deterministic event trace
5. returns a verification plan

## Acceptance criteria
- unit tests pass locally
- event trace is deterministic
- route choice is explainable via returned reasons
- scaffold is small enough to replace module-by-module later

## Follow-up milestones
- add YAML or JSON fixtures for route evals
- add provider adapters
- add CLI entrypoint
- add event sink abstractions
- add MCP registry export for skills and tools
