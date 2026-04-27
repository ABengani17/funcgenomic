"""
Command line entry for funcgenomic.

Usage
-----
    PYTHONPATH=src python3 -m funcgenomic rank [--top N]
    PYTHONPATH=src python3 -m funcgenomic processes [--top N]
    PYTHONPATH=src python3 -m funcgenomic novelty [--min-classes N]

The output is plain text by design. Anyone who wants a different format
can pipe it through their tool of choice.
"""

from __future__ import annotations

import argparse
import sys
from collections import defaultdict

from .atlas import rollup_processes
from .novelty import load_edges, signal
from .scoring import default_csv_path, load_targets, rank


def _edge_indices() -> tuple[dict[str, set[str]], set[str]]:
    edges = load_edges()
    classes_by_module: dict[str, set[str]] = defaultdict(set)
    for e in edges:
        classes_by_module[e["host_module"]].add(e["pathogen_class"])
    novelty_modules = {
        s.host_module for s in signal(edges, min_classes=3) if s.flagged
    }
    return classes_by_module, novelty_modules


def _cmd_rank(args: argparse.Namespace) -> int:
    rows = rank(load_targets(default_csv_path()))
    if args.top:
        rows = rows[: args.top]
    print(f"{'crop':<10} {'pathogen class':<12} {'host process':<32} {'score':>6}  bar")
    print("-" * 80)
    max_score = max((r.convergence_score for r in rows), default=1.0) or 1.0
    for r in rows:
        bar_len = int(round(20 * r.convergence_score / max_score))
        bar = "#" * max(bar_len, 0)
        print(
            f"{r.crop:<10} {r.pathogen_class:<12} "
            f"{r.host_process[:32]:<32} {r.convergence_score:>6.2f}  {bar}"
        )
    return 0


def _cmd_processes(args: argparse.Namespace) -> int:
    classes_by_module, novelty_modules = _edge_indices()
    rows = rollup_processes(
        load_targets(default_csv_path()),
        edge_classes_by_module=classes_by_module,
        novelty_modules=novelty_modules,
    )
    if args.top:
        rows = rows[: args.top]
    print(
        f"{'host process':<36} {'breadth':>7} {'evidence':>9} "
        f"{'novelty':>7} {'score':>6}  bar"
    )
    print("-" * 88)
    max_score = max((p.convergence_score for p in rows), default=1.0) or 1.0
    for p in rows:
        bar_len = int(round(20 * p.convergence_score / max_score))
        bar = "#" * max(bar_len, 0)
        print(
            f"{p.host_process[:36]:<36} {p.breadth_classes:>7} "
            f"{p.evidence_score:>9.2f} {p.novelty_flag:>7} "
            f"{p.convergence_score:>6.2f}  {bar}"
        )
    return 0


def _cmd_novelty(args: argparse.Namespace) -> int:
    edges = load_edges()
    rows = signal(edges, min_classes=args.min_classes)
    print(f"{'host module':<32} {'classes':>7} {'flagged':>7}  classes seen")
    print("-" * 80)
    for s in rows:
        flag = "yes" if s.flagged else "no"
        print(
            f"{s.host_module[:32]:<32} {len(s.pathogen_classes):>7} {flag:>7}  "
            f"{', '.join(s.pathogen_classes)}"
        )
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="funcgenomic")
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_rank = sub.add_parser("rank", help="rank candidate rows")
    p_rank.add_argument("--top", type=int, default=0)
    p_rank.set_defaults(func=_cmd_rank)

    p_proc = sub.add_parser("processes", help="rollup ranking by host process")
    p_proc.add_argument("--top", type=int, default=0)
    p_proc.set_defaults(func=_cmd_processes)

    p_nov = sub.add_parser("novelty", help="show structural novelty signal")
    p_nov.add_argument("--min-classes", type=int, default=3)
    p_nov.set_defaults(func=_cmd_novelty)

    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
