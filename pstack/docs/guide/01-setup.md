# Set up pstack

In this page you install the plugin, pick which models pstack uses, and run your first task. Setup is two install commands plus a short conversation.

## Install the plugin

In a terminal, run:

```bash
claude plugin marketplace add that-mathevs/pstack-for-claude
claude plugin install pstack@pstack-for-claude
```

Claude Code confirms the plugin is installed. Plugin skills carry the plugin's name as a prefix, so you type `/pstack:poteto-mode`, `/pstack:setup-pstack`, and so on.

If you'd rather type the short names, skip the plugin and symlink or copy each directory under `pstack/skills/` into `~/.claude/skills/`. The skills are then `/poteto-mode`, `/setup-pstack`, and so on. This guide writes the short form. With the plugin, add the `pstack:` prefix.

## Pick your models

In a Claude Code session, run:

```text
/setup-pstack
```

[`/setup-pstack`](../../skills/setup-pstack/SKILL.md) asks for a reasoning budget, shows you each role (code delegates, judgment, the review panels), and asks what you want. Answer the questions. It writes `~/.claude/rules/pstack-models.md`, a small rule every pstack skill reads.

Models are Claude tiers: `fable`, `opus`, `sonnet`, and `haiku`. Out of the box, code delegates run on `sonnet`, while judgment, prose, and the hardest tasks run on `fable`, and the review panels run `fable, opus, sonnet`. The budget (`unlimited`, `large`, `medium`, or `small`) moves roles down a ladder of tiers. There is no separate reasoning-effort setting.

You only override what you care about. A role with no line in the rule keeps the skill's default. To restore a default later, delete that role's line, or just run `/setup-pstack` again.

You might be wondering how to keep a role on whatever model your session runs. Set it to `inherit` and pstack omits the subagent `model` field, so the subagent inherits your session's model. `inherit` is not a tier. For a panel role the value is a list, and one subagent runs per entry, so the list length sets the panel size. Setup also configures `swarm workers`, the default model for every `/swarm` worker unless a race names a model for each arm.

## Accept the verification offer, or don't

At the end of setup, `/setup-pstack` looks for a way to prove app behavior in your project, either a `verify-*` skill or an existing harness. If it finds neither, it offers once to generate one with [`/create-verification-skill`](../../skills/create-verification-skill/SKILL.md).

Say yes and it writes `.claude/skills/verify-<app>/`, a project-local skill that teaches agents to drive your app the way a user does. It proves the skill works once before handing it over. Say no and setup moves on. You can run `/create-verification-skill` yourself any time. [Verify and ship](./06-verify-and-ship.md#create-a-project-verification-skill) covers when it earns its place.

After setup, start a new session. Claude Code loads `~/.claude/rules/` when a session starts, so the model rule applies from the next session on.

## Run your first task

Pick something real but small, and describe it the way you'd describe it to a colleague:

```text
/poteto-mode add a --json flag to this command. text output stays byte-identical. verify both.
```

Watch the task list. Its first items are the matched playbook's steps copied in, the Feature playbook for this prompt. If `/poteto-mode` skips a step, the step stays in the list with `skip: <reason>`, so you can see what it chose not to do.

From here you can type normal follow-ups. `/poteto-mode` is sticky. It stays on for the conversation until you opt out by saying so.

Next: [Route work through `/poteto-mode`](./02-poteto-mode.md).
