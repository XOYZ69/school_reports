from modules.error_handling import Error
from modules.format.string import colorize, cutoff_filename, escape_latex_special_chars, fit, format_bytes

class TestStringFunctions:
    def test_colorizing(self):
        assert colorize('<color:red>A Text<color:end>') == '\\textcolor{red}{A Text}'
    
    def test_pathname_from_filepath(self):
        assert cutoff_filename('C:\\test\\2.txt') == 'C:/test/'
        assert cutoff_filename('C:\\test\\2') == 'C:/test/'
    
    def test_escape_latex_special_characters(self):
        assert escape_latex_special_chars('#') == '\\#'
    
    def test_fit(self):
        assert fit(5, 5, '0', False) == '00005'
        assert fit(5, 5) == '5....'
        assert fit('Testing something', 30, '') == 'Testing something             '
    
    def test_format_bytes(self):
        assert format_bytes(1000) == '1000 B'
        assert format_bytes(4096) == '4.0 KB'
        assert format_bytes(1024 ** 4, 0) == '1024.0 GB'
