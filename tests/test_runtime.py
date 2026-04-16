from ravenx_agentic_layer import AgenticLayerRuntime, RouteKind, TaskRequest


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
    assert "broad scope may need integration verification" in result.verification.risk_notes
