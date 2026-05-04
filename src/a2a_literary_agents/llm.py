"""LLM adapters for model-agents.

The runner supports real OpenAI-compatible chat completions, but the protocol
does not depend on a live model. Mock mode is used for deterministic fixtures
and tests.
"""

from __future__ import annotations

import json
import os
import subprocess
import tempfile
import urllib.error
import urllib.request
from dataclasses import dataclass
from typing import Any

from .config import RunnerConfig
from .json_util import parse_json_object


@dataclass
class AgentCompletion:
    agent_name: str
    mode: str
    prompt: str
    raw_output: str
    parsed_output: dict[str, Any] | None
    error: str | None = None


class AgentProvider:
    def complete(self, agent_name: str, prompt: str, fixture: dict[str, Any]) -> AgentCompletion:
        raise NotImplementedError


class MockAgentProvider(AgentProvider):
    def complete(self, agent_name: str, prompt: str, fixture: dict[str, Any]) -> AgentCompletion:
        output = fixture.get("mock_agent_outputs", {}).get(agent_name)
        if output is None:
            output = {
                "agent": agent_name,
                "status": "mock_missing",
                "summary": f"No mock output configured for {agent_name}.",
            }
        raw = json.dumps(output, ensure_ascii=False, indent=2, sort_keys=True)
        return AgentCompletion(
            agent_name=agent_name,
            mode="mock",
            prompt=prompt,
            raw_output=raw,
            parsed_output=output,
        )


class OpenAICompatibleAgentProvider(AgentProvider):
    def __init__(self, config: RunnerConfig):
        self.config = config
        self.calls_made = 0

    def complete(self, agent_name: str, prompt: str, fixture: dict[str, Any]) -> AgentCompletion:
        if not self.config.api_key:
            return AgentCompletion(
                agent_name=agent_name,
                mode="real",
                prompt=prompt,
                raw_output="",
                parsed_output=None,
                error="missing_api_key",
            )
        if self.calls_made >= self.config.max_llm_calls_per_trace:
            return AgentCompletion(
                agent_name=agent_name,
                mode="real",
                prompt=prompt,
                raw_output="",
                parsed_output=None,
                error="max_llm_calls_exceeded",
            )

        self.calls_made += 1
        payload: dict[str, Any] = {
            "model": self.config.model,
            "messages": [
                {
                    "role": "system",
                    "content": (
                        "You are one bounded model-agent inside the a2a-literary-agents protocol. "
                        "Use only the projected context in the user message. Return valid JSON only. "
                        "Do not invent hidden facts, broaden visibility, or bypass authority boundaries."
                    ),
                },
                {"role": "user", "content": prompt},
            ],
            "temperature": self.config.temperature,
        }
        payload[self.config.token_field] = self.config.max_tokens_for(agent_name)

        request = urllib.request.Request(
            url=f"{self.config.base_url.rstrip('/')}/chat/completions",
            data=json.dumps(payload).encode("utf-8"),
            headers={
                "Authorization": f"Bearer {self.config.api_key}",
                "Content-Type": "application/json",
            },
            method="POST",
        )

        try:
            with urllib.request.urlopen(request, timeout=self.config.timeout_seconds) as response:
                body = json.loads(response.read().decode("utf-8"))
        except urllib.error.HTTPError as exc:
            detail = exc.read().decode("utf-8", errors="replace")
            return AgentCompletion(agent_name, "real", prompt, detail, None, f"http_error_{exc.code}")
        except Exception as exc:  # pragma: no cover - environment dependent
            return AgentCompletion(agent_name, "real", prompt, "", None, f"request_error: {exc}")

        raw = body.get("choices", [{}])[0].get("message", {}).get("content", "")
        parsed, parse_error = parse_json_object(raw)
        return AgentCompletion(
            agent_name=agent_name,
            mode="real",
            prompt=prompt,
            raw_output=raw,
            parsed_output=parsed,
            error=parse_error,
        )


