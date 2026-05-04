"""Human-readable trace reports."""

from __future__ import annotations

from typing import Any

from .json_util import stable_json


def write_report(path: str, trace: dict[str, Any]) -> None:
    lines: list[str] = []
    lines.append(f"# Trace Report: {trace['trace_id']}")
    lines.append("")
    lines.append(f"- Final decision: `{trace.get('final_decision', 'unknown')}`")
    lines.append(f"- LLM mode: `{trace.get('llm_mode')}`")
    lines.append(f"- Model: `{trace.get('model')}`")
    lines.append("")

    lines.append("## Projection Manifests")
    lines.append("")
    for manifest in trace.get("projection_manifests", []):
        lines.append("```json")
        lines.append(stable_json(manifest))
        lines.append("```")
        lines.append("")

    lines.append("## Agent Runs")
    lines.append("")
    for run in trace.get("agent_runs", []):
        lines.append(f"### {run['agent_name']} Agent")
        lines.append("")
        lines.append("#### Projected Context")
        lines.append("```json")
        lines.append(stable_json(run.get("projected_context")))
        lines.append("```")
        lines.append("")
        lines.append("#### Raw Output")
        lines.append("```json")
        lines.append(run.get("raw_output") or "")
        lines.append("```")
        if run.get("error"):
            lines.append("")
            lines.append(f"- Error: `{run['error']}`")
        lines.append("")

    if "scene_packet" in trace:
        lines.append("## Sealed ScenePacket")
        lines.append("")
        lines.append("```json")
        lines.append(stable_json(trace["scene_packet"]))
        lines.append("```")
        lines.append("")

    if "memory_handoff" in trace:
        lines.append("## Memory Handoff")
        lines.append("")
        lines.append("```json")
        lines.append(stable_json(trace["memory_handoff"]))
        lines.append("```")
        lines.append("")

    lines.append("## Validation")
    lines.append("")
    lines.append("```json")
    lines.append(stable_json(trace.get("validation", {})))
    lines.append("```")
    lines.append("")

    with open(path, "w", encoding="utf-8", newline="\n") as handle:
        handle.write("\n".join(lines))
        handle.write("\n")
