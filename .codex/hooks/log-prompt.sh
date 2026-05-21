#!/usr/bin/env bash
set -euo pipefail

LOG_FILE="${CODEX_PROMPT_HISTORY:-./prompt-history.md}"

# Read hook payload from stdin
PAYLOAD=$(cat)

# Extract fields
PROMPT=$(echo "$PAYLOAD" | jq -r '.prompt // ""')
SESSION_ID=$(echo "$PAYLOAD" | jq -r '.session_id // "unknown"')
TURN_ID=$(echo "$PAYLOAD" | jq -r '.turn_id // "unknown"')

# ISO timestamp
TIMESTAMP=$(date -u +"%Y-%m-%d %H:%M:%S UTC")

# Convert prompt to markdown-safe blockquote
FORMATTED_PROMPT=$(printf "%s\n" "$PROMPT" | sed 's/^/> /')

# Append entry
{
  echo "## $TIMESTAMP"
  echo
  echo "_session: ${SESSION_ID} • turn: ${TURN_ID}_"
  echo
  echo "$FORMATTED_PROMPT"
  echo
  echo "---"
  echo
} >> "$LOG_FILE"

# Tell Codex to continue normally
exit 0
