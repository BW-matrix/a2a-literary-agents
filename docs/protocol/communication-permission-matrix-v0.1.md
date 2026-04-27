# Communication + Permission Matrix v0.1

This document is the first protocol draft for `vibe-somnium / 织梦`.

目标不是一次性定死全部实现，而是先给系统一个足够清晰的 law layer，让 agent swarm 不会重新塌回 hidden single-author mode。

## Protocol Axioms

1. `character decides intent`
2. `world decides consequence`
3. `plot decides pressure`
4. `narrator decides expression`
5. `canon steward decides canon mutation`
6. `orchestrator decides routing and validation`

## Master Matrix

| Constraint | Character Agent | World Agent | Plot Agent | Narrator Agent | Canon Steward | Orchestrator |
| --- | --- | --- | --- | --- | --- | --- |
| Core role | Subjective actor | Reality adjudicator | Structural pressure source | Prose renderer | Canon lawkeeper | Routing and guardrail layer |
| Core authority | Will, motive, choice, self-interpretation | Consequence, causality, state transition | Conflict pressure, pacing pressure, stakes escalation | Voice, pacing, textual rendering | Accept or reject canon mutations | Validate, route, schedule, quarantine |
| Primary output | `Intent`, `ActionProposal`, optional `DialogueWindow` | `Observation`, `Resolution`, `StateDelta` | `Pressure`, `EscalationSeed`, `ScenePressurePacket` | `Narration`, `SceneDraft` | `CanonDecision`, `CanonDelta` | `Warning`, `RepairRequest`, `ScenePacket`, scheduling directives |
| Allowed outbound message types | `Intent`, `ActionProposal`, `DialogueWindow`, `SelfNote` | `Observation`, `Resolution`, `StateDelta`, `CanonQuery`, `CanonMutationRequest` | `Pressure`, `EscalationSeed`, `ScenePressurePacket` | `Narration`, `SceneDraft`, `StyleNote` | `CanonDecision`, `CanonDelta`, `CanonClarification` | `Warning`, `RepairRequest`, `RouteNotice`, `ScenePacket`, `QuarantineNotice` |
| Allowed inbound message types | `Observation`, public `Pressure`, `Warning`, projected `ScenePacketView` | `Intent`, `ActionProposal`, `DialogueWindow`, `CanonDecision`, `Warning` | projected `ScenePacketView`, global progress summaries, `Warning` | `NarratorInputPacket`, approved style guide, `Warning` | `CanonQuery`, `CanonMutationRequest`, `CanonReviewContext`, `Warning` | all message envelopes and validation metadata |
| Default visibility | `private_self` for raw cognition; `private_target` for proposals to world | `system_restricted` by default; public only through committed state | `scene_public` or `system_restricted` depending on pressure type | `system_restricted` until prose is committed | `system_restricted` | `system_restricted` |
| Read scope | Self biography, self memory, public canon, visible scene facts, public event ledger, `CharacterContextPacket` | World state ledger, public event ledger, canon, submitted proposals, rulesets | Global structure progress, public event ledger, relationship map, limited world-state summaries, `PlotContextSummary` | `NarratorInputPacket`, authorized POV material, style guide | Full canon layers and canon change log, canon-relevant state, `CanonReviewContext` | Envelope metadata, policy tables, validation rules, projection policy |
| Private memory access | Full self memory only | No direct access to character raw memory | No direct access to character raw memory | Limited POV-scoped access only when authorized | Canon memory only | No literary private memory by default |
| Proposal scope | What I want, what I do, what I say, how I frame myself | What happens, what changes, what becomes visible | What pressure enters the scene | How committed events become prose | Whether a new fact enters canon | How messages move and whether they need repair |
| Commit scope | None on objective world state | May commit `Resolution` and `StateDelta` within current rules | None on factual story state | May commit manuscript text only, not facts | May commit `CanonDecision` and `CanonDelta`; emergent origin must still receive public, latent, or scoped visibility | May commit routing results, validation outcomes, and scene packets |
| Cannot declare | Other minds, objective results, canon changes, guaranteed success | Character inner truth, theme meaning, plot intention, miraculous exceptions | Specific character choices, final outcomes, canon facts | New facts, retroactive fixes, hidden causal changes | Scene outcomes, character choices, prose facts outside canon review | Story content, character motive, canon invention |
| Cannot see | Other characters' raw cognition, hidden canon, rejected branches of others | Full unfiltered inner monologue unless explicitly transformed into action | Raw private cognition, narrator draft internals | Rejected branches, private canon review debate, raw hidden cognition unless authorized | Irrelevant private character cognition | Should avoid reading style content beyond what is needed for validation |
| Normal tempo | One dramatic move per window | One resolution cycle per window | One pressure packet per scene or major beat | One render pass per committed scene packet | Only on canon-triggering events | Continuous but lightweight supervision |
| Granularity | `dramatic window`, not single utterance | `dramatic window`, not single utterance | scene-level or act-level pressure | scene packet or subscene packet | event-triggered | per-envelope validation and routing |
| Failure behavior | Warn and request repair if message is malformed | Warn and hold resolution if action cannot be interpreted safely | Warn and downgrade pressure packet if ambiguous | Warn and reject prose if it invents facts | Warn and defer canon mutation if unsupported | Never crash the system on soft schema failure |
| Hard block conditions | Claims objective outcome, writes others' minds, changes canon | Violates canon, bypasses steward, ignores rules for drama | Puppeteers characters, declares facts, edits canon | Invents facts, leaks latent canon, rewrites events | Alters immutable canon without explicit override path | Silently rewrites content or becomes hidden author |

