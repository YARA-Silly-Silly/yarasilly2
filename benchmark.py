import time
import os
from pkgs.searchpattern import SearchPattern

# Create some dummy files
os.makedirs("temp", exist_ok=True)
with open("temp/file1.txt", "w") as f:
    for i in range(1000):
        f.write(f"pattern{i}\n")
with open("temp/file2.txt", "w") as f:
    for i in range(1000):
        f.write(f"pattern{i}\n")
with open("temp/file3.txt", "w") as f:
    for i in range(1000):
        f.write(f"pattern{i}\n")

with open("testfile.txt", "w") as f:
    for _ in range(5):
        for i in range(1000):
            f.write(f"pattern{i}\n")

sp = SearchPattern("temp", "match.txt", occurance=2)

start = time.time()
sp.search("testfile.txt")
end = time.time()

print(f"Time taken: {end - start:.4f} seconds")

# Cleanup
os.remove("testfile.txt")
for i in range(1, 4):
    os.remove(f"temp/file{i}.txt")
os.rmdir("temp")
os.remove("match.txt")
