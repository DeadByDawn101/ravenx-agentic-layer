from __future__ import annotations

from .contracts import RuntimeEvent, RuntimeResult, TaskRequest
from .handoff import HandoffBuilder
from .profiles import ProfileRegistry
from .router import PolicyRouter
from .skills import match_skill
from .verification import VerificationPlanner


class AgenticLayerRuntime:
    def __init__(self) -> None:
        self.router = PolicyRouter()
        self.verification = VerificationPlanner()
        self.profiles = ProfileRegistry()
        self.handoff = HandoffBuilder()

    def run(self, request: TaskRequest) -> RuntimeResult:
        skill = match_skill(request)
        route = self.router.decide(request)
        verification = self.verification.build(request)
        execution = self.profiles.match(route.kind)
        handoff = self.handoff.build(request, skill, execution)

        events = [
            RuntimeEvent("task.accepted", request.task),
            RuntimeEvent("route.selected", route.kind.value),
        ]
        if skill:
            events.append(RuntimeEvent("skill.matched", skill.name))
        events.append(RuntimeEvent("verification.planned", str(len(verification.commands))))
        events.append(RuntimeEvent("execution.ready", execution.name))
        if handoff:
            events.append(RuntimeEvent("handoff.prepared", handoff.skill))
        events.append(RuntimeEvent("task.completed", request.deliverable or "result prepared"))

        return RuntimeResult(
            route=route,
            skill=skill.name if skill else None,
            events=events,
            verification=verification,
            execution=execution,
            handoff=handoff,
        )
