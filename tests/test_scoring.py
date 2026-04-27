from pathlib import Path

from crop_host_atlas.scoring import load_candidates, rank_candidates


def test_rank_candidates_returns_highest_score_first() -> None:
    csv_path = Path(__file__).resolve().parents[1] / "data" / "host_factor_candidates.csv"
    candidates = load_candidates(csv_path)
    ranked = rank_candidates(candidates)

    assert ranked
    assert ranked[0].total_score >= ranked[-1].total_score
    assert ranked[0].host_target == "SWEET promoter axis"


def test_all_candidates_have_bounded_scores() -> None:
    csv_path = Path(__file__).resolve().parents[1] / "data" / "host_factor_candidates.csv"
    for candidate in load_candidates(csv_path):
        assert -1.0 <= candidate.total_score <= 5.0
