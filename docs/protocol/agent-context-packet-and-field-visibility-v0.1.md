# AgentContextPacket and Field Visibility v0.1

This document defines the first runtime context assembly contract for `a2a-literary-agents`.

The access matrices define what each agent is allowed to know in principle. This spec defines what each agent actually receives during a protocol step.

Its central rule is simple:

- complete protocol objects are system objects
- agents receive projected views
- visibility labels are not security by themselves unless context assembly enforces them

## Purpose

`AgentContextPacket` exists to solve five protocol problems:

1. prevent hidden omniscience from returning through prompt construction
2. define per-agent projected views of `ScenePacket`, `DialogueWindow`, memory, canon, and public events
3. distinguish recoverable schema fields from security-critical authority fields
4. make `Narrator Agent` consume `NarratorInputPacket`, not raw system state
5. give `Orchestrator` a mechanical assembly contract instead of editorial content power

Without this layer, the protocol may say that an agent cannot know a fact while still accidentally placing that fact inside the agent's prompt context.

## Design Constraints

Context assembly should satisfy these constraints:

1. no agent receives a complete system object by default
2. each projected field must have an explicit source and permission basis
3. hidden facts, hidden cognition, and pending canon may not leak through summaries
4. security-critical fields are never silently invented unless the route context has one unique legal value
5. context compression must cite source refs and must not create new facts

## Core Objects

| Object | Meaning | Owner | Notes |
| --- | --- | --- | --- |
| `AgentContextPacket` | the general per-agent context envelope assembled for one protocol step | `Orchestrator` | not literary content |
| `ScenePacketView` | a projected slice of a committed `ScenePacket` | `Orchestrator` | recipient-specific |
| `NarratorInputPacket` | the only legal factual input for narration | `Orchestrator` | derived from committed material only |
| `CharacterContextPacket` | the context a `Character Agent` may use to form intent or dialogue | `Orchestrator` | owner-specific memory plus visible world |
| `PlotContextSummary` | the structural view a `Plot Agent` may use to propose pressure | `Orchestrator` | no raw hidden truth |
| `CanonReviewContext` | the canon-relevant context for `Canon Steward` | `Orchestrator` | may include restricted canon refs |
| `FieldProjection` | a field-level allowlist mapping from source object to recipient view | protocol policy | prevents object-level leakage |

## AgentContextPacket Shape

Suggested payload fields:

| Field | Required | Type | Meaning |
| --- | --- | --- | --- |
| `context_id` | yes | string | stable id for this context packet |
| `scene_id` | yes | string | parent scene identity |
| `window_id` | recommended | string | active dramatic window if applicable |
| `recipient_agent_id` | yes | string | exact receiving agent instance |
| `recipient_role` | yes | string | `character_agent`, `world_agent`, `plot_agent`, `narrator_agent`, `canon_steward`, or `orchestrator` |
| `protocol_step` | yes | string | why this context is being assembled |
| `visible_inputs` | yes | object | projected observations, events, packets, memory, canon, or pressure |
| `source_refs` | yes | array | all source object ids used to build the context |
| `projection_policy` | yes | string | policy name or version used for field redaction |
| `redaction_notes` | recommended | array | what was removed and why |
| `validation_warnings` | optional | array | non-fatal assembly issues |
| `forbidden_sources` | recommended | array | source families this packet explicitly did not include |
| `based_on` | recommended | array | route, packet, policy, and matrix refs |

Important rule:

- `AgentContextPacket` is an infrastructure object, not a new story fact
- it may package, filter, and cite, but it may not invent or editorialize

## Context Assembly Flow

Recommended flow:

1. identify the recipient role and active protocol step
2. collect candidate source objects by route table
3. apply role-level allowlist
4. apply field-level projection
5. remove unresolved, pending, unauthorized, or out-of-scope material
6. attach source refs and redaction notes
7. validate security-critical fields
8. deliver only the projected context

Important rule:

