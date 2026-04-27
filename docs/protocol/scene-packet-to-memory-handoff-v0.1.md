# ScenePacket-to-Memory Handoff v0.1

This document defines the first rule set for deriving `MemoryDelta` objects from a committed `ScenePacket`.

The handoff is the protocol step that turns one committed scene packet into zero, one, or many owner-specific memory updates.

Its job is to preserve local knowledge while still letting committed scene reality leave a usable trace inside `private_memory`.

## Purpose

This document exists to solve five protocol problems:

1. define how `ScenePacket` becomes owner-specific `MemoryDelta` output
2. prevent automatic full-packet fanout into every character's memory
3. separate world-written perceptual memory from owner-written interpretation
4. preserve traceability from stored memory back to committed scene material
5. keep `public_event_ledger` and `private_memory` distinct even when both grow from the same scene

Without handoff rules, `ScenePacket` and `MemoryDelta` are both defined, but the transition between them remains underspecified.

## Design Constraints

The handoff should satisfy these constraints:

1. every derived memory must belong to an explicit owner
2. no packet field should automatically duplicate into all owners
3. world-side derivation must stay perception-backed or effect-backed
4. owner-side interpretation must remain owner-scoped rather than globally certified
5. public publication should not be confused with private memory ingestion

## Placement in the Protocol

Recommended flow:

1. `World Agent` resolves scene outcomes
2. `Orchestrator` seals committed material into `ScenePacket`
3. handoff logic determines which owners are eligible for packet-derived memory
4. `World Agent` derives owner-specific perception or impact deltas
5. `Character Agent` may append owner-side suspicion, emotional aftermath, or self-commitment
6. `private_memory` stores valid deltas with lineage back to the source packet

Important distinction:

- complete `ScenePacket` is a system committed source object
- handoff receives an owner-specific `owner_projection`, not a full packet dump
- `MemoryDelta` output remains owner-divergent

## Core Rule: No Automatic Full-Packet Duplication

A committed packet is not a broadcast memory object.

Important rule:

- the existence of a committed `ScenePacket` does **not** mean every character receives the packet as memory
- only owner-relevant, legally accessible, perception-backed, or impact-backed material may become `MemoryDelta`

This prevents a slide back into hidden omniscience.

## Eligibility: Which Owners May Receive Packet-Derived Memory

An owner becomes a handoff candidate when at least one of the following is true:

1. the owner is an actor in one of the packet's `resolved_events`
2. the owner is the target of a `state_delta`
3. the owner appears inside a relevant `visibility_delta`
4. the owner is the subject of `authorized_interiority`
5. the owner directly receives a report, declaration, or publication inside the committed scene span

Important consequence:

- if none of these apply, the packet may produce no memory delta for that owner

## `owner_projection`

Before writing memory, the packet should be filtered into an `owner_projection`.

`owner_projection` means the owner-specific slice of a committed `ScenePacket` that the handoff logic is allowed to use for one owner's memory derivation.

Suggested contents:

| Component | Meaning |
| --- | --- |
| `owner_agent_id` | whose projection this is |
| `visible_events` | which `resolved_events` this owner can directly witness or legally register |
| `owner_impacts` | which `state_deltas` directly affect this owner |
| `owner_visibility` | which `visibility_deltas` explicitly mention this owner or their scope |
| `authorized_inner_material` | which packet-level inner material is legally accessible for this owner |
| `public_contact` | whether the owner actually encountered a publication or declaration within the packet span |

Important rule:

- `owner_projection` is a handoff filter, not a new truth layer

## Source-to-Delta Contribution Rules

Different packet fields contribute to memory in different ways.

| Packet field | May produce `MemoryDelta` | Typical delta kinds | Important limits |
| --- | --- | --- | --- |
| `resolved_events` | yes | `observation`, `noticed_absence`, limited `received_report` | only for owners who witnessed, participated in, or were directly informed by the event |
| `state_deltas` | limited | `observation`, `emotional_aftereffect`, `self_commitment` seed | only when the owner is directly affected or can plausibly perceive the effect |
| `visibility_deltas` | yes | `observation`, `inference`, `suspicion` seed | strongest basis for owner-specific knowledge distribution |
| `publication_candidates` | no direct memory write | none | candidate publication is not yet public knowledge |
| `public_event_deltas` | conditional | `received_report`, `observation` | approved publications only; do not auto-copy into every owner; require an encounter path |
| `authorized_interiority` | yes, but tightly scoped | `emotional_aftereffect`, `recollection`, owner-authorized `belief_revision` seed | do not convert one owner's interiority into another owner's memory |
| `canon_reveal_candidates` | no direct memory write | none | candidate reveal is not yet owner-legal canon knowledge unless separately exposed |
| `canon_effects_committed` | conditional | `received_report`, `belief_revision` | only if the owner is legally exposed to the approved reveal in the packet span |
| `narration_bounds` | no direct content write | none | constrains prose, not memory content |

