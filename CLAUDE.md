# CLAUDE.md - a2a-literary-agents / vibe-somnium / 织梦

This file is onboarding context for Claude or any reviewer joining the project.

## Project Identity

| Key | Value |
| --- | --- |
| Repository | `a2a-literary-agents` |
| Codename | `vibe-somnium / 织梦` |
| Author | Bowen Qi |
| License | Code: Apache-2.0; docs/protocol text: CC BY 4.0 |
| Stage | MVP runtime prototype + protocol hardening |

The core claim: AI writing fails when authorial power collapses into one prompt-following model. This project splits authority across bounded agents and records every context projection, decision, and validation step.

## Agent Roles

| Agent | Owns | Must Not Do |
| --- | --- | --- |
| `Plot Agent` | pressure, tension, stakes | decide destiny, puppet characters, declare facts |
| `Character Agent` | intent, motive, local choice | decide objective outcome, write others' minds |
| `World Agent` | consequence, causality, state transition | write prose, promote canon, invent inner truth |
| `Narrator Agent` | prose rendering from committed inputs | invent facts, leak hidden truth, broaden visibility |
| `Canon Steward` | canon mutation review | decide scene outcome or rewrite prose |
| `Judge Agent` | authority-overreach review | create story material, rewrite outputs |
| `Orchestrator` | routing, projection, validation, sealing, trace records | author meaning or editorially reshape story facts |

## Fixed Single-Window Flow

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

Every creative model-agent receives only projected context. Full system objects are not normal prompt inputs. Judge receives an audit context, but it is not part of literary creation and cannot repair by rewriting content.

## Runtime Backends

The MVP runner supports:

- `mock`: deterministic fixture outputs
- `codex-cli`: isolated headless `codex exec` calls
- `real`: OpenAI-compatible chat completions
- `auto`: API when configured, otherwise mock

`codex-cli` mode uses an isolated `CODEX_HOME`, defaulting to `.local/codex-cli-home`. `.local/` is ignored and must never be committed because it may contain login state.

## Current Runnable Commands

```powershell
python -m unittest discover -s tests
python scripts/run_trace.py run --fixture fixtures/traces/allowed_archive_probe.json --llm-mode mock
python scripts/run_trace.py run --fixture fixtures/traces/adversarial_narrator_leak.json --llm-mode mock
python scripts/run_trace.py run --fixture fixtures/traces/adversarial_plot_railroading.json --llm-mode mock
```

Codex CLI real backend:

```powershell
$env:A2A_CODEX_HOME="D:\vibe-somnium\.local\codex-cli-home"
$env:A2A_CODEX_WORKDIR="D:\vibe-somnium\.local\codex-cli-workdir"
$env:A2A_LLM_MODEL="gpt-5.5"
python scripts/run_trace.py run --fixture fixtures/traces/allowed_archive_probe.json --llm-mode codex-cli
```

## What To Preserve

- `soft validation, hard permission`
- `private cognition, public consequence`
- `plot provides pressure, not destiny`
- `narrator cannot invent facts`
- `complete objects are system objects; agents receive projected views`
- `judge reviews authority; judge does not author`

## Important Files

- `src/a2a_literary_agents/runner.py`: single-window protocol runner
- `src/a2a_literary_agents/projection.py`: projected context construction
- `src/a2a_literary_agents/llm.py`: mock, OpenAI-compatible, and Codex CLI providers
- `src/a2a_literary_agents/validation.py`: deterministic validators and Judge verdict handling
- `fixtures/traces/`: allowed and adversarial trace fixtures
- `docs/runner/mvp-runner-v0.1.md`: runner documentation
- `docs/protocol/`: protocol specs
- `docs/reference/terminology-index-v0.1.md`: canonical terminology

## Current Limits

- Single-window only.
- No repair loop yet.
- Judge can request repair, but MVP currently converts that into a block.
- Validators are intentionally minimal.
- Codex CLI mode is slower than direct API mode.
- Exact token accounting is not implemented yet.

## Reviewer Guidance

When reviewing this project, focus on:

- whether projected context prevents hidden omniscience
- whether World consequence is auditable
- whether Plot pressure preserves meaningful choice
- whether Narrator prose is grounded in `NarratorInputPacket`
- whether Judge detects semantic overreach without becoming a hidden author
- whether `.local/` and auth material remain untracked
