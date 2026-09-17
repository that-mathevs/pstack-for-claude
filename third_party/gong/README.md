# Gong

Cursor plugin that connects agents to [Gong](https://www.gong.io) through Gong's official hosted [Model Context Protocol](https://modelcontextprotocol.io/) server.

Pull account summaries, deal insights, and call briefs into chat.

<!-- claude-code:start -->
## Install in Claude Code

Add the MCP server this plugin uses:

```bash
claude mcp add --transport http --scope user \
  --client-id <client-id> \
  --client-secret \
  --callback-port 8787 \
  gong \
  https://mcp.gong.io/mcp
```

- Replace `<client-id>` with the client ID of the OAuth app described in Setup. Register `http://localhost:8787/callback` as a redirect URL on that app. `--client-secret` prompts for the secret without echoing it.
- Run `/mcp` inside Claude Code to finish any sign-in and check that the server connected.
- `--scope user` makes the server available in every project. Use `--scope project` to share it through the repo's `.mcp.json`.

<!-- claude-code:end -->

## Install

1. Open **Cursor Settings → Plugins**.
2. Search for **Gong**.
3. Click **Install**, then set the client ID and secret (below) and complete the Gong sign-in prompt.

Or run `/add-plugin gong` in chat.

## MCP

```json
{
  "mcpServers": {
    "gong": {
      "url": "https://mcp.gong.io/mcp",
      "auth": {
        "CLIENT_ID": "${CLIENT_ID}",
        "CLIENT_SECRET": "${CLIENT_SECRET}"
      }
    }
  }
}
```

## Setup

Gong's MCP server uses static OAuth client credentials plus a per-user OAuth login, so an administrator has to register Cursor before anyone can connect.

1. A Gong technical administrator creates an MCP integration under **Company Settings → Ecosystem → API → Integrations** and enables the MCP scope.
2. Register both redirect URIs on that integration:
   - Desktop: `http://localhost:8787/callback`
   - Web and Cloud Agents: `https://www.cursor.com/agents/mcp/oauth/callback`
3. In **Dashboard → Plugins → Configure**, set **Gong Client ID** and **Gong Client Secret** from that integration.
4. Complete the Gong OAuth login when Cursor prompts.

On a team marketplace an admin sets the client ID and secret once for everyone; each member still completes their own Gong OAuth login, so tool calls run with that member's Gong permissions.

## Docs

- Gong MCP server overview: https://help.gong.io/docs/about-gong-mcp-server

## License

MIT
