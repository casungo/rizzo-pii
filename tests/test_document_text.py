import io
import sys
import unittest
import zipfile

sys.path.insert(0, "src/app")
import document_text


class DocxTextTests(unittest.TestCase):
    def test_extracts_paragraphs_without_python_docx(self):
        xml = (b'<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">'
               b'<w:body><w:p><w:r><w:t>Mario Rossi</w:t></w:r></w:p>'
               b'<w:p><w:r><w:t>CF RSSMRA85M01H501Z</w:t></w:r></w:p></w:body></w:document>')
        data = io.BytesIO()
        with zipfile.ZipFile(data, "w") as archive:
            archive.writestr("word/document.xml", xml)
        self.assertEqual("Mario Rossi\nCF RSSMRA85M01H501Z", document_text.docx_text(data.getvalue()))


if __name__ == "__main__":
    unittest.main()
