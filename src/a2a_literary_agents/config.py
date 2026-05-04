"""Runtime configuration for the trace runner."""

from __future__ import annotations

import json
import os
from dataclasses import dataclass, field
from pathlib import Path


DEFAULT_AGENT_OUTPUT_TOKENS = {
    "plot": 2000,
    "character": 4000,
    "world": 5000,
    "narrator": 6000,
    "canon_steward": 3000,
    "validator": 3000,
}


@dataclass(frozen=True)
class RunnerConfig:
    llm_mode: str = "auto"
    model: str = "gpt-5.5"
    base_url: str = "https://api.openai.com/v1"
    api_key: str | None = None
    auth_json_path: str | None = None
    codex_binary: str = "codex"
    codex_home: str = ""
    codex_workdir: str = ""
    max_llm_calls_per_trace: int = 8
    total_output_token_budget: int = 35000
    per_agent_max_output_tokens: dict[str, int] = field(default_factory=lambda: dict(DEFAULT_AGENT_OUTPUT_TOKENS))
    timeout_seconds: int = 60
    temperature: float = 0.4
    token_field: str = "max_tokens"

    @classmethod
    def from_env(cls, llm_mode: str = "auto") -> "RunnerConfig":
        tokens = dict(DEFAULT_AGENT_OUTPUT_TOKENS)
        for agent in list(tokens):
            env_name = f"A2A_{agent.upper()}_MAX_OUTPUT_TOKENS"
            if env_name in os.environ:
                tokens[agent] = int(os.environ[env_name])

        auth_json_path = os.environ.get("A2A_LLM_AUTH_JSON") or os.environ.get("CODEX_OAUTH_AUTH_JSON")
        explicit_api_key = (
            os.environ.get("A2A_LLM_BEARER_TOKEN")
            or os.environ.get("A2A_LLM_API_KEY")
            or os.environ.get("OPENAI_API_KEY")
        )

        return cls(
            llm_mode=llm_mode,
            model=os.environ.get("A2A_LLM_MODEL") or os.environ.get("OPENAI_MODEL") or "gpt-5.5",
            base_url=os.environ.get("A2A_LLM_BASE_URL") or os.environ.get("OPENAI_BASE_URL") or "https://api.openai.com/v1",
            api_key=explicit_api_key or load_auth_json_access_token(auth_json_path),
            auth_json_path=auth_json_path,
            codex_binary=os.environ.get("A2A_CODEX_BINARY", "codex"),
            codex_home=os.environ.get("A2A_CODEX_HOME") or str(_repo_root() / ".local" / "codex-cli-home"),
            codex_workdir=os.environ.get("A2A_CODEX_WORKDIR") or str(_repo_root() / ".local" / "codex-cli-workdir"),
            max_llm_calls_per_trace=int(os.environ.get("A2A_MAX_LLM_CALLS_PER_TRACE", "8")),
            total_output_token_budget=int(os.environ.get("A2A_TOTAL_OUTPUT_TOKEN_BUDGET", "35000")),
            per_agent_max_output_tokens=tokens,
            timeout_seconds=int(os.environ.get("A2A_LLM_TIMEOUT_SECONDS", "60")),
            temperature=float(os.environ.get("A2A_LLM_TEMPERATURE", "0.4")),
            token_field=os.environ.get("A2A_LLM_TOKEN_FIELD", "max_tokens"),
        )

    def max_tokens_for(self, agent_name: str) -> int:
        return self.per_agent_max_output_tokens.get(agent_name, 2000)


def load_auth_json_access_token(auth_json_path: str | None) -> str | None:
    """Read a bearer token from a Codex-style OAuth auth.json file.

    The file is a local secret source. The runner only extracts the token and
    never writes it into reports, prompts, or trace artifacts.
    """
    if not auth_json_path:
        return None

    try:
        raw = json.loads(Path(auth_json_path).expanduser().read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None

    if not isinstance(raw, dict):
        return None

    tokens = raw.get("tokens")
    if isinstance(tokens, dict):
        token = tokens.get("access_token")
        if isinstance(token, str) and token.strip():
            return token.strip()

    token = raw.get("access_token") or raw.get("OPENAI_API_KEY")
    if isinstance(token, str) and token.strip():
        return token.strip()

    return None


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[2]
