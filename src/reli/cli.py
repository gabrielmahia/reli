"""reli — the on-ramp to East Africa's MCP coordination stack.

One command chain takes an MCP client from zero to the full stack:

    pip install reli && reli up --pack core

Design constraints: stdlib only, offline-tolerant (everything except
``install`` works without a network), plain-language output with a
"what to do next" line at every exit point.
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import subprocess
import sys

from . import configgen, registry
from .registry import DEMO_NOTICE, PACKS, SERVERS


def _installed(name: str) -> bool:
    return importlib.util.find_spec(SERVERS[name]["module"]) is not None


def cmd_list(args: argparse.Namespace) -> int:
    names = registry.resolve([args.pack]) if args.pack else list(SERVERS)
    print(f"East Africa MCP stack — {len(names)} components\n")
    for pack, pdesc in PACKS.items():
        members = [n for n in names if pack in SERVERS[n]["packs"]]
        if not members:
            continue
        print(f"[{pack}] {pdesc}")
        for n in members:
            s = SERVERS[n]
            mark = "installed" if _installed(n) else "pip install " + n
            kind = " (library)" if s["kind"] == "library" else ""
            print(f"  {n}{kind} — {s['gloss']}")
            print(f"      {s['desc']}")
            print(f"      [{mark}]")
        print()
    print(DEMO_NOTICE)
    return 0


def cmd_install(args: argparse.Namespace) -> int:
    try:
        names = registry.resolve(args.targets)
    except KeyError as e:
        print(f"Unknown server or pack: {e}. Run `reli list` to see options.")
        return 2
    todo = [n for n in names if not _installed(n)]
    if not todo:
        print("Everything requested is already installed. Next: `reli config`.")
        return 0
    cmd = [sys.executable, "-m", "pip", "install", *todo]
    print(("DRY RUN — would run: " if args.dry_run else "Running: ") + " ".join(cmd))
    if args.dry_run:
        return 0
    rc = subprocess.call(cmd)
    if rc == 0:
        print(f"\nInstalled {len(todo)} package(s). Next: `reli config` to wire "
              "them into your MCP client, then `reli doctor` to verify.")
    else:
        print("\npip reported a problem. Re-run with a virtual environment "
              "active, or try `pip install --user`.")
    return rc


def cmd_config(args: argparse.Namespace) -> int:
    names = [n for n in SERVERS if SERVERS[n]["kind"] == "server" and _installed(n)]
    if not names:
        print("No stack servers are installed yet. Start with "
              "`reli install core` or `reli install all`.")
        return 1
    block = configgen.build_block(names, python=sys.executable)
    if args.client == "generic" or args.stdout:
        print(json.dumps({"mcpServers": block}, indent=2))
        print(f"\n{len(names)} server(s) configured. Paste the block into your "
              "MCP client's configuration.", file=sys.stderr)
        return 0
    path, backup = configgen.merge_into_claude_config(block, dry_run=args.dry_run)
    verb = "Would update" if args.dry_run else "Updated"
    print(f"{verb}: {path}")
    if backup:
        print(f"Backup of previous config: {backup}")
    print(f"\n{len(names)} server(s) wired in. Next: restart Claude Desktop, "
          "then ask your agent: “what Kenya-stack tools do you have?”")
    return 0


def cmd_doctor(args: argparse.Namespace) -> int:
    names = [n for n in SERVERS if _installed(n)]
    if not names:
        print("Nothing from the stack is installed. Start: `reli install core`.")
        return 1
    print(f"Checking {len(names)} installed component(s)...\n")
    failures = 0
    for n in names:
        s = SERVERS[n]
        mod = s["module"] + (".server" if s["kind"] == "server" else "")
        r = subprocess.run(
            [sys.executable, "-c", f"import {mod}"],
            capture_output=True, text=True, timeout=30,
        )
        ok = r.returncode == 0
        failures += 0 if ok else 1
        print(f"  {'OK  ' if ok else 'FAIL'} {n}  ({mod})")
        if not ok and args.verbose:
            print("       " + r.stderr.strip().splitlines()[-1])
    if failures:
        print(f"\n{failures} component(s) failed import. Try reinstalling: "
              "`pip install --force-reinstall <name>`, or report at the "
              "component's GitHub Issues page.")
        return 1
    print("\nAll healthy. Next: `reli config` if you haven't wired a client yet.")
    return 0


def cmd_demo(args: argparse.Namespace) -> int:
    from . import demo
    return demo.run(args.scenario)


def cmd_up(args: argparse.Namespace) -> int:
    ns = argparse.Namespace(targets=[args.pack], dry_run=False)
    rc = cmd_install(ns)
    if rc != 0:
        return rc
    rc = cmd_config(argparse.Namespace(client=args.client, stdout=False, dry_run=False))
    if rc != 0:
        return rc
    return cmd_doctor(argparse.Namespace(verbose=False))


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(
        prog="reli",
        description="On-ramp to East Africa's MCP coordination stack. "
                    "Zero to a Kenya-aware AI agent in one command: `reli up`.",
        epilog=DEMO_NOTICE,
    )
    sub = p.add_subparsers(dest="cmd", required=True)

    sp = sub.add_parser("list", help="show all stack components by domain pack")
    sp.add_argument("--pack", choices=sorted(PACKS), help="filter to one pack")
    sp.set_defaults(fn=cmd_list)

    sp = sub.add_parser("install", help="install servers or packs from PyPI")
    sp.add_argument("targets", nargs="+",
                    help="server names, pack names, or 'all'")
    sp.add_argument("--dry-run", action="store_true")
    sp.set_defaults(fn=cmd_install)

    sp = sub.add_parser("config", help="wire installed servers into an MCP client")
    sp.add_argument("--client", choices=["claude", "generic"], default="claude")
    sp.add_argument("--stdout", action="store_true", help="print JSON instead of writing")
    sp.add_argument("--dry-run", action="store_true")
    sp.set_defaults(fn=cmd_config)

    sp = sub.add_parser("doctor", help="verify installed components import cleanly")
    sp.add_argument("--verbose", action="store_true")
    sp.set_defaults(fn=cmd_doctor)

    sp = sub.add_parser("demo", help="run a coordination cascade demo in the terminal")
    sp.add_argument("scenario", nargs="?", default="drought",
                    choices=["drought", "outbreak", "flood"])
    sp.set_defaults(fn=cmd_demo)

    sp = sub.add_parser("up", help="install + config + doctor in one step")
    sp.add_argument("--pack", default="core", choices=sorted(PACKS) + ["all"])
    sp.add_argument("--client", choices=["claude", "generic"], default="claude")
    sp.set_defaults(fn=cmd_up)

    args = p.parse_args(argv)
    try:
        return args.fn(args)
    except BrokenPipeError:  # e.g. `reli list | head`
        import os
        os.dup2(os.open(os.devnull, os.O_WRONLY), sys.stdout.fileno())
        return 0


if __name__ == "__main__":
    raise SystemExit(main())
