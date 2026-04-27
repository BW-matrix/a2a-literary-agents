# Resolution, StateDelta, and ScenePacket Commit Pipeline v0.1

This document defines the first auditable pipeline from character proposal to committed scene packet.

The goal is to prevent `World Agent` from becoming a hidden author. The world may decide consequence, but consequence must be traceable to submitted intent, current state, canon, constraints, uncertainty policy, and visible effects.

## Purpose

The commit pipeline exists to solve five protocol problems:

1. define how `World Agent` adjudicates `Intent`, `ActionProposal`, and `DialogueWindow`
2. make `Resolution` and `StateDelta` concrete enough to audit
3. distinguish committed consequence from publication candidates and canon reveal candidates
4. constrain `Orchestrator` assembly so packet sealing does not become editorial power
5. give `Narrator Agent` and memory handoff a stable committed source

Without this pipeline, the system may stop narrator-level invention while still allowing world-level consequence invention.

## Design Constraints

The pipeline should satisfy these constraints:

1. every outcome must cite input refs and applicable rules
2. every state change must be represented as a `StateDelta`
3. every visibility result must distinguish "happened" from "known"
4. publication and canon reveal are two-phase operations
5. packet assembly must be mechanical, source-backed, and sealed

## Pipeline Overview

Recommended flow:

1. `Character Agent` submits `Intent`, `ActionProposal`, or `DialogueWindow`
2. `World Agent` gathers legal world, canon, pressure, and proposal context
3. `World Agent` emits one or more `Resolution` records
4. accepted results produce `StateDelta` and `VisibilityResult` records
5. optional `PublicationCandidate` and `CanonRevealCandidate` records are marked but not yet promoted
6. `Orchestrator` assembles a `ResolvedScenePacket` from committed world outputs
7. publication thresholds and canon governance run as separate follow-up decisions
8. `NarratorInputPacket` is projected only after packet sealing and candidate filtering

Important rule:

- consequence commits before narration
- publication and canon promotion require explicit gates after consequence

## Resolution Shape

Suggested `Resolution` fields:

| Field | Required | Type | Meaning |
| --- | --- | --- | --- |
| `resolution_id` | yes | string | stable id for the adjudication |
| `scene_id` | yes | string | parent scene |
| `window_id` | recommended | string | dramatic window being resolved |
| `input_refs` | yes | array | proposals, pressure packets, observations, or prior state refs being adjudicated |
| `actor_refs` | yes | array | acting characters or entities |
| `applicable_rules` | yes | array | canon, world rules, social rules, physical constraints, or scene constraints |
| `constraint_basis` | yes | array | facts or limits that materially shaped the outcome |
| `uncertainty_model` | recommended | object | deterministic, probabilistic, hybrid, or author-defined adjudication mode |
| `outcome_type` | yes | string | `success`, `failure`, `partial_success`, `misfire`, `blocked`, `delayed`, or `contested` |
| `outcome_summary` | yes | string | concise factual consequence |
| `failed_alternatives` | optional | array | attempted branches that did not become true |
| `visibility_result_refs` | recommended | array | visibility records produced by this resolution |
| `state_delta_refs` | recommended | array | committed state deltas produced by this resolution |
| `publication_candidate_refs` | optional | array | possible public event candidates |
| `canon_reveal_candidate_refs` | optional | array | possible reveal candidates |
| `adjudication_basis` | yes | string | audit summary without chain-of-thought |
| `based_on` | recommended | array | policy, matrix, packet, canon, and ledger refs |

Important rule:

- `adjudication_basis` should explain the basis of the decision
- it should not expose chain-of-thought or hidden authorial reasoning

## Outcome Types

| Outcome type | Meaning | Commit behavior |
| --- | --- | --- |
| `success` | attempted action achieves its intended direct effect | may produce direct state deltas |
| `failure` | attempted action does not achieve the intended effect | may still produce side-effect deltas |
| `partial_success` | some effect occurs, but not the full intended effect | commit only the achieved portion |
| `misfire` | attempt produces an unintended consequence | commit the unintended consequence if rule-backed |
| `blocked` | attempt is prevented before meaningful effect | may commit visibility or pressure effects only |
| `delayed` | consequence is scheduled but not complete yet | create pending or future-triggered state refs |
| `contested` | outcome is socially or perceptually disputed | commit objective state separately from public interpretation |

## StateDelta Shape

Suggested `StateDelta` fields:

| Field | Required | Type | Meaning |
| --- | --- | --- | --- |
| `delta_id` | yes | string | stable id for this state change |
| `source_resolution_id` | yes | string | resolution that produced it |
| `target_layer` | yes | string | usually `world_state_ledger`; sometimes route metadata or public/canon candidate refs |
| `target_kind` | yes | string | character, object, location, relation, resource, institution, schedule, or condition |
| `target_id` | yes | string | entity being changed |
| `change_kind` | yes | string | create, update, move, remove, reveal_marker, schedule, damage, transfer, relation_shift |
| `before_ref` | optional | string | previous state ref when available |
| `after_summary` | yes | string | committed state after the change |
| `persistence` | recommended | string | momentary, scene, chapter, persistent, scheduled |
| `visibility_basis` | recommended | array | who could perceive or infer this change |
| `based_on` | recommended | array | input, rule, and resolution refs |

Important rule:

- `StateDelta` records objective change
- it does not decide who knows the change unless paired with visibility records

## VisibilityResult Shape

Suggested `VisibilityResult` fields:

