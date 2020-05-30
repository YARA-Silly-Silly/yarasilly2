import os, time
from tqdm import tqdm

from pkgs.utils import listdir

class FindFiles:

    fileArray = []
    fileHash = []

    def __init__(self,inputFilesPath,folderDepth):
        self.inputFilesPath = inputFilesPath
        self.folderDepth = folderDepth

    def __walk(self, path='.', depth=None):
        if depth and depth == 1:
            for filename in listdir(path):
                yield filename
        else:
            top_pathlen = len(path) + len(os.path.sep)
            for dirpath, dirnames, filenames in os.walk(path):
                dirlevel = dirpath[top_pathlen:].count(os.path.sep)
                if depth != None and dirlevel >= depth-1:
                    # dirnames[:] = []
                    break
                else:
                    for filename in filenames:
                        yield os.path.join(dirpath, filename)

    def searchFiles(self):
        try:
            # Preprocess the total files count
            fileCounter = 0
            for filePath in self.__walk(self.inputFilesPath, self.folderDepth):
                fileCounter += 1
            with tqdm(total=fileCounter, unit="files", desc="Searching Files And Dumping Strings: ") as pbar:
                for filePath in self.__walk(self.inputFilesPath, self.folderDepth):
                    pbar.update(1)
                    pbar.set_postfix(file=filePath.split(os.path.sep)[-1:])
                    yield filePath
            print("\n")

        except Exception as error:            
            raise Exception(error)
            sys.exit(1)
