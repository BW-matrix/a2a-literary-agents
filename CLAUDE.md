# CLAUDE.md — a2a-literary-agents / vibe-somnium / 织梦

> 本文件是你作为 Claude Code 加入本项目时的完整上下文。请在每次对话开始时优先阅读此文件。

---

## 1. Project Identity

| Key | Value |
| --- | --- |
| Repository | `a2a-literary-agents` |
| Codename | `vibe-somnium / 织梦` |
| Author | Bowen Qi |
| License | Code: Apache-2.0 · Docs: CC BY 4.0 |
| Stage | **docs-first runtime protocol hardening** — 尚未进入实现阶段 |

### 一句话定位

这个项目的核心判断是：AI writing 的核心问题不是 prose 不够好，而是 **authorial power 过于集中**，导致世界、人物、冲突都会被当前 prompt 临时改写。我们的方案是把创作拆成多个拥有有限权限的 agents，通过 A2A protocol 和 hard authority boundaries 来构造让文学更可能发生的条件。

---

## 2. Architecture Overview — Six-Agent System

```
┌─────────────────────────────────────────────────────┐
│                   Orchestrator                       │
│         routing · validation · scheduling            │
├────────┬────────┬────────┬────────┬─────────────────┤
│ Char   │ World  │ Plot   │ Narr   │ Canon Steward   │
│ Agent  │ Agent  │ Agent  │ Agent  │                 │
│        │        │        │        │                 │
│ will   │ conse- │ pres-  │ prose  │ canon mutation  │
│ motive │ quence │ sure   │ voice  │ review          │
│ choice │ state  │ tension│ render │ approval        │
└────────┴────────┴────────┴────────┴─────────────────┘
```

| Agent | Core Authority | Cannot Do |
| --- | --- | --- |
| **Character Agent** | will, motive, choice, self-interpretation | declare objective outcome, write others' minds, change canon |
| **World Agent** | consequence, causality, state transition | write character inner truth, bypass canon, ignore rules for drama |
| **Plot Agent** | pressure, tension, structural escalation | puppet characters, declare facts, edit canon |
| **Narrator Agent** | prose, voice, rendering | invent facts, leak latent canon, rewrite committed events |
| **Canon Steward** | canon review and mutation approval | alter immutable canon, decide scene outcome |
| **Orchestrator** | routing, validation, scheduling | rewrite content, become hidden author |

---

## 3. Protocol Axioms (不可违反)

1. `character decides intent`
2. `world decides consequence`
3. `plot decides pressure`
4. `narrator decides expression`
5. `canon steward decides canon mutation`
6. `orchestrator decides routing and validation`

---

## 4. Working Principles

- `soft validation, hard permission` — 格式错误 warn + repair；权限越界 quarantine + hard block
- `private cognition, public consequence` — 内部思维留在 private_self，只有转化后的 intent/action 才能离开自我边界
- `plot provides pressure, not destiny` — plot 提供张力而非命运
- `narrator cannot invent facts` — narrator 只能从 committed scene packet 渲染，不能自造事实
- `character decides intent, world decides consequence` — 意图与后果分属不同 agent
- `complete objects are system objects; agents receive projected views` — 完整对象不默认进入任何 agent prompt

---

## 5. Key Concepts & Terminology

### 5.1 Pacing Unit: `dramatic window`

系统不按每一句台词调度，而按 dramatic window 调度。一个 window 可能包含：
- one short exchange
- one tactical move in a negotiation
- one emotional turn in an argument
- one conceal / probe / reveal attempt

### 5.2 State & Knowledge Layers

| Layer | What it is | Visibility |
| --- | --- | --- |
| `world_state_ledger` | 客观真实——发生了什么 | system-restricted |
| `public_event_ledger` | 已经成为公共知识的事件 | shared/public |
| `private_memory` | agent 自己的记忆、信念、猜测 | self only |
| `public_canon` | 稳定的世界规则和公开设定 | shared/public |
| `latent_canon` | 已经为真但尚未公开的设定 | restricted |

> **关键区分**: "世界里发生了什么" ≠ "谁被允许知道它"。如果两者混为一谈，系统就会退化回 hidden omniscience。

### 5.3 Canon Layers