- validation happens before delivery, not after the receiving agent has already seen the material

## Security-Critical Fields

Some fields are ordinary schema fields. Others carry authority, privacy, or routing power.

| Field family | Examples | Missing-field behavior |
| --- | --- | --- |
| identity | `sender`, `recipient_agent_id`, `recipient_role`, `owner_agent_id` | quarantine unless route context has one unique legal value |
| authority | `message_type`, `writer_role`, `authority_basis`, `mutation_kind`, `outcome_type` | quarantine or require repair |
| visibility | `visibility`, `observer_scope`, `exposure_scope`, `scope_limit`, `knowledge_ceiling` | quarantine or require explicit repair |
| target | `target`, `target_id`, `addressee_ids`, `affected_options` | infer only if mechanically unique; otherwise repair |
| canon reference | `canon_ref`, `latent_ref`, `target_layer`, `canon_delta_ref` | defer or quarantine |
| interiority | `authorized_interiority.subject_id`, `access_mode`, `scope_limit` | reject as unusable if incomplete |

Recoverable fields include `message_id`, `scene_id`, `window_id`, `based_on`, and optional lineage metadata.

Important rule:

- soft validation may repair coordination
- it must not repair privacy or authority by guessing

## Field Projection: DialogueWindow

`DialogueWindow` is not one shareable object. It mixes private tactic, surface speech proposal, resolver input, and audit material.

| Field | Resolver view | Target visible view | Narrator candidate view | Audit-only view |
| --- | --- | --- | --- | --- |
| `window_kind` | allow | allow if visible in behavior | allow after resolution | allow |
| `speaker_id` | allow | allow | allow after resolution | allow |
| `addressee_ids` | allow | allow for included targets | allow after resolution | allow |
| `local_goal` | allow | no by default | no direct read | allow |
| `stance.emotional_tone` | allow | only if externally legible | only if committed or authorized | allow |
| `stance.tactical_posture` | allow | no by default | no direct read | allow |
| `disclosure_policy.must_not_reveal` | allow | no | no | allow |
| `disclosure_policy.may_imply` | allow | no direct read | no direct read | allow |
| `disclosure_policy.can_lie` | allow | no | no | allow |
| `disclosure_policy.preferred_mask` | allow | only as visible performance if resolved | only if committed as visible behavior | allow |
| `speech_acts.intent` | allow | no direct read | no direct read | allow |
| `speech_acts.proposition` | allow | visible if spoken or implied in committed event | allow only after commitment | allow |
| `speech_acts.candidate_lines` | allow as non-authoritative | visible only if chosen or paraphrased in committed surface | candidate reference only, never fact by itself | allow |
| `speech_acts.expected_effect` | allow | no | no | allow |
| `fallback_if_blocked` | allow | no | no direct read | allow |
| `exit_condition` | allow | no direct read | no direct read | allow |

Important rule:

- `Narrator Agent` does not render from raw `DialogueWindow`
- it may only use dialogue material after `World Agent` resolution and `ScenePacket` sealing

## Field Projection: ScenePacket

The complete `ScenePacket` is a system object. Recipient views are narrower.

| View | Recipient | May contain | Must exclude |
| --- | --- | --- | --- |
| `ScenePacketView` | any eligible agent | fields legal for that role and step | unauthorized interiority, pending canon, hidden state not visible to recipient |
| `NarratorInputPacket` | `Narrator Agent` | committed events, authorized interiority, narration bounds, approved public/canon material | raw hidden state, rejected branches, raw DialogueWindow, unapproved candidates |
| `CharacterContextPacket` | one `Character Agent` | visible scene facts, owner memory query results, encountered public events, public canon | other private memory, raw world ledger, hidden canon |
| `PlotContextSummary` | `Plot Agent` | structure progress, public events, relationship trends, limited non-spoiling summaries | raw cognition, exact hidden world facts, future outcomes |
| `CanonReviewContext` | `Canon Steward` | canon refs, mutation request, committed evidence, reveal basis | irrelevant private cognition, prose drafts |

