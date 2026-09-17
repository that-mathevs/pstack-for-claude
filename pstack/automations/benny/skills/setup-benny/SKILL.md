---
name: setup-benny
description: Configure Benny and prepare its triage and repro routines. Use when installing Benny or changing its Slack, tracker, repository, routing, control, schedule, model, or budget settings.
disable-model-invocation: true
---

# Set up Benny

Benny ships as a dormant automation pack inside pstack. The plugin manifest exposes only pstack's normal skill root; this file and the two operational files are not slash skills.

The human enters setup by pointing Claude Code at the pack's `FOR_AGENTS.md`. The bootstrap flow copies the whole pack into the target repository, then reads this file directly at `.claude/automations/benny/skills/setup-benny/SKILL.md`.

Benny needs external configuration and two live Claude Code routines. Routines run in cloud sessions against a checkout of the target repository. Their triggers are scheduled, API, or GitHub events. There is no Slack trigger, so both routines reach Slack through the Slack connector.

Do not create or update a routine until the user explicitly asks. Never put a secret value in plugin files, prompts, or committed configuration.

## 1. Copy the pack and enable shared pstack skills

Do this before asking for Benny configuration and before running `/schedule`.

Ask which repository will run the routines. The source pack is the directory containing `FOR_AGENTS.md`. The destination is `<target-repository>/.claude/automations/benny/`.

Merge the entire source pack into the destination:

1. Create the destination when it is absent.
2. Copy every source file to the same relative path.
3. Preserve destination-only files. Never delete unrelated files during install or refresh.
4. Keep user-owned configuration, feature maps, and routing maps outside the destination. Never overwrite them.
5. When an existing source-managed file differs, inspect the diff and merge without discarding local edits. If ownership is ambiguous, stop and ask before replacing it.
6. Verify that the destination contains `FOR_AGENTS.md`, this setup file, both operational files, their references, and the templates.

If this file is already being read from the target destination, treat the copy as complete and run the same verification before continuing.

Add pstack to the target repository's `.claude/settings.json`. If the file or `.claude` directory does not exist, create it.

Merge these entries into the existing JSON:

```json
{
	"extraKnownMarketplaces": {
		"pstack-for-claude": {
			"source": {
				"source": "github",
				"repo": "that-mathevs/pstack-for-claude"
			}
		}
	},
	"enabledPlugins": {
		"pstack@pstack-for-claude": true
	}
}
```

Preserve every unrelated top-level setting, every other marketplace, and every other plugin entry. If `enabledPlugins["pstack@pstack-for-claude"]` already exists, change only its value. Validate the file after editing it: it must parse as JSON, and the entries must match the shape in the Claude Code settings documentation. Run `claude plugin validate` where it applies. If the documented shape differs from the block above, follow the documentation and tell the user.

Start a fresh Claude Code session rooted in the target repository. Verify that these shared pstack skills resolve from project settings:

- `how`
- `why`
- `tdd`
- `unslop`
- `principle-separate-before-serializing-shared-state`
- `principle-minimize-reader-load`
- `principle-guard-the-context-window`
- `principle-sequence-verifiable-units`
- `principle-fix-root-causes`
- `principle-prove-it-works`

Do not count a skill loaded from the current session, a user-scoped plugin, or `~/.claude/skills/`. The check must show that a fresh session in the target repository receives pstack through project settings.

If project-scoped plugin installation is unavailable or any shared dependency does not resolve, stop and explain the failure.

The Benny files are read directly from `.claude/automations/benny/`. Do not add that directory to a plugin manifest or expect its `SKILL.md` files to appear in the slash-skill list.

Tell the user that `.claude/settings.json`, `.claude/automations/benny/`, and any referenced secret-free configuration must be committed and pushed to the branch the routines check out before either routine is created. Do not commit or push them unless the user asks.

Once this check passes, routine prompts may read the committed operational files by their stable repository-relative paths. They must not embed a plugin cache path or copy the file contents.

## 2. Adapt the configuration

Open these copied examples:

- `../../templates/configuration.example.yaml`
- `../reproduce-and-fix-issues/references/feature-map.example.md`

Create user-owned copies outside `.claude/automations/benny/`. These are configuration files, not pack files. Example locations:

- Project config, such as `.claude/benny/configuration.yaml`
- Project feature map, such as `.claude/benny/feature-map.md`
- Project routing map, such as `.claude/benny/routing.md`
- User config, such as `~/.config/benny/configuration.yaml`
- User feature map, such as `~/.config/benny/feature-map.md`

A routine's cloud session sees only the repository checkout, so user-scoped files under `~/.config/benny/` reach a routine only when their values are paraphrased into its prompt.

Fill one feature-map section for every user-facing feature the routine may reproduce. Keep it at the user point of view. Do not freeze implementation details or current code paths in the map.

