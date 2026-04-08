# DialogueWindow Schema v0.1

This document defines the first concrete payload shape for `DialogueWindow`.

The goal is to keep dialogue coordination compact enough for real scene flow, while preserving private cognition, role boundaries, and dramatic tension.

## Purpose

`DialogueWindow` is the default coordination unit for spoken interaction inside a scene.

It is not:

- one raw utterance
- one full scene
- a direct narrator-facing prose packet

It is:

- one bounded dramatic move
- one short exchange packet
- one unit that a `Character Agent` can submit to `World Agent`
- one unit that can later contribute to a committed `ScenePacket`

## Design Constraints

`DialogueWindow` should satisfy five constraints:

1. It must be faster than line-by-line turn simulation.
2. It must not leak raw private cognition by default.
3. It must let a character express tactic, posture, and speech intent.
4. It must not let a character declare outcomes.
5. It must give `World Agent` enough structure to resolve information flow, pressure shifts, and visible consequences.

## Placement in the Protocol

Recommended loop:

1. `Plot Agent` injects scene pressure if needed
2. `World Agent` publishes current observations
3. active `Character Agent` submits `DialogueWindow`
4. `World Agent` resolves visible effects and updates scene state
5. committed result is packed into `ScenePacket`
6. `Narrator Agent` renders prose from committed material

Important rule:

- `Narrator Agent` should not render directly from raw `DialogueWindow`
- it should render from committed state after world resolution

## Payload Shape

`DialogueWindow` lives inside the generic message envelope described elsewhere.

The fields below describe the `payload` portion.

| Field | Required | Type | Meaning |
| --- | --- | --- | --- |
| `window_kind` | yes | string | the dramatic function of the window |
| `speaker_id` | yes | string | the acting character |
| `addressee_ids` | yes | array | intended dialogue targets |
| `local_goal` | yes | string | what the speaker is trying to achieve in this window |
| `speech_acts` | yes | array | one to three dialogue moves |
| `stance` | recommended | object | emotional and tactical posture |
| `disclosure_policy` | recommended | object | what may or may not be revealed |
| `context_span` | optional | object | how much recent context this window assumes |
| `fallback_if_blocked` | optional | string | what the character defaults to if the move fails |
| `exit_condition` | optional | string | what counts as this window ending |

## Enumerated Guidance

### `window_kind`

Suggested values:

- `probe`
- `deflect`
- `conceal`
- `reveal`
- `persuade`
- `threaten`
- `negotiate`
- `stall`
- `reassure`
- `rupture`
- `routine`

This field is descriptive, not absolute. It helps routing, evaluation, and later analytics.

### `stance`

`stance` captures how the character is approaching the exchange without exposing the full private chain-of-thought.

Suggested subfields:

| Field | Required | Meaning |
| --- | --- | --- |
| `emotional_tone` | recommended | calm, defensive, aggressive, brittle, guarded, warm |
| `tactical_posture` | recommended | direct, evasive, testing, manipulative, conciliatory |
| `urgency` | optional | low, medium, high |
| `risk_tolerance` | optional | low, medium, high |

### `disclosure_policy`

This field protects local knowledge and hidden motive.

Suggested subfields:

| Field | Required | Meaning |
| --- | --- | --- |
| `must_not_reveal` | recommended | facts, motives, names, or links the speaker will protect |
| `may_imply` | optional | what the speaker is willing to hint at |
| `can_lie` | optional | whether deception is allowed in this window |
| `preferred_mask` | optional | the surface role the speaker wants to present |

## `speech_acts`

Each `DialogueWindow` should contain one to three `speech_acts`.

Each `speech_act` is a compact tactical move, not necessarily one literal line.

Suggested shape:

| Field | Required | Meaning |
| --- | --- | --- |
| `act_id` | yes | stable id within the window |
| `intent` | yes | what this act tries to do |
| `content_mode` | yes | question, statement, refusal, accusation, offer, warning, silence |
| `proposition` | yes | the semantic content of the move |
| `delivery_style` | optional | clipped, gentle, formal, mocking, indirect |
| `candidate_lines` | optional | one to three possible lines for later rendering reference |
| `expected_effect` | optional | what the speaker hopes changes |
| `risk_if_misread` | optional | what could go wrong if the addressee interprets it badly |

Important rule:

- `candidate_lines` are optional and non-authoritative
- they help preserve voice and intent
- they do not become canon unless committed through later world resolution and scene packing

## Hard Boundaries

`DialogueWindow` may express:

- what a character tries to communicate
- how a character frames the exchange
- what the character is willing to risk

`DialogueWindow` may not declare:

- that the other character believes something
- that persuasion succeeds
- that a reveal is accepted as true
- that the room's power balance has already changed

Those belong to `World Agent` resolution.

## Validation Rules

| Rule | Behavior |
| --- | --- |
| missing `window_kind` | warn and infer only if obvious from speech acts |
| more than three `speech_acts` | warn and split into multiple windows |
| empty `speech_acts` | reject as unusable |
| explicit outcome claims | quarantine or require rewrite |
| raw chain-of-thought leakage | strip or request repair |
| overly long candidate lines | compress or request repair |

## Default Interpretation Policy

If a `DialogueWindow` is valid, `World Agent` should treat it as:

- a bounded attempt
- a visible or partially visible exchange proposal
- a source for information-flow updates
- a source for social pressure updates

It should not treat it as:

- direct scene truth
- guaranteed persuasion
- reliable evidence of another character's internal state

## Example

```json
{
  "window_kind": "probe",
  "speaker_id": "char_wei",
  "addressee_ids": ["char_lin"],
  "local_goal": "test whether Lin already knows about the missing ledger",
  "stance": {
    "emotional_tone": "guarded",
    "tactical_posture": "testing",
    "urgency": "medium",
    "risk_tolerance": "low"
  },
  "disclosure_policy": {
    "must_not_reveal": [
      "wei_took_the_copy",
      "the_archive_contact"
    ],
    "may_imply": [
      "someone_inside_the_house_is_hiding_information"
    ],
    "can_lie": true,
    "preferred_mask": "concerned_ally"
  },
  "speech_acts": [
    {
      "act_id": "a1",
      "intent": "open indirectly",
      "content_mode": "question",
      "proposition": "ask whether Lin has noticed anything missing",
      "delivery_style": "casual",
      "candidate_lines": [
        "You have been in the archive longer than I have. Did anything feel off to you?",
        "Nothing missing from the records room, I hope?"
      ],
      "expected_effect": "Lin reveals whether they already know about the ledger",
      "risk_if_misread": "Lin suspects Wei knows too much"
    },
    {
      "act_id": "a2",
      "intent": "apply mild pressure",
      "content_mode": "statement",
      "proposition": "suggest that concealment would now be dangerous",
      "delivery_style": "quiet",
      "candidate_lines": [
        "If something is wrong, this is the worst hour to keep it hidden."
      ],
      "expected_effect": "Lin feels pressure to answer honestly"
    }
  ],
  "fallback_if_blocked": "retreat into procedural concern and end the exchange",
  "exit_condition": "Lin answers, refuses clearly, or redirects to a third party"
}
```

## Relationship to Future Specs

This document does not yet define:

- `ScenePacket`
- `Resolution` payload details
- dialogue-specific evaluation metrics

Those should be defined next.
