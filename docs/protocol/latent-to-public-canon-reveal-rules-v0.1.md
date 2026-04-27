# Latent-to-Public Canon Reveal Rules v0.1

This document defines the first rule set for promoting `latent_canon` into `public_canon`.

Reveal is the protocol step that turns already-true but hidden canon into openly established setting knowledge.

Its job is to ensure that hidden canon becomes public only through legal exposure, not through narrator convenience, scene pressure, or accidental implication.

## Purpose

This document exists to solve five protocol problems:

1. define when `latent_canon` may legally become `public_canon`
2. distinguish canon reveal from ordinary public event publication
3. prevent hidden truth from leaking into prose before it is structurally legalized
4. require explicit promotion rather than treating exposure and canon update as automatic
5. preserve continuity between canon review, scene packets, and storage layers

Without reveal rules, the protocol can name `latent_canon` and `public_canon` but cannot reliably govern the transition between them.

## Design Constraints

Reveal governance should satisfy these constraints:

1. hidden canon must already exist before it can be revealed
2. exposure and promotion must be related but not identical steps
3. narrator may not promote canon by implication alone
4. the public scope of a reveal must be explicit
5. promotion must remain traceable in the canon change log

## Placement in the Protocol

Recommended flow:

1. a hidden canon fact already exists in `latent_canon`
2. a committed scene or institutional act creates a possible reveal path
3. packet-level `canon_reveal_candidates` record the reveal candidate
4. `Canon Steward` evaluates whether the reveal path is legal and sufficiently stabilizing
5. if approved, the fact is promoted from `latent_canon` to `public_canon`
6. downstream scenes may now treat the revealed fact as open setting knowledge within the approved scope

Important rule:

- exposure may happen inside a scene
- promotion to `public_canon` happens only after explicit governance
- `canon_reveal_candidates` are not the same as approved `CanonDelta` or committed canon effects

## Core Distinction

The protocol must distinguish three different states:

1. hidden canon exists in `latent_canon`
2. a reveal event exposes that canon to some public or institutional scope
3. the revealed fact is stable enough to be promoted into `public_canon`

Important consequence:

- not every reveal candidate should immediately become public canon
- a leaked hint or partial discovery may expose a fact without yet stabilizing it as public setting knowledge

## What Counts as a Legitimate Reveal Path

A reveal path is usually legitimate when at least one of the following becomes true:

1. a committed scene contains explicit confession, testimony, inscription, or evidence tied to the latent canon fact
2. an institutional declaration or archive release exposes the hidden fact through a recognized channel
3. a public or institution-level discovery makes the hidden fact socially shareable and hard to retract
4. a canon-reviewed packet explicitly marks the hidden fact as legally exposed

Typical examples:

- a sealed lineage record is opened in court
- a hidden oath is publicly read from an authenticated archive
- a secret organization is uncovered through committed documentary proof

## What Does Not Count as a Legitimate Reveal Path

The following do not by themselves justify promotion to `public_canon`:

- narrator implication or stylistic overreach
- one character privately learning a hidden truth
- rumor without committed grounding
- mere reader inference
- plot pressure that assumes the hidden truth for convenience
- packet material marked pending but not approved

Important rule:

- private discovery may update memory or scene tension without promoting canon

## Required Reveal Inputs

Suggested reveal input fields:

| Field | Required | Meaning |
| --- | --- | --- |
| `latent_ref` | yes | which `latent_canon` fact is under consideration |
| `reveal_source_packet_id` | recommended | which committed packet carried the reveal candidate |
| `reveal_basis` | yes | what committed event, evidence, declaration, or packet element exposed it |
| `exposure_scope` | yes | who now has legal access to this reveal |
| `stability_claim` | recommended | why this reveal is durable enough to affect setting knowledge |
| `promotion_request` | yes | whether public promotion is actually being requested |
| `affected_public_refs` | optional | which public canon entries need update or creation |
| `propagation_notes` | optional | which downstream layers or docs need synchronization |

## Candidate vs Approved Canon Effect

Two-phase naming should remain explicit:

| Stage | Field or record | Meaning |
| --- | --- | --- |
| candidate | `canon_reveal_candidates` | committed material may legally expose hidden canon |
| decision | `CanonDecision` | `Canon Steward` approves, rejects, or defers the reveal |
| committed effect | `CanonDelta` or `canon_effects_committed` | approved canon update or approved reveal effect |

Important rule:

- a candidate may affect review workflow
- it must not be treated as public canon, narrator fact, or character knowledge unless exposure scope separately permits it

