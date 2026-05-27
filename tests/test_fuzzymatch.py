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

        # Create a file in confirmPath to pass the first check
        with open(os.path.join(confirmPath, "test_file.txt"), "w") as f:
            f.write("dummy content")

        fm = FuzzyMatch(confirmPath, 80, probablePath, 60, inputFilesPath)
        with pytest.raises(Exception, match="Empty probable virus sample folder."):
            fm.searchFiles()
