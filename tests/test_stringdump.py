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
