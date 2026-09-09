import time
import random
import string
import re

# generate random strings
num_strings = 100000
finalStringList = [''.join(random.choices(string.ascii_letters, k=10)) for _ in range(num_strings)]
regmatchList = finalStringList[:10000] * 2  # Some duplicates

print(f"List size: {len(finalStringList)}")
print(f"Matches to remove: {len(set(regmatchList))}")

# Original approach
start_time = time.time()
test_list = finalStringList.copy()
if len(regmatchList) > 0:
    for match in list(set(regmatchList)):
        test_list.remove(match)
end_time = time.time()
orig_time = end_time - start_time
print(f"Original time: {orig_time:.4f} seconds")

# Optimized approach
start_time = time.time()
test_list2 = finalStringList.copy()
if len(regmatchList) > 0:
    test_list2 = list(set(test_list2) - set(regmatchList))
end_time = time.time()
opt_time = end_time - start_time
print(f"Optimized time: {opt_time:.4f} seconds")

print(f"Improvement: {orig_time / opt_time:.2f}x faster")
