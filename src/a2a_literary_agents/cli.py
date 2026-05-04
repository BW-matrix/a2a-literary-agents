"""Command line interface."""

from __future__ import annotations

import argparse
import sys

from .config import RunnerConfig
from .runner import run_trace


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Run a2a-literary-agents single-window traces.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    run_parser = subparsers.add_parser("run", help="Run one trace fixture.")
    run_parser.add_argument("--fixture", required=True, help="Path to trace fixture JSON.")
    run_parser.add_argument("--out", default="runs", help="Output directory for trace artifacts.")
    run_parser.add_argument("--llm-mode", choices=["mock", "codex-cli", "real", "auto"], default="auto")

    args = parser.parse_args(argv)
    if args.command == "run":
        config = RunnerConfig.from_env(llm_mode=args.llm_mode)
        trace = run_trace(args.fixture, args.out, config)
        print(f"trace_id={trace['trace_id']}")
        print(f"final_decision={trace['final_decision']}")
        print(f"trace_json={trace['artifacts']['trace_json']}")
        print(f"report_md={trace['artifacts']['report_md']}")
        return 0 if trace["final_decision"] == "allowed" else 2

    return 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
