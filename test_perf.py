import time
import os
import shutil
import tempfile
import sys
import gc

sys.stderr = open(os.devnull, 'w')
from pkgs.findfiles import FindFiles

def create_files(base_dir, num_dirs, files_per_dir):
    for i in range(num_dirs):
        dir_path = os.path.join(base_dir, f"dir_{i}")
        os.makedirs(dir_path, exist_ok=True)
        for j in range(files_per_dir):
            with open(os.path.join(dir_path, f"file_{j}.txt"), "w") as f:
                f.write("x")

with tempfile.TemporaryDirectory() as tmpdirname:
    create_files(tmpdirname, 500, 100)

    ff = FindFiles(tmpdirname, None)
    gc.disable()
    start = time.time()
    files = list(ff.searchFiles())
    end = time.time()
    gc.enable()
    print(f"Time: {end - start:.4f}s for {len(files)} files")
