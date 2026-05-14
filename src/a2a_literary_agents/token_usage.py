"""Token usage recording helpers.

The runner can consume exact provider usage when a backend returns it. Some
early backends, especially the isolated Codex CLI process mode, do not expose
usage metadata, so this module also provides a small deterministic estimator.
"""

from __future__ import annotations

import math
import re
from typing import Any


ESTIMATOR_NAME = "cjk_aware_char_estimator_v0.1"
_CJK_RE = re.compile(r"[\u3400-\u4dbf\u4e00-\u9fff\uf900-\ufaff]")


def estimate_tokens(text: str | None) -> int:
    """Estimate tokens for trace accounting without external dependencies.

    This is not a tokenizer. It is intentionally conservative enough for
    budget telemetry: CJK characters count roughly as one token each, while
    non-CJK text is approximated at four characters per token.
    """

    if not text:
        return 0

    cjk_count = len(_CJK_RE.findall(text))
    non_cjk_count = max(0, len(text) - cjk_count)
    estimate = cjk_count + math.ceil(non_cjk_count / 4)
    return max(1, estimate)


def build_token_usage(
    *,
    agent_name: str,
    mode: str,
    model: str,
    input_text: str,
    output_text: str,
    max_output_tokens: int | None,
    provider_usage: dict[str, Any] | None = None,
    input_text_basis: str = "provider_input",
) -> dict[str, Any]:
    """Build one per-agent usage record.

    `provider_usage` wins when it contains recognizable input and output
    counts. Otherwise the record is explicitly marked as locally estimated.
    """

    estimated_input = estimate_tokens(input_text)
    estimated_output = estimate_tokens(output_text)
    normalized = _normalize_provider_usage(provider_usage)

    if normalized:
        input_tokens = normalized.get("input_tokens", estimated_input)
        output_tokens = normalized.get("output_tokens", estimated_output)
        total_tokens = normalized.get("total_tokens", input_tokens + output_tokens)
        source = "provider_usage"
        is_estimated = False
    else:
        input_tokens = estimated_input
        output_tokens = estimated_output
        total_tokens = input_tokens + output_tokens
        source = "estimated_local"
        is_estimated = True

    record: dict[str, Any] = {
        "agent_name": agent_name,
        "mode": mode,
        "model": model,
        "source": source,
        "is_estimated": is_estimated,
        "input_tokens": input_tokens,
        "output_tokens": output_tokens,
        "total_tokens": total_tokens,
        "max_output_tokens": max_output_tokens,
        "input_text_basis": input_text_basis,
    }
    if is_estimated:
        record["estimator"] = ESTIMATOR_NAME
    if max_output_tokens is not None:
        record["output_budget_remaining"] = max_output_tokens - output_tokens
    if provider_usage:
        record["provider_usage_raw"] = provider_usage
    return record


def summarize_token_usage(trace: dict[str, Any]) -> None:
    """Populate aggregate token totals in-place."""

    usage = trace.setdefault("token_usage", {})
    agents = usage.setdefault("agents", [])
    totals = {
        "input_tokens": sum(_as_int(item.get("input_tokens")) for item in agents),
        "output_tokens": sum(_as_int(item.get("output_tokens")) for item in agents),
        "total_tokens": sum(_as_int(item.get("total_tokens")) for item in agents),
        "exact_agent_count": sum(1 for item in agents if not item.get("is_estimated")),
        "estimated_agent_count": sum(1 for item in agents if item.get("is_estimated")),
        "agent_count": len(agents),
        "sources": sorted({str(item.get("source")) for item in agents if item.get("source")}),
    }

    total_output_budget = usage.get("budget", {}).get("total_output_token_budget")
    if isinstance(total_output_budget, int):
        totals["total_output_token_budget"] = total_output_budget
        totals["output_budget_remaining"] = total_output_budget - totals["output_tokens"]
        totals["output_budget_used_ratio"] = (
            round(totals["output_tokens"] / total_output_budget, 4)
            if total_output_budget > 0
            else None
        )

    usage["totals"] = totals


def _normalize_provider_usage(provider_usage: dict[str, Any] | None) -> dict[str, int] | None:
    if not isinstance(provider_usage, dict):
        return None

    input_tokens = _optional_int(provider_usage.get("input_tokens"))
    if input_tokens is None:
        input_tokens = _optional_int(provider_usage.get("prompt_tokens"))

    output_tokens = _optional_int(provider_usage.get("output_tokens"))
    if output_tokens is None:
        output_tokens = _optional_int(provider_usage.get("completion_tokens"))

    total_tokens = _optional_int(provider_usage.get("total_tokens"))
    if total_tokens is None and input_tokens is not None and output_tokens is not None:
        total_tokens = input_tokens + output_tokens

    if input_tokens is None and output_tokens is None and total_tokens is None:
        return None

    normalized: dict[str, int] = {}
    if input_tokens is not None:
        normalized["input_tokens"] = input_tokens
    if output_tokens is not None:
        normalized["output_tokens"] = output_tokens
    if total_tokens is not None:
        normalized["total_tokens"] = total_tokens
    return normalized


def _optional_int(value: Any) -> int | None:
    if isinstance(value, bool):
        return None
    if isinstance(value, int):
        return value
    if isinstance(value, float) and value.is_integer():
        return int(value)
    return None


def _as_int(value: Any) -> int:
    return value if isinstance(value, int) else 0