Important rule:

- a visibility label inside a packet is evidence for projection
- it is not permission to send the whole packet

## Agent Context Matrix

| Recipient | Default context contents | Explicit exclusions |
| --- | --- | --- |
| `Character Agent` | owner `private_memory` query result, visible observations, encountered public events, public canon, public pressure | raw `world_state_ledger`, other agents' private memory, latent canon, full `ScenePacket` |
| `World Agent` | submitted proposals, relevant world state, public canon, limited latent canon if resolution-relevant, canon decisions | raw inner monologue not transformed into action, plot destiny directives |
| `Plot Agent` | structure summary, public event trends, relationship map summaries, pressure budget state | raw hidden truth, exact private cognition, direct outcome authority |
| `Narrator Agent` | `NarratorInputPacket`, approved style guide, narration bounds | raw proposals, hidden world ledger, pending reveal candidates, unauthorized interiority |
| `Canon Steward` | canon refs, review request, committed reveal evidence, affected canon history | scene prose drafts unless canon-relevant, irrelevant private memory |
| `Orchestrator` | route metadata, validation policy, projection policy, source refs | literary content rewriting authority |

## Context Compression Policy

Compression is allowed when a context would be too large, but compression is not free narration.

Allowed compression:

- short factual summaries of already legal material
- role-specific lists of relevant refs
- salience-ranked memory query results
- public event summaries within legal scope

Forbidden compression:

- replacing hidden facts with suggestive summaries that reveal them
- merging suspicion into fact
- turning unresolved candidate material into committed reality
- narrativizing route decisions as story meaning

Any non-mechanical summary should include:

- `source_refs`
- `compression_policy`
- `omitted_categories`

## Hard Boundaries

Context assembly may:

- project fields
- redact illegal material
- attach warnings and source refs
- produce per-agent context packets

Context assembly may not:

- invent facts
- choose literary emphasis as if it were an author
- launder hidden state into summaries
- make pending canon usable as public truth
- repair missing security-critical fields by creative inference

## Example

```json
{
  "context_id": "ctx_char_lin_018_06",
  "scene_id": "scene_018",
  "window_id": "win_018_06",
  "recipient_agent_id": "char_lin",
  "recipient_role": "character_agent",
  "protocol_step": "prepare_dialogue_window",
  "visible_inputs": {
    "observations": [
      "Wei asked about the records room in a way Lin could perceive as unusually careful."
    ],
    "private_memory_query": [
      "Lin remembers hearing hurried footsteps near the archive."
    ],
    "public_events": [],
    "public_canon": [
      "Archive ledgers are normally sealed after dusk."
    ],
    "pressure": [
      "The inspection deadline is approaching."
    ]
  },
  "source_refs": ["sp_018_02:view:char_lin", "md_lin_201", "pc_archive_rule_03", "spp_018_01:view:public"],
  "projection_policy": "field_visibility_v0.1",
  "redaction_notes": [
    "Wei's disclosure_policy and hidden goal were excluded.",
    "Raw world_state_ledger entries were not included."
  ],
  "forbidden_sources": ["raw_world_state_ledger", "latent_canon", "other_private_memory"],
  "based_on": ["agent-constraint-matrix-v0.1", "communication-permission-matrix-v0.1"]
}
```

## Relationship to Adjacent Specs

This document should be read together with:

- `communication-permission-matrix-v0.1.md`
- `agent-constraint-matrix-v0.1.md`
- `dialogue-window-schema-v0.1.md`
- `scene-packet-schema-v0.1.md`
- `scene-packet-to-memory-handoff-v0.1.md`

Next protocol priority after this document:

1. keep `Resolution` and `StateDelta` commit pipeline aligned with these projections
2. keep `ScenePressurePacket` outputs constrained by the same context assembly rules
3. design adversarial trace fixtures before building an autonomous scene runner
