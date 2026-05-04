"""Single-window trace runner."""

from __future__ import annotations

import os
from datetime import datetime, timezone
from typing import Any

from .config import RunnerConfig
from .json_util import load_json_file, write_json_file
from .llm import AgentProvider, build_provider
from .projection import (
    canon_review_context,
    character_context,
    judge_review_context,
    narrator_input,
    owner_projection,
    plot_context,
    world_context,
)
from .prompts import build_prompt
from .report import write_report
from .validation import has_block, final_decision, validate_dialogue, validate_judge, validate_narration, validate_plot, validate_world


def run_trace(fixture_path: str, out_dir: str, config: RunnerConfig) -> dict[str, Any]:
    fixture = load_json_file(fixture_path)
    provider = build_provider(config)
    trace_id = fixture["trace_id"]
    run_dir = os.path.join(out_dir, trace_id)
    os.makedirs(run_dir, exist_ok=True)

    trace: dict[str, Any] = {
        "trace_id": trace_id,
        "fixture_path": fixture_path,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "llm_mode": config.llm_mode,
        "model": config.model,
        "agent_runs": [],
        "projection_manifests": [],
        "validation": {},
        "artifacts": {},
    }

    plot_ctx, plot_manifest = plot_context(fixture)
    trace["projection_manifests"].append(plot_manifest)
    plot_output = _call_agent(provider, "plot", plot_ctx, fixture, trace)
    plot_packet = _payload(plot_output, "scene_pressure_packet")
    trace["validation"]["plot"] = validate_plot(plot_packet)
    if has_block(trace["validation"]["plot"]):
        return _finish_trace(trace, run_dir)

    char_ctx, char_manifest = character_context(fixture, plot_packet)
    trace["projection_manifests"].append(char_manifest)
    character_output = _call_agent(provider, "character", char_ctx, fixture, trace)
    dialogue_window = _payload(character_output, "dialogue_window")
    trace["validation"]["character"] = validate_dialogue(dialogue_window)
    if has_block(trace["validation"]["character"]):
        return _finish_trace(trace, run_dir)

    world_ctx, world_manifest = world_context(fixture, plot_packet, dialogue_window)
    trace["projection_manifests"].append(world_manifest)
    world_output = _call_agent(provider, "world", world_ctx, fixture, trace)
    world_bundle = _payload(world_output, "world_resolution_bundle")
    trace["validation"]["world"] = validate_world(world_bundle)
    if has_block(trace["validation"]["world"]):
        return _finish_trace(trace, run_dir)

    scene_packet = _seal_scene_packet(fixture, plot_packet, dialogue_window, world_bundle)
    trace["scene_packet"] = scene_packet
    narrator_ctx, narrator_manifest = narrator_input(scene_packet)
    trace["projection_manifests"].append(narrator_manifest)

    canon_ctx, canon_manifest = canon_review_context(scene_packet)
    if canon_ctx and canon_manifest:
        trace["projection_manifests"].append(canon_manifest)
        canon_output = _call_agent(provider, "canon_steward", canon_ctx, fixture, trace)
        trace["canon_steward_decision"] = canon_output.get("canon_decision")

    narrator_output = _call_agent(provider, "narrator", narrator_ctx, fixture, trace)
    trace["validation"]["narrator"] = validate_narration(narrator_output, narrator_ctx)

    judge_ctx, judge_manifest = judge_review_context(trace, narrator_output)
    trace["projection_manifests"].append(judge_manifest)
    judge_output = _call_agent(provider, "judge", judge_ctx, fixture, trace)
    judge_report = _payload(judge_output, "judge_report")
    trace["judge_report"] = judge_report
    trace["validation"]["judge"] = validate_judge(judge_report)
    if has_block(trace["validation"]["judge"]):
        return _finish_trace(trace, run_dir)

    trace["memory_handoff"] = _derive_memory_handoff(fixture, scene_packet)
    return _finish_trace(trace, run_dir)


