import re, sys, os
from clint.textui import puts, colored

from pkgs.utils import md5sum
from pkgs.utils import splitDirFileName

class StringDump:
    _blacklist_cache = {}
    _regexblacklist_cache = {}

    def __init__(self, dirPath, fileType, tempFolder, blocksize=8192):
        self.dirPath = dirPath
        self.fileType = fileType
        self.tempFolder = tempFolder
        self.blocksize = blocksize
        self._url_pattern = re.compile(r'(?:ftp|http)[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', re.I)

        # Load and cache blacklists
        cache_key = (self.dirPath, self.fileType)
        if cache_key not in self._blacklist_cache:
            try:
                with open(os.path.join(self.dirPath, 'modules', self.fileType + '_blacklist')) as f:
                    self._blacklist_cache[cache_key] = set(f.read().splitlines())
            except FileNotFoundError:
                self._blacklist_cache[cache_key] = set()

        if cache_key not in self._regexblacklist_cache:
            try:
                with open(os.path.join(self.dirPath, 'modules', self.fileType + '_regexblacklist')) as f:
                    regBlackList = f.read().splitlines()
                    self._regexblacklist_cache[cache_key] = [re.compile(reg) for reg in regBlackList]
            except FileNotFoundError:
                self._regexblacklist_cache[cache_key] = []

    def __linkSearch(self, attachment):
        urls = list(set(self._url_pattern.findall(attachment)))
        return urls

    def __getStrings(self, filePath):
        allStrings = []
        filePointer = open(filePath,'rb')
        chars = r"A-Za-z0-9/\-:.,_$%@'()\\\{\};\]\[<> "
        regexp = '[%s]{%d,100}' % (chars, 6)
        pattern = re.compile(regexp)
        unicode_str = re.compile( r'(?:[\x20-\x7E][\x00]){6,100}',re.UNICODE )
        while True:
            data = filePointer.read(self.blocksize).decode('ISO-8859-1')
            if not data:
                break
            strlist = pattern.findall(data)
            if len(strlist)>0:
                allStrings.append(strlist)
            #Get Wide Strings
            unicodelist = list(set(unicode_str.findall(data)))
            if len(unicodelist)>0:
                allStrings.append(unicodelist)
            #Extract URLs if present
            exeurls = self.__linkSearch(data)
            if exeurls:
              for url in exeurls:
                allStrings.append(url)
        filePointer.close()
        if len(allStrings) > 0:
            return allStrings
        else:
          puts(colored.red('[!] No Extractable Attributes Present in\nFile: {}\nHash: {}\nPlease Remove it from the Sample Set and Try Again!'.format(filePath,md5sum(filePath))))
          sys.exit(1)

    def __removeBlackListStrings(self, allStrings):
        finalStringList = []
        for stringArray in allStrings:
            for str in stringArray:
                finalStringList.append(str.strip())

        cache_key = (self.dirPath, self.fileType)
        blackListSet = self._blacklist_cache.get(cache_key, set())
        regexList = self._regexblacklist_cache.get(cache_key, [])

        #Match Against Blacklist
        finalStringList = list(set(finalStringList) - blackListSet)
        #Match Against Regex Blacklist
        regmatchList = []
        for regex in regexList:
            for str in finalStringList:
                if regex.search(str): regmatchList.append(str)
        if len(regmatchList) > 0:
            for match in list(set(regmatchList)):
                finalStringList.remove(match)
        return finalStringList

    def dumpStringsToTempFile(self, filePath):
        finalStringList = self.__removeBlackListStrings(self.__getStrings(filePath))

        if not os.path.exists(self.tempFolder):
            os.makedirs(self.tempFolder)

        fileName = splitDirFileName(filePath)[1]
        tempFile = os.path.join(self.tempFolder,fileName.replace(".","-"))
        with open(tempFile, 'w') as filePointer:
            for str in finalStringList:
                filePointer.write(str+"\n")
        filePointer.close()
