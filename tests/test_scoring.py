import unittest

from funcgenomic.scoring import (
    compute_score,
    default_csv_path,
    load_targets,
    rank,
)


class ScoringTests(unittest.TestCase):
    def test_rank_returns_highest_score_first(self) -> None:
        rows = rank(load_targets(default_csv_path()))
        self.assertTrue(rows)
        for a, b in zip(rows, rows[1:]):
            self.assertGreaterEqual(a.convergence_score, b.convergence_score)

    def test_all_scores_are_bounded(self) -> None:
        for r in load_targets(default_csv_path()):
            self.assertGreaterEqual(r.convergence_score, -2.0)
            self.assertLessEqual(r.convergence_score, 6.0)

    def test_breadth_saturates(self) -> None:
        low = compute_score(4.0, 1, 4.0, 4.0, 1.0)
        high = compute_score(4.0, 5, 4.0, 4.0, 1.0)
        capped = compute_score(4.0, 50, 4.0, 4.0, 1.0)
        self.assertGreater(high, low)
        self.assertEqual(high, capped)

    def test_fitness_risk_penalizes(self) -> None:
        clean = compute_score(4.0, 2, 4.0, 4.0, 1.0)
        risky = compute_score(4.0, 2, 4.0, 4.0, 4.0)
        self.assertGreater(clean, risky)


if __name__ == "__main__":
    unittest.main()
