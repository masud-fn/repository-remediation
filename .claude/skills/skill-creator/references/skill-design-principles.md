# Skill Design Principles — Workflow Integration

This guide connects each stage of skill-creator to the design vocabulary in `skill-design-glossary.md`. Read that file first for term definitions — this file only maps them onto skill-creator's own workflow steps.

## Applying These Principles in skill-creator

### During Capture Intent

- Identify the skill's **leading word** — the compact concept users will think with
- Decide **model-invoked** or **user-invoked** based on whether the agent must reach it autonomously
- Sketch the **information hierarchy**: will this be steps, reference, or both?

### During Write SKILL.md

- Craft a description that anchors **invocation** with **leading words** users actually say
- Explain **context load** vs **cognitive load** trade-offs for skill boundaries
- Use **progressive disclosure** to keep the body legible — push reference to disclosed files
- Define **completion criteria** that are both clear and demanding

### During Test Cases

- Test cases should cover distinct **branches** of the skill
- Evaluate whether **information hierarchy** and **progressive disclosure** are working (can the agent find what it needs?)

### During Iteration

- Check for **failure modes**: duplication, sediment, sprawl, no-ops, negation, premature completion
- Measure **legwork**: Are completion criteria demanding enough? Is the agent doing thorough work?
- Hunt for **no-ops** and delete them; strengthen weak **leading words**
- Prune stale material — maintain **relevance** discipline
- Ensure **single source of truth** for each meaning
