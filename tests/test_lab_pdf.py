import unittest,io
from unittest.mock import patch
from pypdf import PdfReader,PdfWriter
from src.lab_pdf import extract_labs_from_pdf

class PdfTests(unittest.TestCase):
    def test_pdf_text_extracts_only_identified_units(self):
        class P:
            def extract_text(self, **kwargs):
                return "Glicemia em jejum: 132 mg/dL\nHemoglobina glicada: 6,8 %\n"
        class Fake:
            is_encrypted = False
            pages = [P()]
        with patch('src.lab_pdf.PdfReader', return_value=Fake()):
            labs, warnings = extract_labs_from_pdf(b'%PDFsynthetic')
        self.assertEqual(labs['glicemia_jejum'], 132)
        self.assertEqual(labs['hba1c'], 6.8)
        self.assertTrue(warnings)
    def test_ambiguous_duplicate_is_removed(self):
        class P:
            def extract_text(self, **kwargs):
                return "Hemoglobina glicada: 6,8%\nHemoglobina glicada: 6,9%\n"
        class Fake:
            is_encrypted = False
            pages = [P()]
        with patch('src.lab_pdf.PdfReader', return_value=Fake()):
            labs, warnings = extract_labs_from_pdf(b'%PDFsynthetic')
        self.assertNotIn('hba1c',labs)
        self.assertTrue(any('diferentes' in w for w in warnings))
    def test_bad_file(self):
        with self.assertRaises(ValueError):extract_labs_from_pdf(b'bad')
    def test_pdf_no_text(self):
        writer=PdfWriter();writer.add_blank_page(width=100,height=100)
        data=io.BytesIO();writer.write(data)
        labs,notes=extract_labs_from_pdf(data.getvalue())
        self.assertFalse(labs)
        self.assertTrue(notes)

if __name__=='__main__':unittest.main()