| Layer | Meaning | Who may change |
| --- | --- | --- |
| `Immutable Canon` | 基础世界法则 | 无 |
| `Latent Canon` | 存在但未揭示 | 仅揭示，不修改 |
| `Emergent Canon` | 创作中新生成设定的来源属性 | Canon Steward after review；visibility 另行标为 public / latent / scoped |

### 5.4 Visibility Layers

`private_self` → `private_target` → `scene_public` → `system_restricted`

### 5.5 Discouraged Terms

| ❌ Avoid | ✅ Use instead | Reason |
| --- | --- | --- |
| `public ledger` | `public_event_ledger` or `world_state_ledger` | 太粗糙，混淆 truth 与 publicity |
| `world` (agent context) | `World Agent` | 容易混淆 |
| `character` (authority context) | `Character Agent` | 可能指虚构人物或系统角色 |

---

## 6. Current Document Inventory

```
docs/
├── protocol/
│   ├── communication-permission-matrix-v0.1.md   # 主协议：六角色通信矩阵 + event bus + message envelope
│   ├── agent-constraint-matrix-v0.1.md           # 实现级：constraint × agent 展开表
│   ├── dialogue-window-schema-v0.1.md            # DialogueWindow payload 定义 + JSON 示例
│   ├── scene-packet-schema-v0.1.md               # ScenePacket payload shape + commit semantics + narration bounds
│   ├── agent-context-packet-and-field-visibility-v0.1.md # AgentContextPacket + field-level projection rules
│   ├── resolution-state-delta-commit-pipeline-v0.1.md # Resolution / StateDelta / two-phase commit pipeline
│   ├── scene-pressure-packet-and-plot-budget-v0.1.md # ScenePressurePacket schema + Plot pressure budget
│   ├── memory-delta-format-v0.1.md               # MemoryDelta shape + writer rules + revision lineage
│   ├── canon-mutation-review-checklist-v0.1.md   # CanonMutationRequest 审查流程 + decision outcomes + commit semantics
│   ├── event-publication-thresholds-v0.1.md      # public_event_ledger 的发布阈值 + publication scope + contestability
│   ├── scene-packet-to-memory-handoff-v0.1.md    # ScenePacket 到 MemoryDelta 的 owner-specific 派生规则
│   ├── latent-to-public-canon-reveal-rules-v0.1.md # latent_canon 何时能合法提升为 public_canon
│   └── state-and-knowledge-layers-v0.1.md        # 五层存储模型 + access matrix + promotion rules
└── reference/
    └── terminology-index-v0.1.md                 # 规范术语表（80+ terms）
```

All documents are **v0.1** — stable enough to build on, open for refinement.

---

## 7. Near-Term Roadmap (按优先级)

> 当前阶段是 **protocol design**，不急着做 UI 或 full implementation。

| # | Task | Status | Notes |
| --- | --- | --- | --- |
| 1 | Communication + Permission Matrix | ✅ done | `communication-permission-matrix-v0.1.md` |
| 2 | Agent Constraint Matrix | ✅ done | `agent-constraint-matrix-v0.1.md` |
| 3 | DialogueWindow schema | ✅ done | `dialogue-window-schema-v0.1.md` |
| 4 | State & Knowledge Layers | ✅ done | `state-and-knowledge-layers-v0.1.md` |
| 5 | Terminology Index | ✅ done | `terminology-index-v0.1.md` |
| 6 | **ScenePacket schema** | ✅ done | `scene-packet-schema-v0.1.md` |
| 7 | **Memory delta format** | ✅ done | `memory-delta-format-v0.1.md` |
| 8 | **Canon mutation review checklist** | ✅ done | `canon-mutation-review-checklist-v0.1.md` |
| 9 | **Event publication thresholds** | ✅ done | `event-publication-thresholds-v0.1.md` |
| 10 | **ScenePacket-to-memory handoff rules** | ✅ done | `scene-packet-to-memory-handoff-v0.1.md` |
| 11 | **Latent-to-public canon reveal rules** | ✅ done | `latent-to-public-canon-reveal-rules-v0.1.md` |
| 12 | **AgentContextPacket + field visibility** | ✅ done | `agent-context-packet-and-field-visibility-v0.1.md` |
| 13 | **Resolution / StateDelta / commit pipeline** | ✅ done | `resolution-state-delta-commit-pipeline-v0.1.md` |
| 14 | **ScenePressurePacket + Plot pressure budget** | ✅ done | `scene-pressure-packet-and-plot-budget-v0.1.md` |
| 15 | **Adversarial protocol trace fixtures** | 🔲 next | hidden theft, false report, partial reveal, narrator leak, world overreach, plot railroading |
| 16 | **Narration grounding + dialogue evaluation metrics** | 🔲 planned | prose grounding and dialogue quality evaluation |
| 17 | **Paper scene runner, then minimal runner prototype** | 🔲 planned | 先手动 trace，再自动化 |

