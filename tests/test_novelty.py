import unittest

from funcgenomic.novelty import load_edges, signal


class NoveltyTests(unittest.TestCase):
    def test_signal_picks_up_multi_class_modules(self) -> None:
        rows = signal(load_edges(), min_classes=2)
        flagged = [r for r in rows if r.flagged]
        self.assertTrue(flagged)

    def test_high_min_classes_filters_more(self) -> None:
        loose = [r for r in signal(load_edges(), min_classes=2) if r.flagged]
        strict = [r for r in signal(load_edges(), min_classes=4) if r.flagged]
        self.assertGreaterEqual(len(loose), len(strict))


if __name__ == "__main__":
    unittest.main()
