"""Estrazione minima del testo da DOCX, senza dipendenze aggiuntive."""

import io
import zipfile
from xml.etree import ElementTree


_W = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"


def docx_text(data):
    try:
        with zipfile.ZipFile(io.BytesIO(data)) as archive:
            root = ElementTree.fromstring(archive.read("word/document.xml"))
    except (KeyError, OSError, ValueError, ElementTree.ParseError) as e:
        raise ValueError("File .docx non valido o danneggiato.") from e
    lines = []
    for paragraph in root.iter(_W + "p"):
        parts = []
        for node in paragraph.iter():
            if node.tag == _W + "t":
                parts.append(node.text or "")
            elif node.tag == _W + "tab":
                parts.append("\t")
            elif node.tag == _W + "br":
                parts.append("\n")
        lines.append("".join(parts))
    return "\n".join(lines)
