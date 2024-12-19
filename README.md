# Usage

Usage example:
```python

from pdf_parser.config import BASE_DIR

p = parser.Parser()
pdf_path = BASE_DIR / "tests" / "test_pdfs" / "sth.pdf"
data = p.proceed_pdf(pdf)
pprint.pprint(data)
# or data[0].result_table[0].date_time
```


To run tests use:
```
pytest
```