---

## 8. Open Design Questions (from v0.1 docs)

1. How to format adversarial protocol trace fixtures before implementation
2. Whether `DialogueWindow` should contain candidate lines or only speech acts in high-risk scenes
3. How much of private cognition may be selectively exposed to narrator in close POV modes
4. How scene packets should be summarized for long-form memory retention
5. How `public_event_ledger` entries should interact with owner memory after later encounter
6. How scoped reveal outcomes should propagate across local, institutional, and wider public reasoning without collapsing into global omniscience
7. How to validate narration grounding without overbuilding an automated theorem prover

---

## 9. Collaboration Style

### Language
- **双语工作**: docs 正文用英文（为了可搜索性和开放性），解释和讨论可以用中文
- README 和 protocol docs 都保持英文主体 + 中文注释的风格

### Workflow
- **Docs-first**: 先把 protocol 和 spec 写清楚，再考虑实现
- **Incremental versioning**: 文档用 `-v0.1`, `-v0.2` 等版本后缀
- **One concept, one document**: 每个核心概念独立一个 spec 文件

### Communication
- 用户可能用中文提需求，你可以用中文回复讨论，但产出的文档正文应以英文为主
- 保持术语一致性——先查 `terminology-index-v0.1.md`
- 如果要引入新术语，先加入 terminology index，再在其他文档中使用

---

## 10. What You Should Do

1. **接到任务时，先查看相关的现有文档**，确保你的产出与已有 protocol 一致
2. **写新 spec 时，遵循现有文档的格式和风格**（参考 `dialogue-window-schema-v0.1.md` 作为模板）
3. **引入新术语时，先更新 `terminology-index-v0.1.md`**
4. **保持 agent 权限边界**——在设计中不要让任何 agent 越权
5. **优先推进 roadmap 上标记为 🔲 next 的任务**
6. **不要把完整 system object 直接塞给 agent**；先通过 `AgentContextPacket` / projected view 组包

## 11. What You Should NOT Do

1. ❌ 不要直接开始写代码实现——当前阶段是 protocol design
2. ❌ 不要跳过现有文档直接发明新概念——先 review 再扩展
3. ❌ 不要在设计中让任何 agent 获得超出其 authority 的能力
4. ❌ 不要把 `world_state_ledger` 和 `public_event_ledger` 混为一谈
5. ❌ 不要用 discouraged terms（见 Section 5.5）

---

## 12. Quick Reference: Message Envelope

Every routed message should include:

```
message_id · message_type · sender · target
scene_id · window_id · visibility · payload · based_on
```

Missing recoverable fields should trigger soft recovery (warn, normalize, repair), not hard crash.

Security-critical fields such as `sender`, `message_type`, `visibility`, `target`, `authority_basis`, and `authorized_interiority.scope_limit` should quarantine or require explicit repair unless the route context has exactly one legal value.

---

## 13. Quick Reference: Scene Loop

```
1. Plot Agent     → submits bounded ScenePressurePacket
2. World Agent    → publishes current observations
3. Character Agent → submits DialogueWindow
4. World Agent    → emits Resolution, StateDelta, and VisibilityResult
5. Orchestrator   → seals committed result into ScenePacket and projected views
6. Narrator Agent → renders prose from NarratorInputPacket
```

> Narrator 只能从 committed material 的 `NarratorInputPacket` 获取素材，不能从 raw DialogueWindow、raw world_state_ledger、pending reveal candidate 直接渲染。

---

*Last updated: 2026-04-27*
