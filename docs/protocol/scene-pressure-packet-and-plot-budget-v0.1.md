# ScenePressurePacket and Plot Pressure Budget v0.1

This document defines the first concrete payload and budget policy for `ScenePressurePacket`.

The goal is to let `Plot Agent` create tension without becoming a hidden god-author.

`Plot Agent` may introduce pressure. It may not choose character actions, declare world facts, or guarantee outcomes.

## Purpose

`ScenePressurePacket` exists to solve five protocol problems:

1. make plot pressure inspectable instead of vague authorial force
2. distinguish pressure from committed fact
3. prevent pressure from secretly determining character choices
4. require pressure to declare scope, duration, dependencies, and forbidden outcomes
5. give `World Agent` a clear boundary for translating pressure into actual scene conditions

Without this schema, `plot provides pressure, not destiny` remains correct as a slogan but weak as a runtime constraint.

## Design Constraints

Plot pressure should satisfy these constraints:

1. it must be bounded by scope and duration
2. it must preserve at least one meaningful non-forced option
3. it must cite its structural basis
4. it must not create world facts directly
5. it must not smuggle latent canon or hidden truth into agent context

## ScenePressurePacket Shape

Suggested payload fields:

| Field | Required | Type | Meaning |
| --- | --- | --- | --- |
| `pressure_id` | yes | string | stable id for this pressure packet |
| `scene_id` | yes | string | parent scene |
| `beat_id` | recommended | string | structural beat if applicable |
| `pressure_kind` | yes | string | category of pressure |
| `scope` | yes | string | scene, subscene, location, relationship, institution, or timeline scope |
| `duration` | yes | string | one_window, scene, chapter, scheduled, or until_condition |
| `affected_options` | yes | array | options made harder, costlier, more urgent, or more visible |
| `non_forcing_clause` | yes | string | how character agency remains open |
| `world_fact_dependency` | recommended | array | existing facts or public/canon refs this pressure depends on |
| `world_translation_request` | optional | object | request for `World Agent` to decide whether pressure can become a condition |
| `forbidden_outcomes` | yes | array | outcomes the pressure packet is not allowed to require |
| `visibility` | yes | string | who may know this pressure exists |
| `budget_cost` | recommended | object | how much structural force this pressure spends |
| `based_on` | yes | array | structure, event, canon, or prior packet refs |

Important rule:

- `ScenePressurePacket` is input pressure
- it is not a committed scene event

## Allowed Pressure Kinds

| Pressure kind | Meaning | Example |
| --- | --- | --- |
| `deadline` | time limit or approaching decision point | inspection begins at dawn |
| `resource_scarcity` | limited tool, time, trust, money, access, safety | only one archive key remains available |
| `social_exposure` | risk of being observed, challenged, or judged | servants are gathering near the corridor |
| `institutional_constraint` | legal, bureaucratic, ritual, or command pressure | the court requires a signed record by sunset |
| `relationship_strain` | tension inside an established relationship | Lin has less patience for Wei's evasions |
| `moral_dilemma` | values conflict without forced answer | protecting one person may endanger another |
| `environmental_pressure` | weather, darkness, noise, terrain, crowding | the storm makes quiet travel difficult |
| `information_asymmetry` | uneven access to public or private fragments | Lin knows one clue Wei does not know Lin heard |
| `escalation_signal` | signal that stakes are rising without choosing result | guards have begun asking procedural questions |

## Forbidden Pressure Kinds

The following are not legal pressure:

- "Character X must choose Y"
- "World outcome Z must happen"
- "The hidden canon fact is true and should now shape the scene" without legal reveal path
- "Narrator should make this feel inevitable" as a factual directive
- "A convenient new rule appears"
- "A secret witness arrives" unless `World Agent` validates an existing or scheduled basis

Important rule:

- if pressure requires a new fact, it must be routed as `world_translation_request` or `CanonMutationRequest`
- Plot cannot create the fact itself

## Plot Pressure Budget

Pressure budget prevents every beat from becoming a forced crisis.

Suggested budget fields:

| Field | Required | Meaning |
| --- | --- | --- |
| `intensity` | yes | low, medium, high, critical |
| `novelty` | recommended | recurring, escalated, new |
| `stacking_count` | recommended | how many active pressures affect the same choice space |
| `relief_available` | recommended | whether the scene still permits pause, retreat, or alternate route |
| `agency_risk` | yes | low, medium, high |

Budget rules:

1. high or critical pressure requires stronger `non_forcing_clause`
2. repeated pressure on the same choice must show why it is not railroading
3. pressure should usually make options costly, not impossible
4. if all options but one are removed, the packet should be quarantined or rewritten
5. `agency_risk = high` requires Orchestrator review before routing

