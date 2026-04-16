from __future__ import annotations

from .contracts import RuntimeEvent, RuntimeResult, TaskRequest
from .router import PolicyRouter
from .skills import match_skill
from .verification import VerificationPlanner


class AgenticLayerRuntime:
    def __init__(self) -> None:
        self.router = PolicyRouter()
        self.verification = VerificationPlanner()

    def run(self, request: TaskRequest) -> RuntimeResult:
        skill = match_skill(request)
        route = self.router.decide(request)
        verification = self.verification.build(request)

        events = [
            RuntimeEvent("task.accepted", request.task),
            RuntimeEvent("route.selected", route.kind.value),
        ]
        if skill:
            events.append(RuntimeEvent("skill.matched", skill.name))
        events.append(RuntimeEvent("verification.planned", str(len(verification.commands))))
        events.append(RuntimeEvent("execution.ready", route.reasons[0]))
        events.append(RuntimeEvent("task.completed", request.deliverable or "result prepared"))

        return RuntimeResult(
            route=route,
            skill=skill.name if skill else None,
            events=events,
            verification=verification,
        )
