from __future__ import annotations
from pathlib import Path

SYSTEM_PROMPT_PATH = Path(__file__).parents[1] / "prompts" / "system.md"
DEVELOPER_PROMPT_PATH = Path(__file__).parents[1] / "prompts" / "developer.md"


def load_system_prompt() -> str:
    try:
        return SYSTEM_PROMPT_PATH.read_text(encoding="utf-8")
    except FileNotFoundError:
        raise RuntimeError(f"System-Prompt not found: {SYSTEM_PROMPT_PATH}")


def load_developer_prompt() -> str:
    try:
        return DEVELOPER_PROMPT_PATH.read_text(encoding="utf-8")
    except FileNotFoundError:
        print(f"Developer-Prompt not found: {DEVELOPER_PROMPT_PATH}")
        return ""
