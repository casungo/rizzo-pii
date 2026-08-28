import unittest

import sys
sys.path.insert(0, "src/app")
import scan_qr


class QrGeometryTests(unittest.TestCase):
    def test_opencv_polygon_maps_to_pdf_points(self):
        rect = scan_qr.rect_from_points([[[200, 400], [300, 400], [300, 500], [200, 500]]], 2)
        self.assertEqual(rect, (100.0, 200.0, 150.0, 250.0))


if __name__ == "__main__":
    unittest.main()
