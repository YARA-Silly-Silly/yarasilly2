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
