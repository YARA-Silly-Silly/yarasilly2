from pkgs.utils import listdir
import tempfile
import os
with tempfile.TemporaryDirectory() as tempFolder:
    file_path = os.path.join(tempFolder, "test")
    with open(file_path, 'w') as f: f.write("test")
    for f in listdir(tempFolder):
        print("LISTDIR YIELDS:", f)
