from pdf_parser import parser # type: ignore
import pprint
from pathlib import Path
import json


BASE_DIR = Path().parent


p = parser.Parser()
pdf_path = BASE_DIR / 'tests' / 'test_pdfs' / '15.pdf'
pdf = p.open_pdf(pdf_path)
tabs = p.extract_tables_from_pdf(pdf)
pprint.pprint(tabs)
data = p.fetch_all_data(tabs)
n = len(data)
print(n)
pprint.pprint(data)