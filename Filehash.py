# Python program to find SHA256 hexadecimal hash string of a file
import hashlib
import os
from sqlops import Sqlops

class FileHash:
    filecount = 0 # set filecount to zero
    fileDict = {}

    #computes md5 hash of a file
    def getReadableHash(self,filename):
        with open(filename, "rb") as f:
            bytes = f.read()
            readable_hash = hashlib.md5(bytes).hexdigest()
            return readable_hash

    # computes sha256 of file string
    def getSha256Hash(self,fileString):
        readablehash = hashlib.sha3_256(fileString).hexdigest()
        return readablehash

    #scans folders recursively fo get files
    def checkfoldersave(self,folder,calltype,appid):
        #scans folders
        with os.scandir(folder) as dir_entries:
            #iterates each entry of folder
            for entry in dir_entries:
                info = entry.stat()

                name = entry.name

                filename = folder +"/"+ name

                if(os.path.isdir(filename)):

                    if os.listdir(filename):
                        self.checkfoldersave(filename,calltype,appid)

                    else:

                        print("empty")

                else:

                    hash = self.getReadableHash(filename)

                    # construct filestring by adding filehash + File Size + Last modified time + filename
                    fileString = hash + str(info.st_size) + str(info.st_mtime) + filename

                    fileString = fileString.encode('utf-8')
                    finalHash = self.getSha256Hash(fileString)

                    print(finalHash)
                    FileHash.filecount = FileHash.filecount + 1
                    # FileHash.fileDict[FileHash.filecount]['filehash'] = finalHash
                    FileHash.fileDict[finalHash] = filename

                    #create object of sqloperations
                    if(calltype == "save"):
                        sql = Sqlops()

                        sql.setData(filename=name,filepath=filename,sign=finalHash,appid=appid)

                        #insert values to db
                        sql.sqlSignInsert()

