import pytest
import os
import tempfile
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

def test_stringdump_dump_strings_to_temp_file():
    with tempfile.TemporaryDirectory() as tempFolder:
        # Create a dummy module dir
        modules_dir = os.path.join(tempFolder, 'modules')
        os.makedirs(modules_dir)

        # Create blacklist files
        with open(os.path.join(modules_dir, 'office_blacklist'), 'w') as f:
            f.write("BadString\n")
        with open(os.path.join(modules_dir, 'office_regexblacklist'), 'w') as f:
            f.write("BadRegex.*\n")

        # Create a sample file
        sample_file = os.path.join(tempFolder, 'sample.bin')
        with open(sample_file, 'w') as f:
            f.write("GoodString\nBadString\nBadRegexMatched\n")

        target_temp = os.path.join(tempFolder, 'temp')

        sd = StringDump(tempFolder, 'office', target_temp, blocksize=1024)
        sd.dumpStringsToTempFile(sample_file)

        output_file = os.path.join(target_temp, 'sample-bin')
        assert os.path.exists(output_file)
        with open(output_file, 'r') as f:
            lines = f.read().splitlines()

        assert "GoodString" in lines
        assert "BadString" not in lines
        assert "BadRegexMatched" not in lines

def test_stringdump_dump_strings_to_temp_file_exception(mocker):
    with tempfile.TemporaryDirectory() as tempFolder:
        sd = StringDump(tempFolder, 'office', tempFolder, blocksize=1024)
        mocker.patch.object(sd, '_StringDump__getStrings', side_effect=Exception("Test Exception"))

        with pytest.raises(Exception, match="Test Exception"):
            sd.dumpStringsToTempFile("dummy_path")


def test_stringdump_getstrings_no_extractable(mocker):
    # Mock puts to avoid printing to stdout during tests
    mocker.patch('pkgs.stringdump.puts')

    with tempfile.TemporaryDirectory() as tempFolder:
        file_empty = os.path.join(tempFolder, "file_empty")
        with open(file_empty, 'wb') as f:
            f.write(b'\x01\x02\x03\x04\x05') # Non-printable chars

        sd = StringDump(tempFolder, 'office', tempFolder, blocksize=1024)

        with pytest.raises(SystemExit) as exc_info:
            sd._StringDump__getStrings(file_empty)

        assert exc_info.value.code == 1

def test_stringdump_getstrings_wide_strings():
    with tempfile.TemporaryDirectory() as tempFolder:
        file_wide = os.path.join(tempFolder, "file_wide")
        with open(file_wide, 'wb') as f:
            # Wide string "WideStringTest"
            wide_str = b'W\x00i\x00d\x00e\x00S\x00t\x00r\x00i\x00n\x00g\x00T\x00e\x00s\x00t\x00'
            f.write(wide_str)

        sd = StringDump(tempFolder, 'office', tempFolder, blocksize=1024)

        strings = sd._StringDump__getStrings(file_wide)
        assert len(strings) > 0

        # Look for the extracted wide string in the list
        found_wide = False
        for s_list in strings:
            if isinstance(s_list, list):
                for s in s_list:
                    if 'W\x00i\x00d\x00e\x00S\x00t\x00r\x00i\x00n\x00g\x00T\x00e\x00s\x00t\x00' in s:
                        found_wide = True
            elif isinstance(s_list, str):
                if 'W\x00i\x00d\x00e\x00S\x00t\x00r\x00i\x00n\x00g\x00T\x00e\x00s\x00t\x00' in s_list:
                    found_wide = True

        assert found_wide
