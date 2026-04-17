from ravenx_agentic_layer import AgenticLayerRuntime, OpenClawAdapter, RouteKind, TaskRequest


def test_direct_edit_route_for_bounded_change() -> None:
    runtime = AgenticLayerRuntime()
    request = TaskRequest(
        task="implement retry handling",
        scope=["src/sender.ts", "tests/sender.test.ts"],
        constraints=["preserve API"],
        verification=["bun test tests/sender.test.ts"],
        deliverable="passing tests and summary",
    )

    result = runtime.run(request)

    assert result.route.kind is RouteKind.DIRECT_EDIT
    assert result.skill == "repo-coding-loop"
    assert result.verification.commands == ["bun test tests/sender.test.ts"]
    assert result.execution.name == "tight-edit"
    assert result.execution.rhythm.checkpoints == (
        "inspect-target-files",
        "apply-change",
        "run-requested-checks",
    )
    assert [event.kind for event in result.events] == [
        "task.accepted",
        "route.selected",
        "skill.matched",
        "verification.planned",
        "execution.ready",
        "task.completed",
    ]


def test_delegated_route_for_broader_change() -> None:
    runtime = AgenticLayerRuntime()
    request = TaskRequest(
        task="scaffold a new agentic layer across routing, profiles, runtime, and tests",
        scope=["router.py", "runtime.py", "profiles.py", "tests/test_runtime.py"],
        verification=["pytest tests/test_runtime.py", "pytest tests/test_router.py", "python -m compileall src"],
        deliverable="scaffold with passing tests",
    )

    result = runtime.run(request)

    assert result.route.kind is RouteKind.DELEGATED_LOOP
    assert "scope spans multiple files or modules" in result.route.reasons
    assert result.execution.name == "delegated-rhythm"
    assert "broad scope may need integration verification" in result.verification.risk_notes


def test_openclaw_behavior_payload_exposes_skill_and_execution_rhythm() -> None:
    runtime = AgenticLayerRuntime()
    adapter = OpenClawAdapter()
    request = TaskRequest(
        task="implement retry handling",
        scope=["src/sender.ts", "tests/sender.test.ts"],
        verification=["bun test tests/sender.test.ts"],
        deliverable="passing tests and summary",
    )

    result = runtime.run(request)
    behavior = adapter.build_behavior(result)

    assert behavior["skill_card"] == "repo-coding-loop"
    assert behavior["model_family"] == "local_tool_caller"
    assert behavior["execution_rhythm"] == {
        "mode": "single_pass",
        "checkpoints": ["inspect-target-files", "apply-change", "run-requested-checks"],
    }
