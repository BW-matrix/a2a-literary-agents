# Agent Constraint Matrix v0.1

This document expands the high-level protocol draft into implementation-oriented tables.

Columns are agent types. Rows are constraint items.

The goal is not to freeze every detail right now, but to create a stable matrix that later message schemas, storage design, and scene-loop code can inherit from.

## Legend

- `allow`: normal protocol behavior
- `limited`: only under an explicit scope or policy
- `indirect`: must go through another layer or agent
- `no`: not permitted by default

## Communication Constraint Matrix

| Constraint | Character Agent | World Agent | Plot Agent | Narrator Agent | Canon Steward | Orchestrator |
| --- | --- | --- | --- | --- | --- | --- |
| Primary communication question | What do I want, do, or say now? | What actually happens next? | What pressure enters now? | How does committed state become prose? | Can this new fact legally exist? | Can the system route this safely? |
| Normal outbound message types | `Intent`, `ActionProposal`, `DialogueWindow`, `SelfNote` | `Observation`, `Resolution`, `StateDelta`, `CanonQuery`, `CanonMutationRequest` | `Pressure`, `EscalationSeed`, `ScenePressurePacket` | `Narration`, `SceneDraft`, `StyleNote` | `CanonDecision`, `CanonDelta`, `CanonClarification` | `Warning`, `RepairRequest`, `RouteNotice`, `ScenePacket`, `QuarantineNotice` |
| Normal inbound message types | `Observation`, public `Pressure`, `Warning`, projected `ScenePacketView` | `Intent`, `ActionProposal`, `DialogueWindow`, `CanonDecision`, `Warning` | projected `ScenePacketView`, structure summary, `Warning` | `NarratorInputPacket`, approved style guide, `Warning` | `CanonQuery`, `CanonMutationRequest`, `CanonReviewContext`, `Warning` | all envelopes, validation metadata |
| Default target | `world` | involved agents, event bus, `canon steward` if needed | scene bus, `world`, or structure bus | manuscript layer | `world` and `orchestrator` | any agent or system layer |
| Default visibility | `private_self` for raw cognition; `private_target` for transformed proposals | `system_restricted` until state is committed | `scene_public` for active pressure; `system_restricted` for structure-only notes | `system_restricted` until prose is committed | `system_restricted` | `system_restricted` |
| Raw cognition exposure rule | self only | no raw access | no raw access | limited to explicit POV-authorized extracts | no raw access | no raw access |
| Missing-field handling | warn and request repair | warn and hold unsafe resolution | warn and downgrade or defer | warn and defer render | warn and defer decision | normalize recoverable fields only; quarantine unsafe security-critical gaps |
| Ambiguity handling | clarify intent or narrow scope | ask for repair before consequence commit | downgrade pressure or defer to next beat | ask for grounded packet before render | require rationale before canon decision | issue route warning and preserve flow |
| Privacy breach handling | quarantine outbound message | quarantine unsafe input and refuse hidden-mind inference | quarantine leaked private cognition | reject render built on unauthorized cognition | quarantine request | quarantine envelope and notify sender |
| Hard block if message attempts to | declare objective outcome, declare other minds, alter canon | bypass canon, ignore rules for drama, write inner minds | puppet characters, declare facts, edit canon | invent facts, leak latent canon, rewrite committed events | alter immutable canon or decide scene outcome | rewrite creative content or hide authority breach |
| Normal cadence | one dramatic move per window | one resolution cycle per window | one pressure packet per scene or major beat | one render pass per committed scene packet | event-triggered only | continuous lightweight supervision |
| Default granularity | `dramatic window` | `dramatic window` | scene-level or act-level pressure | scene packet or subscene packet | event-level | envelope-level |
| Dialogue handling | submit speech act and optional candidate lines | resolve visible dialogue consequences and information flow | inject pressure, not line-by-line speech | render final spoken lines from committed window | no dialogue role | enforce window boundaries and pacing rules |
| Interrupt policy | limited to immediate danger, forced choice, or sharp revelation | may interrupt to reject impossible or unsafe action | limited to scheduled escalation trigger | no interrupt during active causality loop | interrupt only on canon breach | may interrupt any unsafe route |
| Allowed fallback on malformed input | retry with narrowed action | safe no-op, hold, or ask repair | defer escalation | skip render for current packet | defer canon mutation | preserve system continuity whenever authority is not violated |

## Permission Constraint Matrix

