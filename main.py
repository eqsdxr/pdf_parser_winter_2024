from pdf_parser import parser # type: ignore
import pprint

import json

from pdf_parser.config import BASE_DIR

from memory_profiler import memory_usage


p = parser.Parser()
pdf_path = BASE_DIR / 'tests' / 'test_pdfs'
data = []
for i in range(1, 54):
    pdf = pdf_path / f'{i}.pdf'
    data = p.proceed_pdf(pdf)
    # pprint.pprint(data)
    print(data[0].lot_data_table.lot_number)
# time