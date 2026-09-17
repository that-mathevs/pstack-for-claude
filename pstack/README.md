# pstack for Claude Code

pstack is a set of skills for engineering work with an agent, written by [poteto](https://x.com/poteto) (Lauren Tan). This fork ports it from Cursor to [Claude Code](https://code.claude.com). The workflows and principles are poteto's. The fork changes the tool names, models, and file paths so every instruction works in Claude Code.

The skills push the agent to understand code before it changes it, write less code, and prove the result by running it. `/poteto-mode` is the entry point. It matches your task to a playbook and pulls in the other skills when a step needs them.

## Contents

- [Why this fork exists](#why-this-fork-exists)
- [Install](#install)
- [Get started](#get-started)
- [How the skills run](#how-the-skills-run)
- [Skills at a glance](#skills-at-a-glance)
- [The entry point](#the-entry-point)
- [Understand code](#understand-code)
- [Design and review](#design-and-review)
- [Build and verify](#build-and-verify)
- [Write](#write)
- [Configure and extend](#configure-and-extend)
- [Principles](#principles)
- [Subagents](#subagents)
- [Automations](#automations)
- [Not included](#not-included)
- [Update from upstream](#update-from-upstream)

## Why this fork exists

Upstream pstack calls Cursor's tools by name. It spawns subagents with Cursor's `Task` tool, picks models by Cursor slugs such as `grok-4.6-fast-xhigh` and `gpt-5.6-sol-max`, saves settings to `~/.cursor/rules/`, and reads transcripts from `~/.cursor/projects/`. None of those exist in Claude Code.

Claude Code reads the same `SKILL.md` format, so the upstream skills install without an error. Then they fail in ways that are hard to see:

- Subagent calls name models that Claude Code rejects.
- `/setup-pstack` writes a settings file that Claude Code never loads.
- `/recall`, `/reflect`, and `/automate-me` search transcript folders that don't exist.
- Most skills set `disable-model-invocation: true`, so Claude can't start them with its `Skill` tool. A skill that says "run the how skill" has no way to do it.

In each case the agent guesses at what the skill meant. This fork rewrites those instructions to name real Claude Code tools, paths, commands, and models. [`PORTING.md`](./PORTING.md) lists every substitution.

## Install

Install pstack as a Claude Code plugin:

```bash
claude plugin marketplace add that-mathevs/pstack-for-claude
claude plugin install pstack@pstack-for-claude
```

Restart Claude Code. Plugin skills carry the plugin name, so you type `/pstack:poteto-mode`. This README writes the short form, `/poteto-mode`.

To get the short names, clone the repo and link the skills and agents into your user directory instead:

```bash
git clone https://github.com/that-mathevs/pstack-for-claude.git ~/pstack-for-claude
for d in ~/pstack-for-claude/pstack/skills/*/; do ln -s "${d%/}" ~/.claude/skills/; done
for f in ~/pstack-for-claude/pstack/agents/*.md; do ln -s "$f" ~/.claude/agents/; done
```

Use one method, not both. With both, every skill and agent loads twice.

## Get started

1. Run `/setup-pstack`. Pick a budget and accept or change the model for each role.
2. Start real work with `/poteto-mode` and a plain description of the task.

```
/poteto-mode add a --json flag to this command. text output stays byte-identical. verify both.
```

The [pstack guide](./docs/guide/README.md) walks through a first task, from setup to verification and overnight runs.

## How the skills run

Every skill except `/setup-pstack` sets `disable-model-invocation: true`. You start a skill by typing its name. Claude doesn't pick one on its own, and the skill descriptions stay out of your context until you use one.

When one skill needs another, it reads that skill's `SKILL.md` from disk and follows it. `/poteto-mode` does this for the playbooks, the principles, and skills like `/how`.

Skills that fan out spawn subagents with the `Agent` tool. Each role has a default model:

| Role | Default |
|---|---|
| Code delegates (feature, refactoring, bug fix, perf, hillclimb), `/how` explorers, `/why` investigators, `/swarm` workers | `sonnet` |
| Judgment and prose, the hardest changes, `/how` explainer, `/why` synthesizer, `/reflect` reviewers | `fable` |
| `/reflect` tooling reviewer | `opus` |
| Review panels in `/arena`, `/architect`, `/interrogate` | `fable`, `opus`, `sonnet` |

`/setup-pstack` changes these. Upstream's review panels mixed models from four vendors. A panel of three Claude models shares more blind spots, so the panel skills give each reviewer a different starting direction where they can.

## Skills at a glance

| Skill | Use it for |
|---|---|
| [`/poteto-mode`](#poteto-mode) | Any task that needs rigor. Routes to a playbook and the other skills. |
| [`/how`](#how) | How a subsystem works, and where new code should live |
| [`/why`](#why) | Why code is shaped the way it is, with cited evidence |
| [`/teach`](#teach) | A plain explanation you can actually follow |
| [`/recall`](#recall) | Catching up on your own recent work on a topic |
| [`/blast-radius`](#blast-radius) | What a change could break outside its diff |
| [`/architect`](#architect) | Settling types and module shape before writing code |
| [`/arena`](#arena) | Several attempts at one task, merged into the best version |
| [`/interrogate`](#interrogate) | An adversarial review of a diff by several models |
| [`/swarm`](#swarm) | Many parallel workers and one combined report |
| [`/figure-it-out`](#figure-it-out) | Large work that no playbook fits |
| [`/tdd`](#tdd) | A bug fix that starts with a failing test |
| [`/create-verification-skill`](#create-verification-skill) | A project skill that drives your app to prove changes |
| [`/maintain-verification-skill`](#maintain-verification-skill) | Keeping that project skill accurate |
| [`/show-me-your-work`](#show-me-your-work) | A decision log for long or unattended runs |
| [`/no-comments`](#no-comments) | Deleting comments before review, and fixing what they excused |
| [`/unslop`](#unslop) | Removing AI writing patterns |
| [`/technical-writing`](#technical-writing) | Docs, READMEs, PR descriptions, and commit messages |
| [`/bro`](#bro) | The last reply again, in plain words |
| [`/setup-pstack`](#setup-pstack) | Choosing models per role |
| [`/automate-me`](#automate-me) | Your own `-mode` skill, built from how you work |
| [`/reflect`](#reflect) | Turning lessons from a session into skill edits |
| [`/make-bot-ui`](#make-bot-ui) | A web page whose buttons start a Claude Code routine |
| [`/typescript-best-practices`](#typescript-best-practices) | TypeScript type rules with examples |
| [`principle-*`](#principles) | 23 short rules the other skills cite |

## The entry point

### `/poteto-mode`

poteto's working style as one skill. Use it at the start of any task that needs rigor.

When you invoke it, the agent:

1. Matches your request to one of 23 playbooks.
2. Copies that playbook's steps into its task list before any other work. A step it skips stays in the list with a reason.
3. Reads the principle skills that apply and names each one that changed a decision.
4. Spawns code-writing subagents as `poteto-agent`, on `sonnet` for routine code and `fable` for the hardest changes.
5. Writes the reply in short declarative sentences, with each claim labeled as measured, inferred, or a guess.

It keeps going on reversible work and pauses before irreversible actions such as force-pushes, deploys, and data deletion. Once invoked, it stays on for the rest of the session until you tell it to stop.

When no playbook fits, or the work is large enough that you'll step away from it, it routes to `/figure-it-out`.

<details>
<summary>The 23 playbooks</summary>

| Playbook | For |
|---|---|
| [Investigation](./skills/poteto-mode/playbooks/investigation.md) | A read-only question. The answer is a cited explanation, not a code change. |
| [Bug fix](./skills/poteto-mode/playbooks/bug-fix.md) | Reproduce a defect, find the root cause, fix it with runtime evidence. |
| [Perf issue](./skills/poteto-mode/playbooks/perf-issue.md) | Capture a baseline trace, then tie every fix to a measurement. |
| [Hillclimb](./skills/poteto-mode/playbooks/hillclimb.md) | Improve one metric against a target, one change and one measurement at a time. |
| [Runtime forensics](./skills/poteto-mode/playbooks/runtime-forensics.md) | Diagnose a leak, CPU spin, or glitch by instrumenting the live process. |
| [Trace forensics](./skills/poteto-mode/playbooks/trace-forensics.md) | Diagnose from a profile, trace, spindump, or heap snapshot someone already captured. |
| [Feature](./skills/poteto-mode/playbooks/feature.md) | New behavior, designed from a named data shape. |
| [Refactoring](./skills/poteto-mode/playbooks/refactoring.md) | A structure change that keeps behavior identical. |
| [Prototype](./skills/poteto-mode/playbooks/prototype.md) | A throwaway sketch to settle a design question. |
| [Visual parity](./skills/poteto-mode/playbooks/visual-parity.md) | Match two UI implementations, proven by an image diff of zero. |
| [Authoring a skill](./skills/poteto-mode/playbooks/authoring-a-skill.md) | Write or edit a `SKILL.md`. |
| [Eval](./skills/poteto-mode/playbooks/eval.md) | Test a skill or prompt change with blinded runs. |
| [Babysit](./skills/poteto-mode/playbooks/babysit.md) | Drive a PR or stack to merge-ready by resolving conflicts, review threads, and CI. |
| [Shipping](./skills/poteto-mode/playbooks/shipping.md) | Verify each PR in a green stack on its own, then land the verified run from the bottom. |
| [Autonomous run](./skills/poteto-mode/playbooks/autonomous-run.md) | Drive one task to a checkable finish condition without stopping. |
| [Orchestrate](./skills/poteto-mode/playbooks/orchestrate.md) | A multi-day program with many PRs and many subagents under one coordinator session. |
| [Autopilot-full](./skills/poteto-mode/playbooks/autopilot-full.md) | A queue of independent PRs, each run to merged by its own owner. |
| [Autopilot-stack](./skills/poteto-mode/playbooks/autopilot-stack.md) | A queue built and verified as one linear stack that you land yourself. |
| [Session pickup](./skills/poteto-mode/playbooks/session-pickup.md) | Resume another session's unfinished work from its transcript or branch. |
| [Pause safely](./skills/poteto-mode/playbooks/pause-safely.md) | Stop at a clean point and leave a checkpoint a new session can resume from. |
| [Multi-phase plan](./skills/poteto-mode/playbooks/multi-phase-plan.md) | Write a plan for work across phases or stacked PRs, without implementing it. |
| [Worktree cleanup](./skills/poteto-mode/playbooks/worktree-cleanup.md) | Free disk space by removing merged worktrees and old iOS simulators, with safety checks. |
| [Opening a PR](./skills/poteto-mode/playbooks/opening-a-pr.md) | Small ordered commits, `/simplify` and `/no-comments` passes, and a short PR description. Every other playbook ends here. |

</details>

```
/poteto-mode this pr has a subtle bug where the scroll drifts every 750ms even when idle. repro first, then fix and verify.
/poteto-mode i'm going to bed. land the stack even if ci flakes. i want everything merged by morning.
```

## Understand code

### `/how`

Explains how a part of the codebase works, at the depth an engineer needs before changing it. It also answers placement questions such as "which package should own this".

For a narrow question, one `fable` subagent reads the code and writes the explanation. For a subsystem, 2 to 4 `sonnet` explorers each take one part of it in parallel, then a `fable` subagent combines their findings. None of them edit files.

The explanation has five sections, and any that don't apply are dropped: Overview, Key concepts, How it works, Where things live, and Gotchas.

```
/how do we cancel runs? do we have an n+1 when we look up every run to cancel?
```

### `/why`

Finds out why code is shaped the way it is. The answer can be a design decision, an incident, a ticket, or the data behind a threshold.

1. It anchors the question in code with `git blame`, `git log`, and `gh pr view`.
2. It checks your MCP tools and sorts them into seven evidence sources: source control, issue tracker, long-form docs, team chat, infrastructure monitoring, error tracking, and analytics.
3. It spawns one `sonnet` investigator per available source, all in parallel. Source control is always searched.
4. A `fable` synthesizer writes the answer.

The answer keeps what the evidence shows separate from what it only suggests, lists competing explanations, and names every source it searched, including the ones that returned nothing and the ones it couldn't reach. If you plan to change the code, it ends with what to preserve, what to change, what to avoid, and the risks.

```
/why is this feature flag not on yet?
```

### `/teach`

Explains a change or subsystem so you understand it, not just so you've read a summary. It runs `/how` and `/why`, then writes one plain explanation at your pace.

It starts with a short definition and adds detail when you ask. It draws a sequence of small diagrams, each one adding a single part to the last. It doesn't quiz you. It changes no code.

```
/teach help me really understand how the virtualized list decides what to evict
```

### `/recall`

Rebuilds your working context on a topic from your recent sessions, before you start or resume work.

It searches this project's transcripts in `~/.claude/projects/` (the last 7 days by default) with parallel `sonnet` subagents. It never reads another project's sessions. When the topic names a feature or a bug, it also runs `/why` investigators across PRs, tickets, and error tracking. Then it checks the PRs and branches it found with `git` and `gh`.

The brief has four parts:

- **Capsule.** Up to 5 bullets on what the work is and where it stands.
- **Threads.** One line each, tagged `[merged #N]`, `[open PR #N]`, `[in flight <branch>]`, `[verified, uncommitted]`, `[reverted #N]`, or `[planned, not started]`.
- **Problems.** Up to 5 recurring ones, including fixes that shipped and were reverted.
- **Next move.** The single most useful next action.

```
/recall my work on the export queue
```

### `/blast-radius`

Finds what a change could break outside its own diff. Listing callers is not the goal, since grep does that. It looks for breakage that a symbol search misses, such as library internals, teardown order, wire formats, database columns, and feature flags.

Most risky-looking changes are safe because of one fact. The skill finds that fact and proves it by running a script or test against the real code. It reports how far each safety claim got on a five-step scale, from "stated" up to "reproduced in the running app", and marks anything it couldn't run as unproven. For a wide change it asks several models the same question through `/arena`.

The report has five parts: what the change does, the fact it's safe because of, real risks with `file:line`, what it checked and cleared, and the cheapest test to run before merge.

```
/blast-radius of switching the cache eviction to LRU
```

## Design and review

### `/architect`

Settles the shape of new code before implementation. Use it when code crosses a function boundary and the wrong shape would be expensive to undo.

1. **Ground.** Runs `/how` on the systems the code touches, and `/why` if the design changes ownership.
2. **Sketch.** Runs `/arena` with `fable`, `opus`, and `sonnet` runners, each starting from a different design. It requires at least two structurally different candidates and checks each against a list of design red flags, such as shallow modules and pass-through methods.
3. **Agree.** Optional. Say "with checkpoint" and it stops to show you the design first.
4. **Implement.** Fills in the sketch. A deviation from the sketch gets reported, not absorbed.
5. **Scrap.** If the same kind of workaround keeps appearing, it throws the sketch out and designs again.

You get the caller's usage written first, the types and signatures, and a rationale that records which design won and why.

```
/architect design this instrumentation to be high signal with no false positives
```

### `/arena`

Runs several attempts at the same task in parallel, then builds one result from the best parts.

1. It writes a rubric of 3 to 6 criteria before any attempt starts.
2. It spawns one candidate each on `fable`, `opus`, and `sonnet` by default, each in its own git worktree.
3. A judge on a different model than yours scores every candidate against the rubric.
4. The agent reads every candidate in full and picks the one that is easiest to extend as the base.
5. It copies the strongest ideas from the other candidates into the base by hand.
6. It verifies the merged result.

A short note records the base, each copied idea and where it came from, the ideas it rejected, and the verification result. If every candidate reaches the same design, it ships that design as is.

```
/arena take my prompt to the arena verbatim. i want to compare their proposals with yours.
```

### `/interrogate`

An adversarial review of a diff. Three reviewers on `fable`, `opus`, and `sonnet` get the same prompt, rubric, and code-quality checklist. By default it reviews your branch against `main`.

The agent states the intent of the change first, then sorts every finding into Act on, Consider, Noted, or Dismissed, and names which reviewers raised it. Findings raised by two or more reviewers count most. It ends with a map of where the reviewers agreed and disagreed. It changes nothing.

```
/interrogate review this pr.
```

### `/swarm`

Splits work across N parallel workers and returns one report. Workers can each cover a different slice, race on the same brief, or do both. For a race you choose the rule up front: first to pass, rank all, or best of.

Workers run on `sonnet` by default. A worker that writes files gets its own git worktree. Each worker reports `PASS`, `ISSUES`, or `BLOCKED` with evidence, and the agent combines them into one table with the issues, gaps, and dropouts.

```
/swarm check every package under packages/ against its check.sh. one worker per package. one report.
```

### `/figure-it-out`

Designs a playbook for work that no existing playbook fits, such as a large migration or a change you want to trust after stepping away.

1. **Frame.** It sets a done condition that can pass or fail, sizes the work, and picks a rigor level. Decisions that are hard to undo get more rigor.
2. **Design.** It orders small units riskiest first and builds a verification check before the work, with a baseline from before the change. Decisions that are hard to reverse go through `/architect`.
3. **Loop.** Each unit is an experiment. It states what it expects, makes the smallest change, measures, then keeps or reverts. A result is VERIFIED, NOT VERIFIED, or INCONCLUSIVE, and inconclusive doesn't count as a pass.
4. **Trail.** It logs every decision with `/show-me-your-work`.
5. **Verify.** It checks the whole result against the done condition on the real product.

```
/figure-it-out migrate every caller from the synchronous store to the new async one, keeping behavior identical
```

## Build and verify

### `/tdd`

Fixes a bug by writing a failing test first. Use it when you want a regression test or when a cheap local test path is obvious.

It writes the smallest test that would have caught the bug and runs it to confirm it fails for the right reason. Then it fixes the bug, runs the test again, and runs nearby checks. If a good test would need heavy setup or brittle mocks, it says so and uses the closest cheap check instead. It never edits a test to match a wrong implementation.

The report names the test that failed before the fix and passed after it.

```
/tdd the date parser accepts 2026-02-30
```

### `/create-verification-skill`

Generates a project skill at `.claude/skills/verify-<app>/` that tells an agent how to drive your app the way a user does. It works for web apps, CLIs, desktop apps, services, and libraries.

The agent reads the repo to learn how the app starts and how a script can control it, and asks you only what the code can't tell it. The generated skill has these sections:

- **Launch.** The start command and the signal that the app is ready.
- **Doctor.** A read-only health check to run before driving.
- **Drive.** Real selectors and commands from this repo.
- **Evidence.** What to capture as proof, and where to keep it.
- **Cleanup.** How to stop only what the run started while keeping the evidence.

It also writes a feature map for the top 3 to 5 features. Before handing the skill over, it runs the skill once end to end.

### `/maintain-verification-skill`

Keeps a verification skill accurate as the app changes.

One read-only subagent per feature file reads the source and flags where the map no longer matches the code. The agent then drives every feature live in the running app. It fixes wrong descriptions and broken driving steps, and reports real product bugs to you without touching product code.

The run ends as `clean` (no changes), `changed` (one PR of proven fixes), or `blocked` (with the exact reason).

### `/show-me-your-work`

Keeps a decision log for long or unattended runs, so you can check the work when you come back.

The log is one TSV file with one row per decision and six columns: `ts`, `phase`, `decision`, `why`, `evidence`, and `result`. Evidence is a pointer, such as a commit SHA, a PR number, or a `file:line`. `scripts/log.sh` appends a row. The log is append-only. The file stays out of git unless a reviewer needs it.

Before handing back, the agent checks every row against the session transcript and removes anything that didn't happen. Then a subagent on a different model reads the log and the transcript, and the reply ends with an Attention section listing what that reviewer flagged.

To read a log in the terminal:

```bash
column -s$'\t' -t decisions.tsv
```

### `/no-comments`

Deletes comments from a diff before review, then fixes the code the comments were explaining away.

It spawns the `comment-sicko` subagent on your diff against `main`. Comment Sicko deletes every comment except license headers, doc comments on a public API, links to issues, and notes about an external constraint the code can't change. When a comment covers for confusing code, it marks that symbol `MUST KILL`.

The agent checks the report, rejects bad deletions, and fixes each accepted flag at its root cause. It runs `/architect` if a fix needs a new shape. For a comment like "do not remove", it offers a type, test, or lint rule that enforces the constraint instead, and waits for your approval.

## Write

### `/unslop`

Removes AI writing patterns from any text. Other skills apply it to replies, docs, logs, and PR descriptions.

It checks a numbered list of patterns. The list covers AI vocabulary ("delve", "leverage", "pivotal"), em dashes, colons used as connectors, bold labels that repeat the line, filler, hedging, passive voice, metaphors in place of a mechanism, and dropped articles. Rule numbers never change, so other skills can cite a rule by number. The agent scans for the patterns, rewrites without changing the meaning, then asks what still reads as machine-written and fixes that.

```
/unslop this PR description
```

### `/technical-writing`

A writing standard for docs, READMEs, RFCs, PR descriptions, and commit messages. It stacks four sources:

1. **Diátaxis.** Each document is one of tutorial, how-to, reference, or explanation, and doesn't mix them.
2. **Google developer style.** Second person, present tense, commands for instructions, and the condition before the step.
3. **Simplified Technical English.** One instruction per sentence, and one word for each meaning.
4. **Global English.** No sentence that reads two ways, no slashes, and no idioms.

It includes a before-and-after example and an eight-point review checklist, and it applies `/unslop` to everything it touches.

### `/bro`

Restates the agent's last reply in plain, short language with no jargon.

## Configure and extend

### `/setup-pstack`

Chooses which Claude model each pstack role uses. It is the only pstack skill Claude can start on its own.

It asks for a budget:

| Budget | Judgment roles | Code roles | Review panels |
|---|---|---|---|
| `unlimited` | `fable` | `sonnet` | `fable, opus, sonnet` |
| `large` | `fable` | `sonnet` | `opus, sonnet` |
| `medium` | `opus` | `sonnet` | `opus, sonnet` |
| `small` | `sonnet` | `haiku` | `sonnet, haiku` |

Then it shows every role and lets you change any of them to `fable`, `opus`, `sonnet`, `haiku`, or `inherit`. `inherit` uses your session's model. A panel runs one subagent per entry, so a two-entry panel runs two reviewers.

It writes `~/.claude/rules/pstack-models.md`. Claude Code loads that file at the start of every session. Delete a line to return that role to its default. At the end it offers to run `/create-verification-skill` if the project has no verification skill.

### `/automate-me`

Builds a `-mode` skill of your own, such as `jay-mode`, from how you actually work.

1. It mines this project's recent transcripts in parallel slices for repeated preferences in reply style, delegation, verification, and git habits. A pattern has to show up in at least two slices to count.
2. It asks you a few multiple-choice questions to fill the gaps.
3. It drafts `.claude/skills/<handle>-mode/SKILL.md` (or the same path under `~/.claude/skills/`) with `skill-creator`, and edits the prose with `/unslop`.
4. You review drafts until the skill reads like you, then it opens a PR.

The mode skill points at pstack skills and principles rather than copying them. Run it again later to update the skill with evidence from sessions since the last edit.

### `/reflect`

Turns lessons from the current session into edits to existing skills. Run it after a long task.

It finds this session's transcript and gives it to three reviewers in parallel. The judgment reviewer runs on `fable`, the tooling reviewer on `opus`, and a divergent reviewer on `fable` looks for what the other two would miss. A synthesizer sorts their findings into Accepted, Rejected, and Backlog. Any lesson a lint rule or script would enforce better moves to Backlog.

It shows you the full list and applies only the edits you approve. Larger edits and new skills go through `skill-creator`.

### `/make-bot-ui`

Builds a web page whose buttons start a Claude Code routine through the routine's API trigger.

1. You create the routine with `/schedule` or on claude.ai/code and copy its fire URL.
2. You store the routine's token with a `!` command, so the token never enters the chat.
3. A local server holds the token and sends each button press as `{"text": "<json>"}` with a bearer token. The browser never sees the token.
4. The routine's prompt treats that text as data, not as instructions.

The server binds to `0.0.0.0`, so other devices on your Tailscale network can open the page. The skill installs and starts Tailscale if the machine isn't on a tailnet yet.

### `/typescript-best-practices`

TypeScript rules that apply the type-system-discipline principle. The rules cover discriminated unions over bags of optional fields, branded primitives, `unknown` over `any`, schemas before hand-written type guards, no `as` casts before validation, `satisfies`, exhaustive `never` checks, and parsing at boundaries. [`references/patterns.md`](./skills/typescript-best-practices/references/patterns.md) has an example for each rule.

## Principles

23 skills, one rule each. `/poteto-mode` lists them with when each applies, reads the full skill before applying one, and names it in the reply. Other skills cite them by name.

### Core

- [**laziness-protocol**](./skills/principle-laziness-protocol/SKILL.md). Use when refactoring or tempted to add a layer. Prefer deletion, keep call chains flat, and make the smallest change that works.
- [**foundational-thinking**](./skills/principle-foundational-thinking/SKILL.md). Use before writing logic. Get the data structures right first, and isolate any state that concurrent actors could change.
- [**redesign-from-first-principles**](./skills/principle-redesign-from-first-principles/SKILL.md). Use when adding a requirement to an existing design. Design as if the requirement had been there from the start, instead of bolting it on.
- [**attack-the-premise**](./skills/principle-attack-the-premise/SKILL.md). Use when two fixes built on the same assumption have failed the same check. Write that assumption down and test it instead of trying a third fix.
- [**subtract-before-you-add**](./skills/principle-subtract-before-you-add/SKILL.md). Use when planning an addition or rewrite. Remove dead code and redundant checks first, then build on the smaller base.
- [**minimize-reader-load**](./skills/principle-minimize-reader-load/SKILL.md). Use when code is hard to follow. Count the layers between a question and its answer and the state a reader must track, then reduce both.
- [**outcome-oriented-execution**](./skills/principle-outcome-oriented-execution/SKILL.md). Use during planned migrations. Move straight to the target design instead of writing throwaway compatibility code for the steps in between.
- [**experience-first**](./skills/principle-experience-first/SKILL.md). Use for product and scope tradeoffs. Choose what is better for the user over what is easier to build, and ship fewer, polished features.
- [**exhaust-the-design-space**](./skills/principle-exhaust-the-design-space/SKILL.md). Use for a new interaction or architecture with no precedent in the codebase. Build 2 or 3 competing prototypes and compare them before committing.
- [**build-the-lever**](./skills/principle-build-the-lever/SKILL.md). Use for any non-trivial work. Write the codemod, script, or generator that does or checks the work, so a reviewer can rerun it.

### Architecture

- [**model-the-domain**](./skills/principle-model-the-domain/SKILL.md). Use for stateful or heavily branching code. Put the domain in a structure, such as a state machine, typed model, or lookup table, instead of scattered conditionals.
- [**boundary-discipline**](./skills/principle-boundary-discipline/SKILL.md). Use when adding validation or error handling. Validate at system boundaries, trust internal types, and keep business logic in pure functions.
- [**type-system-discipline**](./skills/principle-type-system-discipline/SKILL.md). Use when designing types in any typed language. Make illegal states impossible to construct, brand primitives, parse external data at the edge, and handle every variant.
- [**make-operations-idempotent**](./skills/principle-make-operations-idempotent/SKILL.md). Use for commands and loops that can crash and retry. Running an operation twice, or after a half-finished run, reaches the same end state.
- [**migrate-callers-then-delete-legacy-apis**](./skills/principle-migrate-callers-then-delete-legacy-apis/SKILL.md). Use when replacing an internal API. Move every caller and delete the old API in the same change.
- [**separate-before-serializing-shared-state**](./skills/principle-separate-before-serializing-shared-state/SKILL.md). Use when concurrent actors could write the same file, branch, or key. Remove the sharing first, and add locks only when one shared writer is truly required.

### Verification

- [**prove-it-works**](./skills/principle-prove-it-works/SKILL.md). Use before declaring a task done. Check the real result, such as running the feature or reading the actual value, not a compile or a subagent's summary.
- [**fix-root-causes**](./skills/principle-fix-root-causes/SKILL.md). Use when debugging. Reproduce first, trace the symptom to its cause, and fix it there instead of adding a guard.
- [**sequence-verifiable-units**](./skills/principle-sequence-verifiable-units/SKILL.md). Use for multi-step work and stacked commits. Check each small unit before starting the next, and order commits so a reviewer sees the test fail and then pass.
- [**test-behavior-not-implementation**](./skills/principle-test-behavior-not-implementation/SKILL.md). Use when writing or keeping a test. Call the code the way users do and compare against a literal value. A test that still passes when every import returns `undefined` gets rewritten or deleted.

### Delegation

- [**guard-the-context-window**](./skills/principle-guard-the-context-window/SKILL.md). Use when large outputs start to fill the context. Send bulk reading to subagents and keep only their summaries.
- [**never-block-on-the-human**](./skills/principle-never-block-on-the-human/SKILL.md). Use when tempted to ask "should I do X?" about reversible work. Do it, show the result, and save questions for irreversible actions.

### Meta

- [**encode-lessons-in-structure**](./skills/principle-encode-lessons-in-structure/SKILL.md). Use when you catch yourself writing the same instruction twice. Turn it into a lint rule, check, or script instead of more text.

## Subagents

### `poteto-agent`

The subagent `/poteto-mode` uses for code-writing steps. It reads the full `poteto-mode` skill, including the principles list, before doing any work. A `general-purpose` subagent skips that read, so use `subagent_type: "poteto-agent"` when you spawn one yourself. To give an existing `poteto-agent` more work, use `SendMessage` instead of spawning a second one.

### `comment-sicko`

A comment reviewer that deletes comments and flags the code they excuse. It edits only comments and never touches application code. Start it through `/no-comments`, which checks its work.

## Automations

[`automations/benny/`](./automations/benny/) is an optional pack of two Claude Code routines for a Slack channel where people report bugs. The first routine triages new reports. The second reproduces confirmed bugs in the running app and can prepare a small draft fix. Claude Code routines have no Slack trigger, so the triage routine checks the channel on a schedule through the Slack connector and marks each report it has handled.

These files are not slash commands. To set benny up, point Claude Code at [`FOR_AGENTS.md`](./automations/benny/FOR_AGENTS.md). Setup copies the pack to `.claude/automations/benny/` in your repo and keeps your configuration in `.claude/benny/`.

## Not included

Some steps rely on skills and tools from outside pstack:

- The pre-commit cleanup in the Opening a PR playbook uses Claude Code's bundled `/simplify`.
- UI verification uses the `claude-in-chrome` skill or a Playwright MCP server. CLI and TUI verification runs through `Bash` and `tmux`, or Claude Code's bundled `run` skill.
- Skill authoring uses `skill-creator` from [anthropics/skills](https://github.com/anthropics/skills) when you have it installed, and the [Claude Code skills docs](https://code.claude.com/docs/en/skills) when you don't.

pstack has no planning skill, because poteto treats code as the best spec. Claude Code's plan mode works alongside pstack if you want a plan, and the Multi-phase plan playbook writes one for work that spans several PRs.

## Update from upstream

This fork tracks `cursor/plugins` as the `upstream` remote. To pull in poteto's changes:

```bash
git fetch upstream
git merge upstream/main
pstack/scripts/check-cursorisms.sh
```

The script prints every line that names a Cursor tool, path, or model. Port each one with the tables in [`PORTING.md`](./PORTING.md).

## License

MIT. pstack is by Lauren Tan ([poteto](https://x.com/poteto)). Matthew Ernewein ported it to Claude Code.
