# Porting pstack from Cursor to Claude Code

pstack upstream targets Cursor's agent harness. This fork rewrites every harness-specific instruction for Claude Code. This file is the translation table. Apply it when you port a file, and again after every upstream merge.

Last ported from upstream `cursor/plugins` at `e31650e` (pstack 0.15.2). To pick up upstream changes, `git fetch upstream && git merge upstream/main`, then re-port whatever changed under `pstack/`.

Run `scripts/check-cursorisms.sh` after a port or a merge. It exits non-zero while any Cursor-only term remains.

Ground rules for a port edit.

- Change the harness, not the philosophy. Keep poteto's rules, playbook steps, principles, voice, and structure. Rewrite only the tool names, paths, models, and mechanisms that do not exist in Claude Code.
- Name the Claude Code mechanism explicitly. Do not leave a vague "your harness's equivalent".
- When Claude Code has no equivalent, say so in one sentence and give the nearest working substitute. Do not invent a tool, flag, command, or URL.
- Keep the existing lowercase / sentence-case voice of each file.

## Tools and subagents

| Cursor | Claude Code |
|---|---|
| `Task` tool, "Task call", "Task subagent" | the `Agent` tool, "Agent call", "subagent" |
| `subagent_type: generalPurpose` | `subagent_type: "general-purpose"` |
| `readonly: true` on an explorer that only searches | `subagent_type: "Explore"` (read-only, no edit tools) |
| `readonly: true` on an explainer or reviewer that must read whole files | `subagent_type: "general-purpose"` and put "read-only: do not edit, write, or commit anything" in the brief |
| "agent mode (readonly strips MCP)" | drop it. Claude Code subagents inherit the session's MCP tools |
| `run_in_background: true` | drop it. Agent calls run in the background and the parent is notified on completion. Several Agent calls in one message run in parallel |
| `environment: "cloud"` | a local background subagent. Give a writing worker `isolation: "worktree"` so it gets its own git worktree. Use `isolation: "remote"` only when the session offers it |
| `environment: "local"` | a local background subagent (the default) |
| `cloud_base_branch` | put the base branch in the brief. A worktree worker runs `git fetch && git checkout <branch>` first |
| resuming an agent | `SendMessage` to the agent's id or name. A message wakes an idle agent, so the "never resume to check on it" rule still holds |
| `AskQuestion` | `AskUserQuestion` (2 to 4 options, optional multi-select) |
| todo list / todolist | the task list (`TaskCreate`, `TaskUpdate`, `TaskList`) |
| `Shell` | `Bash` |
| `Glob`, `Grep`, `Read` | same names |
| Cursor's image-generation tool | none. Draw a mermaid or ASCII diagram, or an inline SVG in an HTML artifact when the session has the `Artifact` tool |
| the `mcps/` directory, "available-tools map" | the session's tool list. MCP tools are named `mcp__<server>__<tool>`. Deferred tools appear by name in system reminders and load through `ToolSearch`. `claude mcp list` lists configured servers |
| nesting "to depth 3" with "the full Task schema" | subagents can spawn subagents up to 3 layers deep |

Subagent definitions (`agents/*.md`) take `name` (lowercase and hyphens only), `description`, and optionally `tools`, `model`, `permissionMode`, `skills`, `memory`, `isolation`, `maxTurns`. There is no background key, so drop `is_background`.

## Models

Claude Code's `Agent` tool takes `model: "fable" | "opus" | "sonnet" | "haiku"`. Omitting `model` inherits the parent's model. There is no per-subagent reasoning-effort parameter.

Upstream picks models by vendor strength. This fork picks by Claude tier.

| Cursor default | Claude Code default | Used for |
|---|---|---|
| `grok-4.6-fast-xhigh` (fast code model) | `sonnet` | code delegates (feature, refactoring, bug fix, perf, hillclimb), how explorers, why investigators, swarm workers, verification lanes |
| `claude-fable-5-1-thinking-max` (judgment model) | `fable` | judgment and prose, hardest tasks, how explainer, why synthesizer, reflect judgment / divergent / synthesizer |
| `gpt-5.6-sol-max` (tooling model) | `opus` | reflect tooling |
| four-vendor panel (fable, sol, grok, opus) | `fable, opus, sonnet` | arena runners, arena cross-judge pool, architect runners, interrogate reviewers |
| `inherit-parent` or `auto` | `inherit` (omit `model`) | any role |

A panel of Claude tiers is less diverse than a panel of vendors. Say so where a skill relies on "different model families catch different bugs". The fix is different lenses per runner, which the skills already assign. "A different model family" becomes "a different model tier than the parent's".

"Unresolvable slug" fallbacks become: if the `Agent` call rejects the `model` value, drop to the next tier down (`fable` → `opus` → `sonnet` → `haiku`) and note the substitution in the report.

## Configuration

