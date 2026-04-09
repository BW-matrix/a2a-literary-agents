# Terminology Index v0.1

This document is the first canonical vocabulary index for `a2a-literary-agents`.

Its purpose is to keep the project's term family stable as the protocol grows.

## Why This Exists

As the protocol expands, term drift becomes a real risk:

- one idea may collect multiple names
- the same word may be used at different abstraction levels
- an informal shortcut may start replacing a more precise term

This index exists to reduce that drift.

## Scope

This is not a full ontology yet.

It is:

- a canonical naming directory
- a quick-reference glossary
- a place to mark preferred terms and discouraged aliases

## Naming Principles

1. Prefer one canonical term per concept.
2. Keep protocol-layer terms stable once published.
3. Prefer precise storage-layer names over coarse narrative shorthand.
4. Mark ambiguous aliases as discouraged instead of silently letting them spread.
5. Let future schemas inherit vocabulary from this index.

## Term Families

- project identity
- agent roles
- message and packet types
- interaction and pacing units
- state and knowledge layers
- canon and authority layers
- visibility and routing terms

## Canonical Terms

| Term | Family | Meaning | Preferred usage | Discouraged alias or note | Primary source |
| --- | --- | --- | --- | --- | --- |
| `a2a-literary-agents` | project identity | repository and project name | use for repo, searchability, public reference | do not replace with the codename in formal references | `README.md` |
| `vibe-somnium / 织梦` | project identity | working title / codename | use as codename, internal identity, aesthetic label | not ideal as the main searchable repo name | `README.md` |
| `Character Agent` | agent role | owns will, motive, subjective choice | use for role authority and private cognition discussions | avoid shortening to just `character` when authority matters | `agent-constraint-matrix-v0.1.md` |
| `World Agent` | agent role | adjudicates consequence and committed world change | use for causality, resolution, and state transition | avoid treating it as an omniscient narrator | `communication-permission-matrix-v0.1.md` |
| `Plot Agent` | agent role | injects pressure and structural escalation | use for pressure, not fate completion | avoid implying direct control over characters | `communication-permission-matrix-v0.1.md` |
| `Narrator Agent` | agent role | renders committed material into prose | use for expression and voice layers | avoid giving it fact-writing authority | `communication-permission-matrix-v0.1.md` |
| `canon steward` | agent role | governs canon review and canon mutation approval | use for canon law and reveal governance | keep lowercase only when following existing document style | `communication-permission-matrix-v0.1.md` |
| `orchestrator` | agent role | routes, validates, schedules, and guards the protocol | use for coordination infrastructure | avoid turning it into a hidden author | `communication-permission-matrix-v0.1.md` |
| `Intent` | message type | a character's declared intention | use for character-side intention before consequence | avoid using it as a synonym for inner raw thought | `communication-permission-matrix-v0.1.md` |
| `ActionProposal` | message type | a proposed action submitted for resolution | use when a character attempts a concrete move | not a guarantee of outcome | `communication-permission-matrix-v0.1.md` |
| `Observation` | message type | what becomes perceptible to an agent or scene participant | use for delivered sensory or situational input | avoid using for inferred global truth | `communication-permission-matrix-v0.1.md` |
| `Resolution` | message type | a world-side adjudicated result | use for consequence and success/failure | should remain world-owned | `communication-permission-matrix-v0.1.md` |
| `StateDelta` | message type | the state change committed after resolution | use for changes to world or knowledge-bearing state | not the same as narration | `communication-permission-matrix-v0.1.md` |
| `Pressure` | message type | structural or dramatic pressure introduced by plot logic | use for pressure, deadlines, or tension sources | not a fact by itself | `communication-permission-matrix-v0.1.md` |
| `CanonMutationRequest` | message type | formal request for canon review | use when a proposed fact would alter, reveal, or extend canon | not the same as ordinary scene resolution | `canon-mutation-review-checklist-v0.1.md` |
| `CanonDecision` | message type | steward-issued review outcome on a canon request | use for approval, rejection, or deferment of canon mutation | should always leave a traceable decision record | `canon-mutation-review-checklist-v0.1.md` |
| `CanonDelta` | canon record | the recorded change produced by an approved canon decision | use for change-log entries that update canon layers | not a scene-state delta | `canon-mutation-review-checklist-v0.1.md` |
| `DialogueWindow` | interaction unit | the default bounded unit for spoken interaction | use as the standard dialogue coordination unit | prefer this over single-line turn language | `dialogue-window-schema-v0.1.md` |
| `ScenePacket` | packet type | committed scene-level packet for downstream rendering and memory | use for committed scene material and legal narrator input | primary schema now lives in `scene-packet-schema-v0.1.md` | `scene-packet-schema-v0.1.md` |
| `ScenePressurePacket` | packet type | scene-level pressure bundle from plot logic | use for scene or beat pressure inputs | keep distinct from committed events | `communication-permission-matrix-v0.1.md` |
| `SceneDraft` | output type | narrator-side scene draft material | use for prose drafts, not canon facts | should remain downstream of committed packets | `agent-constraint-matrix-v0.1.md` |
| `pov_contract` | packet field | packet-level authority boundary for viewpoint and interiority | use to define what narration may know or claim | do not treat it as a mere style hint | `scene-packet-schema-v0.1.md` |
| `authorized_interiority` | packet field | explicitly permitted inner material included in a `ScenePacket` | use as the legal route for packet-level inner access | absence should be treated as absence of permission | `scene-packet-schema-v0.1.md` |
| `visibility_deltas` | packet field | newly visible or inferable consequences carried by a packet | use to separate event truth from distributed knowledge | keep distinct from `state_deltas` | `scene-packet-schema-v0.1.md` |
| `narration_bounds` | packet field | packet-level limits on compression and factual claims | use to constrain downstream prose rendering | do not let narrator exceed these bounds | `scene-packet-schema-v0.1.md` |
| `MemoryDelta` | memory unit | owner-scoped update unit for `private_memory` | use for owner-specific memory entries derived from committed scenes or legal recollection paths | not objective world truth | `memory-delta-format-v0.1.md` |
| `delta_kind` | memory field | distinguishes what kind of memory update a delta carries | use to separate observation, suspicion, recollection, and revision | do not collapse all memory into generic content text | `memory-delta-format-v0.1.md` |
| `acquisition_mode` | memory field | records how the owner came to hold a memory | use for sensory, reported, inferred, or self-acted acquisition paths | keep distinct from certainty | `memory-delta-format-v0.1.md` |
| `memory_status` | memory field | records the current standing of a memory entry | use for active, superseded, withdrawn, or contested states | preserve revision lineage instead of silently deleting history | `memory-delta-format-v0.1.md` |
| `supersedes` | memory field | points to earlier deltas revised by a later delta | use to trace memory revision lineage | not a delete operation | `memory-delta-format-v0.1.md` |
| `dramatic window` | pacing unit | bounded dramatic move larger than one utterance and smaller than a whole scene | use as the default interaction cadence | avoid defaulting to line-by-line turn simulation | `communication-permission-matrix-v0.1.md` |
| `world_state_ledger` | state layer | objective committed reality log | use for what is true in the world regardless of who knows it | do not flatten into public knowledge | `state-and-knowledge-layers-v0.1.md` |
| `public_event_ledger` | knowledge layer | events that have become publicly knowable | use for shared event history | prefer this over the coarse phrase `public ledger` | `state-and-knowledge-layers-v0.1.md` |
| `private_memory` | knowledge layer | agent-specific memory, belief, and recollection | use for local knowledge and misinterpretation | not always reliable and not equal to world truth | `state-and-knowledge-layers-v0.1.md` |
| `public_canon` | canon layer | stable public setting facts and openly established world rules | use for shared setting reference | keep distinct from scene events | `state-and-knowledge-layers-v0.1.md` |
| `latent_canon` | canon layer | already true canon that is not yet public | use for hidden truths and future reveals | do not leak through narrator convenience | `state-and-knowledge-layers-v0.1.md` |
| `Emergent Canon` | canon layer | newly accepted canon introduced during creation | use for explicit canon growth after review | never treat as ad hoc patching | `communication-permission-matrix-v0.1.md` |
| `Immutable Canon` | canon layer | non-routine foundational rules and anchors | use for hard-setting constraints | avoid casual mutation | `communication-permission-matrix-v0.1.md` |
| `private_self` | visibility layer | sender-only raw cognition scope | use for hidden motive and raw inner state | never expose by default | `communication-permission-matrix-v0.1.md` |
| `private_target` | visibility layer | sender-and-target-only message scope | use for directed but non-public communication | keep distinct from self-only cognition | `communication-permission-matrix-v0.1.md` |
| `scene_public` | visibility layer | visible to legitimate scene participants | use for shared scene-level visibility | not equivalent to global public knowledge | `communication-permission-matrix-v0.1.md` |
| `system_restricted` | visibility layer | reserved for routing, validation, or canon review layers | use for infrastructure-only visibility | do not narrativize it | `communication-permission-matrix-v0.1.md` |
| `event bus` | routing layer | the validation and message-routing path | use for soft schema validation discussions | not an agent in the story world | `communication-permission-matrix-v0.1.md` |
| `soft validation, hard permission` | design principle | recover from malformed communication but block authority leakage | use as a global protocol slogan | one of the project's canonical design principles | `README.md` |

## Discouraged or Ambiguous Terms

| Term | Status | Use instead | Reason |
| --- | --- | --- | --- |
| `public ledger` | discouraged | `public_event_ledger` or `world_state_ledger` | too coarse and collapses truth with publicity |
| `world` | context-dependent | `World Agent` when referring to the agent role | too ambiguous in protocol discussions |
| `character` | context-dependent | `Character Agent` when authority matters | can refer either to the fictional person or the system role |

## How To Extend This Index

Add a term when at least one of these becomes true:

- the term appears in more than one protocol file
- the term carries authority or storage semantics
- the term will likely be inherited by future schemas
- the term can be confused with a nearby concept

When adding a term:

1. choose one canonical spelling
2. assign it to a term family
3. define its meaning in one sentence
4. note any discouraged aliases
5. point to the source file where it is first or best defined

## Near-Term Follow-Ups

1. add a term status field such as `draft`, `stable`, `discouraged`
2. split the index into subfiles if the vocabulary family grows large
3. align future `ScenePacket` and memory delta specs to this index first
