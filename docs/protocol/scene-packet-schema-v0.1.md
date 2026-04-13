# ScenePacket Schema v0.1

This document defines the first concrete schema for `ScenePacket`.

`ScenePacket` is the protocol's committed handoff object between world adjudication and downstream narration or memory work.

It is the main structure that turns "resolved scene reality" into "legal narrative source material."

## Purpose

`ScenePacket` exists to solve four protocol problems at once:

1. give `Narrator Agent` one legal factual input object
2. prevent raw `DialogueWindow` or hidden world state from being narrated directly
3. separate resolved consequence from mere proposal or pressure
4. provide a stable bridge from scene execution into memory and manuscript layers

Without `ScenePacket`, the rule `narrator cannot invent facts` remains a principle without a sufficiently concrete handoff structure.

## Design Constraints

`ScenePacket` should satisfy these constraints:

1. It must only contain committed material.
2. It must distinguish objective consequence from public knowledge.
3. It must expose interiority only through explicit authorization.
4. It must preserve local knowledge and avoid hidden omniscience leakage.
5. It must be useful both for prose rendering and later memory summarization.

## Placement in the Protocol

Recommended loop:

1. `Plot Agent` injects scene pressure if needed
2. `World Agent` publishes observations
3. active `Character Agent` submits `Intent`, `ActionProposal`, or `DialogueWindow`
4. `World Agent` resolves outcomes and commits state change
5. `Orchestrator` assembles committed material into `ScenePacket`
6. `Narrator Agent` renders prose from committed `ScenePacket`
7. memory layers and manuscript layers inherit from the packet rather than from raw proposals

Important rule:

- `Narrator Agent` may read committed `ScenePacket`
- `Narrator Agent` may not read raw hidden truth, rejected branches, or unresolved proposals as factual input

## Source Layers and Read Policy

`ScenePacket` is assembled from multiple layers, but not all layers contribute in the same way.

| Layer | May contribute to `ScenePacket` | Conditions | Why |
| --- | --- | --- | --- |
| `world_state_ledger` | yes | only committed, scene-relevant, resolution-backed material | this is the objective source of what actually happened |
| `public_event_ledger` | yes | when the scene causes something to become publicly knowable | needed for shared-knowledge consequences |
| `private_memory` | limited | only through explicit `authorized_interiority` or POV authorization | preserves local knowledge while allowing controlled inner access |
| `public_canon` | limited | only render-relevant or causally necessary references | keeps setting-grounded narration stable |
| `latent_canon` | no direct raw read | only if a reveal has been explicitly legalized and included as packet material | prevents narrator leakage of hidden canon |

This means `ScenePacket` may indirectly reflect multiple layers, but it should never act like a free omniscient dump.

## Packet Shape

The fields below describe the packet payload.

| Field | Required | Type | Meaning |
| --- | --- | --- | --- |
| `packet_id` | yes | string | stable id for this committed packet |
| `scene_id` | yes | string | parent scene identity |
| `packet_scope` | yes | string | scene, subscene, or window-group scope |
| `commit_status` | yes | string | draft or committed; narrator may only use committed |
| `pov_contract` | yes | object | the viewpoint and interiority rules for narration |
| `resolved_events` | yes | array | what objectively happened in this packet span |
| `state_deltas` | yes | array | committed changes to world state |
| `visibility_deltas` | recommended | array | what became visible to whom |
| `public_event_deltas` | recommended | array | what entered public/shared knowledge |
| `authorized_interiority` | optional | array | explicitly permitted inner material for narration |
| `canon_effects` | optional | array | canon reveals or canon-relevant consequences included in the packet |
| `narration_bounds` | recommended | object | what narration may compress, must preserve, or must not claim |
| `based_on` | recommended | array | source resolution ids, state refs, or packet lineage |

## `pov_contract`

`pov_contract` defines how much interior access the packet grants.

Suggested shape:

| Field | Required | Meaning |
| --- | --- | --- |
| `mode` | yes | external, limited, close, or first_person |
| `focal_agent_id` | recommended | whose viewpoint governs narration |
| `knowledge_ceiling` | recommended | the maximum knowledge level narration may assume |
| `interiority_policy` | yes | whether inner material is forbidden, selective, or primary |
| `multi_agent_policy` | optional | whether more than one mind may be represented in this packet |

Important rule:

- `pov_contract` is not a style suggestion
- it is an authority boundary for what narration may claim

## `resolved_events`

Each packet should contain one or more `resolved_events`.

These are not proposals. They are already-adjudicated scene facts.

Suggested shape:

| Field | Required | Meaning |
| --- | --- | --- |
| `event_id` | yes | stable event identifier |
| `event_kind` | yes | dialogue, movement, confrontation, discovery, injury, reveal, etc. |
| `actors` | yes | which agents or characters were involved |
| `outcome` | yes | what factually happened |
| `visibility` | yes | who can directly know this event from the scene itself |
| `causal_basis` | recommended | what resolution or rule basis produced this event |

## `state_deltas`

`state_deltas` describe what changed in committed world state.

Suggested shape:

| Field | Required | Meaning |
| --- | --- | --- |
| `delta_id` | yes | stable delta id |
| `target_kind` | yes | character, object, location, relation, resource, etc. |
| `target_id` | yes | what changed |
| `change` | yes | the committed state change |
| `persistence` | optional | temporary, scene-long, chapter-long, persistent |

## `visibility_deltas`

This field prevents a collapse between "event happened" and "everyone now knows it."

Suggested shape:

