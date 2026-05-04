"""Deterministic context projection.

This module is the MVP enforcement point for the rule:

complete objects are system objects; model-agents receive projected views.
"""

from __future__ import annotations

from typing import Any


def _public_slice(fixture: dict[str, Any]) -> dict[str, Any]:
    return {
        "scene_id": fixture["scene_id"],
        "window_id": fixture["window_id"],
        "user_request": fixture["user_request"],
        "public_canon": fixture.get("public_canon", []),
        "public_event_ledger": fixture.get("public_event_ledger", []),
    }


def plot_context(fixture: dict[str, Any]) -> tuple[dict[str, Any], dict[str, Any]]:
    context = _public_slice(fixture)
    context.update(
        {
            "context_type": "PlotContextSummary",
            "structure_goal": fixture.get("structure_goal"),
            "relationship_summary": fixture.get("relationship_summary", {}),
            "pressure_history": fixture.get("pressure_history", []),
            "forbidden_sources": ["raw_world_state_ledger", "private_memory", "latent_canon"],
        }
    )
    manifest = {
        "projection_type": "PlotContextSummary",
        "recipient": "plot_agent",
        "included_refs": ["public_canon", "public_event_ledger", "structure_goal", "relationship_summary"],
        "excluded_refs": ["world_state_ledger", "private_memory", "latent_canon"],
        "redaction_rule": "exclude raw hidden truth and private cognition",
    }
    return context, manifest


def character_context(fixture: dict[str, Any], pressure_packet: dict[str, Any]) -> tuple[dict[str, Any], dict[str, Any]]:
    character_id = fixture["active_character_id"]
    character = fixture["characters"][character_id]
    context = _public_slice(fixture)
    context.update(
        {
            "context_type": "CharacterContextPacket",
            "recipient_agent_id": character_id,
            "visible_observations": fixture.get("visible_observations", {}).get(character_id, []),
            "private_memory_query": character.get("private_memory", []),
            "public_pressure": _public_pressure_view(pressure_packet),
            "forbidden_sources": ["raw_world_state_ledger", "other_private_memory", "latent_canon", "full_scene_packet"],
        }
    )
    manifest = {
        "projection_type": "CharacterContextPacket",
        "recipient": character_id,
        "included_refs": ["own_private_memory", "visible_observations", "public_canon", "public_pressure"],
        "excluded_refs": ["world_state_ledger", "other_private_memory", "latent_canon"],
        "redaction_rule": "owner-only memory and visible scene facts",
    }
    return context, manifest


def world_context(
    fixture: dict[str, Any],
    pressure_packet: dict[str, Any],
    dialogue_window: dict[str, Any],
) -> tuple[dict[str, Any], dict[str, Any]]:
    context = {
        "context_type": "WorldResolutionContext",
        "scene_id": fixture["scene_id"],
        "window_id": fixture["window_id"],
        "resolver_view": _dialogue_resolver_view(dialogue_window),
        "scene_pressure_packet": pressure_packet,
        "world_state_slice": fixture.get("world_state_ledger", {}),
        "public_canon": fixture.get("public_canon", []),
        "latent_canon_resolution_refs": fixture.get("latent_canon_resolution_refs", []),
        "forbidden_actions": [
            "write character inner truth",
            "publish without threshold",
            "promote canon without Canon Steward",
            "treat plot pressure as destiny",
        ],
    }
    manifest = {
        "projection_type": "WorldResolutionContext",
        "recipient": "world_agent",
        "included_refs": ["resolver_view", "scene_pressure_packet", "world_state_slice", "public_canon"],
        "excluded_refs": ["raw_private_memory", "narrator_draft"],
        "redaction_rule": "world may inspect state and transformed proposals, not raw private cognition",
    }
    return context, manifest


def narrator_input(scene_packet: dict[str, Any]) -> tuple[dict[str, Any], dict[str, Any]]:
    packet = {
        "context_type": "NarratorInputPacket",
        "packet_id": scene_packet["packet_id"],
        "scene_id": scene_packet["scene_id"],
        "window_id": scene_packet["window_id"],
        "pov_contract": scene_packet.get("pov_contract", {}),
        "resolved_events": scene_packet.get("resolved_events", []),
        "visibility_deltas": scene_packet.get("visibility_deltas", []),
        "authorized_interiority": scene_packet.get("authorized_interiority", []),
        "public_event_deltas": scene_packet.get("public_event_deltas", []),
        "canon_effects_committed": scene_packet.get("canon_effects_committed", []),
        "narration_bounds": scene_packet.get("narration_bounds", {}),
        "forbidden_sources": ["raw_world_state_ledger", "raw_dialogue_window", "publication_candidates", "canon_reveal_candidates"],
    }
    manifest = {
        "projection_type": "NarratorInputPacket",
        "recipient": "narrator_agent",
        "included_refs": ["resolved_events", "visibility_deltas", "authorized_interiority", "narration_bounds"],
        "excluded_refs": ["publication_candidates", "canon_reveal_candidates", "world_state_ledger", "raw_dialogue_window"],
        "redaction_rule": "exclude candidates and raw hidden truth from narration",
    }
    return packet, manifest


