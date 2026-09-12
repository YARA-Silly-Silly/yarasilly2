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

def test_stringdump_dump_to_tempfile(mocker):
    with tempfile.TemporaryDirectory() as tempFolder:
        non_existent_temp = os.path.join(tempFolder, "new_temp")
        sd = StringDump(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'office', non_existent_temp, blocksize=1024)

        mocker.patch.object(sd, '_StringDump__getStrings', return_value=[["string1", "string2"]])
        mocker.patch.object(sd, '_StringDump__removeBlackListStrings', return_value=["string1", "string2"])

        test_file_path = "/fake/dir/test.file.name"
        sd.dumpStringsToTempFile(test_file_path)

        assert os.path.exists(non_existent_temp)

        expected_file_name = "test-file-name"
        expected_file_path = os.path.join(non_existent_temp, expected_file_name)

        assert os.path.exists(expected_file_path)

        with open(expected_file_path, 'r') as f:
            content = f.read()

        assert content == "string1\nstring2\n"
