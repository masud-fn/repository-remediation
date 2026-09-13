---
name: skill-creator
description: Create new skills, modify and improve existing skills, and measure skill performance with DeepEval benchmarking. Use when users want to create a skill from scratch, edit, or optimize an existing skill. Every skill requires test cases and DeepEval-based assertions to verify correctness and measure performance.
---

# Skill Creator

A skill for creating new skills and iteratively improving them.

At a high level, the process of creating a skill goes like this:

- Decide what you want the skill to do and roughly how it should do it
- Write a draft of the skill
- Create a few test prompts and run claude-with-access-to-the-skill on them
- Help the user evaluate the results both qualitatively and quantitatively
  - While the runs happen in the background, draft some quantitative evals if there aren't any (if there are some, you can either use as is or modify if you feel something needs to change about them). Then explain them to the user (or if they already existed, explain the ones that already exist)
  - Use the `eval-viewer/generate_review.py` script to show the user the results for them to look at, and also let them look at the quantitative metrics
- Rewrite the skill based on feedback from the user's evaluation of the results (and also if there are any glaring flaws that become apparent from the quantitative benchmarks)
- Repeat until you're satisfied
- Expand the test set and try again at larger scale

Your job when using this skill is to figure out where the user is in this process and then jump in and help them progress through these stages. So for instance, maybe they're like "I want to make a skill for X". You can help narrow down what they mean, write a draft, write the test cases, figure out how they want to evaluate, run all the prompts, and repeat.

On the other hand, maybe they already have a draft of the skill. In this case you can go straight to the eval/iterate part of the loop.

**Important:** Evals with DeepEval are mandatory for all skill types. Every skill must have test cases and assertions, even if the skill's output is subjective. We'll use DeepEval's LLM-as-judge grading to measure performance objectively.

## Communicating with the user

This skill will be primarily used by engineers who are familiar with the concepts of skills, test cases, and evaluation. However, some users may be less familiar with these concepts.

So please pay attention to context cues to understand how to phrase your communication! In the default case, just to give you some idea:

- "evaluation" and "benchmark" are borderline, but OK
- for "JSON" and "assertion" you want to see serious cues from the user that they know what those things are before using them without explaining them

It's OK to briefly explain terms if you're in doubt, and feel free to clarify terms with a short definition if you're unsure if the user will get it.

---

## Creating a skill

### Capture Intent

Start by understanding the user's intent. The current conversation might already contain a workflow the user wants to capture (e.g., they say "turn this into a skill"). If so, extract answers from the conversation history first — the tools used, the sequence of steps, corrections the user made, input/output formats observed. The user may need to fill the gaps, and should confirm before proceeding to the next step.

1. What should this skill enable Claude to do?
2. When should this skill trigger? (what user phrases/contexts)
3. What's the expected output format?
4. What test cases should we create? We'll craft 2-3 realistic test prompts and DeepEval assertions to verify the skill works correctly, regardless of whether the output is objective or subjective.

**Design perspective (see `references/skill-design-principles.md`):** Identify the skill's **leading word** — the compact, pretrained concept users will think with (e.g., _tracer bullets_, _fog of war_). This anchors both invocation and execution. Also decide early whether this skill should be **model-invoked** (with description, discoverable by the agent) or **user-invoked** (hand-invoked only, no description). This trade-off determines **context load** (model-invoked costs window space) vs **cognitive load** (user-invoked costs what you remember).

### Interview and Research

Proactively ask questions about edge cases, input/output formats, example files, success criteria, and dependencies. Wait to write test prompts until you've got this part ironed out.

Check available MCPs - if useful for research (searching docs, finding similar skills, looking up best practices), research in parallel via subagents if available, otherwise inline. Come prepared with context to reduce burden on the user.

### Write the SKILL.md

Based on the user interview, fill in these components:

- **name**: Skill identifier
- **description**: The primary triggering mechanism — write it as a router: when to reach for this skill, not just what it does. See "Writing an effective description" below for the full guidance.
- **compatibility**: Required tools, dependencies (optional, rarely needed)
- **the rest of the skill :)**

### Writing an effective description

The description is the only part of a skill that's in context before the skill is chosen — it has to work as a router, not a summary. A few principles, drawn from what tends to make descriptions under- or over-trigger in practice:

