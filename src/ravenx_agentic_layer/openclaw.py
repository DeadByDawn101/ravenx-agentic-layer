from __future__ import annotations

from .contracts import RuntimeResult


class OpenClawAdapter:
    def build_behavior(self, result: RuntimeResult) -> dict[str, object]:
        skill = result.skill or "generic-runtime"
        execution = result.execution
        return {
            "skill_card": skill,
            "preferred_route": result.route.kind.value,
            "model_family": execution.model_family,
            "tool_strategy": execution.tool_strategy,
            "execution_rhythm": {
                "mode": execution.rhythm.mode,
                "checkpoints": list(execution.rhythm.checkpoints),
            },
            "verification": {
                "commands": result.verification.commands,
                "artifacts": result.verification.artifacts,
                "risk_notes": result.verification.risk_notes,
            },
            "handoff": (
                {
                    "skill": result.handoff.skill,
                    "continuation_mode": result.handoff.continuation_mode,
                    "summary": result.handoff.summary,
                    "next_actions": result.handoff.next_actions,
                    "checkpoints": result.handoff.checkpoints,
                    "verification": result.handoff.verification,
                    "watchouts": result.handoff.watchouts,
                }
                if result.handoff
                else None
            ),
        }
