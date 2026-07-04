"""MCP client configuration generation.

Builds ``mcpServers`` blocks from the registry and merges them into
Claude Desktop's configuration non-destructively: existing unrelated
entries are preserved, and the previous file is backed up before any
write. Idempotent — re-running produces the same result.
"""

from __future__ import annotations

import json
import os
import platform
import sys
import time
from pathlib import Path

from .registry import launch_spec


def build_block(names: list[str], python: str = sys.executable) -> dict:
    """Return an mcpServers mapping for the given registry server names."""
    block: dict[str, dict] = {}
    for n in sorted(names):
        spec = launch_spec(n, python=python)
        key = n.removesuffix("-mcp")  # concise client-side names
        block[key] = spec
    return block


def claude_config_path() -> Path:
    """Platform-appropriate Claude Desktop config location."""
    system = platform.system()
    if system == "Darwin":
        return Path.home() / "Library/Application Support/Claude/claude_desktop_config.json"
    if system == "Windows":
        return Path(os.environ.get("APPDATA", Path.home())) / "Claude/claude_desktop_config.json"
    return Path.home() / ".config/Claude/claude_desktop_config.json"


def merge_into_claude_config(
    block: dict, path: Path | None = None, dry_run: bool = False
) -> tuple[Path, Path | None]:
    """Merge server entries into the Claude config. Returns (path, backup)."""
    path = path or claude_config_path()
    existing: dict = {}
    backup: Path | None = None
    if path.exists():
        existing = json.loads(path.read_text() or "{}")
    merged = dict(existing)
    merged.setdefault("mcpServers", {})
    if merged["mcpServers"] | block == merged["mcpServers"]:
        return path, None  # idempotent no-op
    merged["mcpServers"] = merged["mcpServers"] | block
    if dry_run:
        return path, None
    if path.exists():
        backup = path.with_suffix(f".bak.{int(time.time())}")
        backup.write_bytes(path.read_bytes())
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(merged, indent=2) + "\n")
    return path, backup
