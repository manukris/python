from Filehash import FileHash
from sqlops import Sqlops

file = FileHash()
file.checkfoldersave('testdir',calltype="scan")
print(FileHash.fileDict)
dict = FileHash.fileDict
print(len(FileHash.fileDict))

db = Sqlops()
result = db.sqlsignSelect()
for rows in result:
    for x, y in dict.items():
        if(rows[2] == y):
            if(rows[4] == x):
                print("no change")
            else:
                print("File changed")
                print(rows[2])
                break



