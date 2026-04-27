"""
Convergence scoring for funcgenomic.

The rule is on purpose simple, transparent, and editable.
Five axes feed in, one number comes out, and you can argue with the weights
in `configs/weights.toml` without touching this file.

Axes
----
evidence_score        How strong is the published support for this host
                      target being a real susceptibility lever for this
                      pathogen. Range 1 to 5.
breadth_classes       Number of distinct pathogen classes (bacterium,
                      fungus, virus, oomycete, protist) that converge on
                      the same host process. Integer, capped softly at 5.
tractability_score    How edit friendly is the locus today. Promoter cis
                      element edits are easy, multi gene knockouts are
                      harder. Range 1 to 5.
deployability_score   How realistic is field deployment in the target
                      crop. Includes regulatory and breeding pipeline
                      considerations. Range 1 to 5.
fitness_risk          Yield or growth penalty likelihood when the locus
                      is perturbed. Range 1 to 5, subtracted not added.

The novelty flag is handled separately in novelty.py and surfaces as a
small bonus at the rollup stage.
"""

from __future__ import annotations

import csv
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Mapping


DEFAULT_WEIGHTS: Mapping[str, float] = {
    "evidence": 0.30,
    "breadth": 0.30,
    "tractability": 0.20,
    "deployability": 0.15,
    "fitness_risk": 0.10,
}


@dataclass(frozen=True)
class TargetRow:
    crop: str
    pathogen: str
    pathogen_class: str
    host_target: str
    host_process: str
    evidence_score: float
    breadth_classes: int
    tractability_score: float
    deployability_score: float
    fitness_risk: float
    structural_novelty_flag: int
    primary_reference: str
    convergence_score: float


def compute_score(
    evidence_score: float,
    breadth_classes: int,
    tractability_score: float,
    deployability_score: float,
    fitness_risk: float,
    weights: Mapping[str, float] = DEFAULT_WEIGHTS,
) -> float:
    """
    Rewards evidence and cross class breadth, discounts fitness risk.

    breadth_classes is normalized into a 1 to 5 range so it sits on the
    same scale as the other axes. A target hit by 5 or more pathogen
    classes saturates at 5.
    """
    breadth_normalized = min(float(breadth_classes), 5.0)
    total = (
        weights["evidence"] * evidence_score
        + weights["breadth"] * breadth_normalized
        + weights["tractability"] * tractability_score
        + weights["deployability"] * deployability_score
        - weights["fitness_risk"] * fitness_risk
    )
    return round(total, 4)


def _row_to_target(row: dict, weights: Mapping[str, float]) -> TargetRow:
    evidence = float(row["evidence_score"])
    breadth = int(row["breadth_classes"])
    tractability = float(row["tractability_score"])
    deployability = float(row["deployability_score"])
    fitness = float(row["fitness_risk"])
    return TargetRow(
        crop=row["crop"],
        pathogen=row["pathogen"],
        pathogen_class=row["pathogen_class"],
        host_target=row["host_target"],
        host_process=row["host_process"],
        evidence_score=evidence,
        breadth_classes=breadth,
        tractability_score=tractability,
        deployability_score=deployability,
        fitness_risk=fitness,
        structural_novelty_flag=int(row.get("structural_novelty_flag", 0)),
        primary_reference=row.get("primary_reference", ""),
        convergence_score=compute_score(
            evidence_score=evidence,
            breadth_classes=breadth,
            tractability_score=tractability,
            deployability_score=deployability,
            fitness_risk=fitness,
            weights=weights,
        ),
    )


def load_targets(
    csv_path: str | Path,
    weights: Mapping[str, float] = DEFAULT_WEIGHTS,
) -> list[TargetRow]:
    rows: list[TargetRow] = []
    with open(csv_path, newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            rows.append(_row_to_target(row, weights))
    return rows


def rank(targets: Iterable[TargetRow]) -> list[TargetRow]:
    return sorted(targets, key=lambda t: t.convergence_score, reverse=True)


def default_csv_path() -> Path:
    return Path(__file__).resolve().parents[2] / "data" / "host_targets.csv"
