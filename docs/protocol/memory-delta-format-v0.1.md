# Memory Delta Format v0.1

This document defines the first concrete update format for `private_memory`.

`MemoryDelta` is the owner-scoped record unit by which scene outcomes, observations, suspicions, and reinterpretations enter a character's memory layer.

It is not objective world truth.

It is the protocol object that lets different agents carry different fragments, different certainty levels, and different interpretations of the same underlying scene reality.

## Purpose

`MemoryDelta` exists to solve five protocol problems:

1. give `private_memory` a concrete write format
2. preserve the distinction between world truth and owner knowledge
3. let `World Agent` inject perception-backed updates without writing a character's full interpretation
4. let `Character Agent` append owner-side suspicion, emotion, and reinterpretation
5. allow memory to remain revisable without collapsing into omniscient fact storage

Without a memory-delta format, the state-layer model remains conceptually correct but operationally under-specified.

## Design Constraints

`MemoryDelta` should satisfy these constraints:

1. every delta must belong to exactly one memory owner
2. observation, inference, suspicion, and self-interpretation must remain distinguishable
3. uncertainty and contradiction must be representable
4. world-written deltas must not silently become mind-reading
5. superseded memory should remain traceable rather than disappearing without lineage

## Placement in the Protocol

Recommended flow:

1. `World Agent` resolves scene outcomes
2. committed material is packed into `ScenePacket`
3. owner-specific `MemoryDelta` objects are derived from committed scene consequences, visibility, and authorized owner cognition
4. `World Agent` may inject perception-backed deltas
5. `Character Agent` may append interpretation, suspicion, emotional aftermath, or self-commitment deltas
6. `private_memory` stores active deltas and keeps superseded lineage

Important distinction:

- one `ScenePacket` may generate zero, one, or many `MemoryDelta` objects
- different owners may receive different deltas from the same scene packet
- owner memory derivation should use `owner_projection`, not the full system `ScenePacket`

## Writer Rules

Memory updates are not symmetric across roles.

| Writer | May write | May not write |
| --- | --- | --- |
| `World Agent` | observation-backed deltas, noticed absence, public report receipt, bodily-state updates, visibility-backed suspicion seeds | full private motive, interpretive monologue, thematic meaning, illegal hidden truth |
| `Character Agent` | suspicion, reinterpretation, recollection, emotional aftermath, self-commitment, self-correction | objective world fact as if globally verified, other minds as certain truth |
| `Orchestrator` | package references, routing metadata, storage lineage | invent literary memory content |

Important rule:

- `World Agent` may write what the owner plausibly perceived or was directly affected by
- `World Agent` may not write what the owner "really concludes" unless that conclusion has been explicitly externalized or authorized

## Delta Shape

The fields below describe the delta payload.

| Field | Required | Type | Meaning |
| --- | --- | --- | --- |
| `delta_id` | yes | string | stable id for this memory update |
| `owner_agent_id` | yes | string | whose `private_memory` this delta belongs to |
| `writer_role` | yes | string | which role authored the delta |
| `source_packet_id` | recommended | string | which committed `ScenePacket` this delta came from |
| `delta_kind` | yes | string | what type of memory update this is |
| `acquisition_mode` | yes | string | how the owner came to hold this memory |
| `content` | yes | string | the memory content itself |
| `certainty` | recommended | string | low, medium, or high certainty |
| `memory_status` | yes | string | active, superseded, withdrawn, or contested |
| `retention` | optional | string | fleeting, scene, chapter, long_term, persistent |
| `supersedes` | optional | array | which earlier deltas this update supersedes or revises |
| `based_on` | recommended | array | causal or evidentiary refs for this delta |

## `delta_kind`

Suggested values:

- `observation`
- `noticed_absence`
- `received_report`
- `inference`
- `suspicion`
- `recollection`
- `emotional_aftereffect`
- `self_commitment`
- `belief_revision`

Important distinction:

- `observation` means the owner directly registered something
- `inference` means the owner drew a conclusion from available material
- `suspicion` means the owner leans toward a possibility without treating it as settled
- `belief_revision` means an earlier memory has been updated, weakened, or reinterpreted

## `acquisition_mode`

Suggested values:

- `saw`
- `heard`
- `was_told`
- `noticed`
- `inferred`
- `remembered`
- `felt`
- `self_acted`

