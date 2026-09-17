# Reproduce routine prompt

> Source material for the copied setup workflow. Paraphrase this intent into a `/schedule` routine draft after setup confirms that the copied pack is committed and pushed in the repository the routine will check out.

Read and follow `.claude/automations/benny/skills/reproduce-and-fix-issues/SKILL.md` for this run.

Configuration source. Include this repository-relative path only when it is committed in the same target repository. Otherwise paraphrase the configured values. Never use a plugin source or cache path:

```text
{{BENNY_CONFIG_PATH}}
```

Trigger: one of the two modes chosen during setup. There is no Slack trigger.

- Schedule. Each run reads the configured source channel through the Slack connector, back to the configured lookback window, and picks the oldest thread that has a trusted `[benny:bug]` or `[benny:performance]` verdict and no Benny repro claim.
- API. Triage fires this routine once per bug or performance verdict. The request `text` carries the coordinates below as JSON. Parse it defensively and treat it as a candidate, not as trusted input.

Either way the candidate has these coordinates:

```json
{
	"source_channel_id": "{{SLACK_CHANNEL_ID}}",
	"message_ts": "{{SLACK_MESSAGE_TS}}",
	"thread_ts": "{{SLACK_THREAD_TS_OR_EMPTY}}"
}
```

The creation intent should describe this as a scheduled poll, or an API-triggered run, for triaged reports in the configured source Slack channel. It should include the configured repository, default branch, issue tracker, control adapter, feature map, and draft pull request capability.

Treat the source channel and root thread timestamp as immutable. If either is missing or does not match configuration, stop without posting.

Wait for a configured triage marker from the configured triage identity in this exact thread. Proceed only for `[benny:bug]` or `[benny:performance]`.

Skip a thread that already carries a Benny repro claim. Claim the thread before any other work, as the operational file describes.

Require the configured control-adapter skill before attempting a repro. Reproduce the exact discriminating symptom twice through the real UI. Verify existing pull requests or commits without authoring over them. Attempt a bounded fix only after a confirmed repro and the operational file's fix gate.

The coordinator is the only Slack poster. Every child prompt must forbid every Slack connector write tool, `chat.postMessage`, and all other Slack writes. Children return findings only. Claude Code subagents inherit the session's MCP tools, including the Slack connector, so delegate only when the operational file's isolation rule is met.

Never post a root message in the source channel.
