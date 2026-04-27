"""
Process level rollup.

Per row scoring is useful for inspection. The actual question we want to
answer is `which host processes are most worth defending across the
crops we care about`. That means rolling up rows that share a host
process and combining their evidence and breadth in a defensible way.

Rules of the rollup
-------------------
- For each host process, breadth is the number of distinct pathogen
  classes touching it. We take the max of three sources:
    1. distinct classes seen across atlas rows for this process
    2. the highest curated breadth_classes value across those rows
    3. distinct classes seen in the effector edge table for this module
  The point is to be honest about what the curator already knows from
  the literature even when the local atlas slice is small.
- Evidence is the maximum row level evidence in that process. Taking
  the max instead of the mean prevents a single weakly supported row
  from dragging down a process with strong direct evidence elsewhere.
- Tractability and deployability are averaged across rows.
- Fitness risk is the maximum across rows. Pessimistic on purpose.
- Novelty bonus fires if any row in the process carries the structural
  novelty flag, or if the edge based novelty signal flags the module.
"""

from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass
from typing import Iterable, Mapping

from .scoring import (
    DEFAULT_WEIGHTS,
    TargetRow,
    compute_score,
)


NOVELTY_BONUS = 0.15


@dataclass(frozen=True)
class ProcessScore:
    host_process: str
    breadth_classes: int
    evidence_score: float
    tractability_score: float
    deployability_score: float
    fitness_risk: float
    novelty_flag: int
    crops_covered: tuple[str, ...]
    pathogen_classes: tuple[str, ...]
    convergence_score: float


def rollup_processes(
    targets: Iterable[TargetRow],
    weights: Mapping[str, float] = DEFAULT_WEIGHTS,
    edge_classes_by_module: Mapping[str, set[str]] | None = None,
    novelty_modules: set[str] | None = None,
) -> list[ProcessScore]:
    by_process: dict[str, list[TargetRow]] = defaultdict(list)
    for t in targets:
        by_process[t.host_process].append(t)

    out: list[ProcessScore] = []
    for process, rows in by_process.items():
        atlas_classes = {r.pathogen_class for r in rows}
        curated_breadth = max(r.breadth_classes for r in rows)
        edge_classes = (edge_classes_by_module or {}).get(process, set())
        breadth = max(
            len(atlas_classes),
            curated_breadth,
            len(edge_classes),
        )
        classes = tuple(sorted(atlas_classes | edge_classes))
        crops = tuple(sorted({r.crop for r in rows}))
        evidence = max(r.evidence_score for r in rows)
        tractability = sum(r.tractability_score for r in rows) / len(rows)
        deployability = sum(r.deployability_score for r in rows) / len(rows)
        fitness = max(r.fitness_risk for r in rows)
        flag_from_rows = any(r.structural_novelty_flag for r in rows)
        flag_from_edges = process in (novelty_modules or set())
        novelty_flag = 1 if (flag_from_rows or flag_from_edges) else 0
        base = compute_score(
            evidence_score=evidence,
            breadth_classes=breadth,
            tractability_score=tractability,
            deployability_score=deployability,
            fitness_risk=fitness,
            weights=weights,
        )
        score = round(base + NOVELTY_BONUS * novelty_flag, 4)
        out.append(
            ProcessScore(
                host_process=process,
                breadth_classes=breadth,
                evidence_score=round(evidence, 3),
                tractability_score=round(tractability, 3),
                deployability_score=round(deployability, 3),
                fitness_risk=round(fitness, 3),
                novelty_flag=novelty_flag,
                crops_covered=crops,
                pathogen_classes=classes,
                convergence_score=score,
            )
        )
    return sorted(out, key=lambda p: p.convergence_score, reverse=True)