- **Imperative, not descriptive.** Write "Use this skill when..." rather than "This skill does...". The agent is deciding whether to act; tell it when to act.
- **User intent, not implementation.** Describe what the user is trying to accomplish, not the skill's internal mechanics — that's what gets matched against what the user actually asked for.
- **Name the non-obvious trigger contexts, but stay precise.** Claude tends to *undertrigger* skills — to not use them when they'd help. Combat that by spelling out contexts where the skill applies even if the user doesn't use the obvious keyword: instead of "How to build a simple fast dashboard to display internal data," write "...Use this whenever the user mentions dashboards, data visualization, or wants to display company metrics, even if they don't explicitly ask for a 'dashboard.'" But don't go so broad that a near-miss request for a genuinely different capability would also match — precision matters as much as coverage.
- **Be ruthlessly concise.** Every installed skill's description loads into context on every turn, competing with every other skill's. 1024 characters is the hard limit, not a target — aim for a tight 2-4 sentence paragraph. If a clause isn't earning its place by narrowing or widening the trigger conditions, cut it.
- **Use your leading word.** Embed the skill's **leading word** (the compact concept users think with) in the description so that when the same word appears in user prompts or team docs, the agent links it to the skill. This anchors invocation through shared language.

**Context load trade-off (see `references/skill-design-principles.md`):** Every description loads into context on every turn — this is **context load**, the cost of model-invocation. Make sure the skill truly benefits from agent autonomy; if it only fires by hand, strip the description and make it **user-invoked** to save context.

Before/after:

```yaml
# Too vague — no concrete triggers, agent won't know when to reach for it
description: Process CSV files.

# Better — concrete triggers, still concise, uses leading word
description: >
  Analyze CSV/TSV/Excel files — summary stats, derived columns, charts,
  data cleaning. Use when the user has tabular data to explore, transform,
  or visualize, even if they don't say "CSV" or "analysis."
```

