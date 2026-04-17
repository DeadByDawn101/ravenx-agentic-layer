from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .profiles import ExecutionProfile


class RouteKind(StrEnum):
    DIRECT_EDIT = "direct_edit"
    ONE_SHOT = "one_shot"
    DELEGATED_LOOP = "delegated_loop"


@dataclass(slots=True)
class TaskRequest:
    task: str
    scope: list[str] = field(default_factory=list)
    constraints: list[str] = field(default_factory=list)
    verification: list[str] = field(default_factory=list)
    deliverable: str = ""


@dataclass(slots=True)
class RouteDecision:
    kind: RouteKind
    reasons: list[str] = field(default_factory=list)


@dataclass(slots=True)
class RuntimeEvent:
    kind: str
    detail: str


@dataclass(slots=True)
class VerificationPlan:
    commands: list[str] = field(default_factory=list)
    artifacts: list[str] = field(default_factory=list)
    risk_notes: list[str] = field(default_factory=list)


@dataclass(slots=True)
class HandoffArtifact:
    skill: str
    continuation_mode: str
    summary: str
    next_actions: list[str] = field(default_factory=list)
    checkpoints: list[str] = field(default_factory=list)
    verification: list[str] = field(default_factory=list)
    watchouts: list[str] = field(default_factory=list)


@dataclass(slots=True)
class RuntimeResult:
    route: RouteDecision
    skill: str | None
    events: list[RuntimeEvent]
    verification: VerificationPlan
    execution: ExecutionProfile
    handoff: HandoffArtifact | None = None
