"""Deterministic MVP validators."""

from __future__ import annotations

from typing import Any


def validate_plot(packet: dict[str, Any] | None) -> list[dict[str, Any]]:
    violations: list[dict[str, Any]] = []
    if not packet:
        return [_violation("plot_schema", "missing_plot_packet", "Plot Agent did not return a packet.")]

    required = ["pressure_kind", "scope", "duration", "affected_options", "non_forcing_clause", "forbidden_outcomes", "visibility"]
    for field in required:
        if field not in packet or packet.get(field) in (None, "", []):
            violations.append(_violation("plot_schema", "missing_required_field", f"Missing `{field}`."))

    text = _flatten_text({key: value for key, value in packet.items() if key != "forbidden_outcomes"})
    forbidden_phrases = ["must accuse", "must confess", "must choose", "no choice", "force the reveal"]
    for phrase in forbidden_phrases:
        if phrase in text.lower():
            violations.append(_violation("plot_authority", "plot_puppeteering", f"Forbidden pressure phrase: {phrase}"))

    budget = packet.get("budget_cost", {})
    if budget and not isinstance(budget, dict):
        violations.append(_warning("plot_schema", "invalid_budget_cost", "`budget_cost` should be an object when present."))
        budget = {}
    if budget.get("agency_risk") == "high" and not budget.get("relief_available", False):
        violations.append(_violation("plot_budget", "agency_risk_without_relief", "High agency risk requires relief or review."))
    return violations


def validate_dialogue(window: dict[str, Any] | None) -> list[dict[str, Any]]:
    violations: list[dict[str, Any]] = []
    if not window:
        return [_violation("dialogue_schema", "missing_dialogue_window", "Character Agent did not return a DialogueWindow.")]
    if not window.get("speech_acts"):
        violations.append(_violation("dialogue_schema", "empty_speech_acts", "DialogueWindow requires speech acts."))
    text = _flatten_text(window)
    forbidden = ["lin believes wei is guilty", "wei confesses", "the room knows"]
    for phrase in forbidden:
        if phrase in text.lower():
            violations.append(_violation("character_authority", "declared_outcome_or_other_mind", phrase))
    return violations


def validate_world(bundle: dict[str, Any] | None) -> list[dict[str, Any]]:
    violations: list[dict[str, Any]] = []
    if not bundle:
        return [_violation("world_schema", "missing_world_bundle", "World Agent did not return a resolution bundle.")]
    for field in ["resolution", "state_deltas", "visibility_results"]:
        if field not in bundle:
            violations.append(_violation("world_schema", "missing_required_field", f"Missing `{field}`."))
    resolution = bundle.get("resolution", {})
    for field in ["input_refs", "applicable_rules", "constraint_basis", "outcome_type", "outcome_summary", "adjudication_basis"]:
        if field not in resolution:
            violations.append(_violation("world_resolution", "missing_resolution_field", f"Missing `{field}`."))
    return violations


def validate_narration(narrator_output: dict[str, Any] | None, narrator_input: dict[str, Any]) -> list[dict[str, Any]]:
    violations: list[dict[str, Any]] = []
    if not narrator_output:
        return [_violation("narration_schema", "missing_narration", "Narrator Agent did not return output.")]
    prose = str(narrator_output.get("prose", ""))
    if not prose:
        violations.append(_violation("narration_schema", "missing_prose", "Narrator output has no prose field."))

    lowered = prose.lower()
    forbidden_patterns = narrator_input.get("narration_bounds", {}).get("forbidden_claim_patterns", [])
    for pattern in forbidden_patterns:
        if pattern.lower() in lowered:
            violations.append(_violation("narration_grounding", "forbidden_claim", f"Prose contains forbidden claim pattern: {pattern}"))

    if "destiny" in lowered or "inevitable" in lowered:
        violations.append(_violation("narration_grounding", "pressure_as_destiny", "Prose turns pressure into destiny."))
    return violations


def validate_judge(report: dict[str, Any] | None) -> list[dict[str, Any]]:
    violations: list[dict[str, Any]] = []
    if not report:
        return [_violation("judge_schema", "missing_judge_report", "Judge Agent did not return a judge_report.")]

    verdict = report.get("verdict")
    if verdict not in {"allow", "warning", "repair_required", "block"}:
        return [_violation("judge_schema", "invalid_verdict", "`verdict` must be allow, warning, repair_required, or block.")]

    findings = report.get("findings", [])
    if not isinstance(findings, list):
        violations.append(_violation("judge_schema", "invalid_findings", "`findings` must be a list."))
        findings = []

    repairs = report.get("required_repairs", [])
    if not isinstance(repairs, list):
        violations.append(_violation("judge_schema", "invalid_required_repairs", "`required_repairs` must be a list."))

    if verdict == "allow":
        return violations

    if verdict == "warning":
        violations.append(_warning("judge_verdict", "judge_warning", "Judge Agent reported a warning."))
        return violations

    if verdict == "repair_required":
        violations.append(_violation("judge_verdict", "judge_repair_required", "Judge Agent requires repair before player-facing output."))
        return violations

    violations.append(_violation("judge_verdict", "judge_block", "Judge Agent blocked the trace for authority overreach."))
    return violations


def final_decision(validation: dict[str, list[dict[str, Any]]]) -> str:
    for violations in validation.values():
        if has_block(violations):
            return "blocked"
    return "allowed"


def has_block(violations: list[dict[str, Any]]) -> bool:
    return any(item.get("severity") == "block" for item in violations)


def _violation(kind: str, code: str, message: str) -> dict[str, Any]:
    return {
        "severity": "block",
        "kind": kind,
        "code": code,
        "message": message,
    }


def _warning(kind: str, code: str, message: str) -> dict[str, Any]:
    return {
        "severity": "warning",
        "kind": kind,
        "code": code,
        "message": message,
    }


def _flatten_text(value: Any) -> str:
    if isinstance(value, dict):
        return " ".join(_flatten_text(item) for item in value.values())
    if isinstance(value, list):
        return " ".join(_flatten_text(item) for item in value)
    return str(value)
