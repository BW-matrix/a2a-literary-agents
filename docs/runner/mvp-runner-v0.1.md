# MVP Trace Runner v0.1

This document describes the first minimal runnable prototype for `a2a-literary-agents`.

The runner is not a full autonomous literary swarm. It is a single-window protocol trace runner that executes allowed and adversarial scene fixtures through the current protocol objects.

## What It Runs

The MVP executes one `dramatic window`:

1. `Plot Agent` receives `PlotContextSummary` and returns `ScenePressurePacket`.
2. `Character Agent` receives `CharacterContextPacket` and returns `DialogueWindow`.
3. `World Agent` receives resolver-legal context and returns `Resolution`, `StateDelta`, and `VisibilityResult`.
4. `Orchestrator` seals a committed `ScenePacket`.
5. `Orchestrator` projects `NarratorInputPacket`.
6. `Narrator Agent` returns prose.
7. `Orchestrator` projects `JudgeReviewContext`.
8. `Judge Agent` returns `judge_report` for authority-overreach review only.
9. Handoff derives owner-specific `owner_projection` and `MemoryDelta` records.
10. Validators produce `allowed` or `blocked`.

Every model-agent prompt is built only from projected context. Full system objects are never passed to model-agents.

## LLM Modes

The runner supports four modes:

| Mode | Behavior |
| --- | --- |
| `mock` | deterministic fixture outputs only |
| `codex-cli` | isolated headless Codex CLI calls using projected prompts |
| `real` | OpenAI-compatible chat completions |
| `auto` | real when a bearer token is configured, otherwise mock |

`Orchestrator`, projection, sealing, and validation are deterministic code in all modes.

## Judge Agent

The `Judge Agent` is not a literary agent. It does not write prose, plot, character intent, world outcomes, canon, or memory.

It receives `JudgeReviewContext`, an audit context containing projected inputs, agent outputs, program validation, the sealed `ScenePacket`, and narrator output. It returns:

```json
{
  "judge_report": {
    "verdict": "allow",
    "findings": [],
    "required_repairs": []
  }
}
```

Valid verdict values:

| Verdict | Runtime handling |
| --- | --- |
| `allow` | continue |
| `warning` | continue and record warning |
| `repair_required` | MVP blocks; future repair loop should retry the target agent |
| `block` | block final player-facing output |

The Judge may identify semantic authority overreach, but it cannot repair by rewriting content.

## Codex CLI Backend

`codex-cli` is the preferred real backend when you want the runner to use local Codex CLI access instead of OpenAI Platform API billing.

It does not turn Codex into an API server. Each model-agent call starts a separate non-interactive `codex exec` process, passes only the projected protocol prompt through stdin, and reads the final JSON message.

Isolation rules:

- every child process gets its own `CODEX_HOME`
- default `CODEX_HOME` is `.local/codex-cli-home`
- default Codex working directory is `.local/codex-cli-workdir`
- the child process runs with `--ephemeral`
- the child process runs with `--ignore-user-config`
- the child process runs with `--ignore-rules`
- the child process runs with `--sandbox read-only`
- the child process runs with `approval_policy="never"`
- `.local/` is not committed

One-time isolated login:

```powershell
$env:A2A_CODEX_HOME="D:\vibe-somnium\.local\codex-cli-home"
$env:CODEX_HOME=$env:A2A_CODEX_HOME
codex login
```

Run with Codex CLI:

```powershell
$env:A2A_CODEX_HOME="D:\vibe-somnium\.local\codex-cli-home"
$env:A2A_CODEX_WORKDIR="D:\vibe-somnium\.local\codex-cli-workdir"
$env:A2A_LLM_MODEL="gpt-5.5"
python scripts/run_trace.py run --fixture fixtures/traces/allowed_archive_probe.json --llm-mode codex-cli
```

Codex CLI output budgets are soft prompt budgets, not hard API token caps. The runner still enforces `A2A_MAX_LLM_CALLS_PER_TRACE` and deterministic protocol validators.

## Real API Configuration

The real adapter is OpenAI-compatible and uses bearer-token auth.

PowerShell example:

