# a2a-literary-agents

Working title / codename: `vibe-somnium / 织梦`

`a2a-literary-agents` is an experimental protocol and MVP runtime for literary multi-agent writing systems. The project explores whether fiction generation can become more stable when authorial power is split across bounded agents instead of concentrated inside one omniscient model prompt.

## Core Premise

Direct AI writing often collapses because the world changes with the latest prompt. Characters know too much, consequences bend toward convenience, and narration can quietly turn suspicion into fact.

This project treats that as an authority-boundary problem:

- `Plot Agent` provides pressure, not destiny.
- `Character Agent` decides intent, not outcome.
- `World Agent` decides consequence, not prose.
- `Narrator Agent` renders committed material, not hidden truth.
- `Canon Steward` reviews canon mutation, not scene outcome.
- `Judge Agent` reviews authority overreach, not story content.
- `Orchestrator` routes, projects, validates, seals, and records, but does not author meaning.

## Runtime Shape

The MVP is a single-window trace runner:

```text
player/request
  -> PlotContextSummary -> Plot Agent -> ScenePressurePacket
  -> CharacterContextPacket -> Character Agent -> DialogueWindow
  -> WorldResolutionContext -> World Agent -> Resolution / StateDelta / VisibilityResult
  -> ScenePacket sealing
  -> NarratorInputPacket -> Narrator Agent -> prose
  -> JudgeReviewContext -> Judge Agent -> judge_report
  -> owner_projection / MemoryDelta handoff
  -> final allowed / blocked decision
```

Every creative model-agent receives only a projected context. Complete protocol objects remain system objects.

## Runnable MVP

The repository now includes a minimal Python runner:

- deterministic `mock` backend for fixtures and tests
- isolated `codex-cli` backend for headless local Codex execution
- OpenAI-compatible `real` backend for API-compatible providers
- trace reports that include projected inputs, raw agent outputs, validation results, Judge verdicts, sealed packets, and memory handoff

See [MVP Trace Runner v0.1](docs/runner/mvp-runner-v0.1.md).

## Quick Start

Run deterministic tests:

```powershell
python -m unittest discover -s tests
```

Run the allowed fixture with mock outputs:

```powershell
python scripts/run_trace.py run --fixture fixtures/traces/allowed_archive_probe.json --llm-mode mock
```

Run with an isolated Codex CLI backend:

```powershell
$env:A2A_CODEX_HOME="D:\vibe-somnium\.local\codex-cli-home"
$env:A2A_CODEX_WORKDIR="D:\vibe-somnium\.local\codex-cli-workdir"
$env:A2A_LLM_MODEL="gpt-5.5"
python scripts/run_trace.py run --fixture fixtures/traces/allowed_archive_probe.json --llm-mode codex-cli
```

`.local/` is ignored and must not be committed. It may contain local Codex CLI login state.

## Current Fixtures

| Fixture | Expected | Purpose |
| --- | --- | --- |
| `allowed_archive_probe.json` | `allowed` | legal pressure, legal character probing, scoped suspicion, legal narration, Judge allow |
| `adversarial_narrator_leak.json` | `blocked` | narrator turns suspicion into confirmed guilt; deterministic validator and Judge block it |
| `adversarial_plot_railroading.json` | `blocked` | Plot pressure puppets character choice and is blocked early |

## Protocol Documents

- [communication-permission-matrix-v0.1](docs/protocol/communication-permission-matrix-v0.1.md)
- [agent-constraint-matrix-v0.1](docs/protocol/agent-constraint-matrix-v0.1.md)
- [agent-context-packet-and-field-visibility-v0.1](docs/protocol/agent-context-packet-and-field-visibility-v0.1.md)
- [scene-pressure-packet-and-plot-budget-v0.1](docs/protocol/scene-pressure-packet-and-plot-budget-v0.1.md)
- [dialogue-window-schema-v0.1](docs/protocol/dialogue-window-schema-v0.1.md)
- [resolution-state-delta-commit-pipeline-v0.1](docs/protocol/resolution-state-delta-commit-pipeline-v0.1.md)
- [scene-packet-schema-v0.1](docs/protocol/scene-packet-schema-v0.1.md)
- [scene-packet-to-memory-handoff-v0.1](docs/protocol/scene-packet-to-memory-handoff-v0.1.md)
- [memory-delta-format-v0.1](docs/protocol/memory-delta-format-v0.1.md)
- [state-and-knowledge-layers-v0.1](docs/protocol/state-and-knowledge-layers-v0.1.md)
- [event-publication-thresholds-v0.1](docs/protocol/event-publication-thresholds-v0.1.md)
- [latent-to-public-canon-reveal-rules-v0.1](docs/protocol/latent-to-public-canon-reveal-rules-v0.1.md)
- [canon-mutation-review-checklist-v0.1](docs/protocol/canon-mutation-review-checklist-v0.1.md)
- [terminology-index-v0.1](docs/reference/terminology-index-v0.1.md)

## Working Principles

- `soft validation, hard permission`
- `private cognition, public consequence`
- `plot provides pressure, not destiny`
- `narrator cannot invent facts`
- `complete objects are system objects; agents receive projected views`
- `judge reviews authority; judge does not author`

## Current Limits

- Single-window only.
- No repair loop yet.
- Judge output is advisory-to-Orchestrator, but MVP currently converts `repair_required` and `block` into hard blocks.
- Validators are intentionally minimal.
- Codex CLI mode is slower than direct API mode because each agent call is a separate headless process.
- Token counting is configured as budget metadata, not exact tokenizer accounting.

## License

This repository uses a mixed-license structure.

- Code and other non-documentation repository contents are licensed under Apache-2.0.
- Documentation and protocol text, including `README.md` and all files under `docs/`, are licensed under CC BY 4.0.
- Attribution and origin context are summarized in `NOTICE`.

See [LICENSE](LICENSE), [LICENSE-docs](LICENSE-docs), and [NOTICE](NOTICE).
