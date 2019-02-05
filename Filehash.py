import hashlib

# Python program to find SHA256 hexadecimal hash string of a file
import hashlib
import os
import sqlite3

def checkfolder(folder):

    def getReadableHash(filename):
        with open(filename, "rb") as f:
            bytes = f.read()  # read entire file as bytes
            readable_hash = hashlib.md5(bytes).hexdigest()
            return readable_hash

    def getSha256Hash(fileString):
        readablehash = hashlib.sha3_256(fileString).hexdigest()
        return readablehash


    with os.scandir(folder) as dir_entries:
        for entry in dir_entries:
            info = entry.stat()
            name = entry.name
            filename = folder +"/"+ name
            if(os.path.isdir(filename)):
                print("folder")
                if os.listdir(filename):
                    checkfolder(filename)
                else:
                    print("empty")
            else:
                print("file")
                hash = getReadableHash(filename)
                print(hash)
                print(info)
                fileString = hash + str(info.st_size) + str(info.st_mtime) + filename
                print(fileString)
                fileString = fileString.encode('utf-8')
                print(fileString)
                finalHash = getSha256Hash(fileString)
                print(finalHash)

checkfolder('testdir')

def sqliteops():
    conn = sqlite3.connect('test.db')
    c = conn.cursor()

    # Create table
    c.execute('''CREATE TABLE stocks
                                 (date text, trans text, symbol text, qty real, price real)''')

    # Insert a row of data
    c.execute("INSERT INTO stocks VALUES ('2006-01-05','BUY','RHAT',100,35.14)")

    # Save (commit) the changes
    conn.commit()

    # We can also close the connection if we are done with it.
    # Just be sure any changes have been committed or they will be lost.
    conn.close()
sqliteops()


#teswts