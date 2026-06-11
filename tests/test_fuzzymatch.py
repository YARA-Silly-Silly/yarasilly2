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

def test_fuzzymatch_empty_probable():
    with tempfile.TemporaryDirectory() as confirmPath, \
         tempfile.TemporaryDirectory() as probablePath, \
         tempfile.TemporaryDirectory() as inputFilesPath:

        # Create a dummy file in confirmPath
        dummy_file_path = os.path.join(confirmPath, "dummy.txt")
        with open(dummy_file_path, "w") as f:
            f.write("dummy content for ppdeep hashing")

        fm = FuzzyMatch(confirmPath, 80, probablePath, 60, inputFilesPath)
        with pytest.raises(Exception, match="Empty probable virus sample folder."):
            fm.searchFiles()
