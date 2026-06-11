import pytest
import os
import tempfile
from pkgs.utils import splitDirFileName, sha256sum, listdir

def test_splitDirFileName():
    path = "/path/to/my/file.txt"
    dir_name, file_name = splitDirFileName(path)
    assert dir_name == "/path/to/my"
    assert file_name == "file.txt"

def test_sha256sum():
    with tempfile.NamedTemporaryFile(delete=False) as f:
        f.write(b"hello world")
        temp_path = f.name

    # sha256 of "hello world" is b94d27b9934d3e08a52e52d7da7dabfac484efe37a5380ee9088f7ace2efcde9
    assert sha256sum(temp_path) == "b94d27b9934d3e08a52e52d7da7dabfac484efe37a5380ee9088f7ace2efcde9"
    os.remove(temp_path)

def test_listdir():
    with tempfile.TemporaryDirectory() as tmpdirname:
        # Create some files
        with open(os.path.join(tmpdirname, "file1.txt"), "w") as f:
            f.write("test")
        with open(os.path.join(tmpdirname, "file2.txt"), "w") as f:
            f.write("test")

        # Create a directory (should be ignored by listdir)
        os.mkdir(os.path.join(tmpdirname, "dir1"))

        files = list(listdir(tmpdirname))
        assert len(files) == 2
        assert any(f.endswith("file1.txt") for f in files)
        assert any(f.endswith("file2.txt") for f in files)
