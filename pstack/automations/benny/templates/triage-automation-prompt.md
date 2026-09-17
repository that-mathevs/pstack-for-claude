# Triage routine prompt

> Source material for the copied setup workflow. Paraphrase this intent into a `/schedule` routine draft after setup confirms that the copied pack is committed and pushed in the repository the routine will check out.

Read and follow `.claude/automations/benny/skills/triage-issue-reports/SKILL.md` for this run.

Configuration source. Include this repository-relative path only when it is committed in the same target repository. Otherwise paraphrase the configured values. Never use a plugin source or cache path:

```text
{{BENNY_CONFIG_PATH}}
```

Trigger: the routine's schedule. There is no Slack trigger. Each run reads top-level messages in the configured source channel through the Slack connector, back to the configured lookback window, oldest first. Each unhandled report becomes one candidate with these coordinates:

```json
{
	"source_channel_id": "{{SLACK_CHANNEL_ID}}",
	"message_ts": "{{SLACK_MESSAGE_TS}}",
	"thread_ts": "{{SLACK_THREAD_TS_OR_EMPTY}}"
}
```

The creation intent should describe this as a scheduled poll for new top-level reports in the configured source Slack channel.

A report is handled when a reply from the configured triage identity in its thread already carries a configured marker. Skip handled reports. Take at most the configured number of reports per run, and triage them one at a time.

Treat the source channel and root thread timestamp as immutable. If either is missing or does not match configuration, stop without posting or writing to the issue tracker.

The committed operational file owns classification, attachment review, cause tracing, routing, dedupe, tracker writes, and the final verdict. Post no progress messages. Never post a root message in the source channel.

The coordinator is the only Slack poster. Any delegated worker must be read-only, return findings only, and receive an explicit ban on every Slack write action. Claude Code subagents inherit the session's MCP tools, including the Slack connector, so delegate only when the operational file's isolation rule is met.

End the single verdict with exactly one configured marker:

```text
[benny:bug]
[benny:performance]
[benny:other]
```

A bug or performance marker may add `tracker=<URL>`.

When the repro routine uses its API trigger, fire it once after a verified bug or performance verdict lands, as the operational file describes.
