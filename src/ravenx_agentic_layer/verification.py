from __future__ import annotations

from .contracts import TaskRequest, VerificationPlan


class VerificationPlanner:
    def build(self, request: TaskRequest) -> VerificationPlan:
        commands = request.verification.copy()
        artifacts = [f"scope:{item}" for item in request.scope]
        risk_notes: list[str] = []

        if not commands:
            risk_notes.append("no verification command supplied")
        if len(request.scope) > 3:
            risk_notes.append("broad scope may need integration verification")

        return VerificationPlan(commands=commands, artifacts=artifacts, risk_notes=risk_notes)
