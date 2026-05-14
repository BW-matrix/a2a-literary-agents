from __future__ import annotations

import json
import os
import shutil
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "src")
if SRC not in sys.path:
    sys.path.insert(0, SRC)

from a2a_literary_agents.config import RunnerConfig
from a2a_literary_agents.llm import CodexCliAgentProvider
from a2a_literary_agents.runner import run_trace
from a2a_literary_agents.token_usage import estimate_tokens
from a2a_literary_agents.validation import validate_plot


class TraceRunnerTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.mkdtemp(prefix="a2a_trace_test_")

    def tearDown(self) -> None:
        shutil.rmtree(self.tmp)

    def fixture(self, name: str) -> str:
        return os.path.join(ROOT, "fixtures", "traces", name)

    def run_fixture(self, name: str):
        config = RunnerConfig.from_env(llm_mode="mock")
        return run_trace(self.fixture(name), self.tmp, config)

    def run_temp_fixture(self, fixture: dict):
        path = os.path.join(self.tmp, f"{fixture['trace_id']}.json")
        with open(path, "w", encoding="utf-8") as f:
            json.dump(fixture, f)
        config = RunnerConfig.from_env(llm_mode="mock")
        return run_trace(path, self.tmp, config)

    def test_allowed_trace_runs_full_pipeline(self) -> None:
        trace = self.run_fixture("allowed_archive_probe.json")
        self.assertEqual(trace["final_decision"], "allowed")
        self.assertEqual([run["agent_name"] for run in trace["agent_runs"]], ["plot", "character", "world", "narrator", "judge"])
        self.assertIn("scene_packet", trace)
        self.assertEqual(trace["judge_report"]["verdict"], "allow")
        self.assertIn("memory_handoff", trace)
        self.assertIn("token_usage", trace)
        self.assertEqual(trace["token_usage"]["totals"]["agent_count"], 5)
        self.assertGreater(trace["token_usage"]["totals"]["total_tokens"], 0)
        self.assertTrue(trace["token_usage"]["totals"]["estimated_agent_count"] >= 5)
        self.assertIn("token_usage", trace["agent_runs"][0])
        self.assertTrue(os.path.exists(trace["artifacts"]["trace_json"]))
        self.assertTrue(os.path.exists(trace["artifacts"]["report_md"]))
        with open(trace["artifacts"]["report_md"], "r", encoding="utf-8") as f:
            self.assertIn("## Token Usage", f.read())

    def test_warning_does_not_stop_pipeline(self) -> None:
        with open(self.fixture("allowed_archive_probe.json"), "r", encoding="utf-8") as f:
            fixture = json.load(f)
        fixture["trace_id"] = "allowed_warning_budget"
        fixture["mock_agent_outputs"]["plot"]["scene_pressure_packet"]["budget_cost"] = "low"

        trace = self.run_temp_fixture(fixture)

        self.assertEqual(trace["final_decision"], "allowed")
        self.assertEqual([run["agent_name"] for run in trace["agent_runs"]], ["plot", "character", "world", "narrator", "judge"])
        self.assertTrue(any(item["severity"] == "warning" for item in trace["validation"]["plot"]))

    def test_narrator_leak_is_blocked_after_full_pipeline(self) -> None:
        trace = self.run_fixture("adversarial_narrator_leak.json")
        self.assertEqual(trace["final_decision"], "blocked")
        self.assertEqual([run["agent_name"] for run in trace["agent_runs"]], ["plot", "character", "world", "narrator", "judge"])
        self.assertTrue(trace["validation"]["narrator"])
        self.assertTrue(trace["validation"]["judge"])
        self.assertEqual(trace["judge_report"]["verdict"], "block")

    def test_plot_railroading_is_blocked_early(self) -> None:
        trace = self.run_fixture("adversarial_plot_railroading.json")
        self.assertEqual(trace["final_decision"], "blocked")
        self.assertEqual([run["agent_name"] for run in trace["agent_runs"]], ["plot"])
        self.assertTrue(trace["validation"]["plot"])

    def test_config_loads_codex_oauth_auth_json(self) -> None:
        auth_path = os.path.join(self.tmp, "auth.json")
        with open(auth_path, "w", encoding="utf-8") as f:
            json.dump({"tokens": {"access_token": "oauth-token"}}, f)

        with patch.dict(os.environ, {"A2A_LLM_AUTH_JSON": auth_path}, clear=True):
            config = RunnerConfig.from_env(llm_mode="real")

        self.assertEqual(config.api_key, "oauth-token")
        self.assertEqual(config.auth_json_path, auth_path)

    def test_explicit_bearer_token_wins_over_auth_json(self) -> None:
        auth_path = os.path.join(self.tmp, "auth.json")
        with open(auth_path, "w", encoding="utf-8") as f:
            json.dump({"tokens": {"access_token": "oauth-token"}}, f)

        env = {
            "A2A_LLM_AUTH_JSON": auth_path,
            "A2A_LLM_BEARER_TOKEN": "explicit-token",
        }
        with patch.dict(os.environ, env, clear=True):
            config = RunnerConfig.from_env(llm_mode="real")

        self.assertEqual(config.api_key, "explicit-token")

    def test_codex_cli_provider_uses_isolated_codex_home(self) -> None:
        codex_home = os.path.join(self.tmp, "codex-home")
        codex_workdir = os.path.join(self.tmp, "codex-workdir")
        config = RunnerConfig(
            llm_mode="codex-cli",
            model="gpt-5.5",
            codex_binary="codex",
            codex_home=codex_home,
            codex_workdir=codex_workdir,
        )
        captured = {}

        def fake_run(command, input, text, encoding, errors, capture_output, timeout, env, cwd, check):
            captured["command"] = command
            captured["input"] = input
            captured["env"] = env
            captured["cwd"] = cwd
            output_path = command[command.index("--output-last-message") + 1]
            with open(output_path, "w", encoding="utf-8") as f:
                f.write('{"agent": "plot", "ok": true}')

            class Completed:
                returncode = 0
                stdout = '{"type":"turn.completed","usage":{"input_tokens":42,"cached_input_tokens":7,"output_tokens":11,"reasoning_output_tokens":0}}\n'
                stderr = ""

            return Completed()

        with patch("subprocess.run", fake_run):
            result = CodexCliAgentProvider(config).complete("plot", "Return JSON.", {})

        self.assertIsNone(result.error)
        self.assertEqual(result.parsed_output, {"agent": "plot", "ok": True})
        self.assertEqual(result.token_usage["mode"], "codex-cli")
        self.assertEqual(result.token_usage["source"], "provider_usage")
        self.assertFalse(result.token_usage["is_estimated"])
        self.assertEqual(result.token_usage["input_tokens"], 42)
        self.assertEqual(result.token_usage["output_tokens"], 11)
        self.assertEqual(captured["env"]["CODEX_HOME"], codex_home)
        self.assertEqual(captured["cwd"], codex_workdir)
        self.assertIn("--ephemeral", captured["command"])
        self.assertIn("--json", captured["command"])
        self.assertIn("--ignore-user-config", captured["command"])
        self.assertIn("--ignore-rules", captured["command"])
        self.assertIn("--skip-git-repo-check", captured["command"])
        self.assertIn('approval_policy="never"', captured["command"])
        self.assertIn("Do not inspect files", captured["input"])

    def test_plot_validator_handles_non_object_budget(self) -> None:
        violations = validate_plot(
            {
                "pressure_kind": "deadline",
                "scope": "scene",
                "duration": "one_window",
                "affected_options": ["delay costs more"],
                "non_forcing_clause": "Either character may refuse.",
                "forbidden_outcomes": ["forced confession"],
                "visibility": "system_restricted",
                "budget_cost": "medium",
            }
        )

        self.assertTrue(any(item["code"] == "invalid_budget_cost" for item in violations))
        self.assertFalse(any(item["severity"] == "block" for item in violations))

    def test_token_estimator_counts_cjk_text_more_conservatively(self) -> None:
        self.assertGreaterEqual(estimate_tokens("中文中文"), 4)
        self.assertGreater(estimate_tokens("Return exactly one JSON object."), 0)


if __name__ == "__main__":
    unittest.main()
