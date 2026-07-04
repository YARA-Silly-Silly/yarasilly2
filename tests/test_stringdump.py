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

def test_stringdump_getstrings_no_attributes(mocker):
    with tempfile.TemporaryDirectory() as tempFolder:
        file1 = os.path.join(tempFolder, "file1_empty")
        with open(file1, 'w') as f:
            f.write("")

        sd = StringDump(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'office', tempFolder, blocksize=1024)
        mock_puts = mocker.patch("pkgs.stringdump.puts")

        with pytest.raises(SystemExit) as exc:
            sd._StringDump__getStrings(file1)

        assert exc.value.code == 1
        mock_puts.assert_called_once()
        assert "No Extractable Attributes Present in" in str(mock_puts.call_args[0][0])
