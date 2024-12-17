import pytest
from pathlib import Path
import pymupdf

from dataclasses import fields, is_dataclass

from pdf_parser import parser, data as data_module

import pprint


class TestParser:

    @pytest.fixture(autouse=True)
    def setup(self):
        self.BASIC_DIR = Path().parent.parent
        self.p = parser.Parser()
        self.pdf_dir_path = self.BASIC_DIR / 'tests/test_pdfs'
        # It's used for for-loops because all test PDF filenames
        # follow the pattern: (number in sequence).pdf
        self.last_file_number = 53
    def test_open_pdf(self):
        '''
        Tests if the function for opening pdfs works OK.
        '''
        correct_pdf_path = self.pdf_dir_path / '1.pdf'
        invalid_pdf_path = self.pdf_dir_path / 'nonexistent.pdf'

        with pytest.raises(pymupdf.FileNotFoundError):
            self.p.open_pdf(invalid_pdf_path)

        assert self.p.open_pdf(correct_pdf_path)

        expected_pdf_object = pymupdf.Document
        actual_pdf_document = self.p.open_pdf(correct_pdf_path)
        assert isinstance(actual_pdf_document, expected_pdf_object)

    def test_fetch_all_data(self):
        '''
        Tests number of ThreeTablesLDR in results of 
        fetching each test file.
        '''
        for i in range(1, self.last_file_number + 1):
            pdf = self.p.open_pdf(self.pdf_dir_path / f'{i}.pdf')
            tables = self.p.extract_tables_from_pdf(pdf)
            data = self.p.fetch_all_data(tables)
            n = len(data)
            if i == 3: # this file has 12 tables instead of 6 and 4 three-table units
                n = 4
            elif i < 31: # needs to be increased
                n == 2


    def test_check_if_theres_no_none_values(self):
        '''
        Tests if all fields are not equals None.
        Checks only non-container data types.
        It works fine with lists, sets, tuples, and dicts.
        '''

        def recursively_check_values(data):
            '''
            Recursively checks for "None" values, not "[]", "()",
            or {} (which is possible for denied tables).
            '''

            assert data is not None, f"Found None value"

            if isinstance(data, (list, tuple, dict)):
                # Iterate over iterable types only if they are not empty
                if data:  # This will be False for empty lists, tuples, or dictionaries
                    iterable = data.items() if isinstance(data, dict) else data
                    for item in iterable:
                        recursively_check_values(item)

            elif is_dataclass(data):
                # It's a dataclass, iterate over its fields
                for field in fields(data):
                    field_value = getattr(data, field.name)
                    recursively_check_values(field_value)
                
        for i in range(1, self.last_file_number + 1):
            pdf = self.p.open_pdf(self.pdf_dir_path / f'{i}.pdf')
            tables = self.p.extract_tables_from_pdf(pdf)
            data = self.p.fetch_all_data(tables)
            recursively_check_values(data)

    # def test_check_amount_of_tables(self):
    #     '''
    #     Checks amount of tables in files. It's important because of
    #     the fact that there may be empty tables.
    #     '''
                
        