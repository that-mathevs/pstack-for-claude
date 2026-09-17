#!/usr/bin/env python3
"""Writes the "Install in Claude Code" section of every third_party connector README.

Reads each connector's mcp.json and turns it into `claude mcp add` commands.
Rerun after merging upstream. The section sits between marker comments, so
reruns replace it instead of appending.

Usage: python3 scripts/claude-code-mcp-docs.py [--check]
"""

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
START = "<!-- claude-code:start -->"
END = "<!-- claude-code:end -->"
CALLBACK_PORT = 8787

# Official Claude Code plugins in the claude-plugins-official marketplace that
# connect to the same service.
OFFICIAL_PLUGINS = {
    "circleback": "circleback",
    "github": "github",
    "hunter": "hunter",
    "intercom": "intercom",
    "playwright": "playwright",
}

# Connectors that also ship as claude.ai connectors. Claude Code loads these
# automatically when you sign in with a claude.ai subscription.
CLAUDE_AI_CONNECTORS = {
    "gmail": "Gmail",
    "google-calendar": "Google Calendar",
    "google-drive": "Google Drive",
}

VAR = re.compile(r"\$\{([A-Z0-9_]+)\}")


def env_vars(value):
    return VAR.findall(json.dumps(value))


def http_command(name, server):
    url = server["url"]
    parts = ["claude mcp add --transport http --scope user"]
    auth = server.get("auth") or {}
    notes = []
    if "CLIENT_ID" in auth:
        client_id = auth["CLIENT_ID"]
        own_app = bool(VAR.fullmatch(client_id))
        parts.append("--client-id " + ("<client-id>" if own_app else client_id))
        if "CLIENT_SECRET" in auth:
            parts.append("--client-secret")
        parts.append(f"--callback-port {CALLBACK_PORT}")
        if own_app:
            notes.append(
                "Replace `<client-id>` with the client ID of the OAuth app described in Setup. "
                f"Register `http://localhost:{CALLBACK_PORT}/callback` as a redirect URL on that app."
                + (" `--client-secret` prompts for the secret without echoing it." if "CLIENT_SECRET" in auth else "")
            )
        else:
            notes.append(
                "The client ID is the one upstream ships for Cursor. "
                f"The command uses port {CALLBACK_PORT} to match Cursor's desktop redirect, "
                "but nobody has tested this sign-in from Claude Code."
            )
        if auth.get("scopes"):
            notes.append(
                "`claude mcp add` has no flag for OAuth scopes, so the server's defaults apply: "
                + ", ".join(f"`{s}`" for s in auth["scopes"][:6])
                + (" and more." if len(auth["scopes"]) > 6 else ".")
            )
    for header, value in (server.get("headers") or {}).items():
        parts.append(f'--header "{header}: {value}"')
    parts.append(name)
    if VAR.fullmatch(url):
        parts.append("<server-url>")
        notes.append("Replace `<server-url>` with your own server URL, as Setup describes.")
    else:
        parts.append(url)
    for var in env_vars(server.get("headers") or {}):
        notes.append(f"Export `{var}` before you run the command. Your shell fills in the value, and Claude Code saves it in `~/.claude.json`.")
    return " \\\n  ".join(parts), notes


def stdio_command(name, server):
    parts = ["claude mcp add --scope user"]
    notes = []
    for key, value in (server.get("env") or {}).items():
        parts.append(f"-e {key}={value}")
        for var in env_vars(value):
            notes.append(f"Export `{var}` before you run the command. Your shell fills in the value, and Claude Code saves it in `~/.claude.json`.")
    parts.append(name)
    parts.append("-- " + " ".join([server["command"], *server.get("args", [])]))
    return " \\\n  ".join(parts), notes


