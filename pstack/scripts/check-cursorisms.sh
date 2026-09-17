#!/usr/bin/env bash
# Fails when pstack still names Cursor-only tools, paths, or models.
# Run after merging upstream to find what needs re-porting (see PORTING.md).
set -euo pipefail

root="$(cd "$(dirname "$0")/.." && pwd)"

pattern='\.cursor/|\.cursor-plugin|\.mdc\b|alwaysApply|AskQuestion|generalPurpose|is_background|\bTask (tool|call|subagent|prompt)|`Task`|environment: "?(cloud|local)|cloud_base_branch|readonly`?: `?true|agent-transcripts|grok-[0-9]|gpt-5\.[0-9]|-thinking-(max|xhigh|high|medium)|cursor-team-kit|create-skill\b|SendToUser|update_state|api2\.cursor\.sh|Cursor'"'"'s built-in|in Cursor|Cursor (restart|dashboard|environment|model picker)'

# PORTING.md, the top-level README, and this script quote the Cursor terms on purpose.
hits="$(grep -rnE "$pattern" "$root" \
	--exclude-dir=node_modules --exclude-dir=images \
	--exclude=PORTING.md --exclude=check-cursorisms.sh |
	grep -v "^$root/README.md:" || true)"

if [ -n "$hits" ]; then
	echo "$hits"
	echo "cursorisms found: port them per PORTING.md" >&2
	exit 1
fi
echo "no cursorisms found"