| Field | Required | Meaning |
| --- | --- | --- |
| `visibility_result_id` | yes | stable id |
| `source_resolution_id` | yes | resolution source |
| `observer_scope` | yes | self, pair, scene group, local public, institution public, or restricted subset |
| `observer_refs` | recommended | specific agents or groups if known |
| `visible_content` | yes | what became visible, reportable, or inferable |
| `certainty` | recommended | low, medium, high |
| `exposure_mode` | recommended | saw, heard, was_told, inferred, discovered, declared |
| `limits` | recommended | what this visibility result does not prove |

Important rule:

- visibility may produce memory eligibility
- it does not automatically produce public event publication

## Two-Phase Publication and Reveal Semantics

`ResolvedScenePacket` may carry candidates, not final promotions.

| Candidate type | Meaning | Finalizing authority |
| --- | --- | --- |
| `PublicationCandidate` | committed scene material may qualify for `public_event_ledger` | publication threshold policy and `World Agent` |
| `CanonRevealCandidate` | committed scene material may expose `latent_canon` | `Canon Steward` |
| `CanonMutationRequest` | current scene may require new or clarified canon | `Canon Steward` |

Field naming rule:

- use `publication_candidates` before threshold approval
- use `public_event_deltas` only after publication is approved
- use `canon_reveal_candidates` before canon review
- use `canon_effects_committed` or `CanonDelta` only after steward decision

## ScenePacket Assembly and Sealing

`Orchestrator` may assemble and seal packets. It may not author content.

| Packet field | Allowed writer/source | Assembly rule |
| --- | --- | --- |
| `resolved_events` | `Resolution` records from `World Agent` | copy or mechanically summarize with source refs |
| `state_deltas` | committed `StateDelta` refs | include refs and summaries, not hidden unfiltered ledger dumps |
| `visibility_deltas` | `VisibilityResult` records | include scope and limits |
| `publication_candidates` | resolution-backed candidate records | mark as candidates until threshold approval |
| `public_event_deltas` | approved publication records only | include only after publication decision |
| `authorized_interiority` | POV contract or character-authorized material | include only with explicit authority basis |
| `canon_reveal_candidates` | resolution-backed reveal markers | mark as candidates until steward approval |
| `canon_effects_committed` | `CanonDecision` or `CanonDelta` | include only after steward decision |
| `narration_bounds` | policy plus resolution constraints | assemble from hard limits and POV contract |
| `based_on` | all source refs | mandatory for sealing |

Seal conditions:

1. all included events have `Resolution` refs
2. all state changes have accepted `StateDelta` refs
3. all visibility claims cite `VisibilityResult` refs
4. all publication and reveal material is clearly marked as candidate or approved
5. no unresolved proposal is represented as fact
6. no summary lacks source refs

## Narrator Input Projection

After sealing, `Narrator Agent` receives a `NarratorInputPacket`, not the full system packet.

It may include:

- committed resolved events
- committed state deltas that are legal to render
- approved or legally bounded visibility changes
- authorized interiority
- narration bounds
- approved public or canon material

It must exclude:

- raw `world_state_ledger`
- rejected alternatives
- unresolved candidate lines
- pending `PublicationCandidate`
- pending `CanonRevealCandidate`
- raw latent canon

## Hard Boundaries

`World Agent` may:

- adjudicate consequence
- commit state deltas under current rules
- mark visibility results
- generate candidates for publication or reveal

`World Agent` may not:

- choose outcomes purely for drama
- write character inner truth
- promote canon without steward review
- treat plot pressure as destiny
- publish hidden facts without threshold support

`Orchestrator` may:

- package refs
- validate commit readiness
- seal packets
- project legal views

`Orchestrator` may not:

- omit source-backed material for literary preference
- add prose emphasis as fact
- upgrade candidates into approved deltas
- rewrite resolutions

## Example

```json
{
  "resolution": {
    "resolution_id": "res_411",
    "scene_id": "scene_018",
    "window_id": "win_018_05",
    "input_refs": ["dw_018_05", "spp_018_01", "wsl_archive_state_07"],
    "actor_refs": ["char_wei", "char_lin"],
    "applicable_rules": ["public_canon:archive_access_rule", "pressure_budget:inspection_deadline"],
    "constraint_basis": [
      "Wei knows the ledger is missing but does not confess.",
      "Lin has prior suspicion but no proof."
    ],
    "uncertainty_model": {
      "mode": "hybrid",
      "notes": "social read resolved by prior memory and visible dialogue pressure"
    },
    "outcome_type": "partial_success",
    "outcome_summary": "Wei's probe makes Lin more suspicious, but Lin does not obtain proof.",
    "failed_alternatives": [
      "Lin does not extract a confession.",
      "Wei does not fully hide his unusual concern."
    ],
    "visibility_result_refs": ["vr_411"],
    "state_delta_refs": ["sd_118"],
    "publication_candidate_refs": [],
    "canon_reveal_candidate_refs": [],
    "adjudication_basis": "The result follows from Wei's cautious probing, Lin's existing suspicion, and the absence of public evidence.",
    "based_on": ["dialogue-window-schema-v0.1", "state-and-knowledge-layers-v0.1"]
  }
}
```

## Relationship to Adjacent Specs

This document should be read together with:

- `scene-packet-schema-v0.1.md`
- `event-publication-thresholds-v0.1.md`
- `latent-to-public-canon-reveal-rules-v0.1.md`
- `canon-mutation-review-checklist-v0.1.md`
- `agent-context-packet-and-field-visibility-v0.1.md`

Next protocol priority after this document:

1. design adversarial trace fixtures for hidden theft, false report, and partial reveal
2. define narration grounding validation against `NarratorInputPacket`
3. prototype a paper runner before an autonomous runner