| Cursor | Claude Code |
|---|---|
| `~/.cursor/rules/pstack-models.mdc` with `alwaysApply: true` | `~/.claude/rules/pstack-models.md`. Claude Code loads every file in `~/.claude/rules/` into every session. No frontmatter needed |
| budget ladder of effort tokens (`max`, `xhigh`, `high`, `medium`) | budget ladder of tiers. See `skills/setup-pstack/SKILL.md` |
| `.cursor/skills/<name>/` | `.claude/skills/<name>/` |
| `~/.cursor/skills/` | `~/.claude/skills/` |
| `~/.cursor/plugins/` | `~/.claude/plugins/` |
| `.cursor/settings.json` enabling a plugin | `.claude/settings.json` with `extraKnownMarketplaces` and `enabledPlugins` |
| `AGENTS.md` | `CLAUDE.md`. Also read `AGENTS.md` when a repo has one |
| `.cursor-plugin/plugin.json` | `.claude-plugin/plugin.json` |

## Transcripts and sessions

| Cursor | Claude Code |
|---|---|
| `~/.cursor/projects/<slug>/agent-transcripts/<uuid>/<uuid>.jsonl` | `~/.claude/projects/<slug>/<session-id>.jsonl` |
| subagent transcripts | `~/.claude/projects/<slug>/<session-id>/subagents/agent-<id>.jsonl` |
| "the system prompt names the path" | derive it. `<slug>` is the absolute working directory with every character that is not a letter or digit replaced by `-` (`/Users/you/my.proj` → `-Users-you-my-proj`). The current session id is `$CLAUDE_CODE_SESSION_ID` |
| "do not glob across `~/.cursor/projects/*/`" | "do not glob across `~/.claude/projects/*/`" (same workspace-boundary reason) |
| the agent's "store" directory | `~/.claude/projects/<slug>/` for session-scoped notes, or a repo-local directory the playbook names |
| a Cursor restart | a Claude Code restart, `/clear`, or context compaction |
| cloud agents in the Cursor dashboard | cloud sessions on claude.ai/code |

Transcript JSONL is an internal format. Parse it defensively: skip lines that fail to parse and do not depend on field order.

## Commands, loops, and automation

| Cursor | Claude Code |
|---|---|
| Cursor's `/loop` | Claude Code's `/loop` (`/loop 30m <prompt>`, or `/loop <prompt>` to self-pace). Backed by `CronCreate` and `ScheduleWakeup` |
| a monitored-shell sleep that emits an output-notification sentinel | the `Monitor` tool on a condition, or a `/loop` tick |
| `/goal` | Claude Code's `/goal <condition>` (check with `/goal`, clear with `/goal clear`). Survives `--resume` |
| a cloud-sleeper wake chain | a scheduled routine (`/schedule`) that fires the tick prompt in a cloud session |
| Cursor automations (Slack-triggered) | Claude Code routines (`/schedule`). Triggers are scheduled (cron or one-off), API (HTTP POST with a bearer token), or GitHub events. There is no Slack trigger, so poll the channel on a schedule through the Slack connector |
| a Grok Bot webhook routine (`update_state`, `api2.cursor.sh`) | a routine with an API trigger. `POST .../v1/claude_code/routines/<id>/fire` with `Authorization: Bearer <token>` and an optional JSON body `{"text": "..."}`. Copy the URL and token from the routine page. Never guess them |
| `SendToUser` secret-request card | none. Ask the user to store the secret themselves (for example `! read -s TOKEN && echo "$TOKEN" > path`) so it never enters the transcript |
| Cursor's plan mode | Claude Code's plan mode |
| Cursor's built-in `/babysit` | none. Drop the "not Cursor's built-in" caveat |

## Skills from other plugins

| Cursor | Claude Code |
|---|---|
| Cursor's built-in `create-skill` | the `skill-creator` skill when installed (from `anthropics/skills`), otherwise the Claude Code skills docs at https://code.claude.com/docs/en/skills |
| `/deslop` from `cursor-team-kit` | Claude Code's bundled `/simplify` (reuse, simplification, efficiency cleanups on the diff) |
| `control-ui` from `cursor-team-kit` | the `claude-in-chrome` skill for browser UIs, or a Playwright MCP server. Electron via its CDP port |
| `control-cli` from `cursor-team-kit` | drive the CLI through `Bash`, and a `tmux` session for TUIs. Claude Code's bundled `run` skill launches and drives the project's app |
| Bugbot | PR review bots in general (Cursor Bugbot, Claude Code's `/code-review --comment`, Copilot, CodeRabbit). The triage rules apply to any of them |

## Invoking pstack skills from other pstack skills

Almost every pstack skill sets `disable-model-invocation: true`. In Claude Code that means only the user can run it with `/name`, and its description stays out of context. The model cannot call it through the `Skill` tool.

So when a skill says "run the **how** skill" or "read the leaf **principle-x** skill", the agent reads that skill's `SKILL.md` with `Read` and follows it. Resolve the path in this order.

1. A sibling of the current skill. When a skill loads, Claude Code states its base directory. Sibling skills are at `<base directory>/../<name>/SKILL.md`.
2. `~/.claude/skills/<name>/SKILL.md`, then `.claude/skills/<name>/SKILL.md`.
3. The plugin install: `find ~/.claude/plugins -path '*/pstack/skills/<name>/SKILL.md'`.

A parent that spawns a subagent passes the resolved absolute path in the brief, because a subagent has no skill base directory.

When pstack is installed as a plugin, the user types `/pstack:<name>`. When the skills are copied or symlinked into `~/.claude/skills/`, the user types `/<name>`. Docs write `/<name>`.
