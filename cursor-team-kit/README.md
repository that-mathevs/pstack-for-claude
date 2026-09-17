# Cursor Team Kit plugin

Internal-style workflows for CI, code review, shipping, and test reliability. The kit is designed to be plug and play without requiring third-party service integrations.

<!-- claude-code:start -->
## Use in Claude Code

16 of the 18 skills don't depend on Cursor. To use them in Claude Code, copy the skill folders into `~/.claude/skills/`. Two need changes first: `pr-review-canvas` opens its page in Cursor's built-in browser (use the `claude-in-chrome` skill instead), and `workflow-from-chats` reads Cursor chat history (Claude Code keeps transcripts in `~/.claude/projects/`, and pstack's `/automate-me` does the same job). Both agents use Cursor-only settings (`model: fast`, `is_background`, the `Task` tool), and the rules use Cursor's `.mdc` format, which Claude Code reads from `~/.claude/rules/*.md` instead. Claude Code's `/simplify` replaces `deslop`. See [the fork README](../README.md#skill-plugins).
<!-- claude-code:end -->

## Installation

```bash
/add-plugin cursor-team-kit
```

## Components

### Skills

| Skill | Description |
|:------|:------------|
| `loop-on-ci` | Watch CI runs and iterate on failures until checks pass |
| `review-and-ship` | Run a structured review, commit changes, and open a PR |
| `pr-review-canvas` | Generate an interactive HTML PR walkthrough with annotated, categorized diffs |
| `verify-this` | Prove or disprove claims with baseline/treatment artifacts and a clear verdict |
| `control-cli` | Build or adapt a local harness to drive and profile interactive CLIs or TUIs |
| `control-ui` | Build or adapt a local browser/CDP harness for web or Electron UIs |
| `make-pr-easy-to-review` | Clean noisy PR history, improve descriptions, and add reviewer guidance |
| `run-smoke-tests` | Run Playwright smoke tests and triage failures |
| `fix-ci` | Find failing CI jobs, inspect logs, and apply focused fixes |
| `new-branch-and-pr` | Create a fresh branch, complete work, and open a pull request |
| `get-pr-comments` | Fetch and summarize review comments from the active pull request |
| `check-compiler-errors` | Run compile and type-check commands and report failures |
| `what-did-i-get-done` | Summarize authored commits over a given time period into a concise status update |
| `weekly-review` | Generate a weekly recap of shipped work with bugfix/tech-debt/net-new highlights |
| `fix-merge-conflicts` | Resolve merge conflicts, validate build/tests, and summarize decisions |
| `deslop` | Remove AI-generated code slop and clean up code style |
| `workflow-from-chats` | Extract durable working preferences from chats into skills, rules, or docs |
| `thermo-nuclear-code-quality-review` | Run an unusually strict maintainability review (code-judo, 1k-line rule, spaghetti, boundaries) |

### Agents

| Agent | Description |
|:------|:------------|
| `ci-watcher` | Monitor GitHub Actions runs and return concise pass/fail summaries |
| `thermo-nuclear-code-quality-review` | Task subagent that runs the thermo-nuclear code quality rubric against a diff |

### Rules

| Rule | Description |
|:-----|:------------|
| `typescript-exhaustive-switch` | Require exhaustive switch handling for unions/enums |
| `no-inline-imports` | Keep imports at module top-level for readability and consistency |

## License

MIT
