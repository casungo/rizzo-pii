"""OCR locale per PDF senza layer testuale.

Usa il binario Tesseract gia' presente nell'immagine Docker. Non invia pagine a
servizi esterni. Le coordinate TSV servono anche a redigere i pixel della scansione.
"""

import csv
import io
import re
import shutil
import subprocess


class OcrError(ValueError):
    pass


def words_from_tsv(tsv, scale):
    """Parsa il TSV di Tesseract e riporta parole con bbox in punti PDF."""
    out = []
    for row in csv.DictReader(io.StringIO(tsv), delimiter="\t"):
        text = (row.get("text") or "").strip()
        if not text or row.get("level") != "5":
            continue
        try:
            left, top = float(row["left"]), float(row["top"])
            width, height = float(row["width"]), float(row["height"])
        except (KeyError, TypeError, ValueError):
            continue
        out.append({"text": text, "rect": (left / scale, top / scale,
                    (left + width) / scale, (top + height) / scale)})
    return out


def _ocr_png(png, scale):
    exe = shutil.which("tesseract")
    if not exe:
        raise OcrError("OCR non disponibile: installa Tesseract con la lingua italiana.")
    try:
        run = subprocess.run([exe, "stdin", "stdout", "-l", "ita", "tsv", "--psm", "6"],
                             input=png, capture_output=True, check=True, timeout=120)
    except subprocess.TimeoutExpired:
        raise OcrError("OCR scaduto dopo 120 secondi.")
    except subprocess.CalledProcessError as e:
        detail = e.stderr.decode("utf-8", "replace").strip()
        raise OcrError(f"OCR non riuscito: {detail or 'Tesseract ha restituito un errore.'}")
    return words_from_tsv(run.stdout.decode("utf-8", "replace"), scale)


def extract(pdf_bytes, dpi=200):
    """Ritorna testo e parole OCR delle sole pagine che non hanno testo nativo."""
    import fitz

    scale = dpi / 72.0
    pages, texts = [], []
    with fitz.open(stream=pdf_bytes, filetype="pdf") as doc:
        for index, page in enumerate(doc):
            native = page.get_text().strip()
            if native:
                texts.append(native)
                continue
            words = _ocr_png(page.get_pixmap(dpi=dpi).tobytes("png"), scale)
            pages.append((index, words))
            texts.append(" ".join(word["text"] for word in words))
    return "\n".join(texts), pages


def _tokens(text):
    return re.findall(r"[^\W_]+", (text or "").casefold(), flags=re.UNICODE)


def redactions(pages, mapping):
    """Trova le sequenze OCR corrispondenti ai valori PII nel dizionario."""
    found = []
    for page_no, words in pages:
        normalized = [_tokens(word["text"]) for word in words]
        for placeholder, value in mapping.items():
            wanted = _tokens(value)
            if not wanted:
                continue
            for start in range(len(words)):
                flat, end = [], start
                while end < len(words) and len(flat) < len(wanted):
                    flat.extend(normalized[end])
                    end += 1
                if flat != wanted:
                    continue
                x0 = min(words[i]["rect"][0] for i in range(start, end))
                y0 = min(words[i]["rect"][1] for i in range(start, end))
                x1 = max(words[i]["rect"][2] for i in range(start, end))
                y1 = max(words[i]["rect"][3] for i in range(start, end))
                found.append({"page": page_no, "rect": (x0, y0, x1, y1),
                              "text": placeholder})
    return found
