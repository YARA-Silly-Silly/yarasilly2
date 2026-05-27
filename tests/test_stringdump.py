import pytest
import os
import tempfile
from unittest.mock import patch, mock_open
from pkgs.stringdump import StringDump

def test_stringdump_getstrings():
    with tempfile.TemporaryDirectory() as tempFolder:
        file1 = os.path.join(tempFolder, "file1")
        with open(file1, 'w') as f:
            f.write("ThisIsAValidStringThatIsLongEnough\nhttp://example.com\n")

        sd = StringDump(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'office', tempFolder, blocksize=1024)

        # Test __getStrings (private method, so need name mangling)
        strings = sd._StringDump__getStrings(file1)
        assert len(strings) > 0

        # Test url extraction
        assert any("http://example.com" in s for s in strings if isinstance(s, str))

@patch('builtins.open')
def test_remove_blacklist_strings(mock_open_func):
    sd = StringDump('/fake_dir', 'office', '/fake_temp', blocksize=1024)

    def mock_open_side_effect(filename, *args, **kwargs):
        if filename.endswith('_blacklist'):
            return mock_open(read_data="blacklisted_word\nanother_blacklisted\n").return_value
        elif filename.endswith('_regexblacklist'):
            return mock_open(read_data="^regex_match_.*\n.*_regex_end$\n").return_value
        else:
            return mock_open(read_data="").return_value

    mock_open_func.side_effect = mock_open_side_effect

    input_strings = [
        ['  hello  ', 'world'],
        ['blacklisted_word', 'keep_me'],
        ['regex_match_123', 'normal_regex_end'],
        ['valid_string']
    ]

    result = sd._StringDump__removeBlackListStrings(input_strings)

    assert 'hello' in result
    assert 'world' in result
    assert 'keep_me' in result
    assert 'valid_string' in result
    assert 'blacklisted_word' not in result
    assert 'regex_match_123' not in result
    assert 'normal_regex_end' not in result