| Constraint | Character Agent | World Agent | Plot Agent | Narrator Agent | Canon Steward | Orchestrator |
| --- | --- | --- | --- | --- | --- | --- |
| Core authority | will, motive, choice, self-interpretation | consequence, causality, state transition | pressure, tension, structural escalation | prose, voice, rendering | canon review and canon mutation approval | routing, validation, scheduling |
| May read public event ledger | allow | allow | allow | limited, committed packets only | allow | limited, metadata and route state only |
| May read world state ledger | no direct access | allow | limited, summary only | no direct access | limited, canon-relevant access | limited, route-relevant access only |
| May read current scene state | limited, visible facts only through `CharacterContextPacket` | allow | limited, summarized or structure-relevant view through `PlotContextSummary` | limited, `NarratorInputPacket` only | limited, canon-relevant slice only | limited, routing-relevant metadata and projection policy only |
| May read public canon | allow | allow | allow | limited, only what render needs | allow | limited, policy summary only |
| May read latent canon | no | limited, only resolution-relevant parts | limited, only structure-relevant parts | no | allow | no by default |
| May read own private memory | allow | no | no | no | no | no |
| May read others' private memory | no | no raw access; only transformed proposals | no | limited, only explicit POV-authorized material | no | no |
| May write own private memory | allow | no | no | no | no | no |
| May write public event ledger | indirect only | allow, after visibility conditions are met | no | no | no | allow, validation metadata and `ScenePacket` references only |
| May write world state ledger | no | allow, through committed `Resolution` and `StateDelta` | no | no | no | no |
| May commit world state | no | allow | no | no | no | no |
| May commit manuscript text | no | no | no | allow | no | no |
| May commit canon | no | no direct canon write | no | no | allow through `CanonDecision` and `CanonDelta`; emergent origin still needs public, latent, or scoped visibility | no |
| May request canon mutation | indirect only, through world-detected gap | allow | no | no | not applicable | no |
| May declare self subjective state | allow | no | not applicable | limited, only when packet grants interior access | no | no |
| May declare another agent's subjective state | no | no | no | limited, only when committed POV packet explicitly provides it | no | no |
| May declare objective result | no | allow | no | no | no | no |
| May declare structural pressure | no | limited, only as environment consequence and never as authorial design | allow through `ScenePressurePacket` and pressure budget | no | no | no |
| May reinterpret committed events | limited, subjective only and non-binding | no | limited, structural only and non-factual | allow, stylistic only and non-factual | no | no |
| May change point of view | no | no | no | limited, only within scene packet and style policy | no | no |
| May override another agent | no | no | no | no | limited, may reject canon mutation but not rewrite scenes | limited, may block or reroute but not rewrite content |
| Must cite `based_on` references for non-trivial actions | recommended | required | required | required when render uses interiority or compression not obvious from packet | required | recommended |
| Default failure mode | self stays local until transformed into a legal proposal | hold state commit and request repair | defer pressure rather than force progress | refuse ungrounded prose rather than invent | defer mutation rather than patch canon ad hoc | preserve flow but stop authority leakage |

## Shared Notes

### 1. Soft validation, hard permission

Malformed communication should usually trigger `warning`, `repair`, or `normalization`.

Authority violations should trigger `quarantine` or `hard block`.

This keeps the system resilient without letting roles melt together.

Security-critical field failures are not ordinary malformed communication. Missing or ambiguous `sender`, `message_type`, `visibility`, `target`, `authority_basis`, or `authorized_interiority.scope_limit` should quarantine or require explicit repair unless the route context has exactly one legal value.

### 2. Private cognition, public consequence

`Character Agent` may carry much richer inner cognition than what leaves the self boundary.

The world should only receive transformed action, dialogue, or decision proposals.

This preserves secrecy, misunderstanding, delayed revelation, and genuine local knowledge.

### 3. Dramatic window over single utterance

The default unit of coordination is a `dramatic window`, not one line of dialogue.

One window may contain:

- one short exchange
- one negotiation move
- one emotional turn
- one conceal / probe / reveal attempt

This is the main protection against slow, over-fragmented scene execution.

### 4. Narrator is bound to committed packets

`Narrator Agent` may compress, stylize, sequence, and voice-shape events.

It may not add new facts, recover rejected branches, or smuggle latent canon into prose.

Operationally, `Narrator Agent` should receive `NarratorInputPacket`, not the complete system `ScenePacket`.

### 5. Canon growth is explicit

Emergent canon provenance is allowed, but it must be reviewed and committed explicitly.

No other agent should be able to solve a scene problem by silently creating lore.

## Immediate Follow-Ups

1. adversarial protocol trace fixtures for hidden theft, false report, narrator leak, world overreach, and plot railroading
2. narration grounding validator against `NarratorInputPacket`
3. public scope registry and audience membership model
4. canon-vs-state classification checklist
5. dialogue-specific evaluation metrics after runtime authority fixtures exist
