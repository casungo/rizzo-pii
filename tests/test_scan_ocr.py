import unittest

import sys
sys.path.insert(0, "src/app")
import scan_ocr


class OcrParsingTests(unittest.TestCase):
    def test_tsv_boxes_and_mapping_are_in_pdf_points(self):
        tsv = "level\tleft\ttop\twidth\theight\ttext\n5\t200\t400\t100\t40\tMario\n5\t310\t400\t100\t40\tRossi\n"
        words = scan_ocr.words_from_tsv(tsv, 2)
        self.assertEqual(words[0]["rect"], (100.0, 200.0, 150.0, 220.0))
        found = scan_ocr.redactions([(0, words)], {"[FULLNAME_1]": "Mario Rossi"})
        self.assertEqual(found[0]["page"], 0)
        self.assertEqual(found[0]["text"], "[FULLNAME_1]")


if __name__ == "__main__":
    unittest.main()
