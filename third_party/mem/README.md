# Mem

Cursor plugin that connects agents to [Mem](https://mem.ai) through Mem's official remote [Model Context Protocol](https://modelcontextprotocol.io/) server.

Capture, search, and organize notes and collections in Mem using semantic search, straight from the editor.

<!-- claude-code:start -->
## Install in Claude Code

Add the MCP server this plugin uses:

```bash
claude mcp add --transport http --scope user \
  mem \
  https://mcp.mem.ai/mcp
```

- Run `/mcp` inside Claude Code to finish any sign-in and check that the server connected.
- `--scope user` makes the server available in every project. Use `--scope project` to share it through the repo's `.mcp.json`.

<!-- claude-code:end -->

## Install

1. Open **Cursor Settings → Plugins**.
2. Search for **Mem**.
3. Click **Install**, then complete the Mem sign-in prompt.

Or run `/add-plugin mem` in chat.

## MCP

```json
{
  "mcpServers": {
    "mem": {
      "type": "http",
      "url": "https://mcp.mem.ai/mcp"
    }
  }
}
```

Auth is OAuth. Cursor prompts for Mem sign-in when the plugin connects.

## What agents can do

| Category | Capabilities |
| --- | --- |
| Notes | Get, list, search, create, update, trash, restore, and delete notes |
| Collections | Create and search collections, and add or remove note membership |
| Attachments | Work with attachments and audio recordings |

The hosted runtime is the source of truth for tool names and schemas.

## Notes

- Tool calls run as the Mem user who authorizes the connection.
- Mem enforces usage quotas. Hitting them returns HTTP 429 with a `UsageQuotaExceeded` or `CommercialUsageLimitRejection` payload.
- An unauthenticated request to the endpoint failing is expected — Mem documents this as normal behaviour, not a broken connection.

## Docs

- Mem MCP overview: https://docs.mem.ai/mcp/overview
- Setup: https://docs.mem.ai/mcp/setup
- Supported tools: https://docs.mem.ai/mcp/supported-tools
- Server URL: https://mcp.mem.ai/mcp

Logo is Mem's official mark, from the `mem-labs` GitHub organization.

## License

MIT