This field answers "through what path did this memory enter the owner?"

## `memory_status`

`private_memory` should preserve revision lineage.

Suggested values:

- `active`
- `superseded`
- `withdrawn`
- `contested`

Important rule:

- a superseded delta should remain in history
- it should stop governing current reasoning unless the owner explicitly revisits it

## Hard Boundaries

`MemoryDelta` may contain:

- what the owner observed
- what the owner inferred
- what the owner suspects
- what the owner emotionally carries forward
- what the owner now intends to remember or act on

`MemoryDelta` may not contain:

- free global truth dump from `world_state_ledger`
- another character's hidden motive as certain fact
- narrator-side thematic interpretation
- latent canon not legally available to the owner

## Validation Rules

| Rule | Behavior |
| --- | --- |
| missing `owner_agent_id` | reject as unusable |
| missing `delta_kind` | warn and require repair |
| `writer_role = world_agent` with purely interpretive inner conclusion | reject or require downgrade to visible seed |
| `memory_status = superseded` without `supersedes` refs | warn and request repair |
| missing `source_packet_id` on world-written delta | warn; require route justification |
| certainty omitted on `inference` or `suspicion` | warn and fill conservatively if needed |
| memory content relies on pending publication or canon reveal candidate | reject until exposure or approval path is explicit |

## Commit Semantics

`MemoryDelta` is not "committed" in the same sense as world truth.

Instead, it should count as stored owner-memory when:

1. the owner is explicit
2. the writer role is permitted for the delta kind
3. the delta is traceable to a committed packet, a legal owner action, or a legal recollection path
4. storage status is assigned (`active`, `superseded`, etc.)

Important consequence:

- `MemoryDelta` may be wrong, partial, or later revised
- but the delta itself must be legally attributable and structurally valid

## Example

Below, the same scene packet produces different deltas for different owners.

```json
[
  {
    "delta_id": "md_lin_201",
    "owner_agent_id": "char_lin",
    "writer_role": "world_agent",
    "source_packet_id": "sp_018_02",
    "delta_kind": "observation",
    "acquisition_mode": "heard",
    "content": "Lin heard hurried footsteps near the archive",
    "certainty": "medium",
    "memory_status": "active",
    "retention": "chapter",
    "based_on": ["ev_412", "vd_019"]
  },
  {
    "delta_id": "md_lin_202",
    "owner_agent_id": "char_lin",
    "writer_role": "character_agent",
    "source_packet_id": "sp_018_02",
    "delta_kind": "suspicion",
    "acquisition_mode": "inferred",
    "content": "Wei may know more about the missing ledger than he should",
    "certainty": "medium",
    "memory_status": "active",
    "retention": "chapter",
    "based_on": ["md_lin_201", "sp_018_02"]
  },
  {
    "delta_id": "md_wei_088",
    "owner_agent_id": "char_wei",
    "writer_role": "character_agent",
    "source_packet_id": "sp_018_02",
    "delta_kind": "self_commitment",
    "acquisition_mode": "self_acted",
    "content": "Wei must continue concealing the archive copy unless direct accusation becomes unavoidable",
    "certainty": "high",
    "memory_status": "active",
    "retention": "chapter",
    "based_on": ["sp_018_02"]
  },
  {
    "delta_id": "md_lin_203",
    "owner_agent_id": "char_lin",
    "writer_role": "character_agent",
    "source_packet_id": "sp_019_01",
    "delta_kind": "belief_revision",
    "acquisition_mode": "inferred",
    "content": "Lin now thinks Wei's evasiveness may come from fear rather than guilt alone",
    "certainty": "low",
    "memory_status": "active",
    "retention": "chapter",
    "supersedes": ["md_lin_202"],
    "based_on": ["sp_019_01", "md_lin_202"]
  }
]
```

## Relationship to Adjacent Specs

This document should be read together with:

- `state-and-knowledge-layers-v0.1.md`
- `scene-packet-schema-v0.1.md`
- `agent-constraint-matrix-v0.1.md`
- `scene-packet-to-memory-handoff-v0.1.md`
- `agent-context-packet-and-field-visibility-v0.1.md`

Next protocol priority after this document:

1. memory retrieval policy for `CharacterContextPacket`
2. adversarial trace fixtures for divergent memory and mistaken inference
3. dialogue evaluation metrics after context assembly is stable
