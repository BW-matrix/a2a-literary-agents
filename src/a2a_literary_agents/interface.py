"""Interface normalization for model-agent payloads.

The protocol prompts ask agents for stable schema names, but real model output
can drift into semantically equivalent aliases. This module is the deterministic
adapter between flexible model output and strict runtime objects.
"""

from __future__ import annotations

from copy import deepcopy
from typing import Any


def normalize_plot_packet(packet: dict[str, Any] | None) -> tuple[dict[str, Any] | None, list[dict[str, Any]]]:
    if not isinstance(packet, dict):
        return packet, []

    normalized = deepcopy(packet)
    notes: list[dict[str, Any]] = []

    budget = normalized.get("budget_cost")
    if isinstance(budget, str):
        normalized["budget_cost"] = {
            "intensity": budget,
            "novelty": "unspecified",
            "stacking_count": 1,
            "relief_available": None,
            "agency_risk": "unknown",
            "source_shape": "string_alias",
        }
        notes.append(
            _note(
                "plot",
                "budget_cost",
                "normalized_string_budget_cost",
                "`budget_cost` string converted into budget object.",
            )
        )

    return normalized, notes


def normalize_dialogue_window(window: dict[str, Any] | None) -> tuple[dict[str, Any] | None, list[dict[str, Any]]]:
    if not isinstance(window, dict):
        return window, []

    normalized = deepcopy(window)
    notes: list[dict[str, Any]] = []

    if "window_id" not in normalized and normalized.get("dialogue_window_id"):
        normalized["window_id"] = normalized["dialogue_window_id"]
        notes.append(_note("character", "window_id", "dialogue_window_id_alias", "Copied `dialogue_window_id` to `window_id`."))

    if "speech_acts" not in normalized and isinstance(normalized.get("candidate_lines"), list):
        normalized["speech_acts"] = [
            {
                "act_id": f"line_{index + 1}",
                "act_type": "candidate_line",
                "text": line,
                "source_shape": "candidate_lines_alias",
            }
            for index, line in enumerate(normalized["candidate_lines"])
        ]
        notes.append(_note("character", "speech_acts", "candidate_lines_alias", "Converted top-level `candidate_lines` into speech acts."))

    return normalized, notes


def normalize_world_bundle(bundle: dict[str, Any] | None) -> tuple[dict[str, Any] | None, list[dict[str, Any]]]:
    if not isinstance(bundle, dict):
        return bundle, []

    normalized = deepcopy(bundle)
    notes: list[dict[str, Any]] = []

    normalized["resolved_events"] = [
        _normalize_resolved_event(item, index, notes)
        for index, item in enumerate(_as_list(normalized.get("resolved_events")))
        if isinstance(item, dict)
    ]
    normalized["state_deltas"] = [
        _normalize_state_delta(item, index, notes)
        for index, item in enumerate(_as_list(normalized.get("state_deltas")))
        if isinstance(item, dict)
    ]
    normalized["visibility_results"] = [
        _normalize_visibility_result(item, index, notes)
        for index, item in enumerate(_as_list(normalized.get("visibility_results")))
        if isinstance(item, dict)
    ]
    normalized["authorized_interiority"] = [
        _normalize_authorized_interiority(item, index, notes)
        for index, item in enumerate(_as_list(normalized.get("authorized_interiority")))
        if isinstance(item, dict)
    ]

    for field in ["publication_candidates", "public_event_deltas", "canon_reveal_candidates", "canon_effects_committed"]:
        if field not in normalized or normalized[field] is None:
            normalized[field] = []
        elif not isinstance(normalized[field], list):
            normalized[field] = [normalized[field]]
            notes.append(_note("world", field, "wrapped_singleton_as_list", f"Wrapped `{field}` singleton as list."))

    return normalized, notes


def _normalize_resolved_event(event: dict[str, Any], index: int, notes: list[dict[str, Any]]) -> dict[str, Any]:
    normalized = deepcopy(event)
    if "event_id" not in normalized:
        normalized["event_id"] = f"event_{index + 1}"
        notes.append(_note("world", "resolved_events.event_id", "generated_event_id", "Generated missing resolved event id."))
    _copy_alias(normalized, "participants", "actors", "world", "resolved_events.actors", notes)
    _copy_alias(normalized, "event_type", "event_kind", "world", "resolved_events.event_kind", notes)
    _copy_alias(normalized, "summary", "outcome", "world", "resolved_events.outcome", notes)
    return normalized