def canon_review_context(scene_packet: dict[str, Any]) -> tuple[dict[str, Any] | None, dict[str, Any] | None]:
    candidates = scene_packet.get("canon_reveal_candidates", [])
    if not candidates:
        return None, None
    context = {
        "context_type": "CanonReviewContext",
        "scene_id": scene_packet["scene_id"],
        "candidate_refs": candidates,
        "based_on": scene_packet.get("based_on", []),
    }
    manifest = {
        "projection_type": "CanonReviewContext",
        "recipient": "canon_steward",
        "included_refs": ["canon_reveal_candidates", "based_on"],
        "excluded_refs": ["irrelevant_private_memory", "narrator_draft"],
        "redaction_rule": "canon review sees only canon-relevant committed evidence",
    }
    return context, manifest


def judge_review_context(trace: dict[str, Any], narrator_output: dict[str, Any] | None) -> tuple[dict[str, Any], dict[str, Any]]:
    context = {
        "context_type": "JudgeReviewContext",
        "review_scope": "authority_overreach_only",
        "instructions": [
            "Judge does not create plot, prose, canon, memory, or world outcomes.",
            "Judge checks whether any agent output exceeded its authority.",
            "Judge may recommend repair, but must not rewrite content.",
            "Judge should distinguish recoverable schema issues from authority leaks.",
        ],
        "trace_id": trace["trace_id"],
        "llm_mode": trace.get("llm_mode"),
        "projection_manifests": trace.get("projection_manifests", []),
        "agent_runs": [
            {
                "agent_name": run.get("agent_name"),
                "projected_context": run.get("projected_context"),
                "parsed_output": run.get("parsed_output"),
                "error": run.get("error"),
            }
            for run in trace.get("agent_runs", [])
            if run.get("agent_name") != "judge"
        ],
        "program_validation": trace.get("validation", {}),
        "scene_packet": trace.get("scene_packet"),
        "narrator_output": narrator_output,
        "judge_policy": {
            "allow": "no meaningful authority overreach detected",
            "warning": "minor recoverable schema or wording risk, no repair required",
            "repair_required": "specific agent should retry before player-facing output",
            "block": "serious authority leak or unsafe claim; do not return prose",
        },
        "required_output_shape": {
            "judge_report": {
                "verdict": "allow | warning | repair_required | block",
                "findings": [
                    {
                        "finding_id": "short stable id",
                        "severity": "info | warning | repair_required | block",
                        "agent": "plot | character | world | narrator | orchestrator | memory",
                        "issue": "what went wrong",
                        "basis": "which input/output/source refs justify this finding",
                    }
                ],
                "required_repairs": [
                    {
                        "target_agent": "agent to retry",
                        "repair_instruction": "what must change without adding new story facts",
                    }
                ],
            }
        },
    }
    manifest = {
        "projection_type": "JudgeReviewContext",
        "recipient": "judge_agent",
        "included_refs": ["projection_manifests", "agent_runs", "program_validation", "scene_packet", "narrator_output"],
        "excluded_refs": ["raw_secret_files", "runtime_auth_tokens"],
        "redaction_rule": "judge may inspect protocol audit material but may not author or mutate story material",
    }
    return context, manifest


def owner_projection(scene_packet: dict[str, Any], owner_agent_id: str) -> dict[str, Any]:
    visible_events = [
        event["event_id"]
        for event in scene_packet.get("resolved_events", [])
        if owner_agent_id in event.get("actors", []) or event.get("visibility") in {owner_agent_id, "scene_pair", "scene_public"}
    ]
    owner_visibility = [
        item["visibility_result_id"]
        for item in scene_packet.get("visibility_deltas", [])
        if owner_agent_id in item.get("observer_refs", []) or item.get("observer_scope") in {owner_agent_id, "scene_pair", "scene_public"}
    ]
    return {
        "owner_agent_id": owner_agent_id,
        "visible_events": visible_events,
        "owner_impacts": [
            delta["delta_id"]
            for delta in scene_packet.get("state_deltas", [])
            if delta.get("target_id") == owner_agent_id
        ],
        "owner_visibility": owner_visibility,
        "authorized_inner_material": [
            item["interiority_id"]
            for item in scene_packet.get("authorized_interiority", [])
            if item.get("subject_id") == owner_agent_id
        ],
        "public_contact": [],
    }


def _public_pressure_view(pressure_packet: dict[str, Any]) -> dict[str, Any]:
    if not pressure_packet:
        return {}
    return {
        "pressure_kind": pressure_packet.get("pressure_kind"),
        "scope": pressure_packet.get("scope"),
        "duration": pressure_packet.get("duration"),
        "affected_options": pressure_packet.get("affected_options", []),
        "non_forcing_clause": pressure_packet.get("non_forcing_clause"),
    }


def _dialogue_resolver_view(dialogue_window: dict[str, Any]) -> dict[str, Any]:
    allowed = [
        "window_kind",
        "speaker_id",
        "addressee_ids",
        "local_goal",
        "stance",
        "disclosure_policy",
        "speech_acts",
        "fallback_if_blocked",
        "exit_condition",
    ]
    return {key: dialogue_window.get(key) for key in allowed if key in dialogue_window}
