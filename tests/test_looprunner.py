import json
from pathlib import Path

from ravenx_agentic_layer import BehaviorLoopRunner
from ravenx_agentic_layer.cli import main


def test_behavior_loop_runner_generates_report_and_default_suggestion() -> None:
    runner = BehaviorLoopRunner()

    record = runner.run_once()

    assert record.report.summary == "baseline passed 5/5 cases"
    assert record.plan.next_mutations == ("raise case difficulty with broader multi-tool or handoff-heavy tasks",)
    assert record.suggestions[0].name.startswith("raise-case-difficulty")


def test_behavior_loop_runner_writes_json_and_markdown_reports(tmp_path: Path) -> None:
    runner = BehaviorLoopRunner()
    record = runner.run_once()

    json_path = runner.write_json_report(record, tmp_path / "reports" / "loop.json")
    markdown_path = runner.write_markdown_report(record, tmp_path / "reports" / "loop.md")

    payload = json.loads(json_path.read_text())
    markdown = markdown_path.read_text()

    assert payload["report"]["summary"] == "baseline passed 5/5 cases"
    assert payload["report"]["pass_rate"] == 1.0
    assert payload["report"]["failed_cases"] == []
    assert payload["suggestions"][0]["name"].startswith("raise-case-difficulty")
    assert "# Behavior loop run" in markdown
    assert "- Pass rate: 100.00%" in markdown
    assert "## Suggested candidate mutations" in markdown


def test_cli_run_loop_writes_requested_outputs(tmp_path: Path, capsys) -> None:
    json_path = tmp_path / "out" / "loop.json"
    markdown_path = tmp_path / "out" / "loop.md"

    exit_code = main(["run-loop", "--json-out", str(json_path), "--markdown-out", str(markdown_path)])
    stdout = capsys.readouterr().out

    assert exit_code == 0
    assert json.loads(stdout)["report"]["summary"] == "baseline passed 5/5 cases"
    assert json_path.exists()
    assert markdown_path.exists()


def test_cli_suggest_mutations_plain_text(capsys) -> None:
    exit_code = main(["suggest-mutations"])
    stdout = capsys.readouterr().out

    assert exit_code == 0
    assert "raise-case-difficulty" in stdout
