# Canon Mutation Review Checklist v0.1

This document defines the first review checklist for canon mutations handled by `Canon Steward`.

Canon mutation review is the protocol step that decides whether a proposed canon addition, clarification, reveal, or structural exception may legally enter stable canon layers.

Its job is to stop scene convenience from quietly turning into hidden retcon.

## Purpose

This checklist exists to solve five protocol problems:

1. give `Canon Steward` a concrete review path instead of a vague gatekeeping role
2. distinguish real canon mutation from ordinary scene resolution or public event publication
3. prevent ad hoc patches introduced only to rescue a scene
4. preserve consistency across `Immutable Canon`, `latent_canon`, `public_canon`, and `Emergent Canon`
5. ensure any accepted canon change is traceable, classified, and propagated

Without a review checklist, `canon steward decides canon mutation` remains a slogan rather than a reliable governance layer.

## Design Constraints

Canon mutation review should satisfy these constraints:

1. every request must be classifiable as reveal, clarification, addition, exception, or rejection candidate
2. no mutation may bypass `Canon Steward`
3. immutable foundations must remain protected unless a separate override path exists
4. accepted mutations must specify which canon layer they affect
5. rejected or deferred requests must remain traceable rather than disappearing without explanation

## Placement in the Protocol

Recommended flow:

1. a role such as `World Agent` raises `CanonMutationRequest` when existing canon is insufficient
2. `Canon Steward` classifies the request
3. the review checklist is applied
4. `Canon Steward` returns `CanonDecision`
5. if approved, a `CanonDelta` is recorded against the correct canon layer and canon change log
6. only then may downstream `ScenePacket` or later scenes treat the change as legal canon material

Important rule:

- scene execution may continue while a request is pending
- but unresolved canon mutation must not be narrated as established fact

## What Triggers Review

Review is required when at least one of the following becomes true:

1. a proposed fact cannot be grounded in existing `public_canon` or `latent_canon`
2. a scene would otherwise need a new setting rule, institution, lineage, exception, or structural fact
3. a hidden canon fact needs to be formally revealed or promoted into `public_canon`
4. a previously unstated rule exception is being proposed
5. a proposed change would affect more than one future scene or more than one agent's reasoning base

Typical examples:

- introducing a newly named secret order
- declaring a previously unknown bloodline rule
- promoting a hidden truth from `latent_canon` into public reality
- adding a rule exception that changes what future scenes may legally do

## What Does Not Trigger Review

Review is usually not required for:

- ordinary `StateDelta` within existing world rules
- publication of an already-legal event into `public_event_ledger`
- POV-limited interior narration
- prose-only wording changes
- local suspicion or mistaken belief stored in `private_memory`

Important distinction:

- scene state change is not automatically canon mutation
- public knowledge change is not automatically canon mutation

## Required Review Inputs

Suggested review input fields:

| Field | Required | Meaning |
| --- | --- | --- |
| `request_id` | yes | stable identifier for the review request |
| `requester_role` | yes | who is asking for review |
| `mutation_kind` | yes | reveal, clarification, addition, exception, promotion, or other |
| `target_layer` | recommended | which canon layer may be affected |
| `proposal_summary` | yes | what canon change is being proposed |
| `motivation` | yes | why this change is needed |
| `supporting_basis` | recommended | which scene packet, world state, or prior canon references support it |
| `affected_refs` | recommended | which canon entries or packets would be affected |
| `reveal_scope` | optional | whether the change remains latent, becomes public, or stays restricted |
| `propagation_notes` | optional | what downstream docs, packets, or summaries need updating |

## Review Checklist

Each request should be checked against the following questions.

