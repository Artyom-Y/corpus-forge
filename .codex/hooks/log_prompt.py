#!/usr/bin/env python3

import json
import os
import sys
from pathlib import Path
from datetime import datetime, timezone


def main():
    try:
        payload = json.load(sys.stdin)
    except Exception:
        payload = {}

    prompt = payload.get("prompt", "")
    session_id = payload.get("session_id", "unknown")
    turn_id = payload.get("turn_id", "unknown")

    timestamp = datetime.now(timezone.utc).strftime(
        "%Y-%m-%d %H:%M:%S UTC"
    )

    log_file = Path(os.environ.get("CODEX_PROMPT_HISTORY", "prompt-history.md"))
    log_file.parent.mkdir(parents=True, exist_ok=True)

    quoted_prompt = "\n".join(
        f"> {line}" for line in prompt.splitlines()
    )

    with open(log_file, "a", encoding="utf-8") as f:
        f.write(f"## {timestamp}\n\n")
        f.write(
            f"_session: {session_id} • turn: {turn_id}_\n\n"
        )

        if quoted_prompt:
            f.write(quoted_prompt)
        else:
            f.write("> ")

        f.write("\n\n---\n\n")


if __name__ == "__main__":
    main()
