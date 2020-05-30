import re, sys, os
from clint.textui import puts, colored
from tqdm import tqdm

from pkgs.utils import md5sum
from pkgs.utils import splitDirFileName

class StringDump:
    def __init__(self, dirPath, fileType, tempFolder, blocksize=8192):
        self.dirPath = dirPath
        self.fileType = fileType
        self.tempFolder = tempFolder
        self.blocksize = blocksize

    def __linkSearch(self, attachment):
        urls = list(set(re.compile('(?:ftp|http)[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', re.I).findall(attachment)))
        return urls

    def __getStrings(self, filePath):
        filePointer = open(filePath,'rb')
        while True:
            data = filePointer.read(self.blocksize).decode('ISO-8859-1')
            if not data:
                break
            chars = r"A-Za-z0-9/\-:.,_$%@'()\\\{\};\]\[<> "
            regexp = '[%s]{%d,100}' % (chars, 6)
            pattern = re.compile(regexp)
            strlist = pattern.findall(data)
            #Get Wide Strings
            unicode_str = re.compile( r'(?:[\x20-\x7E][\x00]){6,100}',re.UNICODE )
            unicodelist = unicode_str.findall(data)
            allStrings = unicodelist + strlist
            #Extract URLs if present
            exeurls = self.__linkSearch(data)
            if exeurls:
              for url in exeurls:
                allStrings.append(url)
        filePointer.close()
        if len(allStrings) > 0:
            return list(set(allStrings))
        else:
          puts(colored.red('[!] No Extractable Attributes Present in\nFile: {}\nHash: {}\nPlease Remove it from the Sample Set and Try Again!'.format(filePath,md5sum(filePath))))
          sys.exit(1)

    def __removeBlackListStrings(self, allStrings):
        finalStringList = []
        for str in allStrings:
            finalStringList.append(str.replace("\x00", "").strip())

        with open(self.dirPath +'/modules/'+self.fileType+'_blacklist') as f:
            blackList = f.read().splitlines()
        with open(self.dirPath +'/modules/'+self.fileType+'_regexblacklist') as f:
            regBlackList = f.read().splitlines()

        #Match Against Blacklist
        for black in blackList:
            if black in finalStringList: finalStringList.remove(black)
        #Match Against Regex Blacklist
        regmatchList = []
        for regblack in regBlackList:
            for str in finalStringList:
                regex = re.compile(regblack)
                if regex.search(str): regmatchList.append(str)
        if len(regmatchList) > 0:
            for match in list(set(regmatchList)):
                finalStringList.remove(match)
        return finalStringList

    def dumpStringsToTempFile(self, filePath):
        try:
            finalStringList = self.__removeBlackListStrings(self.__getStrings(filePath))

            if not os.path.exists(self.tempFolder):
                os.makedirs(self.tempFolder)

            fileName = splitDirFileName(filePath)[1]
            tempFile = os.path.join(self.tempFolder,fileName.replace(".","-"))
            with open(tempFile, 'w') as filePointer:
                for str in finalStringList:
                    filePointer.write(str+"\n")
            filePointer.close()

        except Exception as error:
            raise Exception(error)
            sys.exit(1)
