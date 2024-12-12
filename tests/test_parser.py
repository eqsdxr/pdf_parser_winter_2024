import unittest
import pymupdf
from pdf_parser import parser
from pathlib import Path


class TestParser(unittest.TestCase):
    def setUp(self) -> None:
        self.path = Path().parent.parent
        self.p = parser.Parser()

    def tearDown(self) -> None:
        pass

    def test_open_pdf(self):
        correct_pdf_path = self.path / 'tests' / 'test_pdfs' / '1.pdf'
        invalid_pdf_path = 'path/to/nonexistent.pdf'

        with self.assertRaises(pymupdf.FileNotFoundError):
            self.p.open_pdf(invalid_pdf_path)

        self.assertTrue(self.p.open_pdf(correct_pdf_path))

        expected_pdf_object = pymupdf.Document
        actual_pdf_document = self.p.open_pdf(correct_pdf_path)
        self.assertIsInstance(actual_pdf_document, expected_pdf_object)
        
    def test_extract_tables_from_pdf(self):
        pass

if __name__ == '__main__':
    unittest.main()