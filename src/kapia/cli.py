from __future__ import annotations

import argparse
from pathlib import Path

from kapia import __version__
from kapia.archive import RunArchive


def _cmd_info(_: argparse.Namespace) -> int:
    print(f"Kapia {__version__}")
    print("A lightweight glue library for FEM-based robust optimisation workflows.")
    return 0


def _cmd_init_run(args: argparse.Namespace) -> int:
    archive = RunArchive(args.path)
    archive.save_metadata(extra={"created_by": "kapia init-run"})
    print(f"Created Kapia run archive: {Path(args.path).resolve()}")
    return 0


def _cmd_abracadabra(args: argparse.Namespace) -> int:
    archive = RunArchive(args.path)
    archive.save_metadata(extra={"created_by": "kapia abracadabra"})
    print("✨ Kapia glue activated.")
    print(f"Created Kapia run archive: {Path(args.path).resolve()}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="kapia",
        description="Kapia: glue library for FEM-based robust optimisation workflows.",
    )
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")

    subparsers = parser.add_subparsers(dest="command")

    info_parser = subparsers.add_parser("info", help="Show package information.")
    info_parser.set_defaults(func=_cmd_info)

    init_parser = subparsers.add_parser("init-run", help="Create a new run archive.")
    init_parser.add_argument("path", help="Path to the run archive directory.")
    init_parser.set_defaults(func=_cmd_init_run)

    magic_parser = subparsers.add_parser("abracadabra", help=argparse.SUPPRESS)
    magic_parser.add_argument("path", help=argparse.SUPPRESS)
    magic_parser.set_defaults(func=_cmd_abracadabra)

    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    if not hasattr(args, "func"):
        parser.print_help()
        return 0

    return int(args.func(args))
