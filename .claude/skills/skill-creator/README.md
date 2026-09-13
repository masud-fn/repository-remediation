# skill-creator

A skill for creating new skills, iteratively improving them, and measuring their performance.
Use it to scaffold a skill from scratch, run eval loops, and benchmark improvement.

## What It Does

When activated, this skill guides the agent through the full skill development lifecycle:

1. **Draft** — capture intent, write a SKILL.md, and structure the skill directory correctly.
   - Emphasizes design principles from writing-great-skills: **predictability**, **leading words**, and **invocation** choices (model-invoked vs user-invoked)
2. **Test** — run the skill (with and without it loaded) against a set of eval prompts.
3. **Evaluate** — grade assertions, generate a benchmark report, and launch a browser-based
   review viewer so the user can give qualitative feedback.
4. **Iterate** — rewrite based on feedback, benchmark data, and skill-design principles (check for duplication, sediment, sprawl, no-ops); repeat until satisfied.
5. **Package** — bundle the final skill into a `.skill` file for distribution.

## Skill Design Principles

This skill integrates comprehensive design guidance from **writing-great-skills** (the framework for building predictable, maintainable skills). Key concepts:

- **Predictability** — the agent takes the same process every run, not the same output
- **Information Hierarchy** — rank skill content by how immediately the agent needs it (steps, in-file reference, disclosed reference)
- **Progressive Disclosure** — move reference out of SKILL.md behind context pointers to keep the top legible
- **Leading Words** — compact concepts already in pretraining that anchor behavior with minimal tokens
- **Failure Modes** — duplication, sediment, sprawl, no-ops, negation, premature completion

During the workflow, you'll receive guidance on these principles at natural decision points. See:
- `references/skill-design-principles.md` — Workflow-focused bridge to design concepts
- `references/skill-design-glossary.md` — Complete glossary of terms (adapted from writing-great-skills)

## Skill Structure

```
skill-creator/
├── SKILL.md                        # The skill instructions (loaded into agent context)
├── README.md                       # This file
├── agents/
│   ├── analyzer.md                 # Subagent: analyze benchmark results and find patterns
│   └── comparator.md               # Subagent: blind A/B comparison between configurations
├── references/
│   └── schemas.md                  # JSON schema definitions for evals, grading, benchmarks
├── scripts/
│   ├── __init__.py
│   ├── utils.py                    # Shared file I/O and SKILL.md parser
│   ├── quick_validate.py           # Validate SKILL.md structure and frontmatter
│   ├── run_quality_evals.py        # CI runner: execute all evals and grade results
│   ├── run_deepeval.py             # Low-level grader for a single eval run directory
│   ├── deepeval_providers.py       # Provider factory (claude CLI, Bedrock, Copilot)
│   ├── aggregate_benchmark.py      # Aggregate runs into benchmark.json with stats
│   └── package_skill.py           # Bundle a completed skill into a .skill file
└── eval-viewer/
    ├── viewer.html                 # Interactive browser UI for reviewing eval results
    └── generate_review.py         # Generate and launch the eval viewer
```

## Creating a New Skill

Ask the agent:

> I want to create a skill for [describe what you want the skill to do].

The skill-creator will help you clarify scope, write the initial `SKILL.md`, create eval test
cases, run the eval loop, and iterate until the skill performs well.

## Running Evals for an Existing Skill

Point the agent at a skill's eval file:

```
Skill path:  plugins/fn-software-engineering/skills/<skill-name>
Evals file:  plugins/fn-software-engineering/skills/<skill-name>/evals/evals.json
```

The skill-creator will:

1. Read each eval prompt from `evals.json`
2. Run the prompt with the skill loaded (and optionally without, for a baseline)
3. Grade each assertion against the output
4. Produce a benchmark report with pass rates
5. Launch the eval viewer for human review

## Validating a Skill

Check that a skill's `SKILL.md` frontmatter is well-formed:

```sh
cd .claude/skills/skill-creator
python -m scripts.quick_validate /path/to/skill-dir
```

## Full Workflow Reference

See [SKILL.md](./SKILL.md) for the complete workflow,
including environment-specific notes (Claude.ai vs Claude Code), eval schemas, and iteration
strategy.
