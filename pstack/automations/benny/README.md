# benny

benny gives you two claude code routines for slack issue reports. one triages each report. the other reproduces confirmed bugs and may prepare a small draft fix.

the files in this directory are dormant setup and routine sources. they do not appear as slash skills.

routines have scheduled, api, and github triggers, but no slack trigger. so triage runs on a schedule, reads new reports in the issue channel through the slack connector, and skips any report that already carries its verdict marker. repro runs on its own schedule, or fires through its api trigger after triage posts a bug verdict.

## set it up

1. point claude code at [`FOR_AGENTS.md`](./FOR_AGENTS.md) and name the target repository.
2. let setup merge this whole directory into the target at `.claude/automations/benny/`. it must preserve destination-only files and review conflicts instead of overwriting local edits.
3. let setup enable pstack in the target repository's `.claude/settings.json` for shared dependencies:

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

4. keep user-owned configuration outside the copied pack, for example in `.claude/benny/`. adapt [`configuration.example.yaml`](./templates/configuration.example.yaml) and [`feature-map.example.md`](./skills/reproduce-and-fix-issues/references/feature-map.example.md).
5. commit and push `.claude/settings.json`, `.claude/automations/benny/`, and any secret-free configuration before creating either routine.
6. review each routine draft, then create it with `/schedule` or on the routines page at claude.ai/code, or update an existing routine there. then send a harmless test report and verify every source-channel post stays in the original thread.
