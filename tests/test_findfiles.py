import pytest
import os
import tempfile
from pkgs.findfiles import FindFiles

def test_findfiles_all_depth():
    with tempfile.TemporaryDirectory() as tmpdirname:
        # create some files at different depths
        open(os.path.join(tmpdirname, "file1.txt"), 'w').close()

        dir1 = os.path.join(tmpdirname, "dir1")
        os.mkdir(dir1)
        open(os.path.join(dir1, "file2.txt"), 'w').close()

        dir2 = os.path.join(dir1, "dir2")
        os.mkdir(dir2)
        open(os.path.join(dir2, "file3.txt"), 'w').close()

        ff = FindFiles(tmpdirname, None)
        files = list(ff.searchFiles())

        assert len(files) == 3
        assert any(f.endswith("file1.txt") for f in files)
        assert any(f.endswith("file2.txt") for f in files)
        assert any(f.endswith("file3.txt") for f in files)

import types

def test_searchfiles_returns_generator():
    with tempfile.TemporaryDirectory() as tmpdirname:
        open(os.path.join(tmpdirname, "file1.txt"), 'w').close()

        dir1 = os.path.join(tmpdirname, "dir1")
        os.mkdir(dir1)
        open(os.path.join(dir1, "file2.txt"), 'w').close()

        ff = FindFiles(tmpdirname, None)
        gen = ff.searchFiles()

        assert isinstance(gen, types.GeneratorType)

        files = list(gen)
        assert len(files) == 2
        assert any(f.endswith("file1.txt") for f in files)
        assert any(f.endswith("file2.txt") for f in files)

def test_searchfiles_exception():
    # Pass an integer which will throw an exception when __walk tries to len(path)
    # in top_pathlen = len(path) + len(os.path.sep)
    ff = FindFiles(123, 2)

    with pytest.raises(Exception):
        # We need to iterate over the generator to trigger the exception
        list(ff.searchFiles())

def test_findfiles_depth_1():
    with tempfile.TemporaryDirectory() as tmpdirname:
        open(os.path.join(tmpdirname, "file1.txt"), 'w').close()
        dir1 = os.path.join(tmpdirname, "dir1")
        os.mkdir(dir1)
        open(os.path.join(dir1, "file2.txt"), 'w').close()

        ff = FindFiles(tmpdirname, 1)
        files = list(ff.searchFiles())

        assert len(files) == 1
        assert any(f.endswith("file1.txt") for f in files)

def test_findfiles_depth_2():
    with tempfile.TemporaryDirectory() as tmpdirname:
        open(os.path.join(tmpdirname, "file1.txt"), 'w').close()

        dir1 = os.path.join(tmpdirname, "dir1")
        os.mkdir(dir1)
        open(os.path.join(dir1, "file2.txt"), 'w').close()

        dir2 = os.path.join(dir1, "dir2")
        os.mkdir(dir2)
        open(os.path.join(dir2, "file3.txt"), 'w').close()

        ff = FindFiles(tmpdirname, 2)
        files = list(ff.searchFiles())

        assert len(files) == 2
        assert any(f.endswith("file1.txt") for f in files)
        assert any(f.endswith("file2.txt") for f in files)
