import os, hashlib

def splitDirFileName(filePath):
    return os.path.split(os.path.abspath(filePath))

def md5sum(filename):
  fh = open(filename, 'rb')
  m = hashlib.md5()
  while True:
      data = fh.read(2048)
      if not data:
          break
      m.update(data)
  return m.hexdigest()

def listdir(path):
    with os.scandir(path) as listOfEntries:
        for filename in listOfEntries:
            # print all entries that are files
            if filename.is_file():
                yield filename.path
