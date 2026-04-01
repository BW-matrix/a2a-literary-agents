# a2a-literary-agents

Working title / codename: `vibe-somnium / 织梦`

`a2a-literary-agents` is a docs-first project for literary multi-agent AI writing systems built around A2A communication, hard authority boundaries, and stable world logic.

`vibe-somnium / 织梦` 是这个方向的 project codename。这个项目的核心判断是：现在很多 direct AI writing 的问题，不只是 prose 不够好，而是 authorial power 过于集中，导致世界、人物、冲突都会被当前 prompt 临时改写，最后产出的是可变形文本，不是稳定生长的 fiction。

## Core Premise

我们不把 AI 当成一个万能作者，而是把创作拆成多个拥有有限权限的 agents：

- `character agent`: owns will, motive, subjectivity
- `world agent`: owns consequence, causality, state transition
- `plot agent`: owns pressure, tension, structural conflict
- `narrator agent`: owns prose, voice, rendering
- `canon steward`: owns canon mutation review
- `orchestrator`: owns routing, validation, scene scheduling

这套系统追求的不是 deterministic production of literature，而是构造一种让文学更可能发生的条件：stable world, bounded authority, local knowledge, accumulating tension。

## Current Focus

当前阶段先不做 product，不急着做 UI，也不先做 full implementation。先把 protocol 和约束体系定义清楚：

- communication constraints
- permission constraints
- event bus validation behavior
- scene execution cadence
- canon mutation policy

## Documents

- [communication-permission-matrix-v0.1](docs/protocol/communication-permission-matrix-v0.1.md)
- [agent-constraint-matrix-v0.1](docs/protocol/agent-constraint-matrix-v0.1.md)

## Working Principles

- `soft validation, hard permission`
- `private cognition, public consequence`
- `plot provides pressure, not destiny`
- `narrator cannot invent facts`
- `character decides intent, world decides consequence`

## Near-Term Roadmap

1. Finalize the first communication and permission matrix
2. Expand the matrix into agent-by-constraint implementation tables
3. Define the A2A message envelope and per-agent message allowlists
4. Define public ledger, private memory, and canon stores
5. Prototype a minimal scene runner

## License

This repository uses a mixed-license structure.

- Code and other non-documentation repository contents are licensed under Apache-2.0.
- Documentation and protocol text, including `README.md` and all files under `docs/`, are licensed under CC BY 4.0.
- Attribution and origin context are summarized in `NOTICE`.

See [LICENSE](LICENSE), [LICENSE-docs](LICENSE-docs), and [NOTICE](NOTICE).
