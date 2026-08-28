# -*- coding: utf-8 -*-
"""Contratto della selezione PII manuale, senza Flask o modello."""

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src" / "app"))
import manual_entities  # noqa: E402


class ManualEntityTests(unittest.TestCase):
    def test_accetta_span_e_rifiuta_input_non_valido(self):
        text = "Mario Rossi vive a Roma"
        got = manual_entities.candidates(
            text, [{"start": 0, "end": 11, "label": "fullname"}], {"FULLNAME"})
        self.assertEqual("manuale", got[0]["source"])
        self.assertEqual("FULLNAME", got[0]["label"])
        self.assertEqual([(0, 5)], manual_entities.exclusions(text, [{"start": 0, "end": 5}]))
        for bad in ([{"start": -1, "end": 2, "label": "FULLNAME"}],
                    [{"start": 0, "end": 2, "label": "UNKNOWN"}],
                    "not-a-list"):
            with self.subTest(bad=bad):
                with self.assertRaises(ValueError):
                    manual_entities.candidates(text, bad, {"FULLNAME"})


if __name__ == "__main__":
    unittest.main()