## Non-Forcing Clause

Every pressure packet must state how meaningful choice remains open.

Good clauses:

- "Lin may confront Wei, delay the question, call a witness, or retreat to gather evidence."
- "The deadline raises cost, but it does not decide whether Wei lies, confesses, or redirects."
- "The crowd increases exposure, but characters may still choose silence, public accusation, or private negotiation."

Bad clauses:

- "Wei must confess because pressure is high."
- "Lin has no choice but to accuse."
- "The scene should force the reveal now."

## World Translation Boundary

Some pressure is purely structural. Some pressure wants to become a world condition.

| Pressure request | Who decides if it becomes fact | Rule |
| --- | --- | --- |
| approaching deadline based on established schedule | `World Agent` | may translate if schedule exists |
| crowd gathering in a location | `World Agent` | needs location and cause basis |
| guard arrival | `World Agent` | needs prior route, order, or probability model |
| new institution command | `Canon Steward` if it creates or changes institution law | Plot cannot declare it |
| hidden canon clue becoming active | `Canon Steward` and reveal rules | must not leak raw latent canon |

Important rule:

- `World Agent` may accept, downgrade, transform, or reject a translation request
- rejected translation may still remain as structure note, but not as fact

## Field Projection and Visibility

Not every agent receives the same pressure view.

| Recipient | Legal pressure view |
| --- | --- |
| `Character Agent` | public or character-perceivable pressure only |
| `World Agent` | full pressure packet needed for adjudication, excluding plot-only destiny language |
| `Narrator Agent` | only pressure that is committed into `NarratorInputPacket` or render bounds |
| `Canon Steward` | only canon-relevant pressure requests |
| `Orchestrator` | full routing and validation metadata |

Important rule:

- pressure may guide scene setup
- it must not reveal hidden authorial intent to characters

## Validation Rules

| Rule | Behavior |
| --- | --- |
| missing `pressure_kind` | warn and require repair |
| missing `non_forcing_clause` | quarantine until repaired |
| missing `visibility` | quarantine unless route has one unique legal value |
| pressure specifies character choice | hard block |
| pressure specifies world outcome | reroute to `World Agent` as translation request or hard block |
| pressure depends on new canon | reroute to `CanonMutationRequest` |
| pressure uses raw hidden cognition | quarantine |
| pressure stacks too heavily | downgrade, split, or require budget review |

## Hard Boundaries

`Plot Agent` may:

- create urgency
- raise cost
- highlight unresolved tension
- request world translation
- track structural escalation

`Plot Agent` may not:

- puppet characters
- declare objective events
- decide success or failure
- reveal hidden canon
- make narrator overclaim inevitability
- use private memories as free omniscient planning material

## Example

```json
{
  "pressure_id": "spp_018_01",
  "scene_id": "scene_018",
  "beat_id": "beat_archive_probe",
  "pressure_kind": "deadline",
  "scope": "scene",
  "duration": "until_condition",
  "affected_options": [
    "delaying the archive inspection becomes costlier",
    "open accusation becomes more socially risky",
    "private negotiation becomes harder after guards arrive"
  ],
  "non_forcing_clause": "Lin may confront Wei, stall, call a witness, or leave to gather more evidence; the pressure does not choose for Lin.",
  "world_fact_dependency": [
    "public_canon:archive_inspection_schedule",
    "public_event_ledger:inspection_announced"
  ],
  "world_translation_request": {
    "request": "confirm whether guards are plausibly approaching the archive corridor within the scene",
    "acceptable_translations": ["footsteps heard", "messenger warning", "no visible arrival yet"]
  },
  "forbidden_outcomes": [
    "Lin must accuse Wei",
    "Wei must confess",
    "guards definitely arrive unless World Agent commits it"
  ],
  "visibility": "system_restricted",
  "budget_cost": {
    "intensity": "medium",
    "novelty": "escalated",
    "stacking_count": 2,
    "relief_available": true,
    "agency_risk": "medium"
  },
  "based_on": ["act_structure:archive_thread", "pub_017_02"]
}
```

## Relationship to Adjacent Specs

This document should be read together with:

- `communication-permission-matrix-v0.1.md`
- `agent-constraint-matrix-v0.1.md`
- `resolution-state-delta-commit-pipeline-v0.1.md`
- `agent-context-packet-and-field-visibility-v0.1.md`

Next protocol priority after this document:

1. build adversarial pressure fixtures for railroading, hidden fact smuggling, and over-stacking
2. align dialogue evaluation metrics with agency preservation
3. prototype a paper scene trace before autonomous execution
