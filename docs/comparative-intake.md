# Comparative Intake

## Purpose
Capture the most reusable runtime, skill, and training ideas from the reference repos and translate them into safe, concrete next steps for RavenX Agentic Layer.

## Repos reviewed
- `DeadByDawn101/claw-code-parity`
- `DeadByDawn101/openclaude`
- `RishabhK103/claude-code`
- `nirholas/claude-code`
- `DeadByDawn101/claude-code-empire`
- `DeadByDawn101/ravenx-inference-harness`

## Important boundary
This intake extracts high-level architecture and workflow patterns. It does **not** depend on copying leaked implementation code. RavenX Agentic Layer should use original code and public interfaces only.

## Comparative notes

| Repo | Strong idea | Why it matters | RavenX action |
| --- | --- | --- | --- |
| `claw-code-parity` | Runtime split into distinct crates for API, runtime, tools, telemetry, commands, compat harness | Clean seams make parity and replacement work much easier | Mirror this as explicit layer modules: contract, router, runtime, memory, verification |
| `claw-code-parity` | Deterministic mock parity harness and scenario manifest | Lets the team verify multi-tool behavior without live provider drift | Add fixture-driven scenario tests for route decisions and execution traces |
| `openclaude` | Provider abstraction plus settings-based agent routing | Runtime can pick cheaper or stronger models by job type | Build policy-based routing keyed by task class and risk |
| `openclaude` | Headless service mode with streaming events | Separates runtime from UI and makes integrations easier | Keep first runtime transport-agnostic and event-emitting |
| `openclaude` | Runtime doctor/privacy verification scripts | Operational trust matters as much as raw feature count | Add explicit verification hooks and environment checks |
| `claude-code` | Strong command/tool/session boundaries, permission mediation, session resume | Stable agent loops need explicit state and permission control | Treat permissions and resumability as first-class runtime concerns |
| `nirholas/claude-code` | MCP-facing server exposing tools, commands, prompts, resources | Great pattern for introspection and external orchestration | Add a future adapter for registry export and MCP-safe metadata |
| `claude-code-empire` | Expanded ecosystem shape: web UI, server, prompts, docs | Shows how a local core can later fan out into multiple surfaces | Keep the local core minimal but leave clear extension points |
| `ravenx-inference-harness` | Local inference server with model specialization and compression-aware deployment | Runtime policy should understand local specialized backends, not just SaaS APIs | Add model profile metadata for local reasoning, tool-calling, and low-latency modes |

## Best ideas to carry forward

### 1. Thin runtime contract
The best repos keep the core request contract small even when the surrounding system is large.

Adopt this normalized request shape:
- `task`
- `scope`
- `constraints`
- `verification`
- `deliverable`

### 2. Explicit routing policy
Useful repeated pattern:
- direct local action for small bounded work
- one-shot model synthesis for summarization and planning
- delegated coding loop for broad or iterative work

### 3. Event-based runtime surface
Instead of binding the design to a CLI first, emit durable events:
- `task.accepted`
- `route.selected`
- `execution.started`
- `verification.requested`
- `verification.completed`
- `task.completed`

### 4. Skill cards over ad hoc prompt blobs
The reference repos repeatedly imply the value of structured reusable guidance. RavenX should model skills as metadata plus execution hints:
- intent coverage
- required tools
- preferred route
- verification expectations
- training examples or prompt snippets

### 5. Verification as a runtime phase
Verification should not be an afterthought. Strong pattern from parity and doctor flows:
- route
- execute
- verify
- summarize risk

### 6. Local-model-aware routing
The inference harness makes a strong case for policy that understands model shape:
- reasoning-heavy local model
- tool-calling optimized local model
- cheap summarizer
- fallback cloud model

## Proposed RavenX v0 architecture

### Core modules
- `contracts`: typed request and result objects
- `router`: policy engine for execution mode selection
- `runtime`: orchestration loop and event emission
- `skills`: structured skill cards and matcher
- `profiles`: model and execution profiles
- `verification`: verification plan and result handling

### First execution modes
- `direct_edit`
- `one_shot`
- `delegated_loop`

### First policy signals
- scope size
- task ambiguity
- verification intensity
- required tools
- preference for local or cloud execution

## Training and evaluation ideas

### Training data shape
Create a small internal corpus of request-to-route examples with:
- normalized request
- expected route
- expected skill choice
- verification plan
- rationale

### Eval shape
Start with fixture-based evals for:
- routing correctness
- skill selection correctness
- verification plan generation
- event trace completeness

### Good benchmark scenarios
- one-file copy edit
- two-file refactor with tests
- repo exploration question
- local-model-friendly summarize job
- risky shell command requiring stronger verification

## Immediate build recommendation
1. Add a typed runtime scaffold.
2. Add fixture-style route tests.
3. Add a spec describing contracts, events, and extension points.
4. Keep provider integration out of v0 until routing and verification behavior are stable.
