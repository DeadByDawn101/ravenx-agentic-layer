from __future__ import annotations

from .contracts import HandoffArtifact, TaskRequest
from .profiles import ExecutionProfile
from .skills import SkillCard


class HandoffBuilder:
    def build(self, request: TaskRequest, skill: SkillCard | None, execution: ExecutionProfile) -> HandoffArtifact | None:
        if not skill or skill.name != "repo-coding-loop":
            return None

        summary = self._build_summary(request, execution)
        next_actions = self._build_next_actions(request)
        checkpoints = list(execution.rhythm.checkpoints)
        verification = request.verification.copy()
        watchouts = request.constraints.copy()
        if len(request.scope) > 3:
            watchouts.append("keep commits scoped and summarize cross-file impact for the next agent")
        if not verification:
            watchouts.append("verification commands were not provided, so the next agent should define them before finalizing")

        return HandoffArtifact(
            skill="coding-handoff",
            continuation_mode=execution.rhythm.mode,
            summary=summary,
            next_actions=next_actions,
            checkpoints=checkpoints,
            verification=verification,
            watchouts=watchouts,
        )

    def _build_summary(self, request: TaskRequest, execution: ExecutionProfile) -> str:
        target = ", ".join(request.scope) if request.scope else "repo-wide context"
        deliverable = request.deliverable or "updated code and verification notes"
        return (
            f"Continue the coding task '{request.task}' in {target}. "
            f"Use the {execution.name} profile and finish with {deliverable}."
        )

    def _build_next_actions(self, request: TaskRequest) -> list[str]:
        actions = ["re-read the scoped files and recent diffs before editing"]
        if request.scope:
            actions.append(f"apply or continue edits in: {', '.join(request.scope)}")
        else:
            actions.append("identify the minimum file set required to complete the task")

        if request.verification:
            actions.append(f"run verification: {request.verification[0]}")
            if len(request.verification) > 1:
                actions.append("complete any remaining requested verification commands")
        else:
            actions.append("define a concrete verification command before declaring completion")

        actions.append("leave a concise delta summary for the next session or agent")
        return actions