class CodexCliAgentProvider(AgentProvider):
    """Use an isolated headless Codex CLI process as the model backend."""

    def __init__(self, config: RunnerConfig):
        self.config = config
        self.calls_made = 0

    def complete(self, agent_name: str, prompt: str, fixture: dict[str, Any]) -> AgentCompletion:
        if self.calls_made >= self.config.max_llm_calls_per_trace:
            return AgentCompletion(
                agent_name=agent_name,
                mode="codex-cli",
                prompt=prompt,
                raw_output="",
                parsed_output=None,
                error="max_llm_calls_exceeded",
            )

        self.calls_made += 1
        os.makedirs(self.config.codex_home, exist_ok=True)
        os.makedirs(self.config.codex_workdir, exist_ok=True)

        with tempfile.TemporaryDirectory(prefix=f"a2a_codex_{agent_name}_") as tmp:
            output_path = os.path.join(tmp, "last-message.json")

            command = [
                self.config.codex_binary,
                "exec",
                "--model",
                self.config.model,
                "--sandbox",
                "read-only",
                "-c",
                "approval_policy=\"never\"",
                "--ephemeral",
                "--ignore-rules",
                "--ignore-user-config",
                "--skip-git-repo-check",
                "--cd",
                self.config.codex_workdir,
                "--output-last-message",
                output_path,
                "--color",
                "never",
                "-",
            ]
            env = _isolated_codex_env(self.config.codex_home)

            try:
                completed = subprocess.run(
                    command,
                    input=_codex_cli_prompt(agent_name, prompt, self.config.max_tokens_for(agent_name)),
                    text=True,
                    encoding="utf-8",
                    errors="replace",
                    capture_output=True,
                    timeout=self.config.timeout_seconds,
                    env=env,
                    cwd=self.config.codex_workdir,
                    check=False,
                )
            except subprocess.TimeoutExpired:
                return AgentCompletion(agent_name, "codex-cli", prompt, "", None, "codex_cli_timeout")
            except FileNotFoundError:
                return AgentCompletion(agent_name, "codex-cli", prompt, "", None, "codex_cli_not_found")
            except Exception as exc:  # pragma: no cover - environment dependent
                return AgentCompletion(agent_name, "codex-cli", prompt, "", None, f"codex_cli_error: {exc}")

            raw = _read_text_if_exists(output_path) or completed.stdout.strip()
            if completed.returncode != 0:
                detail = completed.stderr.strip() or completed.stdout.strip() or f"exit_code={completed.returncode}"
                return AgentCompletion(agent_name, "codex-cli", prompt, raw, None, f"codex_cli_failed: {detail}")

            parsed, parse_error = parse_json_object(raw)
            if parsed and isinstance(parsed.get("payload"), dict):
                parsed = parsed["payload"]
            return AgentCompletion(
                agent_name=agent_name,
                mode="codex-cli",
                prompt=prompt,
                raw_output=raw,
                parsed_output=parsed,
                error=parse_error,
            )


class AutoAgentProvider(AgentProvider):
    def __init__(self, config: RunnerConfig):
        self.real = OpenAICompatibleAgentProvider(config)
        self.mock = MockAgentProvider()
        self.has_key = bool(config.api_key)

    def complete(self, agent_name: str, prompt: str, fixture: dict[str, Any]) -> AgentCompletion:
        if not self.has_key:
            return self.mock.complete(agent_name, prompt, fixture)
        result = self.real.complete(agent_name, prompt, fixture)
        if result.error:
            fallback = self.mock.complete(agent_name, prompt, fixture)
            fallback.mode = "mock_fallback"
            fallback.error = f"real_failed: {result.error}"
            return fallback
        return result


def build_provider(config: RunnerConfig) -> AgentProvider:
    if config.llm_mode == "mock":
        return MockAgentProvider()
    if config.llm_mode == "codex-cli":
        return CodexCliAgentProvider(config)
    if config.llm_mode == "real":
        return OpenAICompatibleAgentProvider(config)
    if config.llm_mode == "auto":
        return AutoAgentProvider(config)
    raise ValueError(f"Unknown llm mode: {config.llm_mode}")


def _generic_json_object_schema() -> dict[str, Any]:
    return {"type": "object", "additionalProperties": True}


def _codex_cli_prompt(agent_name: str, prompt: str, max_output_tokens: int) -> str:
    return (
        "You are being called as a headless model backend for a2a-literary-agents.\n"
        "Do not inspect files, edit files, run shell commands, use network tools, or ask follow-up questions.\n"
        "Return only the JSON object requested by the projected protocol prompt.\n"
        f"Agent name: {agent_name}\n"
        f"Approximate maximum output budget: {max_output_tokens} tokens.\n\n"
        f"{prompt}"
    )


def _isolated_codex_env(codex_home: str) -> dict[str, str]:
    env = dict(os.environ)
    env["CODEX_HOME"] = codex_home
    env["NO_COLOR"] = "1"
    for key in ["CODEX_THREAD_ID", "CODEX_INTERNAL_ORIGINATOR_OVERRIDE", "CODEX_SHELL"]:
        env.pop(key, None)
    return env


def _read_text_if_exists(path: str) -> str:
    try:
        with open(path, "r", encoding="utf-8") as f:
            return f.read().strip()
    except OSError:
        return ""
