import timeit
import re
import os
from pkgs.stringdump import StringDump

def run_benchmark():
    # Setup test data
    finalStringList = [f"string_{i}" for i in range(10000)]
    # Use random matches
    regBlackList = [f"^string_{i}$" for i in range(0, 10000, 200)] # 50 regexes

    def original():
        regmatchList = []
        for regblack in regBlackList:
            for s in finalStringList:
                regex = re.compile(regblack)
                if regex.search(s): regmatchList.append(s)
        return regmatchList

    def optimized():
        regmatchList = []
        for regblack in regBlackList:
            regex = re.compile(regblack)
            for s in finalStringList:
                if regex.search(s): regmatchList.append(s)
        return regmatchList

    t_orig = timeit.timeit(original, number=10)
    t_opt = timeit.timeit(optimized, number=10)
    print(f"Original code: {t_orig:.4f} seconds")
    print(f"Optimized code: {t_opt:.4f} seconds")

if __name__ == "__main__":
    run_benchmark()
