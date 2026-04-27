"""
Homology free novelty signal.

The point of this module is small but load bearing: it surfaces host
processes that are hit by structurally similar effectors from sequence
divergent pathogens.

Why that matters. The current DNA synthesis screening layer that gates a
lot of biosecurity defense is built on sequence homology. An AI designed
toxin or binder with no sequence neighbour to anything in public
databases is invisible to it. But the host side does not change. If we
already know that a host process is engaged by structurally convergent
effectors from very different pathogens, that process is exactly where
we should expect novel effectors to land too. Tagging those processes
ahead of time is one of the few defensive moves that does not lose
value when the offensive sequence space stops being predictable.

This module is not running structure prediction. It reads the curated
edge table and counts how many distinct pathogen classes engage the
same host module. A class count of 3 or more is treated as a structural
novelty signal.
"""

from __future__ import annotations

import csv
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


@dataclass(frozen=True)
class NoveltySignal:
    host_module: str
    pathogen_classes: tuple[str, ...]
    effector_families: tuple[str, ...]
    flagged: bool


def default_edges_path() -> Path:
    return Path(__file__).resolve().parents[2] / "data" / "effector_host_edges.csv"


def load_edges(csv_path: str | Path | None = None) -> list[dict]:
    path = Path(csv_path) if csv_path else default_edges_path()
    with open(path, newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def signal(edges: Iterable[dict], min_classes: int = 3) -> list[NoveltySignal]:
    by_module: dict[str, dict[str, set[str]]] = defaultdict(
        lambda: {"classes": set(), "effectors": set()}
    )
    for edge in edges:
        module = edge["host_module"]
        by_module[module]["classes"].add(edge["pathogen_class"])
        by_module[module]["effectors"].add(edge["effector_family"])

    out: list[NoveltySignal] = []
    for module, agg in by_module.items():
        classes = tuple(sorted(agg["classes"]))
        effectors = tuple(sorted(agg["effectors"]))
        out.append(
            NoveltySignal(
                host_module=module,
                pathogen_classes=classes,
                effector_families=effectors,
                flagged=len(classes) >= min_classes,
            )
        )
    return sorted(out, key=lambda s: (-len(s.pathogen_classes), s.host_module))
