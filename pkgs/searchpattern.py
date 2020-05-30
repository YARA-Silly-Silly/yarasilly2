import os
from tqdm import tqdm

from pkgs.utils import listdir

class SearchPattern:
    foundPattern = 0

    def __init__(self,tempFolder,matchPatternFilePath,occurance=5, blocksize=2048):
        self.tempFolder = tempFolder
        self.matchPatternFilePath = matchPatternFilePath
        self.occurance = occurance
        self.blocksize = blocksize

    def __checkPatternPresent(self, writeFilePointer, stringPattern):
        writeFilePointer.seek(0)
        buf = 1
        while (buf):
            buf = writeFilePointer.read(self.blocksize).splitlines()
            for str in buf:
                if stringPattern in str.split("-"):
                    return False
        return True

    def __checkIfStringInFile(self, file, stringToSearch):
        count = 1

        for fileCmp in listdir(self.tempFolder):
            if fileCmp == file:
                continue
            with open(fileCmp, 'r') as filePointer:
                buf = 1
                while (buf):
                    buf = filePointer.read(self.blocksize).splitlines()
                    if stringToSearch in buf:
                        count+=1
            filePointer.close()
        return count

    def search(self, file):
        try:
            # Preprocess the total file size
            sizeCounter = os.stat(file).st_size

            writeFilePointer = open(self.matchPatternFilePath, 'w+')

            with tqdm(total=sizeCounter,
                      unit='B', unit_scale=True, unit_divisor=1024, desc="Searching For Pattern Match: ") as pbar:
                with open(file, 'r') as filePointer:
                    buf = 1
                    while (buf):
                        buf = filePointer.read(self.blocksize)
                        for stringPattern in buf.splitlines():
                            if not stringPattern.strip():
                                continue
                            if self.__checkPatternPresent(writeFilePointer, stringPattern):
                                match = self.__checkIfStringInFile(file, stringPattern)
                                if match>=self.occurance:
                                    self.foundPattern = 1
                                    writeFilePointer.seek(0, 2)
                                    writeFilePointer.write(str(match) + "-" + stringPattern.strip() + "\n")
                        if buf:
                            pbar.set_postfix(file=file)
                            pbar.update(len(buf))
                filePointer.close()
            writeFilePointer.close()
            print("\n")
            return(self.foundPattern)
        except Exception as error:
            raise Exception(error)
            sys.exit(1)
