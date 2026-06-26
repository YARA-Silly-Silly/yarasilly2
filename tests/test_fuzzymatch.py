import pytest
import os
import tempfile
import ppdeep
from pkgs.fuzzymatch import FuzzyMatch

def test_fuzzymatch_empty_confirm():
    with tempfile.TemporaryDirectory() as confirmPath, \
         tempfile.TemporaryDirectory() as probablePath, \
         tempfile.TemporaryDirectory() as inputFilesPath:

        fm = FuzzyMatch(confirmPath, 80, probablePath, 60, inputFilesPath)
        with pytest.raises(Exception, match="Empty confirm virus sample folder."):
            fm.searchFiles()

def test_fuzzymatch_single_file(mocker):
    with tempfile.TemporaryDirectory() as confirmPath, \
         tempfile.TemporaryDirectory() as probablePath, \
         tempfile.TemporaryDirectory() as inputFilesPath:

        file1_path = os.path.join(confirmPath, "file1.txt")
        with open(file1_path, "w") as f:
            f.write("content")

        probable_file_path = os.path.join(probablePath, "prob1.txt")
        with open(probable_file_path, "w") as f:
            f.write("probable")

        FuzzyMatch.confirmPathFileHash = []

        mocker.patch("random.choice", return_value="file1.txt")
        mocker.patch("ppdeep.hash_from_file", return_value="hash1")
        mocker.patch("ppdeep.compare", return_value=100)

        fm = FuzzyMatch(confirmPath, 80, probablePath, 60, inputFilesPath)
        fm.searchFiles()

        assert "hash1" in FuzzyMatch.confirmPathFileHash
        assert "file1.txt" in os.listdir(inputFilesPath)
        assert "prob1.txt" in os.listdir(inputFilesPath)

def test_fuzzymatch_multiple_files(mocker):
    with tempfile.TemporaryDirectory() as confirmPath, \
         tempfile.TemporaryDirectory() as probablePath, \
         tempfile.TemporaryDirectory() as inputFilesPath:

        file1_path = os.path.join(confirmPath, "file1.txt")
        file2_path = os.path.join(confirmPath, "file2.txt")
        file3_path = os.path.join(confirmPath, "file3.txt")

        with open(file1_path, "w") as f: f.write("content1")
        with open(file2_path, "w") as f: f.write("content2")
        with open(file3_path, "w") as f: f.write("content3")

        FuzzyMatch.confirmPathFileHash = []

        mocker.patch("random.choice", return_value="file1.txt")

        def hash_mock(filepath):
            if "file1" in filepath: return "hash1"
            elif "file2" in filepath: return "hash2"
            elif "file3" in filepath: return "hash3"
            return "unknown"

        mocker.patch("ppdeep.hash_from_file", side_effect=hash_mock)

        def compare_mock(h1, h2):
            if h1 == h2: return 100
            if h1 == "hash1" and h2 == "hash2": return 90
            if h1 == "hash1" and h2 == "hash3": return 70
            return 0

        mocker.patch("ppdeep.compare", side_effect=compare_mock)

        fm = FuzzyMatch(confirmPath, 80, probablePath, 60, inputFilesPath)
        fm.searchFiles()

        assert "hash1" in FuzzyMatch.confirmPathFileHash
        assert "hash2" in FuzzyMatch.confirmPathFileHash
        assert "hash3" not in FuzzyMatch.confirmPathFileHash

        input_files = os.listdir(inputFilesPath)
        assert "file1.txt" in input_files
        assert "file2.txt" in input_files
        assert "file3.txt" in input_files
