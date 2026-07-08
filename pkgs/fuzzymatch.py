import os, random, ppdeep, shutil
from tqdm import tqdm

from pkgs.utils import listdir

class FuzzyMatch:

    confirmPathFileHash = []

    def __init__(self, confirmPath, confirmFilesPercent, probablePath, probableFilesPercent, inputFilesPath):
        self.confirmPath = confirmPath
        self.confirmFilesPercent = confirmFilesPercent
        self.probablePath = probablePath
        self.probableFilesPercent = probableFilesPercent
        self.inputFilesPath = inputFilesPath

    def searchFiles(self):
        if os.listdir(self.confirmPath):
            fileName = random.choice(os.listdir(self.confirmPath))
            filePath = os.path.join(self.confirmPath, fileName)
        else:
            raise Exception("Empty confirm virus sample folder.")

        print("Reference File For Fuzzy Hash: {}".format(filePath))
        refHash = ppdeep.hash_from_file(filePath)
        print("Fuzzy Hash Of Reference File: {}\n".format(refHash))
        # Preprocess the total files count
        confirm_files = list(listdir(self.confirmPath))
        fileCounter = len(confirm_files)

        if fileCounter == 1:
            self.confirmPathFileHash.append(refHash)
            shutil.copy(confirm_files[0], self.inputFilesPath)
        else:
            with tqdm(total=fileCounter, unit="files", desc="Fuzzy find in confirm path: ") as pbar:
                for traverseFilePath in confirm_files:
                    pbar.update(1)
                    pbar.set_postfix(file=traverseFilePath.split(os.path.sep)[-1:])
                    if filePath == traverseFilePath:
                        self.confirmPathFileHash.append(refHash)
                        shutil.copy(traverseFilePath, self.inputFilesPath)
                        continue
                    tmpHash = ppdeep.hash_from_file(traverseFilePath)
                    # print("File: ", traverseFilePath, " - ", ppdeep.compare(refHash, tmpHash))
                    if ppdeep.compare(refHash, tmpHash) >= self.confirmFilesPercent:
                        self.confirmPathFileHash.append(tmpHash)
                        shutil.copy(traverseFilePath, self.inputFilesPath)
                    else:
                        shutil.copy(traverseFilePath, self.probablePath)
        print("\n")

        probable_files = list(listdir(self.probablePath))
        fileCounter = len(probable_files)

        if fileCounter == 0:
            raise Exception("Empty probable virus sample folder.")
        else:
            with tqdm(total=fileCounter, unit="files", desc="Fuzzy find in probable path: ") as pbar:
                for traverseFilePath in probable_files:
                    pbar.update(1)
                    pbar.set_postfix(file=traverseFilePath.split(os.path.sep)[-1:])
                    tmpHash = ppdeep.hash_from_file(traverseFilePath)
                    for fileHash in self.confirmPathFileHash:
                        # print("File: ", traverseFilePath, " - ", ppdeep.compare(refHash, tmpHash))
                        if ppdeep.compare(fileHash, tmpHash) >= self.probableFilesPercent:
                            shutil.copy(traverseFilePath, self.inputFilesPath)
                            break
        print("\n")
