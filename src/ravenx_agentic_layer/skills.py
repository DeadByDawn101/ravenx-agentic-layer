from __future__ import annotations

from dataclasses import dataclass, field

from .contracts import RouteKind, TaskRequest


@dataclass(frozen=True, slots=True)
class SkillCard:
    name: str
    triggers: tuple[str, ...]
    preferred_route: RouteKind
    required_tools: tuple[str, ...] = field(default_factory=tuple)
    verification_style: str = "focused"


DEFAULT_SKILLS: tuple[SkillCard, ...] = (
    SkillCard(
        name="repo-coding-loop",
        triggers=("build", "fix", "refactor", "implement", "test"),
        preferred_route=RouteKind.DELEGATED_LOOP,
        required_tools=("read", "edit", "exec"),
        verification_style="narrow-first",
    ),
    SkillCard(
        name="intake-synthesis",
        triggers=("compare", "summarize", "research", "intake", "spec"),
        preferred_route=RouteKind.ONE_SHOT,
        required_tools=("read",),
        verification_style="document-review",
    ),
)


def match_skill(request: TaskRequest, skills: tuple[SkillCard, ...] = DEFAULT_SKILLS) -> SkillCard | None:
    haystack = " ".join([request.task, *request.constraints, request.deliverable]).lower()
    for skill in skills:
        if any(trigger in haystack for trigger in skill.triggers):
            return skill
    return None
