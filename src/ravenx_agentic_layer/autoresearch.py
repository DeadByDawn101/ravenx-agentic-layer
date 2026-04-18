from __future__ import annotations

from dataclasses import dataclass, field

from .contracts import RouteKind, TaskRequest
from .handoff import HandoffBuilder
from .profiles import ProfileRegistry
from .router import PolicyRouter
from .runtime import AgenticLayerRuntime
from .skills import DEFAULT_SKILLS, SkillCard
from .verification import VerificationPlanner


@dataclass(frozen=True, slots=True)
class CandidateMutation:
    name: str
    summary_terms: tuple[str, ...] = field(default_factory=tuple)
    implement_terms: tuple[str, ...] = field(default_factory=tuple)
    extra_skills: tuple[SkillCard, ...] = field(default_factory=tuple)
    notes: tuple[str, ...] = field(default_factory=tuple)


@dataclass(frozen=True, slots=True)
class BehaviorEvalCase:
    name: str
    request: TaskRequest
    expected_route: RouteKind
    expected_skill: str | None = None
    expect_handoff: bool = False
    expected_checkpoints: tuple[str, ...] = field(default_factory=tuple)


@dataclass(frozen=True, slots=True)
class BehaviorEvalOutcome:
    case_name: str
    passed: bool
    score: float
    failures: tuple[str, ...] = field(default_factory=tuple)


@dataclass(frozen=True, slots=True)
class BehaviorEvalReport:
    candidate: str
    outcomes: tuple[BehaviorEvalOutcome, ...]
    total_score: float
    max_score: float
    summary: str


@dataclass(frozen=True, slots=True)
class BehaviorLoopPlan:
    candidate: str
    strengths: tuple[str, ...]
    gaps: tuple[str, ...]
    next_mutations: tuple[str, ...]


class BehaviorEvalHarness:
    def __init__(self, baseline_skills: tuple[SkillCard, ...] = DEFAULT_SKILLS) -> None:
        self.baseline_skills = baseline_skills
        self.profiles = ProfileRegistry()
        self.verification = VerificationPlanner()
        self.handoff = HandoffBuilder()

    def evaluate(
        self,
        cases: tuple[BehaviorEvalCase, ...],
        mutation: CandidateMutation | None = None,
    ) -> BehaviorEvalReport:
        candidate_name = mutation.name if mutation else "baseline"
        runtime = self._build_runtime(mutation)
        outcomes = tuple(self._run_case(runtime, case) for case in cases)
        total_score = sum(outcome.score for outcome in outcomes)
        max_score = float(len(outcomes) * 4)
        passed = sum(1 for outcome in outcomes if outcome.passed)
        summary = f"{candidate_name} passed {passed}/{len(outcomes)} cases"
        return BehaviorEvalReport(
            candidate=candidate_name,
            outcomes=outcomes,
            total_score=total_score,
            max_score=max_score,
            summary=summary,
        )

    def plan_next_loop(self, report: BehaviorEvalReport) -> BehaviorLoopPlan:
        strengths: list[str] = []
        gaps: list[str] = []
        next_mutations: list[str] = []

        for outcome in report.outcomes:
            if outcome.passed:
                strengths.append(f"keep the behavior used for {outcome.case_name}")
                continue

            gaps.append(f"repair {outcome.case_name}: {'; '.join(outcome.failures)}")
            if any("route" in failure for failure in outcome.failures):
                next_mutations.append("adjust routing keywords or add a stronger route policy signal")
            if any("skill" in failure for failure in outcome.failures):
                next_mutations.append("add or refine a skill trigger for the missed behavior")
            if any("handoff" in failure for failure in outcome.failures):
                next_mutations.append("tighten the coding handoff expectation for delegated work")
            if any("checkpoint" in failure for failure in outcome.failures):
                next_mutations.append("align execution checkpoints with the expected rhythm")

        if not next_mutations:
            next_mutations.append("raise case difficulty with broader multi-tool or handoff-heavy tasks")

        return BehaviorLoopPlan(
            candidate=report.candidate,
            strengths=tuple(strengths),
            gaps=tuple(gaps),
            next_mutations=tuple(dict.fromkeys(next_mutations)),
        )

    def _build_runtime(self, mutation: CandidateMutation | None) -> AgenticLayerRuntime:
        router = PolicyRouter(
            summary_words=mutation.summary_terms if mutation else (),
            implement_words=mutation.implement_terms if mutation else (),
        )
        skills = (mutation.extra_skills if mutation else ()) + self.baseline_skills
        return AgenticLayerRuntime(
            router=router,
            verification=self.verification,
            profiles=self.profiles,
            handoff=self.handoff,
            skills=skills,
        )

    def _run_case(self, runtime: AgenticLayerRuntime, case: BehaviorEvalCase) -> BehaviorEvalOutcome:
        result = runtime.run(case.request)
        failures: list[str] = []
        score = 0.0

        if result.route.kind is case.expected_route:
            score += 1
        else:
            failures.append(f"route expected {case.expected_route.value} but saw {result.route.kind.value}")

        if result.skill == case.expected_skill:
            score += 1
        else:
            failures.append(f"skill expected {case.expected_skill!r} but saw {result.skill!r}")

        has_handoff = result.handoff is not None
        if has_handoff is case.expect_handoff:
            score += 1
        else:
            failures.append(f"handoff expected {case.expect_handoff} but saw {has_handoff}")

        checkpoints = tuple(result.execution.rhythm.checkpoints)
        if not case.expected_checkpoints or checkpoints == case.expected_checkpoints:
            score += 1
        else:
            failures.append(f"checkpoint mismatch: expected {case.expected_checkpoints} but saw {checkpoints}")

        return BehaviorEvalOutcome(
            case_name=case.name,
            passed=not failures,
            score=score,
            failures=tuple(failures),
        )


DEFAULT_BEHAVIOR_EVALS: tuple[BehaviorEvalCase, ...] = (
    BehaviorEvalCase(
        name="bounded coding task keeps tight edit rhythm",
        request=TaskRequest(
            task="implement retry handling",
            scope=["src/sender.ts", "tests/sender.test.ts"],
            constraints=["preserve API"],
            verification=["bun test tests/sender.test.ts"],
            deliverable="passing tests and summary",
        ),
        expected_route=RouteKind.DIRECT_EDIT,
        expected_skill="repo-coding-loop",
        expect_handoff=True,
        expected_checkpoints=("inspect-target-files", "apply-change", "run-requested-checks"),
    ),
    BehaviorEvalCase(
        name="synthesis request stays one-shot",
        request=TaskRequest(
            task="compare the repos and produce an intake summary",
            deliverable="comparative memo",
        ),
        expected_route=RouteKind.ONE_SHOT,
        expected_skill="intake-synthesis",
        expect_handoff=False,
        expected_checkpoints=("gather-context", "compose-answer"),
    ),
    BehaviorEvalCase(
        name="broad cross-module task delegates with handoff",
        request=TaskRequest(
            task="continue implementing cross-module handoff support",
            scope=["router.py", "runtime.py", "profiles.py", "openclaw.py"],
            constraints=["preserve event ordering"],
            verification=["pytest tests/test_runtime.py", "python -m compileall src"],
            deliverable="updated runtime and tests",
        ),
        expected_route=RouteKind.DELEGATED_LOOP,
        expected_skill="repo-coding-loop",
        expect_handoff=True,
        expected_checkpoints=("map-scope", "apply-batch", "verify-milestone", "summarize-delta"),
    ),
)
