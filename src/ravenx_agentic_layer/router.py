from __future__ import annotations

from .contracts import RouteDecision, RouteKind, TaskRequest


SUMMARY_WORDS = ("summarize", "summary", "compare", "research", "intake", "plan", "spec")
IMPLEMENT_WORDS = ("fix", "edit", "update", "add", "implement", "refactor", "scaffold")


class PolicyRouter:
    def decide(self, request: TaskRequest) -> RouteDecision:
        task_text = request.task.lower()
        scope_size = len(request.scope)
        verification_size = len(request.verification)
        reasons: list[str] = []

        if any(word in task_text for word in SUMMARY_WORDS) and scope_size == 0:
            reasons.append("task is synthesis-oriented and does not require explicit file mutation")
            return RouteDecision(RouteKind.ONE_SHOT, reasons)

        if scope_size <= 3 and verification_size <= 2 and any(word in task_text for word in IMPLEMENT_WORDS):
            reasons.append("scope is bounded and verification is narrow")
            return RouteDecision(RouteKind.DIRECT_EDIT, reasons)

        if scope_size > 3:
            reasons.append("scope spans multiple files or modules")
        if verification_size > 2:
            reasons.append("verification burden is non-trivial")
        if not reasons:
            reasons.append("task likely needs iterative exploration or multi-step execution")
        return RouteDecision(RouteKind.DELEGATED_LOOP, reasons)
