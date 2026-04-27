import unittest

from funcgenomic.atlas import rollup_processes
from funcgenomic.scoring import default_csv_path, load_targets


class AtlasTests(unittest.TestCase):
    def setUp(self) -> None:
        self.processes = rollup_processes(load_targets(default_csv_path()))

    def test_rollup_produces_sorted_results(self) -> None:
        self.assertTrue(self.processes)
        for a, b in zip(self.processes, self.processes[1:]):
            self.assertGreaterEqual(a.convergence_score, b.convergence_score)

    def test_breadth_is_at_least_one(self) -> None:
        for p in self.processes:
            self.assertGreaterEqual(p.breadth_classes, 1)

    def test_eif4e_translation_rolls_up_across_viruses(self) -> None:
        eif = next(
            (p for p in self.processes if p.host_process == "eIF4E translation initiation"),
            None,
        )
        self.assertIsNotNone(eif)
        self.assertGreaterEqual(eif.breadth_classes, 1)


if __name__ == "__main__":
    unittest.main()
