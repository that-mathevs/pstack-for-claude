# CLI for Agents

Cursor plugin with a single skill that encodes patterns for **CLIs meant to be driven by coding agents**: non-interactive flags first, layered `--help` with examples, stdin and pipelines, fast actionable errors, idempotency, `--dry-run`, and predictable command structure.

<!-- claude-code:start -->
## Use in Claude Code

The skill doesn't depend on Cursor. To use it in Claude Code, copy `skills/*` into `~/.claude/skills/`. See [the fork README](../README.md#skill-plugins).
<!-- claude-code:end -->

## What it includes

- `cli-for-agents`: design and review guidance for agent-friendly command-line tools

## When to use it

Use when you are building or refactoring a CLI, writing subcommand help, or reviewing whether an existing tool will block agents (interactive prompts, missing examples, ambiguous errors).