## Reveal Gate Checklist

Each promotion candidate should be checked against the following questions.

| Check | Question | Pass condition | If not satisfied |
| --- | --- | --- | --- |
| Latent existence | Does the fact already exist in `latent_canon`? | hidden canon entry already exists and is identified | reject as invention or reroute to canon mutation review |
| Committed basis | Is the reveal grounded in committed scene or institutional material? | reveal basis is traceable to committed packet or approved record | defer or reject |
| Scope clarity | Is the exposure scope explicit? | scope such as institutional, local public, or wider is clear | defer |
| Legality | Is the exposure path legitimate under current rules? | no narrator leak, no illegal bypass, no unsupported shortcut | reject |
| Sufficiency | Is the reveal strong enough to support public setting knowledge? | exposure is more than private rumor or isolated suspicion | keep latent or defer |
| Stability | Will future scenes be more coherent if this becomes public canon? | promotion stabilizes open-world reasoning rather than creating confusion | defer or reject pending repair |
| Non-contradiction | Does promotion avoid conflict with established `public_canon` and `Immutable Canon`? | no contradiction or conflict is already resolved | reject |
| Propagation readiness | Are downstream updates identified? | affected public refs and packets are known | defer |

## Exposure Scope vs Public Canon

Exposure scope and canon layer promotion are related but distinct.

Suggested scope examples:

- `institution_public`
- `local_public`
- `city_public`
- `realm_public`

Important rule:

- a reveal may first become institutionally public without immediately becoming universal public canon
- `public_canon` should record what is openly established for relevant shared-world reasoning, not every raw rumor or unstable leak

## Promotion Outcomes

Suggested outcomes:

| Outcome | Meaning | Effect |
| --- | --- | --- |
| `promote_public` | reveal is legal and stable enough for `public_canon` | move or mirror the fact into `public_canon` and log the promotion |
| `remain_latent` | hidden fact stays in `latent_canon` | no public promotion yet |
| `exposed_but_unstable` | exposure happened, but not enough for stable public canon | keep latent, optionally track exposure via packet or event layers |
| `deferred` | reveal case is plausible but underspecified | no promotion yet; request repair |
| `rejected` | reveal path is invalid or contradictory | no promotion; preserve decision record |

## Relationship to `public_event_ledger`

Public event publication and canon reveal are not the same thing.

Example:

- `public_event_ledger` may record that "an archive oath was publicly read"
- `public_canon` should only change if the oath's revealed content is approved as stable public setting knowledge

Important consequence:

- event publication can precede canon promotion
- canon promotion should not be inferred automatically from public-event existence alone

## Hard Boundaries

Reveal governance may approve:

- explicit promotion of an already-existing hidden canon fact
- stable exposure through committed evidence or recognized declaration
- scoped public establishment that improves future world reasoning

Reveal governance may not approve:

- narrator-led leakage
- reader-only implication
- retroactive invention disguised as reveal
- private discovery treated as open canon without public path
- promotion that outruns the actual exposure scope

## Commit Semantics

A latent-to-public promotion should count as committed only when all of the following are true:

1. the hidden fact exists in `latent_canon`
2. a committed reveal basis exists
3. `Canon Steward` has approved the promotion
4. the target public scope and affected public refs are recorded
5. the canon change log records the promotion

Important consequence:

- until these conditions are satisfied, the fact remains hidden canon even if some scene has started exposing it

## Example

Below is a compact example of a legal promotion.

```json
{
  "latent_ref": "latent_canon:oath_royal_archive",
  "reveal_source_packet_id": "sp_021_03",
  "reveal_basis": ["ev_611", "canon_effect:archive_oath_read_in_court"],
  "exposure_scope": "institution_public",
  "stability_claim": "The oath has been authenticated in court and entered the royal record.",
  "promotion_request": true,
  "affected_public_refs": ["public_canon:royal_archive_law"],
  "decision": {
    "outcome": "promote_public",
    "reason": "The hidden canon fact already existed, the reveal path is legal, and downstream archive scenes now require open access to this rule."
  }
}
```

## Relationship to Adjacent Specs

This document should be read together with:

- `state-and-knowledge-layers-v0.1.md`
- `canon-mutation-review-checklist-v0.1.md`
- `scene-packet-schema-v0.1.md`
- `resolution-state-delta-commit-pipeline-v0.1.md`

Next protocol priority after this document:

1. canon-vs-state classification checklist
2. public scope registry and audience membership model
3. adversarial trace fixtures for partial reveal and narrator leakage