Important context rule:

- complete protocol objects such as raw `ScenePacket`, raw `DialogueWindow`, raw `world_state_ledger`, and raw `latent_canon` are system objects
- agents receive projected context packets defined in [agent-context-packet-and-field-visibility-v0.1](agent-context-packet-and-field-visibility-v0.1.md)
- a `visibility` label inside a payload is not itself a safe delivery boundary unless the event bus applies field-level projection

## Event Bus Policy

`event bus` should use a soft-validation pipeline. 格式错误不应该直接导致整轮崩掉，更不应该让系统因为小字段缺失而自杀。

Recommended pipeline:

1. `receive`
2. `inspect`
3. `warn`
4. `normalize if safe`
5. `request repair if needed`
6. `quarantine only if routing or authority is unsafe`
7. `continue scene with fallback`

The important distinction is:

- `schema failure` is usually a recoverable coordination issue
- `authority failure` is a protocol violation
- `security-critical field failure` is treated like a permission risk, not like a harmless schema typo

Recoverable fields may be normalized when safe. Security-critical fields such as `sender`, `message_type`, `visibility`, `target`, `authority_basis`, and `authorized_interiority.scope_limit` should not be guessed from literary convenience.

## Message Envelope v0.1

Every routed message should try to include the following fields:

| Field | Purpose | Handling if missing |
| --- | --- | --- |
| `message_id` | Traceability | event bus may generate one |
| `message_type` | Routing and allowlist check | if missing and not inferable, warn and quarantine |
| `sender` | Source identity | hard stop for this message only if unknown |
| `target` | Intended receiver | infer from route table if obvious; otherwise warn |
| `scene_id` | Scene grouping | inherit current scene if available |
| `window_id` | Dramatic window grouping | inherit current window if available |
| `visibility` | Privacy boundary | security-critical; quarantine or require repair unless route context has one unique legal value |
| `payload` | Actual content | warn and request repair if unusable |
| `based_on` | Causal trace or references | optional, but recommended |

## Visibility Layers

| Visibility | Meaning |
| --- | --- |
| `private_self` | Raw cognition, hidden motive, self-only reflection |
| `private_target` | Only sender and explicit target may inspect |
| `scene_public` | Visible to all agents legitimately participating in the scene |
| `system_restricted` | Reserved for routing, canon review, or validation layers |

Important rule:

- raw inner intention stays in `private_self`
- only transformed intent or action proposal leaves the self boundary

## Dramatic Window Rule

系统默认不按“每一句台词”调度，而按 `dramatic window` 调度。

A dramatic window is a bounded unit of interaction that may contain:

- one short exchange
- one tactical move in a negotiation
- one emotional turn in an argument
- one attempt to conceal, probe, reveal, or deflect

This means a long dialogue does not require one full protocol cycle per utterance.

Default policy:

- one window may include one to three dialogue moves per active character
- narrator renders the result of the window, not every raw candidate line
- switch to finer granularity only when a critical trigger fires

Suggested critical triggers:

- deception is detected
- power relation changes sharply
- hidden information is revealed
- a character breaks prior behavior constraints
- dialogue turns into physical action
- a third party enters and changes the scene state

## Canon Layers

| Canon Layer | Meaning | Who may change it |
| --- | --- | --- |
| `Immutable Canon` | Fundamental world law, hard history anchors, core role definitions | No routine agent |
| `Latent Canon` | Already true but not yet revealed facts | Not changed during scene play; only revealed when valid |
| `Emergent Canon` | Origin/provenance for new facts allowed to grow during writing | `Canon Steward` after review; visibility assigned separately |

For the complementary storage model covering `world_state_ledger`, `public_event_ledger`, and `private_memory`, see [state-and-knowledge-layers-v0.1](state-and-knowledge-layers-v0.1.md).

## Commit Rule

Only committed scene state may be projected into `NarratorInputPacket` as factual source material.

This prevents:

- prose from smuggling rejected branches into the story
- narrator from turning possibilities into facts
- plot pressure from being mistaken for already-happened events
- pending publication or canon reveal candidates from being narrated as approved deltas

For the concrete world-side commit sequence, see [resolution-state-delta-commit-pipeline-v0.1](resolution-state-delta-commit-pipeline-v0.1.md).

## Open Questions for v0.2

1. How to test field-level projection with adversarial fixtures
2. Whether `DialogueWindow` should contain candidate lines or only speech acts in high-risk scenes
3. How much of private cognition may be selectively exposed to narrator in close POV modes
4. How scene packets should be summarized for long-form memory retention
5. How public-scope membership should be modeled for `public_event_ledger` queries