## Writer Split During Handoff

The handoff is not authored by one role alone.

| Role | Handoff responsibility | May not do |
| --- | --- | --- |
| `World Agent` | derive perception-backed or impact-backed owner deltas from the packet | write full private interpretation as if objectively verified |
| `Character Agent` | append owner-side suspicion, belief revision, emotional aftermath, recollection, self-commitment | globalize the owner's interpretation into shared fact |
| `Orchestrator` | route packet refs, owner projections, and lineage metadata | invent memory prose or hidden cognition |

Important rule:

- `World Agent` writes what the owner could plausibly carry away
- `Character Agent` writes what the owner does with it internally

## Public Event Non-Duplication Rule

`public_event_ledger` and `private_memory` must not collapse into one another.

Important rule:

- a `public_event_delta` entering `public_event_ledger` does **not** automatically create a matching `MemoryDelta` for every eligible agent

Recommended policy:

1. if an owner directly encountered the publication in the packet span, a `received_report` or `observation` delta may be written
2. if the owner did not encounter the publication, the event may remain readable through `public_event_ledger` without being duplicated into `private_memory`

This keeps public knowledge queryable without forcing mass memory duplication.

## Suggested Handoff Pipeline

Recommended handoff steps:

1. validate that the packet is `committed`
2. enumerate candidate owners
3. build one `owner_projection` per candidate
4. derive world-side deltas from witnessed events, impacts, and visibility shifts
5. allow owner-side augmentation by `Character Agent`
6. run deduplication and supersession checks
7. store valid deltas into each owner's `private_memory`

## Deduplication and Revision

Handoff should avoid blind duplication when a packet restates something already held in memory.

Recommended behavior:

- if the packet adds no new owner-relevant information, write nothing
- if the packet weakens or revises an existing owner belief, create a new delta with `supersedes`
- if the packet confirms a prior suspicion, prefer a stronger delta rather than parallel duplicates

Important rule:

- handoff is allowed to produce zero deltas
- zero-delta output is better than noisy memory inflation

## Hard Boundaries

The handoff may produce:

- perception-backed memory
- owner-specific impact memory
- owner-scoped suspicion or revision
- legally encountered public-report memory

The handoff may not produce:

- full packet copies inside every owner
- another character's hidden inner truth as memory fact
- narrator-only compression as memory content
- public publication duplicated into all private memories without an encounter path
- raw hidden canon unless the owner is legally exposed within the packet
- pending publication or canon reveal candidates stored as if approved

## Commit Semantics

A packet-to-memory handoff should count as valid only when all of the following are true:

1. the source packet is committed
2. each output delta has an explicit owner
3. each output delta can be traced to allowed packet fields
4. world-written and owner-written responsibilities remain separated
5. any supersession or revision lineage is recorded where needed

Important consequence:

- the handoff can be structurally valid even when resulting memory is partial, mistaken, or owner-biased
- what matters is lawful derivation, not universal correctness

## Example

Below, one committed packet yields different memory outcomes for Lin and Wei.

```json
{
  "source_packet_id": "sp_018_02",
  "owner_projections": [
    {
      "owner_agent_id": "char_lin",
      "visible_events": ["ev_411", "ev_412"],
      "owner_impacts": ["sd_118"],
      "owner_visibility": ["vd_019"],
      "authorized_inner_material": ["ai_001"],
      "public_contact": []
    },
    {
      "owner_agent_id": "char_wei",
      "visible_events": ["ev_411"],
      "owner_impacts": [],
      "owner_visibility": [],
      "authorized_inner_material": [],
      "public_contact": []
    }
  ],
  "derived_memory_deltas": [
    {
      "owner_agent_id": "char_lin",
      "writer_role": "world_agent",
      "delta_kind": "observation",
      "content": "Lin registered Wei's probing interest in the missing ledger."
    },
    {
      "owner_agent_id": "char_lin",
      "writer_role": "character_agent",
      "delta_kind": "suspicion",
      "content": "Wei may know more than he should."
    },
    {
      "owner_agent_id": "char_wei",
      "writer_role": "character_agent",
      "delta_kind": "self_commitment",
      "content": "Wei must keep concealing the archive copy unless accusation becomes unavoidable."
    }
  ]
}
```

This handoff does **not** produce:

- a memory copy of Lin's suspicion for Wei
- a full packet copy for every other character
- automatic `received_report` deltas for uninvolved third parties

## Relationship to Adjacent Specs

This document should be read together with:

- `scene-packet-schema-v0.1.md`
- `memory-delta-format-v0.1.md`
- `event-publication-thresholds-v0.1.md`
- `agent-context-packet-and-field-visibility-v0.1.md`
- `resolution-state-delta-commit-pipeline-v0.1.md`

Next protocol priority after this document:

1. design adversarial trace fixtures for owner projection and candidate leakage
2. define memory retrieval policy for `CharacterContextPacket`
3. prototype a paper scene runner before autonomous execution
