---
name: reflect
description: Spawn three parallel review subagents over the active transcript, surface learnings, and route each to a concrete edit on an existing skill. Use when the user says reflect.
disable-model-invocation: true
---

# Reflect

Mine the current conversation for durable learnings, then route them into skill edits.

## When to invoke

Invoke when the user says "reflect" or "/reflect". Skip when the conversation is trivial, off-topic, or already covered by an existing skill the parent followed correctly. One-offs are not learnings.

## Process

### 1. Locate the active transcript

The parent finds its own transcript file before fanning out. Derive the path. `<slug>` is the absolute working directory the session started in, with every character that is not a letter or digit replaced by `-` (`/Users/you/my.proj` becomes `-Users-you-my-proj`). The current session id is `$CLAUDE_CODE_SESSION_ID`. Use only `~/.claude/projects/<slug>/`. Do not glob across `~/.claude/projects/*/`. That crosses workspace boundaries and reads private chats from unrelated projects.

```bash
dir=~/.claude/projects/<slug>
ls -t "$dir/$CLAUDE_CODE_SESSION_ID.jsonl" "$dir/$CLAUDE_CODE_SESSION_ID"/subagents/*.jsonl 2>/dev/null | head -10
# $CLAUDE_CODE_SESSION_ID unset: fall back to the newest sessions in this workspace only
ls -t "$dir"/*.jsonl 2>/dev/null | head -10
```

Two transcript layouts: the session (`<slug>/<session-id>.jsonl`) and its subagents (`<slug>/<session-id>/subagents/agent-<id>.jsonl`). The parent's own conversation is the session file.

Transcript JSONL is an internal format. Parse it defensively: skip lines that fail to parse and do not depend on field order. When the path came from the fallback, confirm it by checking that an early user message contains the conversation's opening user prompt. Take the matching path. If no path resolves, write a tight digest of the session and pass that instead.

### 2. Spawn three reviewers in parallel

One message, three `Agent` calls, `subagent_type: "general-purpose"`, explicit `model:` on each. Reviewers need MCP access for context lookups (tickets, chat threads, observability traces referenced in the transcript). Subagents inherit the session's MCP tools. Each template already tells the reviewer not to modify files or commit.

| Lens | `model` | Prompt template |
|---|---|---|
| Judgment | your configured reflect-judgment model (default `fable`) | `references/judgment-reviewer.md` |
| Tooling | your configured reflect-tooling model (default `opus`) | `references/tooling-reviewer.md` |
| Divergent | your configured reflect-judgment model (default `fable`) | `references/divergent-reviewer.md` |

The configured models come from `~/.claude/rules/pstack-models.md` when present. A role value of `inherit` means omit `model`. If the `Agent` call rejects a `model` value, drop one tier (`fable` → `opus` → `sonnet` → `haiku`) and note the substitution in the summary.

Pass each template verbatim, substituting the transcript path or digest where marked. Reviewers return findings in the `Agent` result.

### 3. Synthesize

One `Agent` call, `subagent_type: "general-purpose"`, using your configured reflect-judgment model (default `fable`). The synthesizer's quality check includes spot-verifying citations, which can require MCP access. Subagents inherit the session's MCP tools. Use `references/synthesizer.md` verbatim, with each reviewer's full output inlined where marked. The synthesizer returns a structured Accepted / Rejected / Backlog list.

### 4. Structural enforcement check

Sanity-check the synthesizer's Accepted list. For any item that would be enforced more reliably by a lint rule, script, metadata flag, or runtime check, move it from Accepted to Backlog. See the **encode-lessons-in-structure** principle skill.

### 5. Apply

Before applying any Accepted edit, present the synthesizer's full Accepted/Rejected/Backlog output to the user and wait for explicit approval. The user picks which subset to apply and may redirect routings. Skill changes affect every future agent in the org. Do not auto-apply.

Backlog items file to whatever devex / backlog tracker your team uses automatically. Only the Accepted list waits for approval.

For each approved Accepted item, follow the Routing field exactly:

- Trivial existing-skill edit (a one-line bullet, a tightened sentence, a stale fact corrected): parent does directly.
- Substantive existing-skill edit (a new section, a new pattern table, more than ~10 lines): hand to the `skill-creator` skill when installed (from `anthropics/skills`) and run its draft / test / iterate loop. Without it, author against the Claude Code skills docs at https://code.claude.com/docs/en/skills.
- `tune description: <skill path>` (the skill exists but didn't trigger when it should have): hand to `skill-creator` and run its description-optimization loop. Without it, tune by hand against the skills docs.
- `new skill via skill-creator: <kebab-name>`: hand creation to `skill-creator` (or the skills docs when it isn't installed). Do not invent the shape ad hoc.

If your environment ships a SKILL.md validator, run it on every touched skill before declaring done. Skip this step if it doesn't.

### 6. Summarize for the user

Short list, no preamble:

- Edits applied: `<skill path>`. What changed, one line each.
- New skills created: `<skill path>`. One line each (rare).
- Backlog filed to the devex tracker: `<issue title>` (`<tags>`). One line each.
- Dropped: one line per rejected finding + reason from the synthesizer.
