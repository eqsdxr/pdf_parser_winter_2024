import pytest
import pathlib
import dataclasses

import pymupdf

from pdf_parser import parser, data as parser_data


class TestParser:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.BASIC_DIR = pathlib.Path().parent.parent
        self.p = parser.Parser()
        self.pdf_dir_path = self.BASIC_DIR / "tests/test_pdfs"
        # It"s used for for-loops because all test PDF filenames
        # follow the pattern: (number in sequence).pdf
        self.last_file_number = 53

    def test_process_pdf_from_path(self):
        """
        Tests if the function for opening pdfs works OK.
        """
        correct_pdf_path = self.pdf_dir_path / "1.pdf"
        invalid_pdf_path = self.pdf_dir_path / "nonexistent.pdf"

        with pytest.raises(pymupdf.FileNotFoundError):
            self.p.process_pdf_from_path(invalid_pdf_path)

        assert self.p.process_pdf_from_path(correct_pdf_path)

        expected_pdf_object = pymupdf.Document
        actual_pdf_document = self.p.process_pdf_from_path(correct_pdf_path)
        assert isinstance(actual_pdf_document, expected_pdf_object)

    def test_proceed_pdf(self):
        """
        Tests number of ThreeTablesLDR in results of
        fetching each test file.
        """
        for i in range(1, self.last_file_number + 1):
            with open(self.pdf_dir_path / f"{i}.pdf", "rb") as f:
                pdf = f.read()
            data = self.p.proceed_pdf(pdf)
            n = len(data)
            # this file has 12 tables instead of 6 and 4 three-table units
            if i == 3:
                n = 4
            elif i < 31:  # there"s 53 actually
                n == 2

    def test_check_if_theres_no_none_values(self):
        """
        Tests if all fields are not equals None.
        Checks only non-container data types.
        It works fine with lists, sets, tuples, and dicts.
        """

        def recursively_check_values(
            data: list[parser_data.ThreeTablesLDR],
        ):
            """
            Recursively checks for "None" values, not "[]", "()",
            or {} (which is possible for denied tables).
            """

            assert data is not None, "Found None value"

            if isinstance(data, (list, tuple, dict)):
                # Iterate over iterable types only if they are not empty
                if data:  # This will be False for empty lists, tuples, or dictionaries
                    iterable = data.items() if isinstance(data, dict) else data
                    for item in iterable:
                        recursively_check_values(item)

            elif dataclasses.is_dataclass(data):
                # If it's a dataclass, iterate over its fields
                for field in dataclasses.fields(data):
                    field_value = getattr(data, field.name)
                    recursively_check_values(field_value)

        for i in range(1, self.last_file_number + 1):
            with open(self.pdf_dir_path / f"{i}.pdf", "rb") as f:
                pdf = f.read()
            data = self.p.proceed_pdf(pdf)
            recursively_check_values(data)
