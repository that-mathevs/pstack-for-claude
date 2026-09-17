# Intercom

Cursor plugin that connects agents to [Intercom](https://www.intercom.com) through Intercom's official remote [Model Context Protocol](https://modelcontextprotocol.io/) server.

Search conversations and contacts, look up companies, and list, search, create, or update Help Center articles in the signed-in Intercom workspace.

<!-- claude-code:start -->
## Install in Claude Code

The official Claude Code plugin `intercom` connects to this service. Install it instead of adding the server by hand:

```bash
claude plugin install intercom@claude-plugins-official
```

To add the same MCP server this plugin uses without the official plugin:

```bash
claude mcp add --transport http --scope user \
  intercom \
  https://mcp.intercom.com/mcp
```

- Run `/mcp` inside Claude Code to finish any sign-in and check that the server connected.
- `--scope user` makes the server available in every project. Use `--scope project` to share it through the repo's `.mcp.json`.

<!-- claude-code:end -->

## Install

1. Open **Cursor Settings → Plugins**.
2. Search for **Intercom**.
3. Click **Install**, then complete the Intercom sign-in prompt.

Or run `/add-plugin intercom` in chat.

## MCP

```json
{
  "mcpServers": {
    "intercom": {
      "type": "http",
      "url": "https://mcp.intercom.com/mcp"
    }
  }
}
```

Auth is OAuth 2.0 against Intercom with Dynamic Client Registration (DCR) and PKCE. Cursor registers itself and prompts for Intercom sign-in when the plugin connects — there is no API key or client ID to configure.

## Regions

This plugin points at the US endpoint. Intercom MCP is available for US and EU hosted workspaces; AU is not supported yet.

| Region | Workspace URL | MCP URL |
| --- | --- | --- |
| US | `app.intercom.com` | `https://mcp.intercom.com/mcp` |
| EU | `app.eu.intercom.com` | `https://mcp.eu.intercom.com/mcp` |

If your workspace is EU-hosted, change the `url` in `mcp.json` to `https://mcp.eu.intercom.com/mcp` after install.

## Notes

- Tool calls run as the Intercom user who authorizes the connection and cannot exceed that user's permissions.
- Needed Intercom permissions include reading users/companies and conversations, plus read/write articles for Help Center tools.
- Bearer-token auth is also supported by Intercom's server, but this plugin uses the recommended OAuth flow.

## Docs

- Intercom MCP guide: https://developers.intercom.com/docs/guides/mcp
- Server URL (US): https://mcp.intercom.com/mcp

Logo is Intercom's brand mark (Simple Icons) on a white tile, using Intercom blue `#1F8FFF`.

## License

MIT
