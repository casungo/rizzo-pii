import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src" / "app"))
import batch_uploads  # noqa: E402


class BatchUploadTests(unittest.TestCase):
    def test_unisce_senza_riportare_i_nomi_originali(self):
        out = batch_uploads.join_texts(["Mario Rossi", "Mario Rossi"])
        self.assertEqual("--- DOCUMENTO 1 ---\n\nMario Rossi\n\n--- DOCUMENTO 2 ---\n\nMario Rossi", out)


if __name__ == "__main__":
    unittest.main()
