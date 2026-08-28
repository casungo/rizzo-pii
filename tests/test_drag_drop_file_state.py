import unittest
from pathlib import Path


APP = Path(__file__).resolve().parents[1] / "src" / "app" / "app.py"


class DragDropFileStateTests(unittest.TestCase):
    def test_drop_uses_the_file_without_mutating_file_input(self):
        source = APP.read_text(encoding="utf-8")
        self.assertIn("let UPLOAD = null;", source)
        self.assertIn("const currentFile = () => UPLOAD", source)
        self.assertNotIn("new DataTransfer()", source)
        self.assertGreaterEqual(source.count("const file=currentFile();"), 2)


if __name__ == "__main__":
    unittest.main()
