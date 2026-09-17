---
name: setup-pstack
description: Configure which models pstack uses per role and at what budget. Offers the Claude Code model tiers and writes a rule file Claude Code loads into every session, overriding the skill defaults. Use for /setup-pstack, "configure pstack models", "pstack budget", or changing pstack's model choices.
---

# Setup pstack

Write `~/.claude/rules/pstack-models.md`, a rule that sets pstack's model per role. Claude Code loads every file in `~/.claude/rules/` into every session, so the file is plain markdown with no frontmatter.

## Steps

### 1. Detect available models

Claude Code has no API or CLI that lists the user's entitled models. The `Agent` tool's `model` parameter accepts `fable`, `opus`, `sonnet`, and `haiku`, so those four are the available set. The alias `inherit` is always valid too. It means omit `model`, so the role runs on the parent's model. Never write any other value.

### 2. Load current state

The default role-to-model mapping is the rule shape shown in step 5 below. If `~/.claude/rules/pstack-models.md` already exists, read it and treat its `# budget` line and its role values as the current choices. Otherwise start from those defaults.

### 3. Budget, map, and confirm

**(a) Ask for a budget.** Prefer AskUserQuestion over free text. Offer these four options with these exact labels, and name the current budget when the rule records one.

- `unlimited — fable for judgment`
- `large — fable judgment, opus+sonnet panels`
- `medium — opus judgment, opus+sonnet panels`
- `small — sonnet judgment, haiku code, sonnet+haiku panels`

Claude Code has no per-subagent reasoning-effort parameter, so a budget is a tier ladder, not an effort level.

**(b) Apply it.** Build the working table from this ladder. On a re-run, keep any role the user set by hand: a value that matches no budget column for that role, or `inherit`.

| Roles | unlimited | large | medium | small |
|---|---|---|---|---|
| code: feature, refactoring; bug-fix; perf-issue; hillclimb; how explorer; why investigators; swarm workers | `sonnet` | `sonnet` | `sonnet` | `haiku` |
| judgment: judgment and prose; hardest tasks; how explainer; why synthesizer; reflect judgment, divergent, synthesizer | `fable` | `fable` | `opus` | `sonnet` |
| reflect tooling | `opus` | `opus` | `opus` | `sonnet` |
| panels: arena runners; arena cross-judge pool; architect runners; interrogate reviewers | `fable, opus, sonnet` | `opus, sonnet` | `opus, sonnet` | `sonnet, haiku` |

`unlimited` is the skill defaults. The smaller budgets shrink every panel to two entries, so panels fan out to two subagents.

**(c) Show the roles and confirm.** Show every role with its model. Ask whether to accept as-is or change specific roles. AskUserQuestion takes 2 to 4 options, so ask accept-or-change there, then take the changes as free text naming each role and its new value: `fable`, `opus`, `sonnet`, `haiku`, or `inherit` (the role runs on the parent's model). For panel roles (arena runners, architect runners, interrogate reviewers) the value is a list, and one subagent runs per entry, `inherit` entries included, so the list length sets the count. `arena cross-judge pool` is also a list, but Arena selects one value from it whose tier differs from the parent's model when possible. `swarm workers` is the default model for every worker unless a race or comparison assigns another model per arm.

### 4. Validate

Every value written, and every entry in a panel list, must be `fable`, `opus`, `sonnet`, `haiku`, or `inherit`. If a chosen value is anything else, stop and ask again.

### 5. Write the rule

Write `~/.claude/rules/pstack-models.md` (create `~/.claude/rules/` if it is missing) with no frontmatter, a `# budget` line with the chosen label, and one line per role, using the same labels poteto-mode and the routed skills use. Overwrite the whole file so re-runs stay idempotent. Shape, at the `unlimited` defaults:

```
# pstack model configuration. One line per role. Delete a line to fall back to the skill default.
# Values: fable, opus, sonnet, haiku, or inherit. `inherit` runs the role on the parent's model (omit the Agent `model`). Inherit entries in a panel list still count toward its fan-out.
# budget: unlimited — fable for judgment
feature, refactoring: sonnet
bug-fix: sonnet
perf-issue: sonnet
hillclimb: sonnet
judgment and prose: fable
hardest tasks: fable
how explorer: sonnet
how explainer: fable
why investigators: sonnet
why synthesizer: fable
reflect tooling: opus
reflect judgment, divergent, synthesizer: fable
arena runners: fable, opus, sonnet
arena cross-judge pool: fable, opus, sonnet
swarm workers: sonnet
architect runners: fable, opus, sonnet
interrogate reviewers: fable, opus, sonnet
```

### 6. Confirm

Tell the user the rule was written and that it applies to sessions started after this one. Re-running this skill updates it.

### 7. Offer a verification skill (optional)

Check whether the project has a way to drive the real app for proof (a `verify-*` skill under `.claude/skills/`, or an existing harness). If not, offer once: "want a project-local verification skill, so agents can drive the app the way a user does and prove changes work? I can generate one with /create-verification-skill." On yes, read the **create-verification-skill** skill's `SKILL.md` with `Read` and follow it. It writes `.claude/skills/verify-<app>/`. Resolve its path in this order: `<base directory>/../create-verification-skill/SKILL.md` (the base directory Claude Code stated when this skill loaded), then `~/.claude/skills/create-verification-skill/SKILL.md`, then `.claude/skills/create-verification-skill/SKILL.md`, then `find ~/.claude/plugins -path '*/pstack/skills/create-verification-skill/SKILL.md'`. On no, move on without pushing.
