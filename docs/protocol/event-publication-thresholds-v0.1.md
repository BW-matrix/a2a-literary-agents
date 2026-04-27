# Event Publication Thresholds v0.1

This document defines the first threshold policy for promoting committed scene reality into `public_event_ledger`.

Event publication is the protocol step that decides when something stops being merely true in the world and becomes socially shareable event knowledge.

Its job is to prevent a collapse between "it happened" and "everyone may now reason from it."

## Purpose

This document exists to solve five protocol problems:

1. give `public_event_ledger` a concrete promotion threshold instead of a vague intuition
2. separate objective world truth from socially shared knowability
3. allow publication at explicit scope without forcing global omniscience
4. preserve contested public knowledge without pretending public means universally believed
5. ensure published events are traceable back to committed scene material

Without publication thresholds, `public_event_ledger` risks becoming either too empty to matter or too broad to preserve local knowledge.

## Design Constraints

Event publication should satisfy these constraints:

1. nothing may enter `public_event_ledger` without committed source material
2. publication scope must be explicit rather than implied as universal
3. contested public knowledge must remain representable
4. publication summaries must not overclaim beyond what the public scope can legitimately know
5. publication should remain cheaper than canon review, but stricter than private-memory storage

## Placement in the Protocol

Recommended flow:

1. `World Agent` resolves scene outcomes into committed state
2. `ScenePacket` carries `resolved_events`, `visibility_deltas`, and optional `publication_candidates`
3. publication thresholds are checked against committed material
4. qualifying items are written into `public_event_ledger` as approved `public_event_deltas`
5. downstream agents may reason from published summaries according to the recorded scope

Important rule:

- publication happens after committed consequence
- publication does not itself create world truth; it only upgrades who may treat the event as shared knowledge
- `publication_candidates` are not public event entries until this threshold policy approves them

## Core Distinction

The protocol must separate three different states:

1. objectively true in `world_state_ledger`
2. privately known through `private_memory`
3. publicly knowable through `public_event_ledger`

Important consequence:

- an event may be true without being public
- an event may be public without being universally interpreted the same way

## What Counts as Publication

Publication should be triggered only when an event exits purely local knowledge and becomes socially shareable at an explicit scope.

Typical publication modes include:

- direct public witness
- official declaration
- discovered evidence
- verified report release
- consequence too large to remain hidden
- formal broadcast or institutional circulation

## What Does Not Count as Publication

The following do not by themselves justify publication:

- hidden action that only succeeded in `world_state_ledger`
- one character's suspicion
- one character's inference about another
- narrator-side awareness
- raw `latent_canon`
- scene-private dialogue without a legal public leak path

Important rule:

- publicity is a social-access condition, not a prose convenience condition

## Threshold Classes

Suggested publication classes:

| Threshold class | Trigger | Minimum support | Recommended scope | Notes |
| --- | --- | --- | --- | --- |
| `direct_public_witness` | openly visible act or confrontation | committed event + public or crowd visibility | scene_public, local_public | strongest default publication path |
| `official_declaration` | recognized institution or authority makes a public statement | committed declaration event | local_public, city_public, realm_public | statement may still be false or contested, but it becomes public as a report |
| `discovered_evidence` | hidden consequence is found and verified enough to circulate | committed evidence-discovery event | local_public or wider depending on channel | publication is about discovery, not necessarily culprit certainty |
| `verified_report_release` | credible report is released through a legitimate channel | committed report-release event + source trace | local_public, city_public, realm_public | keep source trace explicit |
| `uncontainable_consequence` | outcome is too large to remain hidden | committed large-scale consequence | local_public or wider | example: fire, collapse, mass disappearance |
| `institutional_circulation` | a bounded institution now shares the event internally as common knowledge | committed circulation act | institution_public | not globally public, but no longer private to one owner |

## Suggested Publication Record

Suggested fields for a published event entry:

| Field | Required | Meaning |
| --- | --- | --- |
| `publication_id` | yes | stable id for this publication entry |
| `source_packet_id` | recommended | which committed `ScenePacket` supported publication |
| `source_event_ids` | yes | which committed events back this publication |
| `publication_mode` | yes | which threshold class produced publication |
| `effective_scope` | yes | who may now treat this as shared event knowledge |
| `public_summary` | yes | what can be said publicly without overclaiming |
| `certainty` | recommended | low, medium, high |
| `contestability` | optional | uncontested, disputed, or unclear |
| `based_on` | recommended | supporting refs such as visibility or report evidence |

## Candidate vs Approved Delta

Two-phase naming should remain explicit:

| Stage | Field | Meaning |
| --- | --- | --- |
| candidate | `publication_candidates` | committed scene material may qualify for publication |
| approved | `public_event_deltas` | publication threshold passed and `public_event_ledger` may be updated |

Important rule:

- `Narrator Agent` and `Character Agent` should not treat a publication candidate as socially shared knowledge
- approved publication still requires scope-aware query rules before entering a specific character's `private_memory`

## Scope Rules

`public_event_ledger` should not imply one undifferentiated global public.

Suggested scope values include:

- `scene_public`
- `local_public`
- `institution_public`
- `city_public`
- `realm_public`

Important rule:

- scope should be as small as the evidence justifies
- do not publish as realm-wide knowledge what is only known inside one courtyard or one office

## Contestability

A public event may be socially known while still disputed.

Examples:

- everyone knows an arrest happened, but not whether it was justified
- a proclamation is public, even if many doubt it
- a body is discovered, even if the cause of death is unknown

Therefore:

- `public_event_ledger` stores public knowability, not unanimous interpretation
- contestability should be recorded when relevant

## Hard Boundaries

Publication may include:

- publicly witnessed actions
- discovered consequences
- declared positions and announcements
- institutionally shared event summaries

Publication may not include:

- hidden motives as public fact
- raw private inference presented as social knowledge
- unrevealed `latent_canon`
- culprit certainty that exceeds the evidence actually publicized

## Commit Semantics

An event should count as published into `public_event_ledger` only when all of the following are true:

1. the source event is already committed
2. at least one publication threshold class is satisfied
3. `effective_scope` is explicit
4. the public summary does not exceed what that scope can legitimately know
5. publication is written by `World Agent` or emitted by `Orchestrator` from a committed packet

Important consequence:

- publication is weaker than canon mutation
- publication is stronger than private memory
- publication does not erase the difference between truth, rumor, and interpretation

## Example

Below, a hidden theft becomes public only after discovery.

```json
{
  "publication_id": "pub_018_01",
  "source_packet_id": "sp_019_02",
  "source_event_ids": ["ev_509"],
  "publication_mode": "discovered_evidence",
  "effective_scope": "local_public",
  "public_summary": "The archive break-in has been discovered and the royal ledger is officially missing.",
  "certainty": "high",
  "contestability": "uncontested",
  "based_on": ["sp_019_02", "ev_509", "vd_031"]
}
```

This does **not** publish:

- who stole the ledger
- why it was stolen
- whether Wei is guilty

It only publishes what has actually crossed the threshold into public knowledge.

## Relationship to Adjacent Specs

This document should be read together with:

- `state-and-knowledge-layers-v0.1.md`
- `scene-packet-schema-v0.1.md`
- `memory-delta-format-v0.1.md`
- `resolution-state-delta-commit-pipeline-v0.1.md`

Next protocol priority after this document:

1. public scope registry and audience membership model
2. adversarial trace fixtures for false public reports and over-broad publication
3. memory retrieval and encounter policy for published events
