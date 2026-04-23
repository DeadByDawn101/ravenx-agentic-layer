from ravenx_agentic_layer import AgenticLayerRuntime, RouteKind, TaskRequest


def test_one_shot_route_for_pure_synthesis() -> None:
    runtime = AgenticLayerRuntime()
    request = TaskRequest(
        task="compare the repos and produce an intake summary",
        deliverable="comparative memo",
    )

    result = runtime.run(request)

    assert result.route.kind is RouteKind.ONE_SHOT
    assert result.skill == "intake-synthesis"
    assert result.execution.name == "synthesis-pass"
    assert result.verification.risk_notes == ["no verification command supplied"]
    assert result.route.reasons == ["task is synthesis-oriented and does not require explicit file mutation"]


def test_verification_burden_pushes_bounded_scope_into_delegated_loop() -> None:
    runtime = AgenticLayerRuntime()
    request = TaskRequest(
        task="resume checkout recovery implementation",
        scope=["runtime.py", "openclaw.py", "tests/test_runtime.py"],
        verification=["pytest tests/test_runtime.py", "pytest tests/test_autoresearch.py", "python -m compileall src"],
        deliverable="updated code and handoff",
    )

    result = runtime.run(request)

    assert result.route.kind is RouteKind.DELEGATED_LOOP
    assert result.route.reasons == ["verification burden is non-trivial"]
