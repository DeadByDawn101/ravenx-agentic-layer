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
    assert result.verification.risk_notes == ["no verification command supplied"]