| Check | Question | Pass condition | If not satisfied |
| --- | --- | --- | --- |
| Classification | Is this actually a canon mutation rather than a scene-state issue? | request truly changes, clarifies, reveals, or promotes canon | redirect to world-state, event-publication, or memory workflow |
| Necessity | Is new canon really needed? | existing canon cannot already explain the case cleanly | reject or downgrade to clarification of existing material |
| Layer fit | Does the request target the correct canon layer? | request cleanly fits `public_canon`, `latent_canon`, or `Emergent Canon` | defer until layer is clarified |
| Non-contradiction | Does it avoid conflict with `Immutable Canon` and established canon? | no contradiction, or conflict is explicitly handled by a higher-order override path | reject |
| Causal continuity | Does prior scene logic remain coherent if this is accepted? | earlier packets, ledgers, and role behavior still make sense | defer or reject pending repair |
| Scope discipline | Is the mutation minimal rather than a convenience patch? | proposal solves the real need without over-expanding the world | request narrower rewrite |
| Reveal legality | If hidden truth is involved, is the reveal path legal? | no raw `latent_canon` leak; promotion or reveal is explicit | defer until reveal path is legalized |
| Authority hygiene | Is no role trying to bypass steward authority? | request comes through legal review rather than narrator or plot convenience | reject and quarantine if needed |
| Propagation readiness | Are downstream impacts identified? | affected canon refs, packets, or summaries are known | defer until propagation notes exist |
| Decision clarity | Can the outcome be recorded unambiguously? | approval, rejection, or deferment can be written with a clear reason and target layer | defer |

## Decision Outcomes

Suggested outcomes:

| Outcome | Meaning | Effect |
| --- | --- | --- |
| `approved_public` | accepted as public canon | update `public_canon` and canon change log |
| `approved_latent` | accepted but remains hidden | update `latent_canon` and canon change log |
| `approved_emergent` | accepted as new growth canon | update `Emergent Canon` and canon change log |
| `clarify_existing` | no new canon added; existing canon clarified | link to existing canon refs, no new canon layer entry required |
| `deferred` | request is plausible but under-specified | no canon change yet; return repair needs |
| `rejected` | request is invalid, contradictory, or abusive | no canon change; preserve decision record |

Important rule:

- every non-approval outcome should still produce a review record
- silence is not a valid canon decision

## Hard Boundaries

Canon review may approve:

- explicit promotion from hidden to public canon
- tightly scoped new canon additions
- clarifications that reduce ambiguity without rewriting history
- limited structural exceptions that do not violate immutable foundations

Canon review may not approve:

- retroactive rescue patches created only to save the current scene
- narrator-convenience leaks of hidden truth
- direct violation of `Immutable Canon` without an explicit higher-order override process
- vague "maybe this was always true" requests with no propagation plan

## Commit Semantics

A canon mutation should count as legally committed only when all of the following are true:

1. a `CanonMutationRequest` exists
2. `Canon Steward` has produced a `CanonDecision`
3. the outcome specifies its target canon layer or explicitly states that no new layer entry is needed
4. the change has been recorded in the canon change log
5. downstream narration and scene packets only reference the change according to that decision

Important consequence:

- a canon mutation may be pending while scene execution continues
- but pending mutation is not yet legal canon for narration, world adjudication broadening, or public explanation

## Example

Below is a compact example of a request and decision pair.

```json
{
  "request": {
    "request_id": "cmr_014",
    "requester_role": "world_agent",
    "mutation_kind": "promotion",
    "target_layer": "public_canon",
    "proposal_summary": "The sealed archive oath is now publicly revealed as binding all royal record-keepers",
    "motivation": "A courtroom scene has legally exposed the oath through accepted testimony and documentary proof",
    "supporting_basis": ["sp_021_03", "ev_611", "latent_canon:oath_royal_archive"],
    "affected_refs": ["latent_canon:oath_royal_archive", "public_canon:royal_archive_law"],
    "reveal_scope": "public",
    "propagation_notes": [
      "future archive scenes must treat the oath as public knowledge",
      "scene packet summaries after scene_021 may reference this as public canon"
    ]
  },
  "decision": {
    "decision_id": "cd_014",
    "outcome": "approved_public",
    "reason": "The reveal path is legal, evidence is committed, and no immutable canon is violated",
    "canon_delta_ref": "cdelta_014"
  }
}
```

## Relationship to Adjacent Specs

This document should be read together with:

- `communication-permission-matrix-v0.1.md`
- `state-and-knowledge-layers-v0.1.md`
- `scene-packet-schema-v0.1.md`

Next protocol priority after this document:

1. event publication thresholds for `public_event_ledger`
2. refine `ScenePacket` packet-to-memory handoff rules
3. dialogue evaluation metrics