def _normalize_state_delta(delta: dict[str, Any], index: int, notes: list[dict[str, Any]]) -> dict[str, Any]:
    normalized = deepcopy(delta)
    if "delta_id" not in normalized and normalized.get("state_delta_id"):
        normalized["delta_id"] = normalized["state_delta_id"]
        notes.append(_note("world", "state_deltas.delta_id", "state_delta_id_alias", "Copied `state_delta_id` to `delta_id`."))
    if "delta_id" not in normalized:
        normalized["delta_id"] = f"state_delta_{index + 1}"
        notes.append(_note("world", "state_deltas.delta_id", "generated_delta_id", "Generated missing state delta id."))
    _copy_alias(normalized, "target", "target_id", "world", "state_deltas.target_id", notes)
    _copy_alias(normalized, "target_ref", "target_id", "world", "state_deltas.target_id", notes)
    _copy_alias(normalized, "operation", "change_kind", "world", "state_deltas.change_kind", notes)
    _copy_alias(normalized, "change_type", "change_kind", "world", "state_deltas.change_kind", notes)
    _copy_alias(normalized, "value", "after_summary", "world", "state_deltas.after_summary", notes)
    _copy_alias(normalized, "after", "after_summary", "world", "state_deltas.after_summary", notes)
    return normalized


def _normalize_visibility_result(item: dict[str, Any], index: int, notes: list[dict[str, Any]]) -> dict[str, Any]:
    normalized = deepcopy(item)
    if "visibility_result_id" not in normalized:
        if normalized.get("visibility_id"):
            normalized["visibility_result_id"] = normalized["visibility_id"]
            notes.append(_note("world", "visibility_results.visibility_result_id", "visibility_id_alias", "Copied `visibility_id` to `visibility_result_id`."))
        else:
            normalized["visibility_result_id"] = f"visibility_result_{index + 1}"
            notes.append(_note("world", "visibility_results.visibility_result_id", "generated_visibility_result_id", "Generated missing visibility result id."))

    if "observer_refs" not in normalized and "audience" in normalized:
        normalized["observer_refs"] = _as_list(normalized.get("audience"))
        notes.append(_note("world", "visibility_results.observer_refs", "audience_alias", "Copied `audience` to `observer_refs`."))

    if "observer_scope" not in normalized and normalized.get("scope"):
        normalized["observer_scope"] = normalized["scope"]
        notes.append(_note("world", "visibility_results.observer_scope", "scope_alias", "Copied `scope` to `observer_scope`."))

    if "visible_content" not in normalized and normalized.get("summary"):
        normalized["visible_content"] = normalized["summary"]
        notes.append(_note("world", "visibility_results.visible_content", "summary_alias", "Copied `summary` to `visible_content`."))

    return normalized


def _normalize_authorized_interiority(item: dict[str, Any], index: int, notes: list[dict[str, Any]]) -> dict[str, Any]:
    normalized = deepcopy(item)
    if "interiority_id" not in normalized:
        subject = normalized.get("subject_id") or normalized.get("character_id") or "subject"
        normalized["interiority_id"] = f"interiority_{subject}_{index + 1}"
        notes.append(_note("world", "authorized_interiority.interiority_id", "generated_interiority_id", "Generated missing interiority id."))

    _copy_alias(normalized, "character_id", "subject_id", "world", "authorized_interiority.subject_id", notes)

    if "content" not in normalized and isinstance(normalized.get("authorized_contents"), list):
        normalized["content"] = " ".join(str(value) for value in normalized["authorized_contents"])
        notes.append(_note("world", "authorized_interiority.content", "authorized_contents_alias", "Joined `authorized_contents` into `content`."))

    return normalized


def _copy_alias(
    obj: dict[str, Any],
    source: str,
    target: str,
    agent: str,
    field_path: str,
    notes: list[dict[str, Any]],
) -> None:
    if target not in obj and source in obj:
        obj[target] = obj[source]
        notes.append(_note(agent, field_path, f"{source}_alias", f"Copied `{source}` to `{target}`."))


def _as_list(value: Any) -> list[Any]:
    if value is None:
        return []
    if isinstance(value, list):
        return value
    return [value]


def _note(agent: str, field_path: str, code: str, message: str) -> dict[str, Any]:
    return {
        "agent": agent,
        "field_path": field_path,
        "code": code,
        "message": message,
    }
