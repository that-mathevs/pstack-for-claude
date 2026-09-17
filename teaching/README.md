# Teaching plugin

Teaching workflows: skill mapping, practice plans, and feedback loops.

<!-- claude-code:start -->
## Use in Claude Code

The skills don't depend on Cursor. To use them in Claude Code, copy `skills/*` into `~/.claude/skills/`. "Ask user tool" means Claude Code's `AskUserQuestion`. See [the fork README](../README.md#skill-plugins).
<!-- claude-code:end -->

## Installation

```bash
/add-plugin teaching
```

## Components

### Skills

| Skill | Description |
|:------|:------------|
| `create-learning-path` | Build a personalized learning roadmap with milestones and practice checkpoints |
| `run-learning-retrospective` | Evaluate progress, identify blockers, and adjust the learning plan |

## License

MIT
