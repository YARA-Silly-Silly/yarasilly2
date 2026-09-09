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


def test_stringdump_dumpStringsToTempFile(mocker):
    with tempfile.TemporaryDirectory() as baseFolder:
        file1 = os.path.join(baseFolder, "test.file.txt")
        # Ensure the temp folder does not exist initially to test os.makedirs
        tempFolder = os.path.join(baseFolder, "new_temp_dir")

        sd = StringDump(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'office', tempFolder, blocksize=1024)

        # Mock internal methods to isolate dump logic
        mock_get = mocker.patch.object(sd, '_StringDump__getStrings', return_value=[["ExtractedString1", "ExtractedString2"]])
        mock_remove = mocker.patch.object(sd, '_StringDump__removeBlackListStrings', return_value=["FilteredString1", "FilteredString2"])

        # Temp folder should not exist before calling
        assert not os.path.exists(tempFolder)

        sd.dumpStringsToTempFile(file1)

        mock_get.assert_called_once_with(file1)
        mock_remove.assert_called_once_with([["ExtractedString1", "ExtractedString2"]])

        # Folder should be created
        assert os.path.exists(tempFolder)

        # File name should replace . with -
        expected_file = os.path.join(tempFolder, "test-file-txt")
        assert os.path.exists(expected_file)

        with open(expected_file, 'r') as f:
            content = f.read()

        assert content == "FilteredString1\nFilteredString2\n"

def test_stringdump_dumpStringsToTempFile_existing_dir(mocker):
    with tempfile.TemporaryDirectory() as baseFolder:
        file1 = os.path.join(baseFolder, "test.file.txt")
        tempFolder = os.path.join(baseFolder, "existing_temp_dir")
        os.makedirs(tempFolder)

        sd = StringDump(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'office', tempFolder, blocksize=1024)

        mocker.patch.object(sd, '_StringDump__getStrings', return_value=[])
        mocker.patch.object(sd, '_StringDump__removeBlackListStrings', return_value=["OnlyOneString"])

        sd.dumpStringsToTempFile(file1)

        expected_file = os.path.join(tempFolder, "test-file-txt")
        assert os.path.exists(expected_file)

        with open(expected_file, 'r') as f:
            content = f.read()

        assert content == "OnlyOneString\n"
