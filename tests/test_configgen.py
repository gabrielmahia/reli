"""Config generation — non-destructive, backed-up, idempotent."""
import json
from pathlib import Path

from reli.configgen import build_block, merge_into_claude_config


def test_build_block_uses_concise_keys():
    block = build_block(["mpesa-mcp", "bima-mcp"], python="PY")
    assert set(block) == {"mpesa", "bima"}
    assert block["bima"]["command"] == "bima-mcp"          # script path
    assert block["mpesa"]["args"] == ["-m", "mpesa_mcp.server"]  # module path


def test_merge_preserves_existing_and_backs_up(tmp_path: Path):
    cfg = tmp_path / "claude_desktop_config.json"
    cfg.write_text(json.dumps({"theme": "dark",
                               "mcpServers": {"other": {"command": "x"}}}))
    block = build_block(["mpesa-mcp"], python="PY")
    path, backup = merge_into_claude_config(block, path=cfg)
    data = json.loads(cfg.read_text())
    assert data["theme"] == "dark"
    assert "other" in data["mcpServers"] and "mpesa" in data["mcpServers"]
    assert backup is not None and backup.exists()


def test_merge_is_idempotent(tmp_path: Path):
    cfg = tmp_path / "c.json"
    block = build_block(["mpesa-mcp"], python="PY")
    merge_into_claude_config(block, path=cfg)
    before = cfg.read_text()
    _, backup2 = merge_into_claude_config(block, path=cfg)
    assert cfg.read_text() == before
    assert backup2 is None  # no-op detected, no second backup


def test_dry_run_writes_nothing(tmp_path: Path):
    cfg = tmp_path / "c.json"
    merge_into_claude_config(build_block(["mpesa-mcp"]), path=cfg, dry_run=True)
    assert not cfg.exists()
