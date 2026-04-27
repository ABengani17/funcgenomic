from __future__ import annotations

from dataclasses import dataclass
import csv
from pathlib import Path
from typing import Iterable


@dataclass(frozen=True)
class CandidateScore:
    crop: str
    pathogen: str
    host_target: str
    pathogen_class: str
    evidence_score: float
    breadth_score: float
    tractability_score: float
    deployability_score: float
    fitness_risk: float
    total_score: float


def compute_total(
    evidence_score: float,
    breadth_score: float,
    tractability_score: float,
    deployability_score: float,
    fitness_risk: float,
) -> float:
    """
    The rule is intentionally simple.
    It rewards strong evidence and cross-pathogen breadth,
    then discounts targets that look likely to impose large fitness costs.
    """
    total = (
        0.30 * evidence_score
        + 0.25 * breadth_score
        + 0.20 * tractability_score
        + 0.15 * deployability_score
        - 0.10 * fitness_risk
    )
    return round(total, 4)


def load_candidates(csv_path: str | Path) -> list[CandidateScore]:
    candidates: list[CandidateScore] = []
    with open(csv_path, newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            candidates.append(
                CandidateScore(
                    crop=row["crop"],
                    pathogen=row["pathogen"],
                    host_target=row["host_target"],
                    pathogen_class=row["pathogen_class"],
                    evidence_score=float(row["evidence_score"]),
                    breadth_score=float(row["breadth_score"]),
                    tractability_score=float(row["tractability_score"]),
                    deployability_score=float(row["deployability_score"]),
                    fitness_risk=float(row["fitness_risk"]),
                    total_score=compute_total(
                        evidence_score=float(row["evidence_score"]),
                        breadth_score=float(row["breadth_score"]),
                        tractability_score=float(row["tractability_score"]),
                        deployability_score=float(row["deployability_score"]),
                        fitness_risk=float(row["fitness_risk"]),
                    ),
                )
            )
    return candidates


def rank_candidates(candidates: Iterable[CandidateScore]) -> list[CandidateScore]:
    return sorted(candidates, key=lambda item: item.total_score, reverse=True)


def main() -> None:
    csv_path = Path(__file__).resolve().parents[2] / "data" / "host_factor_candidates.csv"
    for row in rank_candidates(load_candidates(csv_path)):
        print(f"{row.host_target}: {row.total_score}")


if __name__ == "__main__":
    main()
