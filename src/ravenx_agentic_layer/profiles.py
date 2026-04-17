from __future__ import annotations

from dataclasses import dataclass, field

from .contracts import RouteKind


@dataclass(frozen=True, slots=True)
class ExecutionRhythm:
    mode: str
    checkpoints: tuple[str, ...] = field(default_factory=tuple)


@dataclass(frozen=True, slots=True)
class ExecutionProfile:
    name: str
    route: RouteKind
    model_family: str
    tool_strategy: str
    rhythm: ExecutionRhythm


DEFAULT_PROFILES: tuple[ExecutionProfile, ...] = (
    ExecutionProfile(
        name="tight-edit",
        route=RouteKind.DIRECT_EDIT,
        model_family="local_tool_caller",
        tool_strategy="bounded file edits with immediate verification",
        rhythm=ExecutionRhythm(
            mode="single_pass",
            checkpoints=("inspect-target-files", "apply-change", "run-requested-checks"),
        ),
    ),
    ExecutionProfile(
        name="synthesis-pass",
        route=RouteKind.ONE_SHOT,
        model_family="cloud_general",
        tool_strategy="read and synthesize without mutation",
        rhythm=ExecutionRhythm(
            mode="single_response",
            checkpoints=("gather-context", "compose-answer"),
        ),
    ),
    ExecutionProfile(
        name="delegated-rhythm",
        route=RouteKind.DELEGATED_LOOP,
        model_family="local_reasoner",
        tool_strategy="iterative tool loop with milestone verification",
        rhythm=ExecutionRhythm(
            mode="looped",
            checkpoints=("map-scope", "apply-batch", "verify-milestone", "summarize-delta"),
        ),
    ),
)


class ProfileRegistry:
    def match(self, route: RouteKind, profiles: tuple[ExecutionProfile, ...] = DEFAULT_PROFILES) -> ExecutionProfile:
        for profile in profiles:
            if profile.route is route:
                return profile
        raise ValueError(f"no execution profile for route {route}")
