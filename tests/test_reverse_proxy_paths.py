import unittest
from pathlib import Path


APP = Path(__file__).resolve().parents[1] / "src" / "app" / "app.py"


class ReverseProxyPathTests(unittest.TestCase):
    def test_ui_uses_the_wsgi_script_root(self):
        source = APP.read_text(encoding="utf-8")
        self.assertIn('request.script_root.rstrip("/")', source)
        self.assertIn("const API_ROOT = __SCRIPT_ROOT__;", source)
        self.assertNotIn("fetch('/", source)
        self.assertNotIn('fetch(`/', source)
        self.assertNotIn('src="/assets/', source)
        self.assertNotIn(".href='/doc/", source)


if __name__ == "__main__":
    unittest.main()
