import pytest

from pdf_parser.utils import check_data, cast_to_int_float

class TestUtils:
    def test_check_data(self):
        with pytest.raises(Exception):
            check_data('string')
        with pytest.raises(Exception):
            check_data(93048)
        with pytest.raises(Exception):
            check_data([1, 2, 3])

    def test_cast_to_int_float(self):
        assert cast_to_int_float('0') == 0
        assert cast_to_int_float('238756') == 238756
        assert cast_to_int_float('1000000000000') == 1000000000000
        assert cast_to_int_float('0.8732487') == 0.8732487
        assert cast_to_int_float('235458.37') == 235458.37
        assert cast_to_int_float('23457548975348957.3734') == 23457548975348957.3734
        assert cast_to_int_float('235458.37') == 235458.37

 