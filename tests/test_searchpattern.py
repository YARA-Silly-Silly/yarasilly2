import pytest
import os
import tempfile
from pkgs.searchpattern import SearchPattern

def test_preload_files(mocker):
    with tempfile.TemporaryDirectory() as tempFolder:
        # Create dummy files
        file1 = os.path.join(tempFolder, "file1")
        with open(file1, 'w') as f:
            f.write("line1\nline2\nline3")

        file2 = os.path.join(tempFolder, "file2")
        with open(file2, 'w') as f:
            f.write("line4\nline5")

        file3 = os.path.join(tempFolder, "file3")
        with open(file3, 'w') as f:
            f.write("") # Empty file

        # The actual function uses utils.listdir which returns absolute paths. We just need to ensure
        # that os.listdir or whatever is mocked correctly or test directory works correctly.
        # Actually searchpattern's listdir uses scandir yielding path, which is full path.
        sp = SearchPattern(tempFolder, "dummy_pattern.txt")
        sp._preload_files()

        assert file1 in sp._file_contents
        assert file2 in sp._file_contents
        assert file3 in sp._file_contents

        # Verify the sets have the correct elements
        assert {"line1", "line2", "line3"} == sp._file_contents[file1]
        assert {"line4", "line5"} == sp._file_contents[file2]
        assert set() == sp._file_contents[file3]


def test_searchpattern_match():
    with tempfile.TemporaryDirectory() as tempFolder:
        # Create matched pattern file
        match_pattern_file = os.path.join(tempFolder, "matched-pattern.txt")

        # Create test files
        file1 = os.path.join(tempFolder, "file1")
        with open(file1, 'w') as f:
            f.write("test_string\nother_string\n")

        file2 = os.path.join(tempFolder, "file2")
        with open(file2, 'w') as f:
            f.write("test_string\nanother_string\n")

        sp = SearchPattern(tempFolder, match_pattern_file, occurance=2, blocksize=1024)
        sp._preload_files()
        result = sp.search(file1)

        assert result == 1
        with open(match_pattern_file, 'r') as f:
            content = f.read()
            assert "2-test_string" in content

def test_searchpattern_no_match():
    with tempfile.TemporaryDirectory() as tempFolder:
        match_pattern_file = os.path.join(tempFolder, "matched-pattern.txt")

        file1 = os.path.join(tempFolder, "file1")
        with open(file1, 'w') as f:
            f.write("test_string\nother_string\n")

        file2 = os.path.join(tempFolder, "file2")
        with open(file2, 'w') as f:
            f.write("another_string\nyet_another\n")

        sp = SearchPattern(tempFolder, match_pattern_file, occurance=2, blocksize=1024)
        sp._preload_files()
        result = sp.search(file1)

        assert result == 0

def test_preload_files():
    with tempfile.TemporaryDirectory() as tempFolder:
        match_pattern_file = os.path.join(tempFolder, "matched-pattern.txt")

        file1 = os.path.join(tempFolder, "file1")
        with open(file1, 'w') as f:
            f.write("line_one\nline_two\n")

        file2 = os.path.join(tempFolder, "file2")
        with open(file2, 'w') as f:
            f.write("another_string\n")

        # Test with a large blocksize (entire file in one read)
        sp = SearchPattern(tempFolder, match_pattern_file, occurance=2, blocksize=1024)
        sp._preload_files()

        assert len(sp._file_contents) == 2
        assert sp._file_contents[file1] == {"line_one", "line_two"}
        assert sp._file_contents[file2] == {"another_string"}

        # Test with a small blocksize (multiple reads)
        # file2 "another_string\n" -> 15 chars
        # If we read 8 bytes at a time:
        # read 1: "another_" -> ["another_"]
        # read 2: "string\n" -> ["string"]
        sp_small = SearchPattern(tempFolder, match_pattern_file, occurance=2, blocksize=8)
        sp_small._preload_files()

        assert sp_small._file_contents[file2] == {"another_", "string"}

def test_checkIfStringInFile():
    with tempfile.TemporaryDirectory() as tempFolder:
        match_pattern_file = os.path.join(tempFolder, "matched-pattern.txt")

        # The file that is currently being evaluated
        main_file = os.path.join(tempFolder, "main_file")
        with open(main_file, 'w') as f:
            f.write("unique_string_1\ncommon_string\n")

        # A file that has the string
        file_with_string = os.path.join(tempFolder, "file_with_string")
        with open(file_with_string, 'w') as f:
            f.write("some_other_string\ncommon_string\n")

        # A file that does not have the string
        file_without_string = os.path.join(tempFolder, "file_without_string")
        with open(file_without_string, 'w') as f:
            f.write("irrelevant_data\nmore_data\n")

        # Also create a file that has the string MULTIPLE times, but count should only increment by 1 for this file
        # according to the implementation if it exists anywhere in the file.
        file_with_string_multiple = os.path.join(tempFolder, "file_with_string_multiple")
        with open(file_with_string_multiple, 'w') as f:
            f.write("common_string\ncommon_string\ncommon_string\n")

        sp = SearchPattern(tempFolder, match_pattern_file, occurance=2, blocksize=1024)
        sp._preload_files()

        # Test finding "common_string"
        # It starts with count = 1.
        # It checks file_with_string (has it -> count = 2)
        # It checks file_without_string (doesn't have it)
        # It checks file_with_string_multiple (has it -> count = 3)
        # The total count should be 3.
        count = sp._SearchPattern__checkIfStringInFile(main_file, "common_string")
        assert count == 3

        # Test finding a string that is only in the main_file
        count_unique = sp._SearchPattern__checkIfStringInFile(main_file, "unique_string_1")
        assert count_unique == 1
