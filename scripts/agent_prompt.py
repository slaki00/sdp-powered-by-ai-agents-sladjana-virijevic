#!/usr/bin/env python3
"""Edit a Kiro agent prompt as Markdown, then pack it back into the agent JSON.

Usage (from the repo root):
    python3 scripts/agent_prompt.py extract git-agent  # JSON -> .kiro/prompt-drafts/
    python3 scripts/agent_prompt.py pack git-agent     # .kiro/prompt-drafts/ -> JSON
"""

import json
import sys
from pathlib import Path

USAGE = "Usage: python3 scripts/agent_prompt.py {extract|pack} <agent-name>"


def load_config(config_path: Path) -> dict:
    """Read the agent config, stopping with a clear message if it is unusable."""
    if not config_path.is_file():
        sys.exit(f"Error: {config_path} not found. Run this from the repo root.")
    try:
        config = json.loads(config_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as err:
        sys.exit(f"Error: {config_path} is not valid JSON ({err}).")
    if not isinstance(config.get("prompt"), str):
        sys.exit(f"Error: {config_path} has no text 'prompt' field.")
    return config


def main() -> None:
    if len(sys.argv) != 3 or sys.argv[1] not in ("extract", "pack"):
        sys.exit(USAGE)
    command, agent = sys.argv[1], sys.argv[2]
    config_path = Path(".kiro/agents") / f"{agent}.json"
    draft_path = Path(".kiro/prompt-drafts") / f"{agent}.md"
    config = load_config(config_path)

    if command == "extract":
        if draft_path.exists():
            sys.exit(f"{draft_path} already exists; delete it first to re-extract.")
        draft_path.parent.mkdir(exist_ok=True)
        draft_path.write_text(config["prompt"] + "\n", encoding="utf-8")
        print(f"Extracted prompt to {draft_path}")
        return

    if not draft_path.is_file():
        sys.exit(f"Error: {draft_path} not found. Run 'extract' first.")
    prompt = draft_path.read_text(encoding="utf-8").rstrip("\n")
    if not prompt.strip():
        sys.exit(f"Error: {draft_path} is empty; refusing to erase the prompt.")
    config["prompt"] = prompt
    text = json.dumps(config, indent=2, ensure_ascii=False) + "\n"
    config_path.write_text(text, encoding="utf-8")
    print(f"Packed {draft_path} into {config_path}")


if __name__ == "__main__":
    main()
