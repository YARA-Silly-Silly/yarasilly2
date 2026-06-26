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

def test_stringdump_dumpStringsToTempFile():
    with tempfile.TemporaryDirectory() as tempFolder:
        file1 = os.path.join(tempFolder, "file1.txt")
        with open(file1, 'w') as f:
            f.write("ThisIsAValidStringThatIsLongEnough\nhttp://example.com\n")

        out_temp = os.path.join(tempFolder, "output_temp")
        sd = StringDump(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'office', out_temp, blocksize=1024)

        sd.dumpStringsToTempFile(file1)

        expected_temp_file = os.path.join(out_temp, "file1-txt")
        assert os.path.exists(expected_temp_file)

        with open(expected_temp_file, 'r') as f:
            content = f.read().splitlines()

        assert "ThisIsAValidStringThatIsLongEnough" in content
        assert "http://example.com" in content

def test_stringdump_dumpStringsToTempFile_exception():
    with tempfile.TemporaryDirectory() as tempFolder:
        sd = StringDump(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'office', tempFolder, blocksize=1024)
        with pytest.raises(Exception):
            sd.dumpStringsToTempFile("/path/to/nonexistent/file")