def _call_agent(
    provider: AgentProvider,
    agent_name: str,
    projected_context: dict[str, Any],
    fixture: dict[str, Any],
    trace: dict[str, Any],
) -> dict[str, Any] | None:
    prompt = build_prompt(agent_name, projected_context)
    completion = provider.complete(agent_name, prompt, fixture)
    record = {
        "agent_name": agent_name,
        "mode": completion.mode,
        "projected_context": projected_context,
        "prompt": completion.prompt,
        "raw_output": completion.raw_output,
        "parsed_output": completion.parsed_output,
        "error": completion.error,
    }
    trace["agent_runs"].append(record)
    return completion.parsed_output


def _payload(output: dict[str, Any] | None, key: str) -> dict[str, Any] | None:
    if not output:
        return None
    value = output.get(key)
    if isinstance(value, dict):
        return value

    direct_packet_types = {
        "scene_pressure_packet": "ScenePressurePacket",
        "dialogue_window": "DialogueWindow",
        "world_resolution_bundle": "WorldResolutionBundle",
        "canon_decision": "CanonDecision",
        "judge_report": "JudgeReport",
    }
    if output.get("packet_type") == direct_packet_types.get(key):
        return output
    return None


def _seal_scene_packet(
    fixture: dict[str, Any],
    plot_packet: dict[str, Any],
    dialogue_window: dict[str, Any],
    world_bundle: dict[str, Any],
) -> dict[str, Any]:
    resolution = world_bundle["resolution"]
    return {
        "packet_id": f"sp_{fixture['trace_id']}",
        "scene_id": fixture["scene_id"],
        "window_id": fixture["window_id"],
        "packet_scope": "single_window",
        "commit_status": "committed",
        "pov_contract": fixture.get("pov_contract", {"mode": "limited", "interiority_policy": "selective"}),
        "resolved_events": world_bundle.get("resolved_events", []),
        "state_deltas": world_bundle.get("state_deltas", []),
        "visibility_deltas": world_bundle.get("visibility_results", []),
        "publication_candidates": world_bundle.get("publication_candidates", []),
        "public_event_deltas": world_bundle.get("public_event_deltas", []),
        "canon_reveal_candidates": world_bundle.get("canon_reveal_candidates", []),
        "canon_effects_committed": world_bundle.get("canon_effects_committed", []),
        "authorized_interiority": world_bundle.get("authorized_interiority", []),
        "narration_bounds": fixture.get("narration_bounds", {}),
        "based_on": [
            plot_packet.get("pressure_id"),
            dialogue_window.get("window_id"),
            resolution.get("resolution_id"),
        ],
        "sealing_record": {
            "sealed_by": "orchestrator",
            "assembly_rule": "mechanical copy from World output plus fixture narration bounds",
            "excluded_refs": ["raw_world_state_ledger", "raw_dialogue_window", "latent_canon"],
            "candidate_policy": "candidates are retained in system packet but redacted from NarratorInputPacket",
        },
    }


def _derive_memory_handoff(fixture: dict[str, Any], scene_packet: dict[str, Any]) -> dict[str, Any]:
    owners = list(fixture.get("characters", {}).keys())
    projections = [owner_projection(scene_packet, owner) for owner in owners]
    deltas = []
    for projection in projections:
        if projection["owner_visibility"]:
            deltas.append(
                {
                    "delta_id": f"md_{projection['owner_agent_id']}_{scene_packet['packet_id']}",
                    "owner_agent_id": projection["owner_agent_id"],
                    "writer_role": "world_agent",
                    "source_packet_id": scene_packet["packet_id"],
                    "delta_kind": "observation",
                    "acquisition_mode": "noticed",
                    "content": "Owner receives only the visibility-backed slice recorded in owner_projection.",
                    "certainty": "medium",
                    "memory_status": "active",
                    "based_on": projection["owner_visibility"],
                }
            )
    return {
        "owner_projections": projections,
        "derived_memory_deltas": deltas,
    }


def _finish_trace(trace: dict[str, Any], run_dir: str) -> dict[str, Any]:
    trace["final_decision"] = final_decision(trace["validation"])
    trace_path = os.path.join(run_dir, "trace.json")
    report_path = os.path.join(run_dir, "report.md")
    write_json_file(trace_path, trace)
    write_report(report_path, trace)
    trace["artifacts"] = {
        "trace_json": trace_path,
        "report_md": report_path,
    }
    # Persist artifact paths into trace.json as the final step.
    write_json_file(trace_path, trace)
    return trace
