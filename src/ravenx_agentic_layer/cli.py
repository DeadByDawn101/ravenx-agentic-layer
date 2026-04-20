from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Sequence

from .looprunner import BehaviorLoopRunner


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="ravenx-agentic-layer")
    subparsers = parser.add_subparsers(dest="command", required=True)

    run_loop = subparsers.add_parser("run-loop", help="run the behavior eval loop once")
    run_loop.add_argument("--json-out", type=Path, help="write a JSON report")
    run_loop.add_argument("--markdown-out", type=Path, help="write a markdown report")
    run_loop.add_argument(
        "--print-markdown",
        action="store_true",
        help="print the markdown report to stdout instead of JSON",
    )

    suggest = subparsers.add_parser("suggest-mutations", help="print next mutation suggestions")
    suggest.add_argument("--json", action="store_true", help="print suggestions as JSON")
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    runner = BehaviorLoopRunner()

    if args.command == "run-loop":
        record = runner.run_once()
        if args.json_out:
            runner.write_json_report(record, args.json_out)
        if args.markdown_out:
            runner.write_markdown_report(record, args.markdown_out)

        if args.print_markdown:
            print(runner.render_markdown(record), end="")
        else:
            print(json.dumps(record.to_dict(), indent=2))
        return 0

    if args.command == "suggest-mutations":
        record = runner.run_once()
        suggestions = [
            {
                "name": suggestion.name,
                "rationale": suggestion.rationale,
                "notes": list(suggestion.mutation.notes),
            }
            for suggestion in record.suggestions
        ]
        if args.json:
            print(json.dumps(suggestions, indent=2))
        else:
            for suggestion in suggestions:
                print(f"{suggestion['name']}: {suggestion['rationale']}")
        return 0

    parser.error(f"unknown command: {args.command}")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
