from pdf_parser import extractor, parser # type: ignore
import pprint
from pathlib import Path
import json


BASE_DIR = Path().parent


p = parser.Parser()
pdf_path = BASE_DIR / 'tests' / 'test_pdfs' / '3.pdf'
pdf = p.open_pdf(pdf_path)
tables = p.extract_tables_from_pdf()
data = p.get_all_data()
pprint.pprint(data)
# print(len(data))