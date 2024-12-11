import fitz # type: ignore # PyMuPDF alias


class Extractor:
    def __init__(self, pdf_path: str) -> None:
        self.pdf_path = pdf_path

    def open_pdf(self) -> fitz.Document:
        pdf = fitz.open(self.pdf_path)
        return pdf





