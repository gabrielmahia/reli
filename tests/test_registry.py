"""Registry integrity — the data spine must stay internally consistent."""
import subprocess
import sys

from reli.registry import PACKS, SERVERS, by_pack, launch_spec, resolve


def test_every_server_has_required_fields():
    for name, s in SERVERS.items():
        assert s["module"].replace("_", "-") is not None
        assert s["kind"] in ("server", "library")
        assert s["desc"] and not s["desc"].lower().startswith(("i ", "my ")), name
        assert s["packs"] and all(p in PACKS for p in s["packs"]), name


def test_every_pack_is_nonempty():
    for pack in PACKS:
        assert by_pack(pack), pack


def test_launch_spec_shapes():
    for name, s in SERVERS.items():
        spec = launch_spec(name, python="PY")
        if s["script"]:
            assert spec == {"command": s["script"], "args": []}
        else:
            assert spec == {"command": "PY", "args": ["-m", f"{s['module']}.server"]}


def test_resolve_expands_packs_and_dedupes():
    names = resolve(["financial", "soko-mcp"])
    assert names.count("soko-mcp") == 1
    assert "mpesa-mcp" in names


def test_resolve_rejects_unknown():
    try:
        resolve(["not-a-thing"])
        raise AssertionError("should have raised")
    except KeyError:
        pass


def test_registry_matches_pypi_naming_convention():
    for name in SERVERS:
        assert name == name.lower()
        assert " " not in name


def test_cli_entrypoint_runs():
    r = subprocess.run([sys.executable, "-m", "reli.cli", "list"],
                       capture_output=True, text=True)
    assert r.returncode == 0
    assert "financial" in r.stdout and "DEMO" in r.stdout
