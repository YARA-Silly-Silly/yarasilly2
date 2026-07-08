import pytest
import os
import tempfile
from pkgs.utils import splitDirFileName, md5sum, listdir

def test_splitDirFileName():
    path = "/path/to/my/file.txt"
    dir_name, file_name = splitDirFileName(path)
    assert dir_name == "/path/to/my"
    assert file_name == "file.txt"

def test_md5sum():
    with tempfile.NamedTemporaryFile(delete=False) as f:
        f.write(b"hello world")
        temp_path = f.name

    # md5 of "hello world" is 5eb63bbbe01eeed093cb22bb8f5acdc3
    assert md5sum(temp_path) == "5eb63bbbe01eeed093cb22bb8f5acdc3"
    os.remove(temp_path)

def test_md5sum_file_not_found():
    with pytest.raises(FileNotFoundError):
        md5sum("non_existent_file.txt")

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
