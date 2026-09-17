# pstack for Claude Code

This repository is a fork of [cursor/plugins](https://github.com/cursor/plugins). It does three things:

1. Ports [pstack](pstack/), poteto's engineering skills, from Cursor to Claude Code.
2. Removes the plugins that can only run inside Cursor or Grok.
3. Documents how to use each remaining plugin from Claude Code.

## pstack

pstack is the only plugin in this fork that installs as a Claude Code plugin:

```bash
claude plugin marketplace add that-mathevs/pstack-for-claude
claude plugin install pstack@pstack-for-claude
```

[pstack/README.md](pstack/README.md) documents every skill and explains [why the port exists](pstack/README.md#why-this-fork-exists). [pstack/PORTING.md](pstack/PORTING.md) lists every Cursor-to-Claude Code change.

## Use the other plugins in Claude Code

Every other plugin here is still upstream's Cursor plugin. Each one has a `.cursor-plugin/plugin.json` manifest and no `.claude-plugin/plugin.json`, so `claude plugin install` can't install it from this fork. You can still use most of them.

### Connectors

58 plugins in [`third_party/`](third_party/) each wrap one MCP server. Claude Code connects to MCP servers directly, so you add the server with `claude mcp add` instead of installing the plugin. Where an official Claude Code plugin or a claude.ai connector covers the same service, the table names it.

Every connector README has an **Install in Claude Code** section with the exact command. [`scripts/claude-code-mcp-docs.py`](scripts/claude-code-mcp-docs.py) generates those sections and this table from each plugin's `mcp.json`. Run it again after merging from upstream, and run it with `--check` to find docs that no longer match.

None of these commands has been tested against every service. Sign-in can fail when a service only accepts redirect URLs that were registered for Cursor. The rows marked "untested" use a client ID that upstream registered for Cursor.

<!-- claude-code-connectors:start -->
| Connector | How to add it in Claude Code | Credentials |
|---|---|---|
| [ahrefs](third_party/ahrefs/README.md#install-in-claude-code) | `claude mcp add` | Sign in through `/mcp` if the server asks |
| [amplemarket](third_party/amplemarket/README.md#install-in-claude-code) | `claude mcp add` | Sign in through `/mcp` if the server asks |
| [ashby](third_party/ashby/README.md#install-in-claude-code) | `claude mcp add` | Sign in through `/mcp` if the server asks |
| [attio](third_party/attio/README.md#install-in-claude-code) | `claude mcp add` | Sign in through `/mcp` if the server asks |
| [brevo](third_party/brevo/README.md#install-in-claude-code) | `claude mcp add` | Set `BREVO_MCP_TOKEN` |
| [brex](third_party/brex/README.md#install-in-claude-code) | `claude mcp add` | Sign in through `/mcp` if the server asks |
| [calendly](third_party/calendly/README.md#install-in-claude-code) | `claude mcp add` | Sign in through `/mcp` if the server asks |
| [circleback](third_party/circleback/README.md#install-in-claude-code) | Official plugin `circleback@claude-plugins-official` | Sign in through `/mcp` if the server asks |
| [clay](third_party/clay/README.md#install-in-claude-code) | `claude mcp add` | Sign in through `/mcp` if the server asks |
| [coda](third_party/coda/README.md#install-in-claude-code) | `claude mcp add` | Sign in through `/mcp` if the server asks |
| [craft](third_party/craft/README.md#install-in-claude-code) | `claude mcp add` | Sign in through `/mcp` if the server asks |
| [customer-io](third_party/customer-io/README.md#install-in-claude-code) | `claude mcp add` | Sign in through `/mcp` if the server asks |
| [daloopa](third_party/daloopa/README.md#install-in-claude-code) | `claude mcp add` | Sign in through `/mcp` if the server asks |
| [docusign](third_party/docusign/README.md#install-in-claude-code) | `claude mcp add` | OAuth app you create |
| [excalidraw](third_party/excalidraw/README.md#install-in-claude-code) | `claude mcp add` | Sign in through `/mcp` if the server asks |
| [fathom](third_party/fathom/README.md#install-in-claude-code) | `claude mcp add` | Sign in through `/mcp` if the server asks |
| [fireflies](third_party/fireflies/README.md#install-in-claude-code) | `claude mcp add` | Sign in through `/mcp` if the server asks |
| [gamma](third_party/gamma/README.md#install-in-claude-code) | `claude mcp add` | Sign in through `/mcp` if the server asks |
| [github](third_party/github/README.md#install-in-claude-code) | Official plugin `github@claude-plugins-official` | Set `GITHUB_PERSONAL_ACCESS_TOKEN` |
| [gmail](third_party/gmail/README.md#install-in-claude-code) | claude.ai connector, or `claude mcp add` | Sign in through `/mcp` if the server asks |
| [godaddy](third_party/godaddy/README.md#install-in-claude-code) | `claude mcp add` | Sign in through `/mcp` if the server asks |
| [gong](third_party/gong/README.md#install-in-claude-code) | `claude mcp add` | OAuth app you create |
| [google-calendar](third_party/google-calendar/README.md#install-in-claude-code) | claude.ai connector, or `claude mcp add` | Sign in through `/mcp` if the server asks |
| [google-cloud-bigquery](third_party/google-cloud-bigquery/README.md#install-in-claude-code) | `claude mcp add` | Sign in through `/mcp` if the server asks |
| [google-drive](third_party/google-drive/README.md#install-in-claude-code) | claude.ai connector, or `claude mcp add` | Sign in through `/mcp` if the server asks |
| [guru](third_party/guru/README.md#install-in-claude-code) | `claude mcp add` | Sign in through `/mcp` if the server asks |
| [hubspot](third_party/hubspot/README.md#install-in-claude-code) | `claude mcp add` | OAuth app you create |
| [hunter](third_party/hunter/README.md#install-in-claude-code) | Official plugin `hunter@claude-plugins-official` | Set `HUNTER_API_KEY` |
| [interactive-brokers](third_party/interactive-brokers/README.md#install-in-claude-code) | `claude mcp add` | Sign in through `/mcp` if the server asks |
| [intercom](third_party/intercom/README.md#install-in-claude-code) | Official plugin `intercom@claude-plugins-official` | Sign in through `/mcp` if the server asks |
| [jotform](third_party/jotform/README.md#install-in-claude-code) | `claude mcp add` | Sign in through `/mcp` if the server asks |
| [juicebox](third_party/juicebox/README.md#install-in-claude-code) | `claude mcp add` | Sign in through `/mcp` if the server asks |
| [klaviyo](third_party/klaviyo/README.md#install-in-claude-code) | `claude mcp add` | Sign in through `/mcp` if the server asks |
| [mailerlite](third_party/mailerlite/README.md#install-in-claude-code) | `claude mcp add` | Sign in through `/mcp` if the server asks |
| [meltwater](third_party/meltwater/README.md#install-in-claude-code) | `claude mcp add` | Sign in through `/mcp` if the server asks |
| [mem](third_party/mem/README.md#install-in-claude-code) | `claude mcp add` | Sign in through `/mcp` if the server asks |
| [mercury](third_party/mercury/README.md#install-in-claude-code) | `claude mcp add` | Sign in through `/mcp` if the server asks |
| [navan](third_party/navan/README.md#install-in-claude-code) | `claude mcp add` | Sign in through `/mcp` if the server asks |
| [otter](third_party/otter/README.md#install-in-claude-code) | `claude mcp add` | Sign in through `/mcp` if the server asks |
| [outreach](third_party/outreach/README.md#install-in-claude-code) | `claude mcp add` | Sign in through `/mcp` if the server asks |
| [playwright](third_party/playwright/README.md#install-in-claude-code) | Official plugin `playwright@claude-plugins-official` | None |
| [profound](third_party/profound/README.md#install-in-claude-code) | `claude mcp add` | Sign in through `/mcp` if the server asks |
| [readwise](third_party/readwise/README.md#install-in-claude-code) | `claude mcp add` | Sign in through `/mcp` if the server asks |
| [salesforce](third_party/salesforce/README.md#install-in-claude-code) | `claude mcp add` | OAuth app you create |
| [semrush](third_party/semrush/README.md#install-in-claude-code) | `claude mcp add` | Sign in through `/mcp` if the server asks |
| [similarweb](third_party/similarweb/README.md#install-in-claude-code) | `claude mcp add` | Set `SIMILARWEB_API_KEY` |
| [smartsheet](third_party/smartsheet/README.md#install-in-claude-code) | `claude mcp add` | Set `SMARTSHEET_API_TOKEN` |
| [sp-global](third_party/sp-global/README.md#install-in-claude-code) | `claude mcp add` | Sign in through `/mcp` if the server asks |
| [todoist](third_party/todoist/README.md#install-in-claude-code) | `claude mcp add` | Sign in through `/mcp` if the server asks |
| [typeform](third_party/typeform/README.md#install-in-claude-code) | `claude mcp add` | Sign in through `/mcp` if the server asks |
| [upwork](third_party/upwork/README.md#install-in-claude-code) | `claude mcp add` | Sign in through `/mcp` if the server asks |
| [webull](third_party/webull/README.md#install-in-claude-code) | `claude mcp add` | Sign in through `/mcp` if the server asks |
| [workable](third_party/workable/README.md#install-in-claude-code) | `claude mcp add` | Sign in through `/mcp` if the server asks |
| [wrike](third_party/wrike/README.md#install-in-claude-code) | `claude mcp add` | Set `WRIKE_ACCESS_TOKEN` |
| [x](third_party/x/README.md#install-in-claude-code) | `claude mcp add` | OAuth with upstream's client ID (untested) |
| [x-ads](third_party/x-ads/README.md#install-in-claude-code) | `claude mcp add` | OAuth with upstream's client ID (untested) |
| [xero](third_party/xero/README.md#install-in-claude-code) | `claude mcp add` | Set `XERO_CLIENT_ID`, `XERO_CLIENT_SECRET` |
| [zoom](third_party/zoom/README.md#install-in-claude-code) | `claude mcp add` | OAuth app you create |
<!-- claude-code-connectors:end -->

`x` also ships two skills. `claude mcp add` doesn't install skills, so copy `third_party/x/skills/*` into `~/.claude/skills/` if you want them. The `x-api-mcp-guide` skill quotes X API credits by Cursor plan, and those numbers don't apply to Claude Code.

### Skill plugins

| Plugin | In Claude Code | Notes |
|---|---|---|
| [grok-voice](grok-voice/) | Works | The skills call xAI's APIs from your app and don't depend on Cursor. Copy `grok-voice/skills/*` into `~/.claude/skills/`. |
| [teaching](teaching/) | Works | Copy `teaching/skills/*` into `~/.claude/skills/`. |
| [cli-for-agent](cli-for-agent/) | Works | Copy `cli-for-agent/skills/*` into `~/.claude/skills/`. |
| [cursor-team-kit](cursor-team-kit/) | Mostly works | 16 of 18 skills don't depend on Cursor. `pr-review-canvas` opens its page in Cursor's built-in browser, and `workflow-from-chats` reads Cursor chat history. Both agents use Cursor-only settings (`model: fast`, `is_background`, the `Task` tool). The two rules use Cursor's `.mdc` format. pstack already maps `deslop` to Claude Code's `/simplify` and `control-ui` to `claude-in-chrome`. |
| [thermos](thermos/) | Needs a port | Its review subagents spawn helpers with Cursor's `Task` tool and load skills that the model can't start in Claude Code. Claude Code's `/code-review` and `/security-review`, and the official `pr-review-toolkit` and `claude-security` plugins, cover the same reviews. |
| [agent-compatibility](agent-compatibility/) | Needs a port | Its four review agents set `model: fast` and `readonly: true`, which Claude Code doesn't support. The `npx agent-compatibility` scanner itself runs anywhere. |

## Removed from this fork

These plugins depended on a Cursor or Grok service, Cursor's Canvas view, Cursor cloud agents, or Cursor's hook events. None of those exist in Claude Code. Porting them would mean rebuilding what each plugin is, so this fork deletes them and points to the Claude Code option instead.

| Plugin | What it did | Why it can't run in Claude Code | Claude Code alternative |
|---|---|---|---|
| `teams` | Microsoft Teams chats and channels | Connected through Cursor's server at `api.cursor.com/rest-mcp/teams/mcp`, which signs in with your Cursor account | Claude's [Microsoft 365 connector](https://claude.com/docs/connectors/microsoft/365) |
| `outlook` | Outlook mail | Cursor's server at `api.cursor.com/rest-mcp/outlook/mcp` | Claude's Microsoft 365 connector |
| `outlook-calendar` | Outlook calendar | Cursor's server at `api.cursor.com/rest-mcp/outlook-calendar/mcp` | Claude's Microsoft 365 connector |
| `onedrive` | OneDrive files | Cursor's server at `api.cursor.com/rest-mcp/onedrive/mcp` | Claude's Microsoft 365 connector |
| `sharepoint` | SharePoint sites and files | Cursor's server at `api.cursor.com/rest-mcp/sharepoint/mcp` | Claude's Microsoft 365 connector |
| `finance` | Spending, balances, and investments | Grok's connector gateway adds your Grok account's credentials, and upstream marks it Grok Bot only | None |
| `docs-canvas` | Documentation rendered as a Cursor Canvas (a placeholder upstream) | Needs Cursor's Canvas view | None. pstack's `/how` and `/technical-writing` cover walkthroughs and docs. |
| `pr-review-canvas` | PR diffs rendered as a Cursor Canvas | Needs Cursor's Canvas view | Claude Code's `/code-review`, or the official `pr-review-toolkit` plugin |
| `cursor-sdk` | Apps and scripts built on the Cursor TypeScript SDK | It is Cursor's own SDK | The Claude Agent SDK, with the official `agent-sdk-dev` plugin |
| `orchestrate` | Large tasks spread across Cursor cloud agents | Calls the Cursor cloud agent API with `CURSOR_API_KEY` | pstack's Orchestrate playbook and `/swarm` |
| `advisor` | A second model (Grok 4.6 by default) consulted at checkpoints | Cursor hook events (`afterFileEdit`, `afterAgentResponse`) and state in `.cursor/advisor/` | pstack's `/interrogate` for a review by several models |
| `ralph-loop` | The Ralph Wiggum loop, repeating one prompt until done | A Cursor `stop` hook and state in `.cursor/ralph/` | The official `ralph-loop` plugin |
| `continual-learning` | Kept `AGENTS.md` up to date from chat history | A Cursor `stop` hook that reads Cursor transcripts | pstack's `/reflect`, or the official `claude-md-management` plugin |
| `create-plugin` | Scaffolded and reviewed Cursor plugins | Writes `.cursor-plugin/` manifests and `.mdc` rules to `~/.cursor/plugins/local/` | The official `plugin-dev` plugin, plus `claude plugin init` and `claude plugin validate` |

Claude's Microsoft 365 connector covers Outlook, Teams, SharePoint, and OneDrive in one place. Turn it on at [claude.ai/customize/connectors](https://claude.ai/customize/connectors). Claude Code loads claude.ai connectors automatically when you sign in with a claude.ai subscription. It needs a work or school Microsoft account, and on Team and Enterprise plans an organization owner must enable it first.

Install an official plugin with `claude plugin install <name>@claude-plugins-official`.

An upstream merge that changes a removed plugin stops with a modify/delete conflict. Resolve it by deleting the plugin again with `git rm -r <plugin>`, then add a row here if upstream added a new Cursor-only plugin.

---

*Upstream's README follows. Plugins removed above are no longer listed.*

# Cursor plugins

Official Cursor plugins for popular developer tools, frameworks, and SaaS products. Each plugin is a standalone directory at the repository root with its own `.cursor-plugin/plugin.json` manifest.

## Plugins

| `name` | Plugin | Author | Category | `description` (from marketplace) |
|:-------|:-------|:-------|:---------|:-------------------------------------|
| `teaching` | [Teaching](teaching/) | Cursor | Utilities | Skill mapping, practice plans, and learning retrospectives. |
| `cursor-team-kit` | [Cursor Team Kit](cursor-team-kit/) | Eric Zakariasson | Developer Tools | Internal team workflows for CI, code review, shipping, local automation, and verification. |
| `thermos` | [Thermos](thermos/) | Cursor | Developer Tools | Thermo-nuclear branch review: deep security/correctness audits, harsh code-quality rubrics, parallel subagents, thermos orchestration, and optional merge-ready PR flows. |
| `agent-compatibility` | [Agent Compatibility](agent-compatibility/) | Cursor | Developer Tools | CLI-backed repo compatibility scans plus agents that audit startup, validation, and docs against reality. |
| `cli-for-agent` | [CLI for Agents](cli-for-agent/) | Eric Zakariasson | Developer Tools | Patterns for designing CLIs that coding agents can run reliably: flags, help with examples, pipelines, errors, idempotency, dry-run. |
| `pstack` | [pstack](pstack/) | Lauren Tan | Developer Tools | if you want to go fast, go deep first. pstack helps you write less, but higher quality code. rigorous agent workflows you can parallelize with confidence. |
| `grok-voice` | [Grok Voice](grok-voice/) | Eric Zakariasson | Developer Tools | Add Grok voice to an app: realtime speech-to-speech, speech-to-text dictation, text-to-speech read-aloud, and a log-driven fix loop for voice sessions. |
| `gmail` | [Gmail](third_party/gmail/) | Cursor | Productivity | Search, read, draft, and manage email. |
| `google-drive` | [Google Drive](third_party/google-drive/) | Cursor | Productivity | Search, read, create, and share files. |
| `google-calendar` | [Google Calendar](third_party/google-calendar/) | Cursor | Productivity | Search events and schedule meetings. |
| `gong` | [Gong](third_party/gong/) | Cursor | Integrations | Pull account summaries, deal insights, and call briefs. |
| `salesforce` | [Salesforce](third_party/salesforce/) | Cursor | Integrations | Query, create, and update records in your org. |
| `playwright` | [Playwright](third_party/playwright/) | Cursor | Integrations | Navigate, click, screenshot, and test in a real browser. |
| `github` | [GitHub](third_party/github/) | Cursor | Integrations | Manage repos, issues, pull requests, and Actions. |
| `ashby` | [Ashby](third_party/ashby/) | Cursor | Integrations | Search candidates, prep interviews, and manage pipeline tasks. |
| `hubspot` | [HubSpot](third_party/hubspot/) | Cursor | Integrations | Search and update contacts, companies, deals, and tickets. |
| `intercom` | [Intercom](third_party/intercom/) | Cursor | Integrations | Search conversations, contacts, and Help Center articles. |
| `zoom` | [Zoom](third_party/zoom/) | Cursor | Integrations | Search meetings, pull transcripts, and work with Zoom Docs. |
| `x` | [X](third_party/x/) | Cursor | Integrations | Search posts, read timelines, pull trends, and manage bookmarks. |
| `clay` | [Clay](third_party/clay/) | Cursor | Integrations | Enrich people and companies, run AI research agents. |
| `circleback` | [Circleback](third_party/circleback/) | Cursor | Integrations | Search meetings, transcripts, action items, and emails. |
| `docusign` | [Docusign](third_party/docusign/) | Cursor | Integrations | Manage envelopes, templates, workflows, and agreements. |
| `navan` | [Navan](third_party/navan/) | Cursor | Integrations | Query expenses, travel bookings, policies, and cards. |
| `profound` | [Profound](third_party/profound/) | Cursor | Integrations | Track AI visibility, sentiment, and citations. |
| `juicebox` | [Juicebox](third_party/juicebox/) | Cursor | Integrations | Query recruiting analytics, shortlists, and sourcing agents. |
| `outreach` | [Outreach](third_party/outreach/) | Cursor | Integrations | Search sequences, prospects, and Kaia meetings. |
| `amplemarket` | [Amplemarket](third_party/amplemarket/) | Cursor | Integrations | Search people and companies, enrich leads, run sequences. |
| `klaviyo` | [Klaviyo](third_party/klaviyo/) | Cursor | Integrations | Manage profiles, segments, campaigns, and flows. |
| `customer-io` | [Customer.io](third_party/customer-io/) | Cursor | Integrations | Build campaigns, manage segments, and query people. |
| `mailerlite` | [MailerLite](third_party/mailerlite/) | Cursor | Integrations | Manage subscribers, groups, campaigns, and automations. |
| `brevo` | [Brevo](third_party/brevo/) | Cursor | Integrations | Manage contacts, email and SMS campaigns, and CRM deals. |
| `typeform` | [Typeform](third_party/typeform/) | Cursor | Integrations | Build forms, analyze responses, and manage contacts. |
| `jotform` | [Jotform](third_party/jotform/) | Cursor | Integrations | Create and edit forms, then read submissions. |
| `semrush` | [Semrush](third_party/semrush/) | Cursor | Integrations | Research keywords, backlinks, traffic, and competitors. |
| `ahrefs` | [Ahrefs](third_party/ahrefs/) | Cursor | Integrations | Research keywords, backlinks, rankings, and site health. |
| `godaddy` | [GoDaddy](third_party/godaddy/) | Cursor | Integrations | Brainstorm domain names and check availability. |
| `upwork` | [Upwork](third_party/upwork/) | Cursor | Integrations | Search talent, post jobs, and manage contracts. |
| `workable` | [Workable](third_party/workable/) | Cursor | Integrations | Search candidates, move pipelines, and manage HR records. |
| `brex` | [Brex](third_party/brex/) | Cursor | Integrations | Query expenses, receipts, bills, cards, and travel. |
| `mercury` | [Mercury](third_party/mercury/) | Cursor | Integrations | Read balances, transactions, statements, and cards. |
| `todoist` | [Todoist](third_party/todoist/) | Cursor | Integrations | Create, find, and complete tasks and projects. |
| `calendly` | [Calendly](third_party/calendly/) | Cursor | Integrations | Check availability and book, cancel, or reschedule. |
| `smartsheet` | [Smartsheet](third_party/smartsheet/) | Cursor | Integrations | Query and update sheets, rows, and workspaces. |
| `wrike` | [Wrike](third_party/wrike/) | Cursor | Integrations | Search projects, create tasks, and post comments. |
| `coda` | [Coda](third_party/coda/) | Cursor | Integrations | Search docs, read pages, and update tables. |
| `guru` | [Guru](third_party/guru/) | Cursor | Integrations | Search company knowledge and draft verified answers. |
| `fireflies` | [Fireflies](third_party/fireflies/) | Cursor | Integrations | Search meeting transcripts, summaries, and action items. |
| `otter` | [Otter.ai](third_party/otter/) | Cursor | Integrations | Search meeting history and pull full transcripts. |
| `fathom` | [Fathom](third_party/fathom/) | Cursor | Integrations | Search meetings and pull transcripts and summaries. |
| `craft` | [Craft](third_party/craft/) | Cursor | Integrations | Search, create, and update documents and daily notes. |
| `mem` | [Mem](third_party/mem/) | Cursor | Integrations | Capture, search, and organize notes and collections. |
| `readwise` | [Readwise](third_party/readwise/) | Cursor | Integrations | Search highlights and Reader documents, save articles. |
| `similarweb` | [Similarweb](third_party/similarweb/) | Cursor | Integrations | Analyze website traffic, audiences, and competitors. |
| `xero` | [Xero](third_party/xero/) | Cursor | Integrations | Read and write invoices, contacts, reports, and payroll. |
| `x-ads` | [X Ads](third_party/x-ads/) | Cursor | Integrations | Manage ad campaigns, create ads, track conversions, and pull performance stats. |
| `attio` | [Attio](third_party/attio/) | Cursor | Integrations | Search and update CRM records, lists, notes, and tasks. |
| `hunter` | [Hunter](third_party/hunter/) | Cursor | Integrations | Find and verify emails, discover companies, and save leads. |
| `gamma` | [Gamma](third_party/gamma/) | Cursor | Integrations | Generate presentations, documents, and webpages. |
| `webull` | [Webull](third_party/webull/) | Cursor | Integrations | View accounts, positions, orders, watchlists, and market data. |
| `sp-global` | [S&P Global](third_party/sp-global/) | Cursor | Integrations | Query S&P Capital IQ financials, prices, and transcripts. |
| `interactive-brokers` | [Interactive Brokers](third_party/interactive-brokers/) | Cursor | Integrations | Review positions, balances, P&L, and draft trade instructions. |
| `meltwater` | [Meltwater](third_party/meltwater/) | Cursor | Integrations | Search media and social mentions and pull analytics. |
| `daloopa` | [Daloopa](third_party/daloopa/) | Cursor | Integrations | Pull source-linked fundamentals, KPIs, filings, and prices. |
| `excalidraw` | [Excalidraw](third_party/excalidraw/) | Cursor | Integrations | Draw and export hand-drawn diagrams from chat. |
| `google-cloud-bigquery` | [Google Cloud BigQuery](third_party/google-cloud-bigquery/) | Cursor | Integrations | Explore datasets and tables and run SQL queries. |
Author values match each plugin’s `plugin.json` `author.name` (Cursor lists `plugins@cursor.com` in the manifest).

## Repository structure

This is a multi-plugin marketplace repository. The root `.cursor-plugin/marketplace.json` lists all plugins, and each plugin has its own manifest:

```
plugins/
├── .cursor-plugin/
│   └── marketplace.json       # Marketplace manifest (lists all plugins)
├── plugin-name/
│   ├── .cursor-plugin/
│   │   └── plugin.json        # Per-plugin manifest
│   ├── skills/                # Agent skills (SKILL.md with frontmatter)
│   ├── rules/                 # Cursor rules (.mdc files)
│   ├── mcp.json               # MCP server definitions
│   ├── README.md
│   ├── CHANGELOG.md
│   └── LICENSE
└── ...
```

## License

MIT
