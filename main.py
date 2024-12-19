from pdf_parser import parser  # type: ignore
import pprint

from pdf_parser.config import BASE_DIR
from memory_profiler import memory_usage


def main():
    p = parser.Parser()
    with open(BASE_DIR / "tests/test_pdfs/1.pdf", "rb") as f:
        pdf = f.read()
    # pdf = 'tests/test_pdfs/1.pdf'
    data = p.proceed_pdf(pdf)
    pprint.pprint(data)
    # print(data[0].lot_data_table.lot_number)


if __name__ == "__main__":
    main()
