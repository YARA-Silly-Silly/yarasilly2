import time
import tempfile
import os
import sys
import gc

# Suppress tqdm output
sys.stderr = open(os.devnull, 'w')

from pkgs.findfiles import FindFiles

def create_files(base_dir, num_dirs, files_per_dir):
    for i in range(num_dirs):
        dir_path = os.path.join(base_dir, f"dir_{i}")
        os.makedirs(dir_path, exist_ok=True)
        for j in range(files_per_dir):
            with open(os.path.join(dir_path, f"file_{j}.txt"), "w") as f:
                f.write("test")

def run_benchmark():
    with tempfile.TemporaryDirectory() as tmpdirname:
        sys.stdout.write("Creating files for benchmark...\n")
        sys.stdout.flush()
        create_files(tmpdirname, 500, 100) # 50,000 files

        ff = FindFiles(tmpdirname, None)

        sys.stdout.write("Running benchmark...\n")
        sys.stdout.flush()
        gc.disable()
        start_time = time.time()
        files = list(ff.searchFiles())
        end_time = time.time()
        gc.enable()

        sys.stdout.write(f"Found {len(files)} files in {end_time - start_time:.4f} seconds\n")
        sys.stdout.flush()

if __name__ == "__main__":
    run_benchmark()