```powershell
$env:A2A_LLM_BEARER_TOKEN="your_oauth_or_api_token"
$env:A2A_LLM_BASE_URL="https://api.openai.com/v1"
$env:A2A_LLM_MODEL="gpt-5.5"
python scripts/run_trace.py run --fixture fixtures/traces/allowed_archive_probe.json --llm-mode real
```

Codex OAuth auth-file example:

```powershell
$env:A2A_LLM_AUTH_JSON="C:\path\to\auth.json"
$env:A2A_LLM_BASE_URL="http://127.0.0.1:<gateway-port>/v1"
$env:A2A_LLM_MODEL="gpt-5.5"
python scripts/run_trace.py run --fixture fixtures/traces/allowed_archive_probe.json --llm-mode real
```

`A2A_LLM_AUTH_JSON` reads `tokens.access_token` from a local Codex-style OAuth file. This is only a token source. It does not imply that `https://api.openai.com/v1` will accept the token for generation; some OAuth tokens require a compatible gateway or lack direct API scopes such as `api.responses.write`.

Supported environment variables:

| Variable | Meaning |
| --- | --- |
| `A2A_LLM_BEARER_TOKEN` | OAuth or API bearer token |
| `A2A_LLM_API_KEY` | fallback API key variable |
| `OPENAI_API_KEY` | standard fallback API key variable |
| `A2A_LLM_AUTH_JSON` | local Codex-style OAuth auth file; reads `tokens.access_token` |
| `CODEX_OAUTH_AUTH_JSON` | fallback auth-file variable |
| `A2A_LLM_BASE_URL` | OpenAI-compatible base URL |
| `OPENAI_BASE_URL` | standard fallback base URL |
| `A2A_LLM_MODEL` | model name |
| `OPENAI_MODEL` | standard fallback model name |
| `A2A_LLM_TOKEN_FIELD` | token field, default `max_tokens` |
| `A2A_CODEX_BINARY` | Codex CLI executable, default `codex` |
| `A2A_CODEX_HOME` | isolated Codex home for `codex-cli` mode |
| `A2A_CODEX_WORKDIR` | isolated read-only working directory for `codex-cli` mode |

High-context default output caps:

```json
{
  "max_llm_calls_per_trace": 8,
  "total_output_token_budget": 35000,
  "per_agent_max_output_tokens": {
    "plot": 2000,
    "character": 4000,
    "world": 5000,
    "narrator": 6000,
    "canon_steward": 3000,
    "validator": 3000
  }
}
```

## Fixtures

Current fixtures:

| Fixture | Expected decision | Purpose |
| --- | --- | --- |
| `allowed_archive_probe.json` | `allowed` | legal pressure, legal dialogue probe, scoped suspicion, legal narration |
| `adversarial_narrator_leak.json` | `blocked` | full pipeline reaches narrator and Judge, then catches suspicion-to-fact overclaim |
| `adversarial_plot_railroading.json` | `blocked` | Plot pressure puppets character choice and is blocked early |

## Outputs

Each run writes:

- `runs/<trace-id>/trace.json`
- `runs/<trace-id>/report.md`

The report includes:

- projection manifests
- every agent's projected input context
- every agent's raw output
- sealed `ScenePacket`
- `judge_report`
- memory handoff
- validation report
- final `allowed` / `blocked` decision

## Commands

Run allowed fixture:

```powershell
python scripts/run_trace.py run --fixture fixtures/traces/allowed_archive_probe.json --llm-mode mock
```

Run adversarial narrator fixture:

```powershell
python scripts/run_trace.py run --fixture fixtures/traces/adversarial_narrator_leak.json --llm-mode mock
```

Run adversarial plot fixture:

```powershell
python scripts/run_trace.py run --fixture fixtures/traces/adversarial_plot_railroading.json --llm-mode mock
```

Run tests:

```powershell
python -m unittest discover -s tests
```

## Current Limits

- This is single-window only.
- There is no repair loop yet; `repair_required` currently blocks.
- Validators are intentionally minimal.
- Real API mode assumes an OpenAI-compatible `/chat/completions` endpoint.
- Codex CLI mode is process-based and slower than direct API mode.
- Token counting is configured as budget metadata, but exact tokenizer accounting is not yet implemented.
- `Orchestrator Projection, Assembly, and Sealing Contract v0.1` should be formalized next.
