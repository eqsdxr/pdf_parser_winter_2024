from pdf_parser import extractor, parser # type: ignore
import pprint


path = 'tests\\test_pdfs\\1.pdf'
e = extractor.Extractor(path)
pdf = e.open_pdf()

p = parser.Parser(pdf)
tables = p.extract_tables_from_pdf()
# pprint.pprint(tables)
results = p.get_results_tables()
pprint.pprint(results)
