# Architecture

## Intent
RavenX Agentic Layer is a thin coordination layer for agent workflows in the RavenX workspace.

## Proposed pieces
- **Interface layer**: receives tasks and normalizes intent, scope, and constraints
- **Routing layer**: chooses direct execution, one-shot model calls, or delegated coding loops
- **Execution layer**: runs tools, captures outputs, and maintains tight verify loops
- **Context layer**: keeps local repo context, skill instructions, and result summaries grounded

## Early principles
- prefer small scoped actions over broad autonomous behavior
- keep repo-local patterns as the source of truth
- make verification explicit for each change
- separate durable docs from future runtime code

## First implementation target
Start with a minimal runtime contract that accepts:
1. task
2. scope
3. constraints
4. verification command
5. expected deliverable
