import os, time, random, ppdeep, shutil
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

    def _process_confirm_file(self, traverseFilePath, refHash, filePath):
        if filePath == traverseFilePath:
            self.confirmPathFileHash.append(refHash)
            shutil.copy(traverseFilePath, self.inputFilesPath)
            return

        tmpHash = ppdeep.hash_from_file(traverseFilePath)
        if ppdeep.compare(refHash, tmpHash) >= self.confirmFilesPercent:
            self.confirmPathFileHash.append(tmpHash)
            shutil.copy(traverseFilePath, self.inputFilesPath)
        else:
            shutil.copy(traverseFilePath, self.probablePath)

    def _process_probable_file(self, traverseFilePath):
        tmpHash = ppdeep.hash_from_file(traverseFilePath)
        for fileHash in self.confirmPathFileHash:
            if ppdeep.compare(fileHash, tmpHash) >= self.probableFilesPercent:
                shutil.copy(traverseFilePath, self.inputFilesPath)
                break

    def searchFiles(self):
        try:
            if os.listdir(self.confirmPath):
                fileName = random.choice(os.listdir(self.confirmPath))
                filePath = os.path.join(self.confirmPath, fileName)
            else:
                raise Exception("Empty confirm virus sample folder.")

            print("Reference File For Fuzzy Hash: {}".format(filePath))
            refHash = ppdeep.hash_from_file(filePath)
            print("Fuzzy Hash Of Reference File: {}\n".format(refHash))
            # Preprocess the total files count
            fileCounter = 0
            for _ in listdir(self.confirmPath):
                fileCounter += 1

            if fileCounter == 1:
                self.confirmPathFileHash.append(refHash)
                shutil.copy(filePath, self.inputFilesPath)
            else:
                with tqdm(total=fileCounter, unit="files", desc="Fuzzy find in confirm path: ") as pbar:
                    for traverseFilePath in listdir(self.confirmPath):
                        pbar.update(1)
                        pbar.set_postfix(file=traverseFilePath.split(os.path.sep)[-1:])
                        self._process_confirm_file(traverseFilePath, refHash, filePath)
            print("\n")

            fileCounter = 0
            for _ in listdir(self.probablePath):
                fileCounter += 1

            if fileCounter == 0:
                raise Exception("Empty probable virus sample folder.")
            else:
                with tqdm(total=fileCounter, unit="files", desc="Fuzzy find in probable path: ") as pbar:
                    for traverseFilePath in listdir(self.probablePath):
                        pbar.update(1)
                        pbar.set_postfix(file=traverseFilePath.split(os.path.sep)[-1:])
                        self._process_probable_file(traverseFilePath)
            print("\n")
        except Exception as error:
            raise Exception(error)
            sys.exit(1)
