from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import UTC, datetime
import json
from pathlib import Path

from .autoresearch import (
    DEFAULT_BEHAVIOR_EVALS,
    BehaviorEvalCase,
    BehaviorEvalHarness,
    BehaviorEvalReport,
    BehaviorLoopPlan,
    CandidateMutation,
)
from .skills import SkillCard
from .contracts import RouteKind


@dataclass(frozen=True, slots=True)
class MutationSuggestion:
    name: str
    rationale: str
    mutation: CandidateMutation


@dataclass(frozen=True, slots=True)
class LoopRunRecord:
    created_at: str
    report: BehaviorEvalReport
    plan: BehaviorLoopPlan
    suggestions: tuple[MutationSuggestion, ...] = field(default_factory=tuple)

    def to_dict(self) -> dict[str, object]:
        return {
            "created_at": self.created_at,
            "report": {
                "candidate": self.report.candidate,
                "summary": self.report.summary,
                "total_score": self.report.total_score,
                "max_score": self.report.max_score,
                "outcomes": [asdict(outcome) for outcome in self.report.outcomes],
            },
            "plan": asdict(self.plan),
            "suggestions": [
                {
                    "name": suggestion.name,
                    "rationale": suggestion.rationale,
                    "mutation": {
                        "name": suggestion.mutation.name,
                        "summary_terms": list(suggestion.mutation.summary_terms),
                        "implement_terms": list(suggestion.mutation.implement_terms),
                        "extra_skills": [asdict(skill) for skill in suggestion.mutation.extra_skills],
                        "notes": list(suggestion.mutation.notes),
                    },
                }
                for suggestion in self.suggestions
            ],
        }


class BehaviorLoopRunner:
    def __init__(self, harness: BehaviorEvalHarness | None = None) -> None:
        self.harness = harness or BehaviorEvalHarness()

    def run_once(
        self,
        cases: tuple[BehaviorEvalCase, ...] = DEFAULT_BEHAVIOR_EVALS,
        mutation: CandidateMutation | None = None,
    ) -> LoopRunRecord:
        report = self.harness.evaluate(cases, mutation=mutation)
        plan = self.harness.plan_next_loop(report)
        suggestions = self.suggest_mutations(plan)
        return LoopRunRecord(
            created_at=datetime.now(UTC).isoformat(),
            report=report,
            plan=plan,
            suggestions=suggestions,
        )

    def suggest_mutations(self, plan: BehaviorLoopPlan) -> tuple[MutationSuggestion, ...]:
        suggestions: list[MutationSuggestion] = []

        for idea in plan.next_mutations:
            if idea == "raise case difficulty with broader multi-tool or handoff-heavy tasks":
                suggestions.append(
                    MutationSuggestion(
                        name="raise-case-difficulty-multi-tool",
                        rationale=idea,
                        mutation=CandidateMutation(
                            name="raise-case-difficulty-multi-tool",
                            notes=("Add a harder fixture with broader tool usage and richer handoff expectations.",),
                        ),
                    )
                )
            elif "routing keywords" in idea:
                suggestions.append(
                    MutationSuggestion(
                        name="route-signal-rename-and-safe-edit",
                        rationale=idea,
                        mutation=CandidateMutation(
                            name="route-signal-rename-and-safe-edit",
                            implement_terms=("rename", "safely"),
                            notes=("Boost direct-edit detection for bounded rename work.",),
                        ),
                    )
                )
            elif "skill trigger" in idea:
                suggestions.append(
                    MutationSuggestion(
                        name="audit-synthesis-skill",
                        rationale=idea,
                        mutation=CandidateMutation(
                            name="audit-synthesis-skill",
                            summary_terms=("audit",),
                            extra_skills=(
                                SkillCard(
                                    name="audit-synthesis",
                                    triggers=("audit",),
                                    preferred_route=RouteKind.ONE_SHOT,
                                    required_tools=("read",),
                                    verification_style="document-review",
                                ),
                            ),
                            notes=("Catch repo audit requests as synthesis instead of delegated work.",),
                        ),
                    )
                )
            elif "handoff" in idea:
                suggestions.append(
                    MutationSuggestion(
                        name="delegated-handoff-hardening",
                        rationale=idea,
                        mutation=CandidateMutation(
                            name="delegated-handoff-hardening",
                            notes=("Expand delegated handoff assertions for watchouts and verification carryover.",),
                        ),
                    )
                )
            elif "execution checkpoints" in idea:
                suggestions.append(
                    MutationSuggestion(
                        name="checkpoint-rhythm-alignment",
                        rationale=idea,
                        mutation=CandidateMutation(
                            name="checkpoint-rhythm-alignment",
                            notes=("Reconcile expected checkpoint order with route policy for missed cases.",),
                        ),
                    )
                )
            else:
                slug = idea.replace(" ", "-")[:48]
                suggestions.append(
                    MutationSuggestion(
                        name=slug,
                        rationale=idea,
                        mutation=CandidateMutation(name=slug, notes=(idea,)),
                    )
                )

        return tuple(suggestions)

    def write_json_report(self, record: LoopRunRecord, path: str | Path) -> Path:
        target = Path(path)
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(json.dumps(record.to_dict(), indent=2) + "\n")
        return target

    def write_markdown_report(self, record: LoopRunRecord, path: str | Path) -> Path:
        target = Path(path)
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(self.render_markdown(record))
        return target

    def render_markdown(self, record: LoopRunRecord) -> str:
        lines = [
            "# Behavior loop run",
            "",
            f"- Created at: {record.created_at}",
            f"- Candidate: {record.report.candidate}",
            f"- Score: {record.report.total_score}/{record.report.max_score}",
            f"- Summary: {record.report.summary}",
            "",
            "## Case outcomes",
        ]
        for outcome in record.report.outcomes:
            status = "pass" if outcome.passed else "fail"
            lines.append(f"- {outcome.case_name}: {status} ({outcome.score}/4)")
            for failure in outcome.failures:
                lines.append(f"  - {failure}")

        lines.extend(["", "## Next loop plan"])
        lines.append(f"- Strengths: {', '.join(record.plan.strengths) or 'none'}")
        lines.append(f"- Gaps: {', '.join(record.plan.gaps) or 'none'}")
        lines.append(f"- Next mutations: {', '.join(record.plan.next_mutations) or 'none'}")

        lines.extend(["", "## Suggested candidate mutations"])
        if record.suggestions:
            for suggestion in record.suggestions:
                lines.append(f"- {suggestion.name}: {suggestion.rationale}")
        else:
            lines.append("- none")

        return "\n".join(lines) + "\n"
