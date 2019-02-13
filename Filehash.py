import hashlib

# Python program to find SHA256 hexadecimal hash string of a file
import hashlib #hashlib library to create hash
import os # os library to scan folders and files
from sqlops import Sqlops #contains sql operations

class FileHash:
    filecount = 0 # set filecount to zero

    #computes md5 hash of a file
    def getReadableHash(self,filename):
        with open(filename, "rb") as f:
            bytes = f.read()  # read entire file as bytes
            readable_hash = hashlib.md5(bytes).hexdigest() # get readable hash
            FileHash.filecount = FileHash.filecount + 1 # incrementing filecount
            return readable_hash

    # computes sha256 of file string
    def getSha256Hash(self,fileString):
        readablehash = hashlib.sha3_256(fileString).hexdigest()# get readable hash
        return readablehash

    #scans folders recursively fo get files
    def checkfoldersave(self,folder):
        #scans folders
        with os.scandir(folder) as dir_entries:
            #iterates each entry of folder
            for entry in dir_entries:
                info = entry.stat()  #get info about each files

                name = entry.name   #get file name

                filename = folder +"/"+ name # set filepath + filename used to identify files uniquely

                if(os.path.isdir(filename)): #check wheather entry is a folder

                    if os.listdir(filename): #check the folder is empty

                        self.checkfolder(filename) # if the folder is not empty recursively scans the new folder

                    else:

                        print("empty") #it is a empty folder

                else:

                    hash = self.getReadableHash(filename) # gets the readabale hash md5 of the file

                    # construct filestring by adding filehash + File Size + Last modified time + filename
                    fileString = hash + str(info.st_size) + str(info.st_mtime) + filename

                    fileString = fileString.encode('utf-8') #encodes fileString to binary

                    finalHash = self.getSha256Hash(fileString) # geting Finalhash

                    print(finalHash)

                    #create object of sqloperations
                    sql = Sqlops(filename=name,filepath=filename,sign=finalHash,appId=1)

                    #insert values to db
                    sql.sqlSignInsert()

    #funntion to scan and generate filehash
    def checkfolderscan(self,folder):
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
                    return filename,finalHash


#oops object
file = FileHash()
#checking folder testdir
file.checkfolderSave('testdir')
#printing no of files
print(FileHash.filecount)






