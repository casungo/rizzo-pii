import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src" / "data_pipeline"))
import generate_synthetic_pii as synthetic  # noqa: E402


class SyntheticNameTests(unittest.TestCase):
    def test_nome_maiuscolo_mantiene_le_label(self):
        pieces = synthetic._name_pieces(upper=True)
        values = [value for value, label in pieces if label]
        self.assertTrue(all(value == value.upper() for value in values))
        self.assertEqual({"GIVENNAME", "SURNAME"}, {label for _, label in pieces if label})


if __name__ == "__main__":
    unittest.main()
