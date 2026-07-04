import time
import os
import shutil
import ppdeep
from pkgs.fuzzymatch import FuzzyMatch

def run_bench():
    os.makedirs("bench_confirm", exist_ok=True)
    os.makedirs("bench_probable", exist_ok=True)
    os.makedirs("bench_input", exist_ok=True)

    # We want a lot of files to be copied from confirm to probable
    # so that the rehashing cost is obvious.
    # Create 200 files in confirm
    content = b"A" * 1024 * 50 # 50 KB
    for i in range(200):
        # We need them to be different enough so they don't match the reference hash
        with open(f"bench_confirm/file_{i}.bin", "wb") as f:
            f.write(content + os.urandom(1024) + str(i).encode())

    # And 50 files already in probable
    for i in range(200, 250):
        with open(f"bench_probable/file_{i}.bin", "wb") as f:
            f.write(content + os.urandom(1024) + str(i).encode())

    # Ensure FuzzyMatch uses empty confirmPathFileHash for accurate run
    FuzzyMatch.confirmPathFileHash = []

    fm = FuzzyMatch("bench_confirm", 99, "bench_probable", 99, "bench_input")
    start = time.time()
    fm.searchFiles()
    end = time.time()

    shutil.rmtree("bench_confirm", ignore_errors=True)
    shutil.rmtree("bench_probable", ignore_errors=True)
    shutil.rmtree("bench_input", ignore_errors=True)

    print(f"\n--- BENCHMARK TIME: {end - start:.4f}s ---")

if __name__ == "__main__":
    run_bench()