Do not edit the copied examples. Pack refreshes may update source-managed files after conflict review, but they must never touch the user-owned copies.

Prefer committed, secret-free files in the target repository when a fresh routine checkout must read them. Otherwise paraphrase the required values into the routine prompt. Reference a repository file only after you confirm with `git` that the file is committed and pushed on the branch the routine checks out.

Use stable repository-relative paths for committed pack and configuration files. Never reference the plugin source directory or a plugin cache path from a routine.

## 3. Fill the required choices

Ask for or confirm:

- Source Slack channel ID
- Optional operations or status channel ID
- Repository URL and default branch
- Triage identity or Slack user ID
- Issue tracker type, team, project, labels, and intake status
- Tracker adapter skill or MCP tools
- Optional routing map path
- Required control skill name
- Required user-facing feature-map path
- Status emoji strings
- Pull request URL format
- Triage schedule as a cron expression
- Repro trigger mode, `schedule` or `api`, and the repro cron expression for `schedule`
- Report lookback window and reports per triage run
- Polling and effort budgets
- Model for triage, repro, code work, and media review

Models are Claude tiers: `fable`, `opus`, `sonnet`, or `haiku`, or `inherit` to use the routine's own model. Use a tier the routine or the `Agent` tool accepts for this account. If a tier is rejected, drop to the next tier down (`fable` → `opus` → `sonnet` → `haiku`) and tell the user.

The Slack connector posts as the Slack account that authorized it. That account is the triage identity. Recommend a dedicated account, because the repro routine trusts any marker from the triage identity, including one a person types by hand from that account.

The source channel, triage identity, repository, tracker adapter, control skill, and feature map must be explicit. Fail setup if any required value stays ambiguous.

Use pstack's `unslop` skill on the final routine names, descriptions, and prompt shims before saving them.

## 4. Check integration capabilities

The triage routine needs:

- Read access to the configured source Slack channel and its threads through the Slack connector
- Thread-reply access in that channel
- Attachment metadata and file download access when reports include media
- Search, read, create, and update access through the configured issue-tracker adapter
- Reaction access when `slack.reaction_action` is configured for claims
- When the repro routine uses its API trigger, the repro routine's fire URL and token as environment variables in the triage routine's environment

The repro routine needs:

- Read access to the source channel and thread
- Thread-reply access in the source channel
- Reaction access on the source root, or an operations channel, so it can claim a report
- Optional post and edit access in the configured operations channel
- Repository read and history access
- A pull request action that can open a draft pull request
- The configured control-adapter skill, working inside the routine's cloud environment

Prefer the configured Slack connector tools for reads, posts, and reactions. The optional `BENNY_SLACK_BOT_TOKEN` may fill a narrow gap such as editing one operations status message or downloading an attachment. Store the value in a secret manager or the routine's environment, not in YAML.

A secret never enters the transcript. When the user must store one, ask them to set it in the routine's environment themselves, or to run something like `! read -s TOKEN && echo "$TOKEN" > path` for a local file.

Copy the repro routine's fire URL and token from its routine page on claude.ai/code. Never guess them.

Do not use undocumented integration endpoints.

Claude Code subagents inherit the session's MCP tools, including the Slack connector. Tell the user that a routine can delegate to workers only through a subagent defined in the target repository whose `tools` field leaves out every Slack connector tool, and leaves out `Bash` when a Slack or fire token is set in the environment. Without one, the coordinator does all the work.

## 5. Prepare the routing map

If the user wants reroutes or owner pings:

1. Copy `../triage-issue-reports/references/routing.example.md` outside `.claude/automations/benny/`.
2. Replace every placeholder with public or organization-local values.
3. Keep owner pings off by default.
4. Allow a ping only for a configured feature owner or a confirmed likely regression author.

If no routing map is configured, triage may classify a report but must not guess a destination or owner.

## 6. Verify the control adapter

Read `../reproduce-and-fix-issues/references/control-adapter.md` and the user's completed feature map.

Confirm that the named skill can, inside the routine's cloud environment:

- Bring up the target app
- Navigate every mapped feature through the real UI
- Exercise mapped states through declared adapter actions
- Inspect state without forcing the result
- Capture screenshots
- Start and stop a recording
- Clean up its processes and temporary data

If any capability is missing, do not create the repro routine. It must fail closed rather than claim a reproduction it did not perform.

## 7. Prepare the routines

Ask whether this is first-time creation or configuration of existing routines.

Read `../../FOR_AGENTS.md` from the copied pack as the primary user-intent source for either path. Use it to understand the two triggers, tools, instructions, outcomes, and shared rules.

### First-time creation

Create one routine at a time.

For each routine:

