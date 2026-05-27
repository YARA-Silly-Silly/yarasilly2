import pytest
import os
import tempfile
from pkgs.searchpattern import SearchPattern

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
        result = sp.search(file1)

        assert result == 0

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
