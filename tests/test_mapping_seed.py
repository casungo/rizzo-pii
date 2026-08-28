import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src" / "app"))
import mapping_seed  # noqa: E402


class MappingSeedTests(unittest.TestCase):
    def test_riusa_contatore_e_valore(self):
        counters, seen, mapping = mapping_seed.seed({"[FULLNAME_2]": "Mario Rossi"}, {"FULLNAME"})
        self.assertEqual(2, counters["FULLNAME"])
        self.assertEqual("[FULLNAME_2]", seen[("FULLNAME", "mario rossi")])
        self.assertEqual("Mario Rossi", mapping["[FULLNAME_2]"])


if __name__ == "__main__":
    unittest.main()