1. Read the matching copied prompt template as secondary internal source material.
2. Turn `FOR_AGENTS.md`, the finished Benny configuration, and the template intent into a complete natural-language routine prompt.
3. Tell the routine prompt to read and follow its exact committed operational file under `.claude/automations/benny/`.
4. Use the stable repository-relative path, not a plugin source or cache path. Do not copy the operational file contents into the prompt.
5. Confirm with `git` that the copied pack and any referenced configuration files are committed and pushed on the branch the routine checks out.
6. Show the user one draft table: name, repository and branch, trigger and schedule, connectors, environment variable names (never values), model, and prompt.
7. Get the user's explicit approval of that draft.
8. Create the routine with `/schedule`, or have the user create it on the routines page at claude.ai/code from the approved draft.
9. Confirm the routine exists with the approved trigger and prompt before starting the next one.

Give `/schedule` this complete triage intent, filled from configuration:

- Name `benny-triage`.
- Read and follow `.claude/automations/benny/skills/triage-issue-reports/SKILL.md` for every run.
- Run on the configured triage schedule. Poll the configured source Slack channel through the Slack connector for top-level reports that have no Benny verdict yet.
- Read each report's thread and reply only inside it.
- Use the configured issue-tracker integration.
- Classify, inspect evidence, trace cause, dedupe, and create only clear new bugs.
- End one thread-only verdict with the configured `[benny:bug]`, `[benny:performance]`, or `[benny:other]` marker and optional tracker URL.
- When the repro routine uses its API trigger, fire it once per verified bug or performance verdict.
- Never post a source-channel root message.

After the triage routine exists, give `/schedule` this complete repro and fix intent:

- Name `benny-reproduce`.
- Read and follow `.claude/automations/benny/skills/reproduce-and-fix-issues/SKILL.md` for every run.
- Run on the configured repro schedule and poll for triaged threads, or use an API trigger that triage fires.
- Use the configured repository and default branch.
- Read the source thread and reply only inside it.
- Include pull request creation and the configured tracker, control-adapter, and feature-map requirements. Paraphrase mapped user paths and states unless the file is committed and pushed in the same repository.
- Claim each report before work and skip reports that already carry a claim.
- Wait for a trusted triage marker before acting.
- Reproduce the exact symptom twice through the mapped real UI and capture evidence.
- Verify an existing fix without authoring over it.
- Attempt an optional bounded fix only after confirmed repro, then open a draft pull request when proof and checks pass.
- Never post a source-channel root message.

When the repro routine uses its API trigger, finish by having the user copy its fire URL and token from its routine page into the triage routine's environment. Triage skips the fire step until both variables exist.

### Existing routines

Do not create new routines for this path. Do not update an existing routine until the user explicitly asks.

Finish configuration, routing, control-adapter, and feature-map validation. Then give the user this concise checklist.

For the existing triage routine, update:

- Name and description
- Direct instruction to read `.claude/automations/benny/skills/triage-issue-reports/SKILL.md`
- Schedule trigger and source channel
- Slack connector with thread read, reply, and optional reaction access
- Issue-tracker integration
- Repro fire URL and token environment variables when the repro routine uses its API trigger
- Paraphrased triage instructions, thread-only rule, and Benny verdict markers

For the existing repro routine, update:

- Name and description
- Direct instruction to read `.claude/automations/benny/skills/reproduce-and-fix-issues/SKILL.md`
- Schedule or API trigger and source channel
- Repository and default branch
- Slack connector with thread read, reply, and reaction access
- Pull request action
- Tracker, control-adapter, and feature-map requirements
- Paraphrased claim, marker wait, evidence, verification, and bounded-fix instructions

Ask the user to update each existing routine on its routines page at claude.ai/code, or to tell you to make the change with `/schedule`. Do not create replacements or duplicates.

### Creation boundary

Create or change a routine only through `/schedule` or the routines page at claude.ai/code, and only after the user's explicit go. Never call a routines backend or API to create or edit one. Never build a URL that carries draft fields. Never guess a routine URL or token.

Do not point either routine at the real source channel until the thread-safety test passes.

## 8. Test thread safety

Use a test channel or a harmless test report. Run each routine once on demand, from `/schedule` or its routine page, instead of waiting for the schedule.

Before testing, confirm that the target repository's `.claude/settings.json`, `.claude/automations/benny/`, and every referenced secret-free configuration file are committed and pushed on the branch the routines check out. Confirm that both routine prompts point at their exact committed operational files. If any check fails, stop. Tell the user that the routines cannot run on real traffic yet.

Verify:

1. Triage stores the root `thread_ts` and posts exactly one verdict as a reply.
2. The verdict contains one configured marker.
3. Repro accepts the marker only from the configured triage identity.
4. Repro keeps the same immutable source coordinates.
5. No source-channel root message appears.
6. A delegated worker cannot use any Slack write action.
7. Missing coordinates, a deleted parent, or a failed preflight produces no post and no tracker issue.
8. A second triage run and a second repro run on the same test report post nothing new and open no second claim.

Point the routines at normal traffic only after all eight checks pass.
