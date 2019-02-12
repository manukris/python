import hashlib

# Python program to find SHA256 hexadecimal hash string of a file
import hashlib
import os
import sqlops

class FileHash:

    def getReadableHash(self,filename):
        with open(filename, "rb") as f:
            bytes = f.read()  # read entire file as bytes
            readable_hash = hashlib.md5(bytes).hexdigest()
            return readable_hash

    def getSha256Hash(self,fileString):
        readablehash = hashlib.sha3_256(fileString).hexdigest()
        return readablehash

    def checkfolder(self,folder):
        with os.scandir(folder) as dir_entries:
            for entry in dir_entries:
                info = entry.stat()
                name = entry.name
                filename = folder +"/"+ name
                if(os.path.isdir(filename)):
                    print("folder")
                    if os.listdir(filename):
                        self.checkfolder(filename)
                    else:
                        print("empty")
                else:
                    print("file")
                    hash = self.getReadableHash(filename)
                    print(hash)
                    print(info)
                    fileString = hash + str(info.st_size) + str(info.st_mtime) + filename
                    print(fileString)
                    fileString = fileString.encode('utf-8')
                    print(fileString)
                    finalHash = self.getSha256Hash(fileString)
                    print(finalHash)
                    sqlops.sqlSignInsert(filename=name,filepath=filename,sign=finalHash,appId=1)
#OOPS OBJECT
file = FileHash()
file.checkfolder('testdir')




