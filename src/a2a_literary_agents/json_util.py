"""JSON helpers used by the runner."""

from __future__ import annotations

import json
import re
from typing import Any


def stable_json(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True)


def load_json_file(path: str) -> dict[str, Any]:
    with open(path, "r", encoding="utf-8") as handle:
        return json.load(handle)


def write_json_file(path: str, value: Any) -> None:
    with open(path, "w", encoding="utf-8", newline="\n") as handle:
        handle.write(stable_json(value))
        handle.write("\n")


def parse_json_object(text: str) -> tuple[dict[str, Any] | None, str | None]:
    """Parse a JSON object from an LLM response.

    The real API path asks agents to return JSON only, but this helper is
    intentionally forgiving for early experimentation.
    """

    cleaned = text.strip()
    if cleaned.startswith("```"):
        cleaned = re.sub(r"^```(?:json)?\s*", "", cleaned)
        cleaned = re.sub(r"\s*```$", "", cleaned)

    try:
        parsed = json.loads(cleaned)
    except json.JSONDecodeError:
        match = re.search(r"\{.*\}", cleaned, flags=re.DOTALL)
        if not match:
            return None, "no_json_object_found"
        try:
            parsed = json.loads(match.group(0))
        except json.JSONDecodeError as exc:
            return None, f"json_decode_error: {exc}"

    if not isinstance(parsed, dict):
        return None, "json_root_is_not_object"
    return parsed, None