| Field | Required | Meaning |
| --- | --- | --- |
| `delta_id` | yes | stable delta id |
| `observer_scope` | yes | self, pair, scene group, public, or restricted subset |
| `newly_visible` | yes | what became newly visible or inferable |
| `certainty` | optional | low, medium, high |

## `authorized_interiority`

This field is the main safeguard against narrator overreach.

It is the only packet-level route by which inner material may legally enter narration unless the POV contract itself already allows full focal interiority.

Suggested shape:

| Field | Required | Meaning |
| --- | --- | --- |
| `subject_id` | yes | whose interiority is being exposed |
| `access_mode` | yes | feeling, thought, memory, motive, suppression, uncertainty |
| `content` | yes | the authorized inner material |
| `authority_basis` | yes | why this interiority is legal to narrate |
| `scope_limit` | optional | one line, one beat, this packet only, etc. |

Important rule:

- absence of `authorized_interiority` should be treated as absence of permission
- narrator must not infer full interiority from consequence alone unless the POV contract allows it

## `canon_effects`

`canon_effects` should only appear when the packet includes a canon-relevant reveal or consequence.

Suggested shape:

| Field | Required | Meaning |
| --- | --- | --- |
| `effect_kind` | yes | reveal, clarification, mutation_request, mutation_approved |
| `canon_ref` | recommended | which canon element is affected |
| `effect_summary` | yes | what changed or was revealed |
| `review_status` | yes | pending, approved, rejected, not_needed |

Important rule:

- raw `latent_canon` should not be injected into narration through this field
- only legalized reveal material belongs here

## `narration_bounds`

`narration_bounds` tells the downstream prose layer what flexibility it has.

Suggested shape:

| Field | Required | Meaning |
| --- | --- | --- |
| `must_preserve` | recommended | facts, order, wording, or constraints narration must preserve |
| `may_compress` | recommended | what may be summarized rather than shown beat-by-beat |
| `must_not_claim` | yes | facts or minds the narrator may not assert |
| `ordering_flex` | optional | whether exact order may be reordered for prose clarity |

## Hard Boundaries

`ScenePacket` may contain:

- committed scene facts
- committed state change
- explicit visibility consequences
- explicitly authorized inner material

`ScenePacket` may not contain:

- rejected branches
- unresolved proposals
- free omniscient hidden truth
- raw chain-of-thought dumps
- unapproved latent canon presented as public fact

## Commit Semantics

A `ScenePacket` should count as `committed` only when all of the following are true:

1. included `resolved_events` already have world adjudication
2. included `state_deltas` have been accepted as committed world change
3. visibility consequences have been resolved to the needed level
4. any canon-relevant content is either approved, explicitly marked pending, or excluded from factual narration
5. the packet has been sealed by `Orchestrator` with source references

Narrator rule:

- `commit_status = committed` is required for factual narration
- draft packets may be reviewed by system layers but must not be treated as legal prose source material

## Example

```json
{
  "packet_id": "sp_018_02",
  "scene_id": "scene_018",
  "packet_scope": "window_group",
  "commit_status": "committed",
  "pov_contract": {
    "mode": "close",
    "focal_agent_id": "char_lin",
    "knowledge_ceiling": "lin_only",
    "interiority_policy": "selective",
    "multi_agent_policy": "single_focal"
  },
  "resolved_events": [
    {
      "event_id": "ev_411",
      "event_kind": "dialogue_probe",
      "actors": ["char_wei", "char_lin"],
      "outcome": "Wei probes Lin about the missing ledger; Lin withholds certainty",
      "visibility": "scene_pair",
      "causal_basis": ["res_411"]
    },
    {
      "event_id": "ev_412",
      "event_kind": "discovery_shift",
      "actors": ["char_lin"],
      "outcome": "Lin becomes more suspicious of Wei's knowledge",
      "visibility": "char_lin_only",
      "causal_basis": ["res_412"]
    }
  ],
  "state_deltas": [
    {
      "delta_id": "sd_118",
      "target_kind": "relation",
      "target_id": "lin_wei_trust",
      "change": "trust decreases slightly",
      "persistence": "chapter_long"
    }
  ],
  "visibility_deltas": [
    {
      "delta_id": "vd_019",
      "observer_scope": "char_lin_only",
      "newly_visible": "Wei may know more than he should",
      "certainty": "medium"
    }
  ],
  "public_event_deltas": [],
  "authorized_interiority": [
    {
      "subject_id": "char_lin",
      "access_mode": "suspicion",
      "content": "Lin feels the exchange has shifted from routine concern to veiled testing",
      "authority_basis": "close focal POV",
      "scope_limit": "this_packet_only"
    }
  ],
  "canon_effects": [],
  "narration_bounds": {
    "must_preserve": [
      "Wei does not confess",
      "Lin does not publicly accuse"
    ],
    "may_compress": [
      "minor pauses and repeated evasions"
    ],
    "must_not_claim": [
      "Wei's full hidden motive",
      "objective proof that Wei stole the ledger"
    ],
    "ordering_flex": "low"
  },
  "based_on": [
    "dw_018_05",
    "res_411",
    "res_412",
    "wsl_018_07"
  ]
}
```

## Relationship to Adjacent Specs

This document should be read together with:

- `dialogue-window-schema-v0.1.md`
- `state-and-knowledge-layers-v0.1.md`
- `communication-permission-matrix-v0.1.md`

Next protocol priority after this document:

1. align reveal and handoff terms with the terminology index
2. dialogue evaluation metrics
3. prototype a minimal scene runner once protocol terminology stabilizes
