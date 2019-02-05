import hashlib

# Python program to find SHA256 hexadecimal hash string of a file
import hashlib
import os




def getReadableHash(filename):
    with open(filename, "rb") as f:
        bytes = f.read()  # read entire file as bytes
        readable_hash = hashlib.md5(bytes).hexdigest()
        return readable_hash

def getSha256Hash(fileString):
    readablehash = hashlib.sha3_256(fileString).hexdigest()
    return readablehash


folder = "testdir"

with os.scandir(folder) as dir_entries:
    for entry in dir_entries:
        info = entry.stat()
        name = entry.name
        filename = folder +"/"+ name
        hash = getReadableHash(filename)
        print(hash)
        print(info)
        fileString = hash + str(info.st_size) + str(info.st_mtime) + filename
        print(fileString)
        fileString = fileString.encode('utf-8')
        print(fileString)
        finalHash = getSha256Hash(fileString)
        print(finalHash)



