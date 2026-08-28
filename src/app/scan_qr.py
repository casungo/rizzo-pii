"""Rilevamento QR locale per PDF. Il contenuto non viene decodificato o inviato."""

import numbers


class QrError(ValueError):
    pass


def _pairs(value):
    if isinstance(value, (list, tuple)):
        if len(value) == 2 and all(isinstance(v, numbers.Real) for v in value):
            yield float(value[0]), float(value[1])
        else:
            for item in value:
                yield from _pairs(item)
    elif hasattr(value, "tolist"):
        yield from _pairs(value.tolist())


def rect_from_points(points, scale):
    """Poligono OpenCV in pixel -> rettangolo in punti PDF."""
    pairs = list(_pairs(points))
    if len(pairs) < 4 or scale <= 0:
        return None
    xs, ys = zip(*pairs)
    return min(xs) / scale, min(ys) / scale, max(xs) / scale, max(ys) / scale


def _page_points(detector, image):
    import cv2

    try:
        detected, _, points, _ = detector.detectAndDecodeMulti(image)
        if detected and points is not None:
            return points
    except cv2.error:
        pass
    _, points, _ = detector.detectAndDecode(image)
    return () if points is None else (points,)


def redactions(pdf_bytes, dpi=200):
    """Ritorna i rettangoli di tutti i QR, anche se non sono decodificabili."""
    try:
        import cv2
        import fitz
        import numpy as np
    except ImportError as e:
        raise QrError("QR non disponibile: installa opencv-python-headless.") from e

    scale, found = dpi / 72.0, []
    with fitz.open(stream=pdf_bytes, filetype="pdf") as doc:
        for page_no, page in enumerate(doc):
            image = cv2.imdecode(np.frombuffer(page.get_pixmap(dpi=dpi).tobytes("png"),
                                               dtype=np.uint8), cv2.IMREAD_COLOR)
            if image is None:
                continue
            for points in _page_points(cv2.QRCodeDetector(), image):
                rect = rect_from_points(points, scale)
                if rect:
                    found.append({"page": page_no, "rect": rect,
                                  "text": f"[QRCODE_{len(found) + 1}]", "kind": "qr"})
    return found
