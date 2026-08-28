import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src" / "app"))
import model_safety  # noqa: E402


class ModelSafetyTests(unittest.TestCase):
    def test_importo_richiede_valuta_nel_contesto(self):
        self.assertFalse(model_safety.keep("AMOUNT", "articolo 120 del codice", 9, 12))
        self.assertTrue(model_safety.keep("AMOUNT", "importo €120,00", 9, 12))
        self.assertTrue(model_safety.keep("AMOUNT", "120 EUR", 0, 3))
        self.assertTrue(model_safety.keep("FULLNAME", "Mario Rossi", 0, 11))


if __name__ == "__main__":
    unittest.main()
