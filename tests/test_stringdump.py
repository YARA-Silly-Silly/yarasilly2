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
        sourceFile = os.path.join(tempFolder, "source.exe")
        with open(sourceFile, 'w') as f:
            f.write("ThisIsAValidStringThatIsLongEnough\nhttp://example.com\n")

        dumpFolder = os.path.join(tempFolder, "dump")
        sd = StringDump(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'office', dumpFolder, blocksize=1024)

        sd.dumpStringsToTempFile(sourceFile)

        assert os.path.exists(dumpFolder)

        # filename with . replaced by -
        expectedFileName = "source-exe"
        expectedFilePath = os.path.join(dumpFolder, expectedFileName)

        assert os.path.exists(expectedFilePath)

        with open(expectedFilePath, 'r') as f:
            content = f.read()

        assert "ThisIsAValidStringThatIsLongEnough" in content
        assert "http://example.com" in content

def test_stringdump_dumpStringsToTempFile_exception():
    with tempfile.TemporaryDirectory() as tempFolder:
        dumpFolder = os.path.join(tempFolder, "dump")
        sd = StringDump(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'office', dumpFolder, blocksize=1024)

        with pytest.raises(Exception):
            sd.dumpStringsToTempFile("non_existent_file.exe")