For now, treat this as a judgment call rather than something to test empirically: from the skill-creator directory, run `python -m scripts.quick_validate <skill-path>` for the structural check (naming, length, formatting), and sanity-check triggering by re-reading the description against a few realistic user phrasings yourself. (We previously had a scripted eval loop for measuring triggering accuracy; we're not using that for now, but may bring it back later.)

### Skill Writing Guide

#### Anatomy of a Skill

```
skill-name/
├── SKILL.md (required)
│   ├── YAML frontmatter (name, description required)
│   └── Markdown instructions
└── Bundled Resources (optional)
    ├── scripts/    - Executable code for deterministic/repetitive tasks
    ├── references/ - Docs loaded into context as needed
    └── assets/     - Files used in output (templates, icons, fonts)
```

#### Information Hierarchy and Progressive Disclosure

Skills use a three-level loading system (see `references/skill-design-principles.md`):

1. **Metadata** (name + description) - Always in context (~100 words)
2. **SKILL.md body** - In context whenever skill triggers (<500 lines ideal)
3. **Bundled resources** - As needed (unlimited, scripts can execute without loading)

**Progressive disclosure** means moving material down this ladder — out of SKILL.md and behind **context pointers** (clear references that tell the agent _when_ to reach the material) — so the top stays legible. A skill's content is ranked by how immediately the agent needs it:

- **Steps** (in-file, primary) — ordered actions the agent performs
- **Reference** (in-file, secondary) — definitions, facts, examples consulted on demand
- **Reference** (disclosed, behind context pointer) — kept in separate files, loaded only when relevant

**Key patterns:**

- Keep SKILL.md under 500 lines; if you're approaching this limit, add an additional layer of hierarchy along with clear pointers about where the model using the skill should go next to follow up.
- Reference files clearly from SKILL.md with guidance on _when_ to read them — a well-worded context pointer fires reliably; a vague one does not
- For large reference files (>300 lines), include a table of contents
- Inline what every branch/path through the skill needs; push behind pointers what only some paths need

**Domain organization**: When a skill supports multiple domains/frameworks, organize by variant:

```
cloud-deploy/
├── SKILL.md (workflow + selection)
└── references/
    ├── aws.md
    ├── gcp.md
    └── azure.md
```

Claude reads only the relevant reference file.

**Be precise about some things, ambiguous about others.** Once a skill is loaded, it's tempting to over-specify. Resist that for anything that changes faster than the skill gets updated:

- Precise about: the goal (what does "done" look like — give a concrete definition or a way to self-verify), constraints/guardrails that prevent a bad outcome, and context the model can't derive on its own (where data lives, which tool to use, a schema it would otherwise have to guess).
- Ambiguous about: the exact steps (describe the goal and let the model find the files), failure modes (you can't anticipate everything that goes wrong — let the model read the error), and runtime specifics (line numbers, file lists, counts, versions — these go stale fast).

#### Principle of Lack of Surprise

This goes without saying, but skills must not contain malware, exploit code, or any content that could compromise system security. A skill's contents should not surprise the user in their intent if described. Don't go along with requests to create misleading skills or skills designed to facilitate unauthorized access, data exfiltration, or other malicious activities. Things like a "roleplay as an XYZ" are OK though.

#### Writing Patterns

Prefer using the imperative form in instructions.

**Defining output formats** - You can do it like this:

```markdown
## Report structure

ALWAYS use this exact template:

# [Title]

## Executive summary

## Key findings

## Recommendations
```

**Examples pattern** - It's useful to include examples. You can format them like this (but if "Input" and "Output" are in the examples you might want to deviate a little):

```markdown
## Commit message format

**Example 1:**
Input: Added user authentication with JWT tokens
Output: feat(auth): implement JWT-based authentication
```

### Writing Style

Try to explain to the model why things are important in lieu of heavy-handed musty MUSTs. Use theory of mind and try to make the skill general and not super-narrow to specific examples. Start by writing a draft and then look at it with fresh eyes and improve it.

### Test Cases

Every skill needs test cases and assertions. After writing the skill draft, create 2-3 realistic test prompts — the kind of thing a real user would actually say. Share them with the user: "Here are a few test cases I'd like to try. Do these look right, or do you want to add more?" Then run them.

**Design perspective:** Test cases should cover distinct **branches** (different ways the skill can be invoked). This helps verify that your **information hierarchy** and **progressive disclosure** are working — can the agent find the material it needs for each path? Are completion criteria clear and demanding enough to drive thorough **legwork**?

Save test cases to `evals/evals.json`. Don't write assertions yet — just the prompts. You'll draft assertions in the next step while the runs are in progress.

```json
{
  "skill_name": "example-skill",
  "evals": [
    {
      "id": 1,
      "prompt": "User's task prompt",
      "expected_output": "Description of expected result",
      "files": []
    }
  ]
}
```

See `references/schemas.md` for the full schema (including the `assertions` field, which you'll add later).

## Running and evaluating test cases

This section is one continuous sequence — don't stop partway through. Do NOT use `/skill-test` or any other testing skill.

Put results in `<skill-name>-workspace/` as a sibling to the skill directory. Within the workspace, organize results by iteration (`iteration-1/`, `iteration-2/`, etc.) and within that, each test case gets a directory (`eval-0/`, `eval-1/`, etc.). Don't create all of this upfront — just create directories as you go.

### Step 1: Spawn all runs (with-skill AND baseline) in the same turn

For each test case, spawn two subagents in the same turn — one with the skill, one without. This is important: don't spawn the with-skill runs first and then come back for baselines later. Launch everything at once so it all finishes around the same time.

**With-skill run:**

```
Execute this task:
- Skill path: <path-to-skill>
- Task: <eval prompt>
- Input files: <eval files if any, or "none">
- Save outputs to: <workspace>/iteration-<N>/eval-<ID>/with_skill/outputs/
- Outputs to save: <what the user cares about — e.g., "the .docx file", "the final CSV">
```

**Baseline run** (same prompt, but the baseline depends on context):

- **Creating a new skill**: no skill at all. Same prompt, no skill path, save to `without_skill/outputs/`.
- **Improving an existing skill**: the old version. Before editing, snapshot the skill (`cp -r <skill-path> <workspace>/skill-snapshot/`), then point the baseline subagent at the snapshot. Save to `old_skill/outputs/`.

Write an `eval_metadata.json` for each test case (assertions can be empty for now). Give each eval a descriptive name based on what it's testing — not just "eval-0". Use this name for the directory too. If this iteration uses new or modified eval prompts, create these files for each new eval directory — don't assume they carry over from previous iterations.

```json
{
  "eval_id": 0,
  "eval_name": "descriptive-name-here",
  "prompt": "The user's task prompt",
  "assertions": []
}
```

### Step 2: While runs are in progress, draft assertions

Don't just wait for the runs to finish — you can use this time productively. Draft quantitative assertions for each test case and explain them to the user. If assertions already exist in `evals/evals.json`, review them and explain what they check.

Good assertions are objectively verifiable and have descriptive names — they should read clearly in the benchmark viewer so someone glancing at the results immediately understands what each one checks. Even for subjective skills (writing style, design quality), craft assertions that capture your quality standards as measurable criteria. For example, "Output follows brand voice guidelines" can be graded by LLM-as-judge using DeepEval's GEval metric.

Update the `eval_metadata.json` files and `evals/evals.json` with the assertions once drafted. Also explain to the user what they'll see in the viewer — both the qualitative outputs and the quantitative benchmark.

### Step 3: As runs complete, capture timing data

When each subagent task completes, you receive a notification containing `total_tokens` and `duration_ms`. Save this data immediately to `timing.json` in the run directory:

```json
{
  "total_tokens": 84852,
  "duration_ms": 23332,
  "total_duration_seconds": 23.3
}
```

This is the only opportunity to capture this data — it comes through the task notification and isn't persisted elsewhere. Process each notification as it arrives rather than trying to batch them.

### Choosing Your Grading Provider

The DeepEval grader supports three providers. Choose based on your environment:

| Provider    | Use When                                               | Setup                                   |
| ----------- | ------------------------------------------------------ | --------------------------------------- |
| **claude**  | Running in Claude Code, local machine.                 | Claude login locally                    |
| **bedrock** | Using AWS (EC2, Lambda, local AWS credentials via IAM) | AWS_BEDROCK_REGION environment variable |
| **copilot** | Using GitHub Models API                                | GITHUB_TOKEN                            |

**Recommended:** Start with `claude` or `copilot` locally, use `bedrock` for CI/CD.

### Step 4: Grade, aggregate, and launch the viewer

Once all runs are done:

1. **Grade each run** — use the DeepEval grader (`scripts/run_deepeval.py`). It writes `grading.json` using DeepEval's GEval metric (LLM-as-a-judge). The grading.json expectations array must use the fields `text`, `passed`, and `evidence` (not `name`/`met`/`details` or other variants) — the viewer depends on these exact field names.

   Setup (once, from the skill-creator directory):

   ```bash
   uv sync --extra claude    # Claude Code local auth (no API key needed)
   uv sync --extra bedrock   # AWS Bedrock    — set AWS_BEDROCK_REGION; uses IAM default chain
   uv sync --extra copilot   # GitHub Models  — set GITHUB_TOKEN
   ```

   Run (one invocation per run directory; choose one `--provider`):

   ```bash
   # Claude (local claude -p CLI — no API key needed)
   uv run python -m scripts.run_deepeval \
     --eval-dir <workspace>/iteration-N/eval-<ID>/with_skill/run-1 \
     --eval-metadata <workspace>/iteration-N/eval-<ID>/eval_metadata.json \
     --provider claude \
     --verbose

   # AWS Bedrock
   uv run python -m scripts.run_deepeval \
     --eval-dir <workspace>/iteration-N/eval-<ID>/with_skill/run-1 \
     --eval-metadata <workspace>/iteration-N/eval-<ID>/eval_metadata.json \
     --provider bedrock \
     --region us-east-1 \
     --verbose

   # GitHub Models (Copilot)
   uv run python -m scripts.run_deepeval \
     --eval-dir <workspace>/iteration-N/eval-<ID>/with_skill/run-1 \
     --eval-metadata <workspace>/iteration-N/eval-<ID>/eval_metadata.json \
     --provider copilot \
     --verbose
   ```

   The script reads `eval_metadata.json` for assertions, reads `user_notes.md` from the outputs directory, concatenates the transcript and output files (truncated at 40K chars each to avoid context-window overflow), runs one `GEval` call per assertion with up to 2 retries on transient errors, and writes `grading.json` to the run directory.

2. **Aggregate into benchmark** — run the aggregation script from the skill-creator directory:

   ```bash
   python -m scripts.aggregate_benchmark <workspace>/iteration-N --skill-name <name>
   ```

   This produces `benchmark.json` and `benchmark.md` with pass_rate, time, and tokens for each configuration, with mean ± stddev and the delta. If generating benchmark.json manually, see `references/schemas.md` for the exact schema the viewer expects.
   Put each with_skill version before its baseline counterpart.

3. **Do an analyst pass** — read the benchmark data and surface patterns the aggregate stats might hide. See `agents/analyzer.md` (the "Analyzing Benchmark Results" section) for what to look for — things like assertions that always pass regardless of skill (non-discriminating), high-variance evals (possibly flaky), and time/token tradeoffs.

4. **Launch the viewer** with both qualitative outputs and quantitative data:

   ```bash
   nohup python <skill-creator-path>/eval-viewer/generate_review.py \
     <workspace>/iteration-N \
     --skill-name "my-skill" \
     --benchmark <workspace>/iteration-N/benchmark.json \
     > /dev/null 2>&1 &
   VIEWER_PID=$!
   ```

   For iteration 2+, also pass `--previous-workspace <workspace>/iteration-<N-1>`.

   **Cowork / headless environments:** If `webbrowser.open()` is not available or the environment has no display, use `--static <output_path>` to write a standalone HTML file instead of starting a server. Feedback will be downloaded as a `feedback.json` file when the user clicks "Submit All Reviews". After download, copy `feedback.json` into the workspace directory for the next iteration to pick up.

Note: please use generate_review.py to create the viewer; there's no need to write custom HTML.

5. **Tell the user** something like: "I've opened the results in your browser. There are two tabs — 'Outputs' lets you click through each test case and leave feedback, 'Benchmark' shows the quantitative comparison. When you're done, come back here and let me know."

### What the user sees in the viewer

The "Outputs" tab shows one test case at a time:

- **Prompt**: the task that was given
- **Output**: the files the skill produced, rendered inline where possible
- **Previous Output** (iteration 2+): collapsed section showing last iteration's output
- **Formal Grades** (if grading was run): collapsed section showing assertion pass/fail
- **Feedback**: a textbox that auto-saves as they type
- **Previous Feedback** (iteration 2+): their comments from last time, shown below the textbox

The "Benchmark" tab shows the stats summary: pass rates, timing, and token usage for each configuration, with per-eval breakdowns and analyst observations.

Navigation is via prev/next buttons or arrow keys. When done, they click "Submit All Reviews" which saves all feedback to `feedback.json`.

### Step 5: Read the feedback

When the user tells you they're done, read `feedback.json`:

```json
{
  "reviews": [
    {
      "run_id": "eval-0-with_skill",
      "feedback": "the chart is missing axis labels",
      "timestamp": "..."
    },
    { "run_id": "eval-1-with_skill", "feedback": "", "timestamp": "..." },
    {
      "run_id": "eval-2-with_skill",
      "feedback": "perfect, love this",
      "timestamp": "..."
    }
  ],
  "status": "complete"
}
```

Empty feedback means the user thought it was fine. Focus your improvements on the test cases where the user had specific complaints.

Kill the viewer server when you're done with it:

```bash
kill $VIEWER_PID 2>/dev/null
```

---

## Improving the skill

This is the heart of the loop. You've run the test cases, the user has reviewed the results, and now you need to make the skill better based on their feedback.

### Diagnosing Common Failure Modes

Before iterating, check for these patterns using the framework in `references/skill-design-principles.md`. These are the most common issues that degrade skill quality:

**Duplication** — The same meaning in more than one place (same completion criterion stated twice, same rule in two sections). Cost: maintenance burden, wasted tokens, inflated prominence. Fix: Keep each meaning in a **single source of truth**; use **leading words** to anchor behavior without restating it.

**Sediment** — Old content that accumulated because removing felt risky. Cost: readers wade through stale material, harder to maintain **relevance**. Fix: Does each line still bear on what the skill does? Prune ruthlessly. Shorter skills are easier to keep relevant.

**Sprawl** — SKILL.md simply too long, even when every line is live and unique. Cost: readability, maintainability, tokens. Fix: Use **information hierarchy** — push reference behind **context pointers**, split sequences so each path carries only what it needs.

**No-Op** — An instruction that changes nothing because the agent would do it by default. Cost: wasted load. Test: Does this line change behavior versus the agent's default? If not, delete it. Exception: A weak **leading word** is a no-op; strengthen it (_relentless_ instead of _thorough_) or remove it.

**Negation** — Steering by prohibition ("don't be verbose") names the forbidden behavior and makes it _more_ available. Fix: Prompt the positive ("write concise comments") so the banned behavior is never spoken. Use negation only as a hard guardrail paired with the positive target.

**Premature Completion** — Agent ends the current step before done, attention slipping to _being done_ rather than _finishing_. Causes: visible post-completion steps + vague completion criterion. Fix (in order): (1) Sharpen the **completion criterion** first (local, cheap), (2) only if irreducibly fuzzy _and_ you observe the rush, hide post-completion steps by splitting into separate skills.

### How to think about improvements

1. **Generalize from the feedback.** The big picture thing that's happening here is that we're trying to create skills that can be used a million times (maybe literally, maybe even more who knows) across many different prompts. Here you and the user are iterating on only a few examples over and over again because it helps move faster. The user knows these examples in and out and it's quick for them to assess new outputs. But if the skill you and the user are codeveloping works only for those examples, it's useless. Rather than put in fiddly overfitty changes, or oppressively constrictive MUSTs, if there's some stubborn issue, you might try branching out and using different metaphors, or recommending different patterns of working. It's relatively cheap to try and maybe you'll land on something great.

2. **Keep the prompt lean.** Remove things that aren't pulling their weight. Make sure to read the transcripts, not just the final outputs — if it looks like the skill is making the model waste a bunch of time doing things that are unproductive, you can try getting rid of the parts of the skill that are making it do that and seeing what happens.

3. **Explain the why.** Try hard to explain the **why** behind everything you're asking the model to do. Today's LLMs are _smart_. They have good theory of mind and when given a good harness can go beyond rote instructions and really make things happen. Even if the feedback from the user is terse or frustrated, try to actually understand the task and why the user is writing what they wrote, and what they actually wrote, and then transmit this understanding into the instructions. If you find yourself writing ALWAYS or NEVER in all caps, or using super rigid structures, that's a yellow flag — if possible, reframe and explain the reasoning so that the model understands why the thing you're asking for is important. That's a more humane, powerful, and effective approach.

4. **Look for repeated work across test cases.** Read the transcripts from the test runs and notice if the subagents all independently wrote similar helper scripts or took the same multi-step approach to something. If all 3 test cases resulted in the subagent writing a `create_docx.py` or a `build_chart.py`, that's a strong signal the skill should bundle that script. Write it once, put it in `scripts/`, and tell the skill to use it. This saves every future invocation from reinventing the wheel.

This task is pretty important (we are trying to create billions a year in economic value here!) and your thinking time is not the blocker; take your time and really mull things over. I'd suggest writing a draft revision and then looking at it anew and making improvements. Really do your best to get into the head of the user and understand what they want and need.

### The iteration loop

After improving the skill:

1. Apply your improvements to the skill
2. Rerun all test cases into a new `iteration-<N+1>/` directory, including baseline runs. If you're creating a new skill, the baseline is always `without_skill` (no skill) — that stays the same across iterations. If you're improving an existing skill, use your judgment on what makes sense as the baseline: the original version the user came in with, or the previous iteration.
3. Launch the reviewer with `--previous-workspace` pointing at the previous iteration
4. Wait for the user to review and tell you they're done
5. Read the new feedback, improve again, repeat

Keep going until:

- The user says they're happy
- The feedback is all empty (everything looks good)
- You're not making meaningful progress

---

## Advanced: Blind comparison

For situations where you want a more rigorous comparison between two versions of a skill (e.g., the user asks "is the new version actually better?"), there's a blind comparison system. Read `agents/comparator.md` and `agents/analyzer.md` for the details. The basic idea is: give two outputs to an independent agent without telling it which is which, and let it judge quality. Then analyze why the winner won.

This is optional, requires subagents, and most users won't need it. The human review loop is usually sufficient.

---

### Package and Present (only if `present_files` tool is available)

Check whether you have access to the `present_files` tool. If you don't, skip this step. If you do, package the skill and present the .skill file to the user:

```bash
python -m scripts.package_skill <path/to/skill-folder>
```

After packaging, direct the user to the resulting `.skill` file path so they can install it.

---

## Claude.ai-specific instructions

In Claude.ai, the core workflow is the same (draft → test → review → improve → repeat), but because Claude.ai doesn't have subagents, some mechanics change. Here's what to adapt:

**Running test cases**: No subagents means no parallel execution. For each test case, read the skill's SKILL.md, then follow its instructions to accomplish the test prompt yourself. Do them one at a time. This is less rigorous than independent subagents (you wrote the skill and you're also running it, so you have full context), but it's a useful sanity check — and the human review step compensates. Skip the baseline runs — just use the skill to complete the task as requested.

**Reviewing results**: If you can't open a browser (e.g., Claude.ai's VM has no display, or you're on a remote server), skip the browser reviewer entirely. Instead, present results directly in the conversation. For each test case, show the prompt and the output. If the output is a file the user needs to see (like a .docx or .xlsx), save it to the filesystem and tell them where it is so they can download and inspect it. Ask for feedback inline: "How does this look? Anything you'd change?"

**Benchmarking**: Skip the quantitative benchmarking — it relies on baseline comparisons which aren't meaningful without subagents. Focus on qualitative feedback from the user.

**The iteration loop**: Same as before — improve the skill, rerun the test cases, ask for feedback — just without the browser reviewer in the middle. You can still organize results into iteration directories on the filesystem if you have one.

**Blind comparison**: Requires subagents. Skip it.

**Packaging**: The `package_skill.py` script works anywhere with Python and a filesystem. On Claude.ai, you can run it and the user can download the resulting `.skill` file.

**Updating an existing skill**: The user might be asking you to update an existing skill, not create a new one. In this case:

- **Preserve the original name.** Note the skill's directory name and `name` frontmatter field -- use them unchanged. E.g., if the installed skill is `research-helper`, output `research-helper.skill` (not `research-helper-v2`).
- **Copy to a writeable location before editing.** The installed skill path may be read-only. Copy to `/tmp/skill-name/`, edit there, and package from the copy.
- **If packaging manually, stage in `/tmp/` first**, then copy to the output directory -- direct writes may fail due to permissions.

---

## Cowork-Specific Instructions

If you're in Cowork, the main things to know are:

- You have subagents, so the main workflow (spawn test cases in parallel, run baselines, grade, etc.) all works. (However, if you run into severe problems with timeouts, it's OK to run the test prompts in series rather than parallel.)
- You don't have a browser or display, so when generating the eval viewer, use `--static <output_path>` to write a standalone HTML file instead of starting a server. Then proffer a link that the user can click to open the HTML in their browser.
- For whatever reason, the Cowork setup seems to disincline Claude from generating the eval viewer after running the tests, so just to reiterate: whether you're in Cowork or in Claude Code, after running tests, you should always generate the eval viewer for the human to look at examples before revising the skill yourself and trying to make corrections, using `generate_review.py` (not writing your own boutique html code). Sorry in advance but I'm gonna go all caps here: GENERATE THE EVAL VIEWER _BEFORE_ evaluating inputs yourself. You want to get them in front of the human ASAP!
- Feedback works differently: since there's no running server, the viewer's "Submit All Reviews" button will download `feedback.json` as a file. You can then read it from there (you may have to request access first).
- Packaging works — `package_skill.py` just needs Python and a filesystem.
- **Updating an existing skill**: The user might be asking you to update an existing skill, not create a new one. Follow the update guidance in the claude.ai section above.

---

## Reference files

The agents/ directory contains instructions for specialized subagents. Read them when you need to spawn the relevant subagent.

- `agents/comparator.md` — How to do blind A/B comparison between two outputs
- `agents/analyzer.md` — How to analyze why one version beat another

The references/ directory has additional documentation:

- `references/schemas.md` — JSON structures for evals.json, grading.json, etc.
- `references/skill-design-glossary.md` — Definitions of the design vocabulary (predictability, context load, progressive disclosure, failure modes like sediment/sprawl/no-op, etc.). Read when you need the precise meaning of one of these terms.
- `references/skill-design-principles.md` — How that vocabulary maps onto skill-creator's own workflow steps. Read during drafting and iteration to check the skill you're building against these principles.

---

Repeating one more time the core loop here for emphasis:

- Figure out what the skill is about
- Draft or edit the skill
- Run claude-with-access-to-the-skill on test prompts
- With the user, evaluate the outputs:
  - Create benchmark.json and run `eval-viewer/generate_review.py` to help the user review them
  - Run quantitative evals
- Repeat until you and the user are satisfied
- Package the final skill and return it to the user.

Please add steps to your TodoList, if you have such a thing, to make sure you don't forget. If you're in Cowork, please specifically put "Create evals JSON and run `eval-viewer/generate_review.py` so human can review test cases" in your TodoList to make sure it happens.

Good luck!