def section(name, servers):
    lines = [START, "## Install in Claude Code", ""]
    if name in OFFICIAL_PLUGINS:
        plugin = OFFICIAL_PLUGINS[name]
        lines += [
            f"The official Claude Code plugin `{plugin}` connects to this service. Install it instead of adding the server by hand:",
            "",
            "```bash",
            f"claude plugin install {plugin}@claude-plugins-official",
            "```",
            "",
            "To add the same MCP server this plugin uses without the official plugin:",
            "",
        ]
    elif name in CLAUDE_AI_CONNECTORS:
        lines += [
            f"Claude has a {CLAUDE_AI_CONNECTORS[name]} connector. Turn it on at [claude.ai/customize/connectors](https://claude.ai/customize/connectors). "
            "Claude Code loads claude.ai connectors automatically when you sign in with a claude.ai subscription.",
            "",
            "To add the MCP server this plugin uses instead:",
            "",
        ]
    else:
        lines += ["Add the MCP server this plugin uses:", ""]
    notes = []
    for server_name, server in servers.items():
        if "url" in server:
            command, extra = http_command(server_name, server)
        else:
            command, extra = stdio_command(server_name, server)
        lines += ["```bash", command, "```", ""]
        notes += extra
    notes.append("Run `/mcp` inside Claude Code to finish any sign-in and check that the server connected.")
    notes.append("`--scope user` makes the server available in every project. Use `--scope project` to share it through the repo's `.mcp.json`.")
    lines += [f"- {note}" for note in notes]
    lines += ["", END]
    return "\n".join(lines)


def render(readme_text, block):
    if START in readme_text:
        return re.sub(re.escape(START) + r".*?" + re.escape(END), lambda _: block, readme_text, flags=re.S)
    match = re.search(r"^## ", readme_text, flags=re.M)
    if not match:
        return readme_text.rstrip() + "\n\n" + block + "\n"
    return readme_text[: match.start()] + block + "\n\n" + readme_text[match.start():]


TABLE_START = "<!-- claude-code-connectors:start -->"
TABLE_END = "<!-- claude-code-connectors:end -->"


def sign_in(server):
    auth = server.get("auth") or {}
    if "CLIENT_ID" in auth:
        return "OAuth app you create" if VAR.fullmatch(auth["CLIENT_ID"]) else "OAuth with upstream's client ID (untested)"
    secrets = env_vars({k: server.get(k) for k in ("headers", "env")})
    if secrets:
        return "Set " + ", ".join(f"`{v}`" for v in secrets)
    if server.get("url", "").startswith("${"):
        return "Your own server URL"
    return "Sign in through `/mcp` if the server asks" if "url" in server else "None"


def connector_table():
    rows = ["| Connector | How to add it in Claude Code | Credentials |", "|---|---|---|"]
    for mcp in sorted((ROOT / "third_party").glob("*/mcp.json")):
        name = mcp.parent.name
        server = next(iter(json.loads(mcp.read_text())["mcpServers"].values()))
        if name in OFFICIAL_PLUGINS:
            route = f"Official plugin `{OFFICIAL_PLUGINS[name]}@claude-plugins-official`"
        elif name in CLAUDE_AI_CONNECTORS:
            route = "claude.ai connector, or `claude mcp add`"
        else:
            route = "`claude mcp add`"
        rows.append(f"| [{name}](third_party/{name}/README.md#install-in-claude-code) | {route} | {sign_in(server)} |")
    return "\n".join([TABLE_START, *rows, TABLE_END])


def main():
    check = "--check" in sys.argv
    stale = []
    root_readme = ROOT / "README.md"
    before = root_readme.read_text()
    if TABLE_START in before:
        after = re.sub(re.escape(TABLE_START) + r".*?" + re.escape(TABLE_END), lambda _: connector_table(), before, flags=re.S)
        if after != before:
            stale.append("README.md")
            if not check:
                root_readme.write_text(after)
    for mcp in sorted((ROOT / "third_party").glob("*/mcp.json")):
        name = mcp.parent.name
        readme = mcp.parent / "README.md"
        servers = json.loads(mcp.read_text())["mcpServers"]
        before = readme.read_text()
        after = render(before, section(name, servers))
        if after != before:
            stale.append(name)
            if not check:
                readme.write_text(after)
    if check and stale:
        print("stale Claude Code install docs: " + ", ".join(stale))
        sys.exit(1)
    print(("would update" if check else "updated") + f" {len(stale)} README(s)")


if __name__ == "__main__":
    main()
