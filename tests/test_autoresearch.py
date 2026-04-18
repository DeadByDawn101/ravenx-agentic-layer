from ravenx_agentic_layer import (
    DEFAULT_BEHAVIOR_EVALS,
    BehaviorEvalHarness,
    CandidateMutation,
    RouteKind,
    SkillCard,
)


def test_behavior_eval_harness_scores_baseline_cases() -> None:
    harness = BehaviorEvalHarness()

    report = harness.evaluate(DEFAULT_BEHAVIOR_EVALS)
    plan = harness.plan_next_loop(report)

    assert report.candidate == "baseline"
    assert report.total_score == report.max_score
    assert report.summary == "baseline passed 3/3 cases"
    assert len(plan.strengths) == 3
    assert plan.gaps == ()
    assert plan.next_mutations == ("raise case difficulty with broader multi-tool or handoff-heavy tasks",)


def test_candidate_mutation_can_add_new_summary_trigger_and_skill() -> None:
    harness = BehaviorEvalHarness()
    case = DEFAULT_BEHAVIOR_EVALS[1]
    mutated_case = case.__class__(
        name="audit request becomes synthesis",
        request=case.request.__class__(
            task="audit the repos and produce an intake summary",
            deliverable="comparative memo",
        ),
        expected_route=RouteKind.ONE_SHOT,
        expected_skill="audit-synthesis",
        expect_handoff=False,
        expected_checkpoints=("gather-context", "compose-answer"),
    )
    mutation = CandidateMutation(
        name="audit-synthesis-candidate",
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
    )

    report = harness.evaluate((mutated_case,), mutation=mutation)

    assert report.summary == "audit-synthesis-candidate passed 1/1 cases"
    assert report.total_score == 4.0


def test_behavior_loop_plan_calls_out_missed_route_signal() -> None:
    harness = BehaviorEvalHarness()
    tricky_case = DEFAULT_BEHAVIOR_EVALS[0].__class__(
        name="rename task needs route help",
        request=DEFAULT_BEHAVIOR_EVALS[0].request.__class__(
            task="rename sender internals safely",
            scope=["src/sender.ts", "tests/sender.test.ts"],
            verification=["bun test tests/sender.test.ts"],
            deliverable="code changes complete",
        ),
        expected_route=RouteKind.DIRECT_EDIT,
        expected_skill=None,
        expect_handoff=False,
        expected_checkpoints=("inspect-target-files", "apply-change", "run-requested-checks"),
    )

    report = harness.evaluate((tricky_case,))
    plan = harness.plan_next_loop(report)

    assert report.total_score == 2.0
    assert plan.gaps == (
        "repair rename task needs route help: route expected direct_edit but saw delegated_loop; checkpoint mismatch: expected ('inspect-target-files', 'apply-change', 'run-requested-checks') but saw ('map-scope', 'apply-batch', 'verify-milestone', 'summarize-delta')",
    )
    assert "adjust routing keywords or add a stronger route policy signal" in plan.next_mutations
    assert "align execution checkpoints with the expected rhythm" in plan.next_mutations
